from bson import ObjectId
from django import forms
from models import *

class dateForm(forms.Form):
    dia = forms.CharField(label='Dia', max_length=100)
    ano = forms.CharField(label='Ano', max_length=100)
    inicial = forms.CharField(label='Ano', max_length=100)
    final = forms.CharField(label='Ano', max_length=100)