from django.conf.urls import patterns, include, url
from bandeja_entrada import views

urlpatterns = patterns('',
    url(r'^inbox_list', views.listar_bandeja, name="inbox_list"),
    url(r'^certificado/(?P<id_documento>\w{1,50})/$', views.descargar_pdf, name='id_certificado'),
                       )