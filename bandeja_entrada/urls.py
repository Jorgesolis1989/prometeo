from django.conf.urls import patterns, include, url
from bandeja_entrada import views

urlpatterns = patterns('',
    url(r'^inbox_list', views.listar_bandeja, name="inbox_list"),)