from django.shortcuts import render

from modelos_existentes.models import Usuario_Web_Vinculacion_Folder , Usuario_Web
from empresas.views import cargar_empresas_vinculadas, cargar_logos_empresas


# Create your views here.

def crear_carpeta(request):
    if request.POST:
        # Obteniendo el usuario
        usuario_web = Usuario_Web.objects.get(email_usrio=request.user.email)

        # Creando el Usuario Web Vinculacion folder
        usuario_web_vinculacion_folder = Usuario_Web_Vinculacion_Folder()
        usuario_web_vinculacion_folder.email_usrio = usuario_web
        usuario_web_vinculacion_folder.nmbre_flder = request.POST['name_carpeta']

        # Numero de folder Autoincrement
        try:
            nmro_flder = Usuario_Web_Vinculacion_Folder.objects.latest('nmro_flder').nmro_flder
        except Exception as e:
            nmro_flder = 0

        usuario_web_vinculacion_folder.nmro_flder = nmro_flder  + 1

        #Numero de orden folder usuario
        ultimo_folder_registrado = Usuario_Web_Vinculacion_Folder.objects.filter(email_usrio=usuario_web)
        if ultimo_folder_registrado:
           nmro_orden = ultimo_folder_registrado.latest('nmro_orden').nmro_orden + 1
        else:
            nmro_orden = 1
        usuario_web_vinculacion_folder.nmro_orden = nmro_orden

        try:
            usuario_web_vinculacion_folder.save()
        except Exception as e:
            print(e)

    return render(request, 'base-principal.html', {'empresas_vinculadas': cargar_empresas_vinculadas(request) , 'logos_empresas':cargar_logos_empresas(request), 'carpetas': cargar_carpetas(request)})

def cargar_carpetas(request):
    usuario_web = Usuario_Web.objects.get(email_usrio=request.user.email)
    return Usuario_Web_Vinculacion_Folder.objects.filter(email_usrio=usuario_web)
