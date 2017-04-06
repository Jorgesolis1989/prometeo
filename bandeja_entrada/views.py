from django.shortcuts import render
from empresas.views import *

def listar_bandeja(request):
    return render(request, 'bandeja_entrada.html',{'empresas_vinculadas': cargar_empresas_vinculadas(request),
                                                        })