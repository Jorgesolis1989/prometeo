from django.shortcuts import render
from empresas.models import Empresa

def selection_concepto(request):
    return render(request, 'seleccion-concepto.html', {'empresas': Empresa.objects.all()})

