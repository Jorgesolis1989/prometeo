from django.shortcuts import render
#from empresas.models import Logo_Empresa
from modelos_existentes.models import Empresa , Usuario_Web_Vinculacion_Empresa
from django.contrib.auth.models import User
from modelos_existentes.models import Usuario_Web
from django.shortcuts import render, get_object_or_404
from empresas.forms import FormularioVincularEmpresas


def seleccion_concepto(request):
    return render(request, 'seleccion-concepto.html', {'empresas': cargar_empresas_vinculadas(request)})

def cargar_empresas_vinculadas(request):
        usuario_web = get_object_or_404(Usuario_Web, email_usrio=request.user.email)
        Empresas_Vinculadas = Usuario_Web_Vinculacion_Empresa.objects.filter(email_usrio= usuario_web.email_usrio).values_list('id_emprsa')
        return Empresa.objects.filter(id_emprsa__in=Empresas_Vinculadas , actvo=True)

     #   return Logo_Empresa.objects.filter(empresa__id_empresa__in=Empresas_Vinculadas)


def vincular_empresas(request):
    empresas = Empresa.objects.filter(actvo=True)
    if request.method == 'POST' and 'btnRegisterEmpresa':
        #display_type = request.POST['empresas']
        #display_type = FormularioVincularEmpresas(request.POST)
        display_type = request.POST.getlist('empresas')
        print(display_type)
        for display in display_type:
            display

    #else:
    #   empresas = Empresa.objects.filter(actvo=True)

    return render(request, 'vincular_empresas.html', {'todas_las_empresas':  empresas , 'empresas_vinculadas': cargar_empresas_vinculadas(request)})