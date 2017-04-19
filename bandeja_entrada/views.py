from django.shortcuts import render
from modelos_existentes.models import Documentos_Correo
from empresas.views import *

def listar_bandeja(request):
    usuario = get_object_or_404(User, email=request.user.email)
    usuario_web = Usuario_Web.objects.get(email_usrio= usuario.email)

    documentos_correo = Documentos_Correo.objects.filter(email_usrio=usuario.email)

    return render(request, 'bandeja_entrada.html',{'empresas_vinculadas': cargar_empresas_vinculadas(request),
                                                   'documentos_correo': documentos_correo,
                                                   })
