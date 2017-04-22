from django.shortcuts import render
from modelos_existentes.models import Documentos_Correo
from empresas.views import *
from django.contrib.auth.decorators import permission_required , login_required
from django.http import HttpResponse
from PROMETEO.settings import MEDIA_ROOT

@login_required
def listar_bandeja(request):
    usuario = get_object_or_404(User, email=request.user.email)

    documentos_correo = Documentos_Correo.objects.filter(email_usrio=usuario.email).order_by('-fcha_dcmnto')

    return render(request, 'bandeja_entrada.html',{'empresas_vinculadas': cargar_empresas_vinculadas(request),
                                                   'documentos_correo': documentos_correo,
                                                   })

@login_required
def descargar_pdf(request, id_documento):
    try:
        documento_correo = Documentos_Correo.objects.get(id_dcmnto=id_documento)

        if documento_correo.email_usrio == request.user.email:

            with open(MEDIA_ROOT +'pdf/'+str(documento_correo.id_dcmnto)+'.pdf', 'rb') as pdf:
                response = HttpResponse(pdf.read(),content_type='application/pdf')
                response['Content-Disposition'] = 'attachment;'  'filename='+str(id_documento)+'.pdf'
                return response

        else:
            return redirect('login_url')

    except Documentos_Correo.DoesNotExist:
        return redirect('login_url')

