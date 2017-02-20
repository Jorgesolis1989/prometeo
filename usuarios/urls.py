from django.conf.urls import patterns, include, url
from django.contrib import admin
from usuarios import views

urlpatterns = patterns('',
    #url(r'^sign_up/', ('yourappname.views.register_user')),
    #url(r'^register_success/', ('yourappname.views.register_success')),
    #url(r'^confirm/(?P<activation_key>\w+)/', ('yourappname.views.register_confirm')),

    url(r'^register_user', views.registro_usuario, name="register_user"),
    url(r'^register_success/', views.confirmar_registro),
    url(r'^activate/(?P<activation_key>\w+)/',views.confirmar_registro, name="register_confirm"),
)