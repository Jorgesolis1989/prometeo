from django.conf.urls import patterns, include, url
from django.contrib import admin
from certificados import views

urlpatterns = patterns('',
                        url(r'^selection_concept/(?P<id_emprsa>\w{1,50})/$', views.seleccion_concepto, name="selection_concept"),
                       )