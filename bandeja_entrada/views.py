from django.shortcuts import render
from empresas.views import *

def listar_bandeja(request):
    print('ingreso a listar banjde')
    return render(request, 'bandeja_entrada.html',{'empresas_vinculadas': cargar_empresas_vinculadas(request),
                                                       'logos_empresas': cargar_logos_empresas(request),
                                                        })