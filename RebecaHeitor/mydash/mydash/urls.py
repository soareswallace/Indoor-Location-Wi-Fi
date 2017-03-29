"""mydash URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from specificMac.views import *
from visitors.views import *

urlpatterns = [
    url(r'^fabricantes/',include('manufacturer.urls')),
    url(r'^redes/',include('redes.urls')),
    url(r'^about/$','core.views.index', name='about'),
    url(r'^visitors/$','visitors.views.index',name='index'),
    url(r'^visitors/live/','visitors.views.live',name='live'),
    url(r'^visitors/charts','visitors.views.allClients', name='allClients'),
    url(r'^visitors/posthour/','visitors.views.postHour', name='postHour'),
    url(r'^visitors/postYear/','visitors.views.postYear', name='postYear'),
    url(r'^visitors/postPeriod/','visitors.views.postPeriod', name='postPeriod'),
    url(r'^visitors/periodCharts/(?P<query>[\w|\W]+)/$','visitors.views.makeDataPeriodo', name='makeDataPeriodo'),
    url(r'^visitors/donutcharts/(?P<query>[\w|\W]+)/$','visitors.views.makeDonutHour', name='makeDonutHour'),
    url(r'^visitors/barcharts/(?P<query>[\w|\W]+)/$','visitors.views.makeBarMonth', name='makeDonutHour'),
    url(r'^teste','core.views.funcaoTeste', name='list'),
    url(r'^mac_dash/(?P<query>[\w|\W]+)/$','specificMac.views.macLineGraph',name='macLineGraph'),
    url(r'^showMac/(?P<query>[\w|\W]+)/$','specificMac.views.getMac', name = 'getMac'),
    url(r'^visitors/postName/','visitors.views.postName', name='postName'),
    url(r'^showMac/postMacTable/$','specificMac.views.postMacTable', name = 'postMacTable'),
    url(r'^showMac/portMacsquares/$','specificMac.views.portMacsquares', name = 'portMacsquares'),
    url(r'^showMac/showMacDatas/(?P<query>[\w|\W]+)/$','specificMac.views.showMacDatas', name = 'showMacDatas'),
    url(r'^showMac/showTableMonth/(?P<query>[\w|\W]+)/$','specificMac.views.showTableMonth', name = 'showTableMonth'),
    url(r'^loadgif/','visitors.views.loadgif',name='loadgif'),
    url(r'^friend/(?P<query>[\w|\W]+)/$','visitors.views.postfriend',name='postfriend'),
    url(r'^vendas/','visitors.views.vendas', name='vendas'),
    url(r'^postvendas/','visitors.views.postGetVendas', name='postGetVendas'),
    url(r'^visitors/periodVendas/(?P<query>[\w|\W]+)/$','visitors.views.vendasDataPeriodo', name='makeDataPeriodo')

] 

