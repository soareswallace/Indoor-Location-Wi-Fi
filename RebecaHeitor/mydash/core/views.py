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
from visitors.models import distribuicaoHorariaClientes
from django.http import HttpResponseRedirect


def index(request):
	return render(request, 'about.html')


