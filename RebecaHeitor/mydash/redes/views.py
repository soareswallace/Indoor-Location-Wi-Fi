from decimal import Decimal
from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from visitors.models import *
from django.http import HttpResponseRedirect
import json
import datetime
from django.core import serializers

def index(request):
	context = {}
	redes, taxa = redes_mais_acessadas()
	data_to_plot={}
	data_to_plot['data1'] = []

	for i in range (0, len(redes)):
		taxa [i] = float(Decimal(taxa[i]).quantize(Decimal('.01')))
		redes[i] = redes[i].encode('utf-8')
		if redes[i]=="null":
			redes[i] = "UNKNOWN"
		data_to_plot['data1'].append([str(redes[i]), taxa[i]] )

	
	context['plot'] =  data_to_plot
	return render(request, 'redes.html', context)

