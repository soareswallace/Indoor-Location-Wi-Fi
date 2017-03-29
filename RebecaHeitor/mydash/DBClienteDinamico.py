# coding=UTF-8
# Importando biblioteca datetime.
from datetime import datetime
# Estabelecendo conexão com o MongoDB.
import pymongo
from pymongo import MongoClient

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
# Criando coleção de aparelhos.
aparelho = riotdb['aparelho']
# Criando coleção de funcionários.
funcionario = riotdb['funcionario']

# Inicializando contador
contador = 0
# Estabelecendo valor minimo de potencia para o filtro.
minimo = -70
# Data 2010-01-01T00:00:00 escolhida arbitrariamente, por ser uma data menor que todas coletadas.
lastSeen = "2010-01-01T00:00:00"
c1 = riotdb.cliente.find().count()
# Caso haja alguém no banco de clientes, só serão processados os dados a partir da última saída.
if (c1 > 0):
	# Tomando maior lastSeen armazenado, para não processar novamente os dados já analizados.
	for v in riotdb.cliente.find():
		if v["saida"] > lastSeen:
 			lastSeen = v["saida"]
else:
	# Zerando as coleções utilizadas.
	riotdb.cliente.remove({})
	riotdb.aparelho.remove({})
	riotdb.funcionario.remove({})
# Transformando lastSeen no formato isoDate.
# lastSeen = datetime.strptime(lastSeen, "%Y-%m-%dT%H:%M:%S")
print "last: ",lastSeen

# Criando loop infinito, para processar dados dinâmicos.
while (True):
	print "aqui"
	# Caso o contador detecte que foram acrescentados mais dados no banco,
	# se inicia o processo de inserção no banco.
	if (contador < riotdb.device.find().count()):
		contador = riotdb.device.find().count()
		print contador
		# Esse for serve para coletar apenas os dados recém inseridos. Assumimos que dados recém chegados possuem lastSeen
		# maior que todos os anteriores, necessariamente.
		for pacote in riotdb.device.find({"lastSeen": {"$gte": lastSeen}}).sort([('firstSeen',1) ,('lastSeen',1)]):
			# Implementando filtro para longas distâncias e saidas anteriores a chegadas.
			if pacote["firstSeen"] <= pacote["lastSeen"]:
				# Adquirir o numero MAC.
 				mac = pacote["stationMac"]
 				# Adquirir a saída, no formato aaaa-mm-ddThh:mm:ss.
 				saida = pacote["lastSeen"]
 				# Gravando a maior saída.
 				if pacote["lastSeen"] > lastSeen:
 					lastSeen = pacote["lastSeen"]
 				# Caso o pacote não possua o termo Bran, consideramos que se trata de um cliente e procedemos normalmente.
 				if (str(list(pacote)).find("probedSSID") == -1 or not("Lysa" in pacote["probedSSID"])) and (str(list(pacote)).find("currentApESSID") == -1 or pacote["currentApESSID"] != "Lysa"):
 					# Adquirir a entrada, no formato aaaa-mm-ddThh:mm:ss.
 					entrada = pacote["firstSeen"]
 					# Adquirir riot
 					riot = pacote["riotId"]
					# Adquirir redes
					redes = pacote["probedSSID"]
 					# Adquirir power.
 					power = pacote["power"]
 					# Adquirindo manufacturer.
 					if str(list(pacote)).find("manufacturer") == -1:
 						manufacturer = "UNKNOWN"
 					else:
	 					manufacturer = pacote["manufacturer"].upper().split(" ")
	 					manufacturer = manufacturer[0]
	 					fabricante = manufacturer.split(',')
	 					if fabricante != manufacturer:
	 						manufacturer = fabricante[0]

	 					###### Inserindo no banco de dados cliente ######
#########################################################################################################################
 					# Testando se essa visita já se encontra no banco de dados.
 					presente = riotdb.cliente.find({'mac':mac,'entrada':entrada,'riot':riot}).count()
 					# Caso já se encontre, são atualizados os dados.
 					if presente != 0:
 						v = riotdb.cliente.find({'mac':mac,'entrada':entrada,'riot':riot})[0]
 						if str(v["saida"]) < saida:
							# Aqui será verificado quais redes diferem entre a nova entrada e 
							# a já existente, e serão adicionadas no banco apenas as que ainda não estiverem nele.
							vet = v["redes"]
							for net in redes:
								if (not(net in v["redes"])):
									if vet =='null':
										vet = [net]
									else:
										vet = vet+[net]
							# Atualização do horário de saída, do vetor de redes e armazenamento de mais um power no vetor.
 							riotdb.cliente.update({'mac': mac, 'entrada': entrada, 'riot': riot}, {"$set": {'saida': saida, 'redes': vet}, "$push": {'power': power}})
					# Caso contrario
 					else:
 						p = [power]
 						riotdb.cliente.insert({'mac': mac, 'entrada': entrada, 'saida': saida, 'riot': riot, 'power': p, 'redes': redes})

	 					###### Inserindo no banco de dados aparelhos ######
#########################################################################################################################
	 				# Verificar se fabricante está no banco de dados.
 					presente = riotdb.aparelho.find({'nome':manufacturer}).count()
 					# Se nao estiver presente.
 					if presente == 0:
 						riotdb.aparelho.insert({'nome':manufacturer,'mac':[mac],'quantidade':1})
 					# Se estiver presente
 					else:
 						# Verificar se o mac já foi inserido no banco de dados.
 						dados = riotdb.aparelho.find({'nome':manufacturer})[0]
 						flag = True
 						for p in dados["mac"]:
 							if mac == p:
 								flag = False
 						# Se nao estiver no banco de dados
 						if flag:
	 						riotdb.aparelho.update({'nome':manufacturer}, {"$push": {'mac': mac}, "$inc": {'quantidade': 1}})

						###### Inserindo no banco de dados funcionario ######
#########################################################################################################################
	 			else:
					# Verificar se funcionario esta no banco
					present = riotdb.funcionario.find({'mac':mac}).count()
					#Inserir funcionario no banco
					if present == 0:
						riotdb.funcionario.insert({'mac' : mac})