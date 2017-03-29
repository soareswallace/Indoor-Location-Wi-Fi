from bson import ObjectId
from django import forms
from models import *

class macForm(forms.Form):
    mac = forms.CharField(label='Mac', max_length=100)
    dia = forms.CharField(label='Dia', max_length=100)
    ano = forms.CharField(label='Ano', max_length=100)
    mes = forms.CharField(label='Mes', max_length=100)
    data = forms.CharField(label='Ano', max_length=100)
    genero = forms.CharField(label='genero',max_length=100)
    nomeMac = forms.CharField(label='Nome', max_length=200)