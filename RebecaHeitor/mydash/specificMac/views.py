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


def index(request):
    # return HttpResponse("ola")
    return render(request, 'indexspecific.html')
# Create your views here.

def macLineGraph(request,query):
    context = {}
    # retorno = distribuicaoHorariaClientes("2015-11-16","2015-11-21")
    #MAC = "14:1A:A3:6C:7C:80"
    #141AA36C7C80
    MAC = query
    mac = [0]*16
    mac = MAC[0]+MAC[1]+":"+MAC[2]+MAC[3]+":"+MAC[4]+MAC[5]+":"+MAC[6]+MAC[7]+":"+MAC[8]+MAC[9]+":"+MAC[10]+MAC[11]
    retorno = frequenciaVisitaClienteMes(mac,"2015")
    
    data_to_plot ={}
    data_to_plot['m1'] = retorno[0]
    data_to_plot['m2'] = retorno[1]
    data_to_plot['m3'] = retorno[2]
    data_to_plot['m4'] = retorno[3]
    data_to_plot['m5'] = retorno[4]
    data_to_plot['m6'] = retorno[5]
    data_to_plot['m7'] = retorno[6]
    data_to_plot['m8'] = retorno[7]
    data_to_plot['m9'] = retorno[8]
    data_to_plot['m10'] = retorno[9]
    data_to_plot['m11'] = retorno[10]
    data_to_plot['m12'] = retorno[11]

    context['plot']=data_to_plot
    return render_to_response('specificMAC.html',context)

def postMacTable(request):
    erro =request.method
    if request.method == "POST":
        post = request.POST.copy()
        MAC = post['myMAC']
        Mes = post['myMes']
        Ano = post['myAno']
        # retorno = frequenciaVisitaClienteMes(mac,"2015")
        response = {'status': 1, 'mac':MAC[0]+MAC[1]+MAC[3]+MAC[4]+
        							   MAC[6]+MAC[7]+MAC[9]+MAC[10]+
        							   MAC[12]+MAC[13]+MAC[15]+MAC[16], 'mes':Mes,'ano':Ano} 
        return HttpResponse(json.dumps(response), content_type='application/json')

    else:
        erro = u"Erro2"
        response = {'status': 0} 
    return HttpResponse(json.dumps(response), content_type='application/json')


def postName(request):
    erro =request.method
    if request.method == "POST":
        post = request.POST.copy()
        MAC = post['myMAC']
        nome = post['myName']
        response = {'status': 1, 'mac':MAC, 'mac_name':nome} 
        return HttpResponse(json.dumps(response), content_type='application/json')

    else:
        erro = u"Erro2"
        response = {'status': 0} 
    return HttpResponse(json.dumps(response), content_type='application/json')

def portMacsquares(request):
    erro =request.method
    if request.method == "POST":
        post = request.POST.copy()
        MAC = post['myMAC']
        Dia = post['myDia']
        Mes = post['myMes']
        Ano = post['myAno']
        # retorno = frequenciaVisitaClienteMes(mac,"2015")
        response = {'status': 1, 'mac':MAC, 'mes':Mes,'ano':Ano, 'dia':Dia} 
        return HttpResponse(json.dumps(response), content_type='application/json')

    else:
        erro = u"Erro2"
        response = {'status': 0} 
    return HttpResponse(json.dumps(response), content_type='application/json')

def getMac(request,query):
    context = {'form':macForm}
    data_to_plot = {}
    # data_to_plot['nome'] 
    data_to_plot['mac'] = str(query)
    tempomedio, total = tempoMedioCliente(str(query)) 
    t_medio = str(tempomedio[0])+":"+str(tempomedio[1])+":"+str(tempomedio[2])+":"+str(tempomedio[3])
    data_to_plot['total'] = total
    data_to_plot['tempo_medio'] = t_medio
    data_to_plot['fabricante'] = achaFabricante(data_to_plot['mac'])
    data_to_plot['nome'] = achaNome(data_to_plot['mac'])

    data_to_plot['redes'] = []
    redes = achaRedes(str(query))
    for i in range (0, len(redes)):
        data_to_plot['redes'].append(redes[i])

    context['plot'] = data_to_plot 
    return render(request, "findMac.html",context)

def showMacDatas(request,query):
    startDate = query.split(":")[6]
    mac = query.split(":")[0]+":"+query.split(":")[1]+":"+query.split(":")[2]+":"+query.split(":")[3]+":"+query.split(":")[4]+":"+query.split(":")[5]
    dia = startDate.split("/")[0]
    if len(dia)<2:
        dia = "0"+dia
    startDate = startDate.split("/")[2]+"-"+startDate.split("/")[1]+"-"+dia
    context = {}
    total = quantidadeVisitasClienteNaLoja(mac)
    dados = {}
    dados['total'] = total
    dados['tempo_medio'] = 111
    context['valores'] =dados
    return render_to_response("macDatas.html",context)


def showTableMonth(request,query):
    context = {}    
    return render(request,"indexspecific.html",context)
