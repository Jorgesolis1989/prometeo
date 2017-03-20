from django.conf.urls import patterns, include, url
from django.contrib import admin
from carpetas import views

urlpatterns = patterns('',
    url(r'^crear_carpeta', views.crear_carpeta, name="create_folder"),
)