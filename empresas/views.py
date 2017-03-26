from django.shortcuts import render, redirect
from empresas.models import Empresa_Con_Logo
from modelos_existentes.models import Empresa , Usuario_Web_Vinculacion_Empresa , Usuario_Web_Vinculacion_Folder
from django.contrib.auth.models import User
from modelos_existentes.models import Usuario_Web
from certificados.forms import FormularioEscogerCertificado
from django.shortcuts import render, get_object_or_404
import datetime
from certificados.views import  generarPdf_general

from empresas.forms import FormularioVincularEmpresas

from django.utils.timezone import activate
from django.conf import settings
activate(settings.TIME_ZONE)


def cargar_logos_empresas(request):
    return Empresa_Con_Logo.objects.filter(activo=1)

def seleccion_concepto(request, id_emprsa=None):
    # POST
    if request.POST and "btnGenerer" in request.POST:
        form = FormularioEscogerCertificado(request.POST)
        print(form)
        if form.is_valid():
            tipo_certificado = form.cleaned_data["tipo_certificado"]
            periodo = form.cleaned_data["tipo_certificado"]
            return generarPdf_general(request,tipo_certificado, periodo,id_emprsa )
        else:
            print("no valido")

    try:
        empresa_logo = Empresa_Con_Logo.objects.get(id_emprsa=id_emprsa)
    except Exception:
        return redirect('login_user')

    logo_empresa = empresa_logo.lgtpo_emprsa

    return render(request, 'seleccion-concepto.html', {'empresas_vinculadas': cargar_empresas_vinculadas(request) ,
                                                       'logos_empresas': cargar_logos_empresas(request),
                                                       'logo_empresa':logo_empresa , 'carpetas': cargar_carpetas(request) ,
                                                        'FormularioEscogerCertificado': FormularioEscogerCertificado()
                                                        })

def cargar_empresas_vinculadas(request):
        usuario_web = get_object_or_404(Usuario_Web, email_usrio=request.user.email ,)
        Empresas_Vinculadas = Usuario_Web_Vinculacion_Empresa.objects.filter(email_usrio= usuario_web.email_usrio , actvo= 1).values_list('id_emprsa')
        return Empresa.objects.filter(id_emprsa__in=Empresas_Vinculadas , actvo=1)

     #   return Logo_Empresa.objects.filter(empresa__id_empresa__in=Empresas_Vinculadas)


def vincular_empresas(request):
    empresas_vinculadas = cargar_empresas_vinculadas(request)
    empresas = Empresa.objects.filter(actvo=1)


    if request.method == 'POST' and 'btnRegisterEmpresa':
        checkboxs_selected = request.POST.getlist('empresas_checkbox[]')
        empresas_vinculadas_arreglo = []
        for empresa_vinculada in  empresas_vinculadas:
            empresas_vinculadas_arreglo.append(str(int(empresa_vinculada.id_emprsa)))

        #print("checkbox_selected " , checkboxs_selected)
        #print("empresas_vinculadas " ,empresas_vinculadas_arreglo)
        empresas_a_ingresar = list(set(checkboxs_selected) - set(empresas_vinculadas_arreglo))
        #print("checkbox_selected - empresas_vinculadas " , empresas_a_ingresar)

        usuario_web = Usuario_Web.objects.get(email_usrio = request.user.email , actvo=1)

        ## Ingresar empresas
        for empresa_a_ingresar in  empresas_a_ingresar:
            usuario_web_vinculacion_empresa = Usuario_Web_Vinculacion_Empresa()
            usuario_web_vinculacion_empresa.email_usrio = usuario_web
            usuario_web_vinculacion_empresa.id_emprsa = int(empresa_a_ingresar)
            usuario_web_vinculacion_empresa.fcha_crcion = datetime.datetime.now()
            usuario_web_vinculacion_empresa.actvo = 1

            try:
                usuario_web_vinculacion_empresa.save()
            except Exception as e:
                print(e)


        #print("checkbox selected con nuevas empresas",checkboxs_selected)

        ## Sacar empresas
        empresas_a_sacar = list(set(empresas_vinculadas_arreglo) - set(checkboxs_selected) )
        #print("empresas a sacar " , empresas_a_sacar)
        for empresa_a_sacar in empresas_a_sacar:
            usuario_web_vinculacion_empresa_a_sacar = Usuario_Web_Vinculacion_Empresa.objects.get(id_emprsa=empresa_a_sacar , email_usrio=usuario_web , actvo=1 )
            usuario_web_vinculacion_empresa_a_sacar.actvo = 0
            try:
                usuario_web_vinculacion_empresa_a_sacar.save()
            except Exception as e:
                print(e)

        empresas_vinculadas = cargar_empresas_vinculadas(request)

    #else:
    #   empresas = Empresa.objects.filter(actvo=True)

    return render(request, 'vincular_empresas.html', {'todas_las_empresas':  empresas , 'empresas_vinculadas': empresas_vinculadas , 'logos_empresas': cargar_logos_empresas(request), 'carpetas': cargar_carpetas(request)})



def cargar_carpetas(request):
    usuario_web = Usuario_Web.objects.get(email_usrio=request.user.email)
    #print(usuario_web)
    carpetas = Usuario_Web_Vinculacion_Folder.objects.filter(email_usrio=usuario_web)
    #print(carpetas)
    return carpetas