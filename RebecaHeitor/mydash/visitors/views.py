from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from models import *
from mongoengine import *
from django.shortcuts import render_to_response
from visitors.models import *
from django.http import HttpResponseRedirect
from .forms import *
import json
import datetime
import random 

months = { 1 : "Jan", 
    2 : "Feb", 
    3 : "Mar", 
    4 : "Abr", 
    5 : "Mai", 
    6 : "Jun", 
    7 : "Jul",
    8 : "Ago",
    9 : "Set", 
    10 : "Out", 
    11 : "Nov",
    12 : "Dez" } 

def loadgif(request):
    return render(request, 'load.html')

def index(request):

    print "\n\n\n\n\n\nALO"
    data_to_plot ={}
    context = {}
    now = datetime.datetime.now()
    month = now.month
    day = now.day
    year = now.year
    if(month<10):
        month = "0"+str(month)
    if(day<10):
        day = "0"+str(day)
    startDate = str(year)+"-"+"01-01T00:00:00"
    finalDate = str(year)+"-"+str(month)+"-"+str(day)+"T23:59:59"
    #Figindo que hj eh dia 20 de novembro de 2015
    startDate = "2016-03-28T00:00:00"
    finalDate = "2016-03-28T23:59:59"
    # "2015-11-16T00:00:00", "2015-11-22T00:00:00")
    retorno = distribuicaoMensalClientes(startDate,finalDate)
    #retorno = [0]*12
    year = 2016
    month = 02
    day = 2
    data_to_plot['ano'] = year


    data_to_plot['months'] = []

    for i in range (0, len(retorno)):
        data_to_plot['months'].append({'month': months[i+1],'value': retorno[i]})
        
    retorno = distribuicaoHorariaClientes((str(year)+"-"+str(month)+"-"+str(day)+"T00:00:00"),(str(year)+"-"+str(month)+"-"+str(day)+"T23:59:59"))
    data_to_plot['hour'] = []
    for i in range (0, len(retorno)):
        data_to_plot['hour'].append({'hora': str(i)+'h','value': retorno[i]})

    data_to_plot['hoje_dia'] = day
    data_to_plot['hoje_mes'] = month

    data_to_plot['novo']= []
    data_to_plot['nomes'] = []
    data_to_plot['velhos'] = []
    data_to_plot['funcionarios'] = []
    contador = 0
    vetor = showlive()
    lastseen = vetor[0]
    macNew, macOld = statusCliente(vetor[1])
    macFunc = len(vetor[2])
    qtd_pessoas = len(macNew)+len(macOld)
    for i in range (0, len(macNew)):
        data_to_plot['novo'].append(macNew[i].upper())

    for i in range (0, len(macOld)):
        data_to_plot['velhos'].append(macOld[i].upper())

    for i in range (0, macFunc):
        data_to_plot['funcionarios'].append(vetor[2][i].upper())

    context['plot']=data_to_plot
    context['total']= qtd_pessoas
    context['totalFunc'] = macFunc
    context['totalNew'] = len(macNew)
    context['totalOld'] = len(macOld)
    return render(request, 'dashboard.html', context)

def live(request):
    data_to_plot ={}
    context = {}
    
    data_to_plot['novo']= []
    data_to_plot['velhos'] = []
    macNew = [random.randint(1, 300)]*7 
    macOld = ["7C:E9:D3:CA:9D:C4"]*3
    qtd_pessoas = len(macNew)+len(macOld)
    for i in range (0, len(macNew)):
        data_to_plot['novo'].append(macNew[i])

    for i in range (0, len(macOld)):
        data_to_plot['velhos'].append(macOld[i])

    context['plot']=data_to_plot
    context['total']= qtd_pessoas
    context['totalNew'] = len(macNew)
    context['totalOld'] = len(macOld)
    return render(request, 'tableLive.html', context)


def postPeriod(request):
    erro =request.method
    if request.method == "POST":
        post = request.POST.copy()
        startDate = post['initalPeriod']
        finalDate = post['endPeriod']
        tipoBusca = post['tipoBusca']

        response = {'status': 1, 'startDate':startDate,'finalDate':finalDate, 'tipoBusca':tipoBusca} 
        return HttpResponse(json.dumps(response), content_type='application/json')

    else:
        erro = u"Erro2"
        response = {'status': 0} 
    return HttpResponse(json.dumps(response), content_type='application/json')

def postName(request):

    erro =request.method
    if request.method == "POST":
        post = request.POST.copy()
        MAC = post['myMAC'].lower()
        nome = post['myName']
        genero = post['mygender']
        setNameGender(MAC,nome,genero)
        response = {'status': 1} 
        return HttpResponse(json.dumps(response), content_type='application/json')

    else:
        erro = u"Erro2"
        response = {'status': 0} 
    return HttpResponse(json.dumps(response), content_type='application/json')


def makeDataPeriodo(request,query):
    startDate = query.split(":")[0]
    finalDate = query.split(":")[1]
    tipoBusca = int(query.split(":")[2])
    startDate = startDate[6:10]+"-"+startDate[3:5]+"-"+startDate[0:2]
    finalDate = finalDate[6:10]+"-"+finalDate[3:5]+"-"+finalDate[0:2]
    startDate = startDate+"T00:00:00"
    finalDate = finalDate+"T23:59:59"
    context = {}


    vetor_tempo = tempo_medio_data(startDate,finalDate)  

    horas = vetor_tempo[1]*24+vetor_tempo[2]

    if(vetor_tempo[3]<10):
        tempo_medio = str(horas)+":"+'0'+str(vetor_tempo[3])+":"+str(vetor_tempo[4])
    else:
        tempo_medio = str(horas)+":"+str(vetor_tempo[3])+":"+str(vetor_tempo[4])

   

    data_to_plot ={}
    data_to_plot['hour'] = []
    data_to_plot['months'] = []
    if(tipoBusca==7):
        retorno = distribuicaoHorariaClientes(startDate,finalDate)
    else:
        retorno = visitaDiasSemana(startDate,finalDate,tipoBusca)

    for i in range (0, len(retorno)):
        data_to_plot['hour'].append({'hora': str(i)+'h','value': retorno[i]})

    retorno = distribuicaoMensalClientes(startDate,finalDate)
    
    for i in range (0, len(retorno)):
        data_to_plot['months'].append({'month': months[i+1],'value': retorno[i]})

    context['plot']=data_to_plot
    dados = {}
    dados['total'] = vetor_tempo[0]#ContadorVisitas(startDate,finalDate)
    novosAntigos = ClientesNovosEAntigos(startDate,finalDate)
    
    dados['novos'] = novosAntigos[0]
    dados['antigos'] = novosAntigos[1]
    dados['tempo_medio'] = tempo_medio
    context['valores'] = dados
    return render_to_response("periodClients.html",context)



def allClients(request):
    context = {'form':dateForm}
    data_to_plot ={}
    data_to_plot['hour'] = []
    data_to_plot['months'] = []
    context['plot']=data_to_plot
    return render(request, "allClients.html",context)

def postfriend(request, query):
    context = {}
    data_to_plot ={}
    lista = query.split(",")
    lista = lista[len(lista)-1]
    if len(lista) > 1:
        tam = len(lista)
        i = 0
        amigos=[]
        k = 0
        aux = ""
        while(i<tam):
            aux = aux+str(lista[i])
            if ((i+1)%12!=0):
                if ((i+1)%2==0):
                    aux =aux+ ":"
            else:
                amigos.append(aux.upper())
                aux = ""
            i+=1
        mac = amigos[0]
        amigos = amigos[1:]
        data_to_plot['amigos'] = amigos
    else:
        mac = lista[0]
    context['plot']=data_to_plot
    total = quantidadeVisitasClienteNaLoja(mac.lower())
    dados = {}
    data_to_plot['totalVisitas'] = total
    context['valores'] =dados
    data_to_plot['mac'] = mac
    tempomedio, total = tempoMedioCliente(mac.lower()) 
    hora = 24*tempomedio[0]+tempomedio[1]
    t_medio = str(hora)+":"
    if tempomedio[2] < 10:
        t_medio = t_medio + "0" + str(tempomedio[2]) + ":"
    else:
        t_medio = t_medio + str(tempomedio[2]) + ":"
    if tempomedio[3] < 10:
        t_medio = t_medio + "0" + str(tempomedio[3])
    else:
        t_medio = t_medio + str(tempomedio[3])
    data_to_plot['total'] = total
    data_to_plot['tempo_medio'] = t_medio
    data_to_plot['fabricante'] = achaFabricante(data_to_plot['mac'])
    data_to_plot['redes'] = []
    redes = achaRedes(mac.lower())
    for i in range (0, len(redes)):
        data_to_plot['redes'].append(redes[i])

    context['plot'] = data_to_plot 
    return render_to_response("macDatas.html",context)


def vendasDataPeriodo(request,query):
    startDate = query.split(":")[0]
    finalDate = query.split(":")[1]
    startDate = startDate[6:10]+"-"+startDate[3:5]+"-"+startDate[0:2]
    finalDate = finalDate[6:10]+"-"+finalDate[3:5]+"-"+finalDate[0:2]
    startDate = startDate+"T00:00:00"
    finalDate = finalDate+"T23:59:59"

    context = {}
    dados = {}
    data_to_plot= {}
    print startDate, finalDate
    tipocompras, ticketporhora,valorporhora, valormedporHora, ticketpormes, valorpormes, valormedpormes  = tipoCompras(startDate,finalDate)
    # context['valores'] = dados
    dados['debito']= round(tipocompras[0],2)
    dados['credito'] = round(tipocompras[1],2)

    data_to_plot['ticketporhora'] = []
    data_to_plot['valorporhora'] = []
    data_to_plot['valormedporHora'] = []
    data_to_plot['ticketpormes'] = []
    data_to_plot['valorpormes'] = []
    data_to_plot['valormedpormes'] = []

    for i in range (0, len(ticketporhora)):
        data_to_plot['ticketporhora'].append({'hora': str(i)+'h','value': ticketporhora[i]})
    for i in range (0, len(valorporhora)):
        data_to_plot['valorporhora'].append({'hora': str(i)+'h','value': valorporhora[i]})
    for i in range (0, len(valormedporHora)):
        data_to_plot['valormedporHora'].append({'hora': str(i)+'h','value': valormedporHora[i]})

    for i in range (0, len(ticketpormes)):
        data_to_plot['ticketpormes'].append({'month': months[i+1],'value': ticketpormes[i]})
    for i in range (0, len(valorpormes)):
        data_to_plot['valorpormes'].append({'month': months[i+1],'value': valorpormes[i]})
    for i in range (0, len(valormedpormes)):
        data_to_plot['valormedpormes'].append({'month': months[i+1],'value': valormedpormes[i]})

    context['plot'] = data_to_plot
    context['dados'] = dados
    context['startDate'] = startDate
    context['finalDate'] = finalDate
    return render_to_response("periodVendas.html",context)
def vendas(request):
    context = {'form':dateForm}
    return render(request, "allvendas.html",context)

def postGetVendas(request):
    erro =request.method
    if request.method == "POST":
        post = request.POST.copy()
        startDate = post['initalPeriod']
        finalDate = post['endPeriod']

        response = {'status': 1, 'startDate':startDate,'finalDate':finalDate} 
        return HttpResponse(json.dumps(response), content_type='application/json')

    else:
        erro = u"Erro2"
        response = {'status': 0} 
    return HttpResponse(json.dumps(response), content_type='application/json')
