from django.conf.urls import patterns, include, url
from django.contrib import admin
from empresas import views

urlpatterns = patterns('',
                       url(r'^selection_concept', views.seleccion_concepto, name="selection_concept"),
                       url(r'^vinculate_enterprise', views.vincular_empresas, name="vinculate_enterprise"),
                       )