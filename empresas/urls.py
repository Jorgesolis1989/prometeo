from django.conf.urls import patterns, include, url
from django.contrib import admin
from empresas import views

urlpatterns = patterns('',
                       url(r'^selection_concept', views.selection_concepto, name="selection_concept"),
                       )