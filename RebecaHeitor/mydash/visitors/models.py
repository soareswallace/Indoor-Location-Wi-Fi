# coding=UTF-8
from __future__ import unicode_literals
from datetime import datetime
from django.db import models
from mongoengine import *
from mongoengine.django.auth import User
from django.core.urlresolvers import reverse
import time
from datetime import datetime
import datetime as dttt

class Cliente(Document):
  meta = {'allow_inheritance': False}
  riot = StringField()
  dia = StringField()
  power = ListField(FloatField())
  saida = StringField()
  mac = StringField()
  entrada = StringField()
  redes = ListField(StringField(max_length=30))
  genero = StringField()
  nome = StringField()

class Loja(Document):
  meta = {'allow_inheritance': False}
  mac = StringField()
  saida = StringField()
  cargo = StringField()

class Visitas(Document):
  meta = {'allow_inheritance': False}
  mac = StringField()
  entrada = StringField()
  saida = StringField()
  duracao = ListField(IntField())
  flag = IntField()

class Vendas(Document):
  meta = {'allow_inheritance': False}
  ident = IntField()
  data = StringField()
  dia = StringField()
  valor = FloatField()
  pagamento = IntField()
  parcelamento = IntField ()

class Device(Document):
  meta = {'allow_inheritance': False}
  stationMac = StringField()
  firstSeen = DateTimeField()
  lastSeen = DateTimeField()
  power = FloatField()
  probedSSID = ListField(StringField(max_length=30))
  currentApBSSID = StringField()
  currentApESSID = StringField()
  sessionId = StringField()
  riotId = StringField()
  createdAt = DateTimeField()
  manufacturer = StringField()

class Aparelho(Document):
  meta = {'allow_inheritance': False}
  nome = StringField()
  mac = ListField(StringField(max_length=30))
  quantidade = IntField()


class Frontdata(Document):
  meta = {'allow_inheritance': False}
  contador = IntField()
  lastSeen = DateTimeField()


class Manufacturer(Document):
  nome = StringField()
  mac = ListField(StringField())
  quantidade = IntField()

  def __unicode__(self):
    return unicode(self.mac) or u''

def distribuicaoHorariaClientes(startDate, finalDate):
	qtdporhora = [0] * 24
	for client in Cliente.objects(dia__gte=startDate, dia__lte=finalDate):
		i = int(client["entrada"][0:2])
		j = int(client["saida"][0:2])
		while(i<=j):
			qtdporhora[i] = qtdporhora[i] + 1
			i = i + 1
	return qtdporhora

def frequenciaVisitaClienteMes(macCliente, Ano):

	qtdPorMes = [0] * 12
	for client in Cliente.objects(mac=macCliente):
		if(client["dia"][0:4] == Ano):
			i = int(client["dia"][5:7]) - 1 #porque o mes comeca em 1 e o indice comeca em 0
			qtdPorMes[i] = qtdPorMes[i]+1

	return qtdPorMes

def DistribuicaoMensalClientes(startDate, finalDate):
  print "distri\n\n\n\n"
  qtdPorMes = [0] * 12

  for client in Cliente.objects(dia__gte=startDate,dia__lte=finalDate):
    i = int(client["dia"][5:7]) - 1 
    qtdPorMes[i] = qtdPorMes[i] +1 

  return qtdPorMes

def quantidadeClientesLojas(startDate, finalDate):
	return len(Cliente.objects(dia__gte=startDate,dia__lte=finalDate))

def extrair_horario(entrada):
	
	entrada = entrada.split(':')
	hora = int(entrada[0])
	minuto = int(entrada[1])
	segundo = int(entrada[2])

	return hora*3600 + minuto*60 + segundo

def TransformaDiaEmSegundo(DiferencaDias):
  seg = DiferencaDias[0]*24*3600 + DiferencaDias[1]*3600 + DiferencaDias[2]*60 + DiferencaDias[3]
  return seg

def TransformaSegundoEmDias(seg):
  hora = seg/3600
  minuto = (seg%3600)/60
  segundo = seg - hora*3600 - minuto*60
  dia = hora/24
  hora = hora%24
  return [dia, hora, minuto, segundo]


def tempo_medio_data(startDate,finalDate):

  now = time.time()
  aux = [0,0,0,0]
  total = Visitas.objects(entrada__lte=finalDate,saida__gte=startDate).count()
  for v in Visitas.objects(entrada__lte=finalDate,saida__gte=startDate):
    i = 0
    while i < 4:
      aux[i] += v["duracao"][i]
      i += 1

  tempo_total = TransformaDiaEmSegundo(aux)
  media = tempo_total/total
  tempo_m = TransformaSegundoEmDias(media)
  

  fim = time.time()

  

  return [total]+tempo_m


def quantidadeVisitasClienteNaLoja(macCliente):
  return Visitas.objects(mac=macCliente).count()


def ContadorVisitas(startDate, finalDate):
  n_visitas = Visitas.objects(entrada__lte=finalDate,saida__gte=startDate).count()
  return n_visitas

def ContadorVisitasCliente(mac, startDate, finalDate):
  n_visitas = Visitas.objects(mac=mac,entrada__lte=finalDate,saida__gte=startDate).count()
  return n_visitas


def PrimeiraVezCliente(mac, startDate, finalDate):
  c = 0
  for v in Visitas.objects(mac=mac,saida__gte=startDate):
    c += 1

    if(c>=2):
      return c

  return c

def ClientesNovosEAntigos (startDate, finalDate):
  now = time.time()

  recorrencia = [0, 0]
  velho = [""]
  
  aux = Visitas.objects(entrada__lte=finalDate,saida__gte=startDate).distinct("mac")
  

  for v in Visitas.objects(entrada__lte=finalDate,saida__gte=startDate):
    if v["flag"]:
      if not (v["mac"] in velho):
        recorrencia[1] +=1
        velho.append(v["mac"])
    else:
        recorrencia[0] +=1

  fim = time.time()

 

  return recorrencia


def statusCliente (macs):
  novo = []
  antigo = []
  for mac in macs:
    if Visitas.objects(mac=mac).count()>1:
      antigo += [str(mac)]
    else:
      novo += [str(mac)]

  return novo,antigo

def visitaDiasSemana (startDate, finalDate, semana):

    qtdporhoraDia = [0]*24
    diaSemana = datetime.strptime(startDate, '%Y-%m-%dT%H:%M:%S')
    finald = datetime.strptime(finalDate, '%Y-%m-%dT%H:%M:%S')
    delta = dttt.timedelta(days=1)

    while(diaSemana.weekday() != semana):
      diaSemana+=delta


    ds = datetime.strftime(diaSemana, '%Y-%m-%dT%H:%M:%S')
    for visita in Visitas.objects(saida__gte=ds,entrada__lte=finalDate):
        d = datetime.strptime(visita["entrada"],'%Y-%m-%dT%H:%M:%S')

        if( str(d.weekday()) == str(semana) ):

            i = int(visita["entrada"][11:13]) # No caso em que a hora da entrada da loja
            j = int(visita["saida"][11:13])      # For menor do que a hora do startDate
                                              # Passa a contar a partir da hora do startDate
            if(i < int(startDate[11:13])):
                i = int(startDate[11:13])

            if(j > int(finalDate[11:13])):
                j = int(finalDate[11:13])

            while(i<=j):
                qtdporhoraDia[i] = qtdporhoraDia[i] + 1
                i = i + 1

    return qtdporhoraDia

def distribuicaoMensalClientes(startDate, finalDate):
  qtdPorMes = [0]*12
  for visita in Visitas.objects(entrada__lte=finalDate,saida__gte=startDate):
    i = int(visita["entrada"][5:7])
    j = int(visita["saida"][5:7])

    if(i < int(startDate[5:7])):
      i = int(startDate[5:7])
    if(j > int(finalDate[5:7])):
      j = int(finalDate[5:7])
    while(i<=j):
      qtdPorMes[i-1] = qtdPorMes[i-1] + 1 
      i = i+1

  print "\n\n\n\n\n\nALO",qtdPorMes
  return qtdPorMes


def distribuicaoHorariaClientes(startDate, finalDate):

  qtdporhora = [0]*24
  for visita in Visitas.objects(entrada__lte=finalDate,saida__gte=startDate):
    i = int(visita["entrada"][11:13]) # No caso em que a hora da entrada da loja
    j = int(visita["saida"][11:13])   # For menor do que a hora do startDate
                      # Passa a contar a partir da hora do startDate
    if(i < int(startDate[11:13])):
      i = int(startDate[11:13])
    if(j > int(finalDate[11:13])):
      j = int(finalDate[11:13])

    while(i<=j):
      qtdporhora[i] = qtdporhora[i] + 1
      i = i + 1

  return qtdporhora

def redes_mais_acessadas():
 # Vetores de redes  mais acessadas pelos clientes
 top_redes = [""]
 top_quant = [0]

 for v in Cliente.objects:
   # Acessar numero MAC do cliente
   mac = v["mac"]
   vet = [mac]

   for r in v["redes"]:
    if r != "" and r!="null":
     cont = 1
     # Verificar quantidade de usuarios de uma dada rede
     if not (r in top_redes):
       for p in Cliente.objects(redes=r):
         if mac != p["mac"] and not(p["mac"] in vet):
           cont += 1
           vet = vet + [p["mac"]]

       index = len(top_quant)
       for element in top_quant:
         if cont >= element:
           index = top_quant.index(element)
           break
       top_redes.insert(index,r)
       top_quant.insert(index,cont)
 index = top_redes.index('')
 if index < 10:
   top_redes = top_redes[:index]
   top_quant = top_quant[:index]
 else:
   top_redes = top_redes[:11]
   top_quant = top_quant[:11]

 total = 0
 for element in top_quant:
   total += element*1.0
   element = element*1.0

 for element in top_quant:
   element = element/total

 return top_redes,top_quant


def comparaManufacturer():
  total = (Cliente.objects.count())*1.0

  fabricantes = []
  porcentagem = []
  valor = 100.0

  for marca in Aparelho.objects.order_by('-quantidade'):
    if marca["nome"] == "UNKNOWN":
      total -= marca["quantidade"]
  for marca in Aparelho.objects.order_by('-quantidade'):
    if marca["nome"] != "UNKNOWN":  
      p = (marca["quantidade"]*100.0)/total

      if p >= .1:
        fabricantes.insert(len(fabricantes),marca["nome"])
        porcentagem.insert(len(porcentagem),p)
        valor -= p
      else:
        fabricantes.insert(len(fabricantes),"Outras marcas")
        porcentagem.insert(len(porcentagem),valor)
        break

  return fabricantes,porcentagem

def clientesNoMomento(startDate, finalDate):

    clientesNoMomento = []

    for cliente in Visitas.objects(saida__gte=startDate,entrada__lte=finalDate):
        lastSeenCliente = int(cliente["saida"][11:13])*3600 + int(cliente["saida"][14:16])*60 + int(cliente["saida"][17:19])
        timeNow = int(finalDate[11:13])*3600 + int(finalDate[14:16])*60 + int(finalDate[17:19])

        if( abs(timeNow - lastSeenCliente) < 600):
            clientesNoMomento.append(cliente["mac"])


    return clientesNoMomento

#-----------------------------------------------------------------------------------------------
# Função que quebra uma determinada entrada an forma aaaa-mm-ddThh:mm:ss
# em um vetor com ints de [ano, mes, dia, hora, minuto, segundo].
def QuebraEntrada (First_seen):
  # Separando data do tempo.
  First_seen = First_seen.split('T')
  data = First_seen[0]
  tempo = First_seen[1]
  # Quebrando a data e o tempo.
  # Data:
  data = data.split('-')
  ano = int(data[0])
  mes = int(data[1])
  dia = int(data[2])
  # Tempo:
  tempo = tempo.split(':')
  hora = int(tempo[0])
  minuto = int(tempo[1])
  segundo = int(tempo[2])
  return [ano, mes, dia, hora, minuto, segundo]



#-----------------------------------------------------------------------------------------------
# Função que devolve a diferença entre duas entradas na forma aaaa-mm-ddThh:mm:ss 
# como um vetor com ints de [dia, hora, minuto, segundo]. Diferença = Entrada2 - Entrada1.
def DiferencaEntradas (Entrada1, Entrada2):
  # Conversao de string para datetime
  Entrada1 = datetime.strptime(Entrada1, "%Y-%m-%dT%H:%M:%S")
  Entrada2 = datetime.strptime(Entrada2, "%Y-%m-%dT%H:%M:%S")
  # Verificar validade da diferenca
  if Entrada2 > Entrada1:
    dif = Entrada2 - Entrada1
    return [dif.days,dif.seconds/3600,(dif.seconds/60)%60,dif.seconds%60]
  else:
    return False

def achaFabricante(mac):
  mac = mac.lower()
  fabricante = Aparelho.objects(mac=mac)
  if len(fabricante) != 0:
    return fabricante[0]["nome"]
  else:
    return "Sem fabricante"

def achaNome(mac):
  mac = mac.lower()
  for pessoa in Cliente.objects(mac=mac):
    aux = str(list(pessoa))
    if aux.find("nome")>0:
      if pessoa["nome"]!= None:
        return pessoa["nome"]

  return "desconhecido"

def tempoMedioCliente(mac):
  now = datetime.now()
  now = now.strftime("%Y-%m-%dT%H:%M:%S")

  aux = [0,0,0,0]
  total = Visitas.objects(mac=mac,entrada__lte=now).count()
  print "total eh \n\n\n",total
  if total == 0:
    return aux, 0
  for v in Visitas.objects(mac=mac,entrada__lte=now):
    i = 0
    while i < 4:
      aux[i] += v["duracao"][i]
      i += 1

  tempo_total = TransformaDiaEmSegundo(aux)
  media = tempo_total/total

  return TransformaSegundoEmDias(media), total


def achaRedes(mac):
 redes = []
 for c in Cliente.objects(mac=mac):
  if len(c['redes'])>0:
    print "\n\n\n\nRedes:",c['redes']
    redes = list(set(redes) | set(c['redes']))
    print redes
 return redes


def setNameGender(mac,nome,genero):
  Cliente.objects(mac=mac).update(set__nome=nome, set__genero=genero)

def showlive():
  print "showliveeeee\n"
  # Iniciando variáveis.
  contador = Frontdata.objects[0]['contador']
  minimo = -800
  # Data 2010-01-01T00:00:00 escolhida arbitrariamente, por ser uma data menor que todas coletadas.
  # lastSeen = datetime.strptime("2010-01-01T00:00:00", "%Y-%m-%dT%H:%M:%S")

  # lastSeen = Device.objects.order_by('-lastSeen')
  # lastSeen = lastSeen[0]['lastSeen']
  lastSeen = Frontdata.objects[0]['lastSeen']
  
  # Zerando as coleções utilizadas.
  # Loja.objects.delete()

  # while(True):
  # Booleana responsável por verificar se houve alteração nos dados mostrados pelo banco.
  # Se for o caso, ela faz com que esses dados sejam atualizados na interface.
  Atualizacao = False
                       ###### Inserção de dados ######
#########################################################################################################################
  # Caso o contador detecte que foram acrescentados mais dados no banco,
  # se inicia o processo de inserção no banco.
  c = Device.objects.count()
  print "\n\n\n\n",contador,lastSeen,c
  if (contador < c):
    N = contador 
    print "\n\n\n\n\n\n",Device.objects[N:c]
    # contador = c
    # Esse for serve para coletar apenas os dados recém inseridos. Assumimos que dados recém chegados possuem lastSeen
    # maior que todos os anteriores, necessariamente.
    for pacote in Device.objects[N:c]:
      print "\n\n\n",pacote
    #for pacote in Device.objects(lastSeen__gte=lastSeen):
      # Implementando [0]filtro para longas distâncias e saidas anteriores a chegadas.
      presente =0
      if (pacote["power"] > minimo and pacote['power'] < -1) and pacote["firstSeen"] < pacote["lastSeen"]:
        saida = pacote["lastSeen"]
        mac = pacote["stationMac"]
        # print mac
        presente = Loja.objects(mac=mac).count()
        if presente !=0:
          # print "entou no if", mac
          v = Loja.objects(mac=mac)[0]
          # print "cara eh ", v
          # print v["saida"]
          if v["saida"] < saida:
            Loja.objects(mac=mac).update(set__saida=saida)
            contador+=1
        else:
            # print "entrou no else", mac
            if (str(list(pacote)).find("currentApESSID") == -1 or pacote["currentApESSID"] != "Lysa"):
              # print "entrou no if dentro do else"
              newLoja = Loja(mac=mac,saida=saida,cargo='cliente').save()
              Atualizacao = True
              contador+=1
            else:
                # print "entrou no else dentro do else"
                newLoja = Loja(mac=mac,saida=saida,cargo='funcionario').save()
                newLoja.save()
                Atualizacao = True
                contador+=1

###### Verificação dos dados ######
#########################################################################################################################
  
  for pessoa in Loja.objects():
    # Adquirir o numero MAC.
    mac = pessoa["mac"]
    # Adquirir a saída, no formato aaaa-mm-ddThh:mm:ss.
    saida = pessoa["saida"]
    # Adiquirir horário atual, no formato aaaa-mm-ddThh:mm:ss.
    atual = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    # Calculando a diferença entre os tempos, para verificar se o cliente saiu da loja.
    diferenca = DiferencaEntradas(saida, atual)
    # Verificando se o cliente ainda está na loja. Definiremos que se o cliente não for 
    if diferenca[2] > 4:
      Loja.objects(mac=mac).delete()
      Atualizacao = True

                    ###### Exibição dos dados ######
#########################################################################################################################
  vet_cliente = []
  vet_funcionario = []
  vet_last = []
  if (True):
    # Criando vetores de macs:

    for cliente in Loja.objects(cargo='cliente'):
      mc = cliente["mac"]
      last = cliente['saida']
      vet_cliente = vet_cliente + [mc]
      vet_last = vet_last +[last]
    for funcionario in Loja.objects(cargo='funcionario'):
      mc = funcionario["mac"]
      vet_funcionario = vet_funcionario + [mc]
    # print "Pessoas na loja:"
    # print vet_cliente, vet_funcionario, len(vet_cliente), len(vet_funcionario)

  Frontdata.objects[0].update(set__lastSeen=lastSeen,set__contador=contador)

  print "\n\n\n\n\n\saiu"
  return vet_last,vet_cliente, vet_funcionario, len(vet_cliente), len(vet_funcionario)

#Vendas
def tipoCompras(startDate, finalDate):
  c = 0
  tipoCompras=[0]*2
  ticketpormes = [0]*12
  valorpormes=[0]*12
  valormedpormes=[0]*12
  ticketporhora = [0]*24
  valorporhora = [0]*24
  valormedporHora=[0]*24
  for venda in Vendas.objects(data__gte=startDate, data__lte=finalDate):
    
    i = int(venda["pagamento"])-1 #pagamento eh 1 ou 2
    tipoCompras[i]+=1
    c+=1

    i = int(venda["data"][11:13]) 
    ticketporhora[i]+=1

    valorporhora[i]+= float(venda["valor"])

    i = int(venda["data"][5:7])-1
    ticketpormes[i]+=1

    valorpormes[i]+= float(venda["valor"])

  for i in range(24):
    if(ticketporhora[i]!=0):
      valormedporHora[i]+= float(valorporhora[i]/ticketporhora[i])
    else:
      valormedporHora[i]=0

  for i in range(0,11):
    if(ticketpormes[i]!=0):
      valormedpormes[i]+= valorpormes[i]/ticketpormes[i]
    else:
      valormedpormes[i]=0

  if c!= 0:
    print "tipoCompras: ",tipoCompras
    tipoCompras[0] = 100*tipoCompras[0] / float(c)
    tipoCompras[1] = 100*tipoCompras[1] / float(c)
    print "tipoCompras: ",tipoCompras
  else:
    tipoCompras[0] = 0
    tipoCompras[1] = 0
#[deb|credi]
  return tipoCompras, ticketporhora, valorporhora, valormedporHora, ticketpormes, valorpormes, valormedpormes

def qtdParcelamentoCredito(startDate, finalDate):

  qtdParcelamentoCredito=[0]*12
  total = 0 

  for venda in Vendas.objects(data__gte=startDate, data__lte=finalDate):
    
    if(venda["pagamento"]==2):
      i = int(venda["parcelamento"])-1
      qtdParcelamentoCredito[i]+=1
      total += 1

  for v in qtdParcelamentoCredito:
    v = v/total

  return qtdParcelamentoCredito    

