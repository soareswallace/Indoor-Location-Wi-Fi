# coding=UTF-8
# Importando biblioteca datetime.
from datetime import datetime
# Estabelecendo conexão com o MongoDB.
import pymongo
from pymongo import MongoClient

# Função que devolve a diferença entre duas entradas na forma isoDate como um 
# vetor com ints de [dia, hora, minuto, segundo]. Diferença = Entrada2 - Entrada1.
def DiferencaEntradas (Entrada1, Entrada2):
	# Conversao de string para datetime
	Entrada1 = datetime.strptime(Entrada1, "%Y-%m-%dT%H:%M:%S")
	Entrada2 = datetime.strptime(Entrada2, "%Y-%m-%dT%H:%M:%S")
	# Verificar validade da diferenca
	if Entrada2 > Entrada1:
		dif = Entrada2 - Entrada1
		return [dif.days,dif.seconds/3600,(dif.seconds/60)%60,dif.seconds%60]
	else:
		dif = Entrada1 - Entrada2
		return [(dif.days)*(-1),(dif.seconds/3600)*(-1),((dif.seconds/60)%60)*(-1),(dif.seconds%60)*(-1)]

# Estabelecendo conexão com os bancos de dados.
# Banco com os dados captados pelo riot.
banco_riot = "riotdb"
# Renomeando MongoClient().
connection_riot = MongoClient()
# Realizando a conexão.
riotdb = connection_riot[banco_riot]
# Criando coleção.
device = riotdb['device']
# Criando coleção de clientes.
cliente = riotdb['cliente']
# Criando coleção de visitas.
visitas = riotdb['visitas']
# Criando coleção dos Riots.
riots = riotdb['riots']
# Criando coleção auxiliar.
aux = riotdb['aux']

# Inicializando contador
contador = 0
# Contador de Riots.
n_riots = 0
# Estabelecendo a partir de qual data os dados serão processados, para se 
# evitar que o mesmo dado seja processado duas vezes.
# Data 2010-01-01T00:00:00 escolhida arbitrariamente, por ser uma data menor que todas coletadas.
lastSeen = "2010-01-01T00:00:00"
c1 = riotdb.visitas.find().count()
c2 = riotdb.aux.find().count()
# Caso haja alguém no banco de visitas ou no auxiliar, só serão processados os dados a partir da última saída.
if (c1 + c2 > 0):
	# Tomando maior lastSeen armazenado, para não processar novamente os dados já analizados.
	for v in riotdb.visitas.find():
		if v["saida"] > lastSeen:
 			lastSeen = v["saida"]
 	for v in riotdb.aux.find():
 		if v["saida"] > lastSeen:
 			lastSeen = v["saida"]
 	riotdb.riots.remove({})
else:
	riotdb.riots.remove({})

# Criando loop infinito, para processar dados dinâmicos.
##############################################################################
# Visitas dinamico serve para atualizar os dados que existem no banco device #
##############################################################################
while (True):

							  ###### Realizando inserções no banco de visitas ######
#####################################################################################################################
	# Caso seja recebido mais dados na coleção device. É utilizado este banco porque dados novos podem, além de 
	# acrescentar novas entradas, atualizar as antigas. Logo, não podemos mudar o sistema de entrada para o caso
	# de acréscimo de dados na coleção cliente.
	c = riotdb.device.find().count()
	if contador < c:
		contador = c
		# Verificanto se existem dados provenientes de novos riots.
		newNRiots = riotdb.cliente.distinct("riot")
		if len(newNRiots) > n_riots:
			n_riots = len(newNRiots)
			for riot in newNRiots:
				# Caso existam, procura-se quais os novos riots e o acrescentam ao banco de riots, 
				# em conjunto com a saida default.
				if riotdb.riots.find({'nome': riot}).count() == 0:
					riotdb.riots.insert({"nome": riot, "saida": lastSeen})
		# Analisando para cada riot no banco.
		for riot in riotdb.riots.find():
			aux_s = riot["saida"]
			for objeto in riotdb.cliente.find({"riot": riot["nome"], "saida": {"$gte": riot["saida"]}}):
				# Adquirir o numero MAC.
				mac_a = objeto["mac"]
				# Adquirir a entrada, no formato aaaa-mm-ddThh:mm:ss.
				entrada_a = objeto["entrada"]
				# Adquirir a saída, no formato aaaa-mm-ddThh:mm:ss.
				saida_a = objeto["saida"]
				# Gravando a maior saída.
 				if saida_a > aux_s:
 					aux_s = saida_a
 				# Verificando se este mac já está no banco auxiliar.
 				presente = riotdb.aux.find({"mac": mac_a}).count()
 				# Caso esteja presente, se verifica se é aumentada a visita, ou se é fechada
 				# a atual, e é inciada uma nova.
 				if presente != 0:
 					v = riotdb.aux.find({"mac": mac_a})[0]
 					# Caso esteja presente, existem três posições relativas para os novos dados.
 					# Para o caso em que a entrada será alterada.
 					if DiferencaEntradas(saida_a, v["entrada"])[2] < 10 and DiferencaEntradas(v["saida"], entrada_a)[2] < 10:
 						if entrada_a < v["entrada"]:
 							riotdb.aux.update({'mac': mac_a}, {"$set": {'entrada': entrada_a}})
 						if saida_a > v["saida"]:
 							riotdb.aux.update({'mac': mac_a}, {"$set": {'saida': saida_a}})
 					# Para o caso em que uma nova visita é adicionada.
 					if DiferencaEntradas(v["saida"], entrada_a)[2] >= 10:
 						# Filtro para visitas muito curtas (Menores que 10 segundos).
 						duracao = DiferencaEntradas(v["entrada"], v["saida"])
 						if duracao[3] > 10:
 							# Inserindo novo objeto no banco de dados de visitas.
 							riotdb.visitas.insert({"mac": v["mac"], "entrada": v["entrada"], "saida": v["saida"], "duracao": duracao})
 						# Atualizando objeto na coleção auxiliar.
 						riotdb.aux.update({'mac': mac_a}, {"$set": {'entrada': entrada_a, 'saida': saida_a}})
 					# O último caso, em que a a saida_a é mais de 10 minutos antes da entrada, é propositalmente ignorado,
 					# pois se isso acontecer, provém de um bug.
 				else:
 					# Caso ainda não esteja presente, o mac correspondente será inserido no banco auxiliar.
 					riotdb.aux.insert({"mac": mac_a, "entrada": entrada_a, "saida": saida_a})
 			riotdb.riots.update({'nome': riot["nome"]}, {"$set": {'saida': aux_s}})

									###### Verificação no banco auxiliar ######
#####################################################################################################################
	# Verifica se existe algum obejo no banco auxiliar.
	if riotdb.aux.find().count() != 0:
		# Caso exista, ele verifica a diferença entre a sua saida e o horário atual. Se essa diferença for
		# maior que 10 minutos (Tempo máximo estipulado para ser considerada a mesma visita), ele 
		# realiza as operações necessárias e acrescenta uma nova visita.
		for objeto in riotdb.aux.find():
			# Caso a diferença entre o horário atual e a saida no banco auxiliar seja maior que 10 minutos.
			if DiferencaEntradas(objeto["saida"], datetime.now().strftime("%Y-%m-%dT%H:%M:%S"))[2] > 10:
				# Inserindo nova visita.
				riotdb.visitas.insert({"mac": objeto["mac"], "entrada": objeto["entrada"], "saida": objeto["saida"], "duracao": DiferencaEntradas(objeto["entrada"], objeto["saida"])})
				# Removendo obejo do banco.
				riotdb.aux.remove({"mac": objeto["mac"]})
