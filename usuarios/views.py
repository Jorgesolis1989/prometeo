from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import render, render_to_response, redirect,  get_object_or_404
from usuarios.forms import FormularioLogin, FormularioRegistroUsuario , FormularioActualizarUsuario , FormularioCambiarContrasena
from usuarios.models import  Perfil_Usuario , Usuario_Web, Usuario_Web_Vinculacion_Empresa
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login
from django.template.context import RequestContext
from django.core.mail import send_mail


from django.core.validators import validate_email

from django.utils import timezone
from django.utils.timezone import activate
from django.conf import settings
activate(settings.TIME_ZONE)

import hashlib, datetime, random
import hmac
import string

# Create your views here.
def utc_to_local(utc_dt):
    return utc_dt.replace(tzinfo=timezone.utc).astimezone(tz=None)

#Pagina de login
def login_user(request):
    mensaje = ""
    mensajeE = ""

    if request.user.is_authenticated() and not request.user.is_superuser:
        return render(request, 'base-principal.html')

    elif request.method == 'POST':
        form = FormularioLogin(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            usuario = authenticate(username=cd['username'], password=cd['password'])
            if usuario is not None:
                print("autenticado")
                if usuario.is_active:
                    login(request, usuario)
                    #Redireccionar
                    return render(request, 'base-principal.html')
                else:
                   mensajeE = "Usuario no activado"
            else:
                   mensajeE = "Datos erróneos. Por favor, inténtelo otra vez.    "
    else:
        print("else")
        form = FormularioLogin()
    return render(request, 'login.html', {'mensaje': mensaje,'mensajeE': mensajeE, 'form': form })


# Este metodo se utiliza para el cambio de contrasena del usuario
def cambio_contrasena(request):

    mensaje = ""

    if request.method == 'POST' and 'btnCambiarContrasena':
        usuario = User.objects.get(email = request.user.email)
        print(usuario)
        form = FormularioCambiarContrasena(request.POST)
        #Si el formulario es valido y tiene datos

        if form.is_valid():
            if usuario.check_password(form.cleaned_data['old_password']):
                usuario.set_password(form.cleaned_data['new_password'])

                usuario_web = Usuario_Web.objects.get(email_usrio=usuario.email)
                usuario_web.email_usrio = make_password(form.cleaned_data['new_password'])
                try:
                    usuario.save()
                    usuario_web.save()
                except Exception as e:
                    print (e)
                user = authenticate(username=usuario.email, password=form.cleaned_data['new_password'])
                login(request, user)
                mensaje = "La contraseña fue cambiada exitosamente"
            else:
                form._errors["old_password"] = "La contraseña no es igual a la anterior"

    else:
        form = FormularioCambiarContrasena()
        print()

    return render(request, 'cambiar_contrasena.html', {'form': form , 'mensaje': mensaje})



def make_salt():
    salt = ""
    for i in range(5):
        salt = salt + random.choice(string.ascii_letters)
    return salt

def make_pw_hash(pw, salt = None):
    if (salt == None):
        salt = make_salt() #.encode('utf-8') - not working either
        pw_bytes = pw.encode('utf-8')
        salt_bytes = salt.encode('utf-8')
    return hashlib.sha256(pw_bytes + salt_bytes).hexdigest() + ""


#Vista de registro de usuarios
def registro_usuario(request):
    mensaje = ""
    llamarMensaje = ""
    #bandera para ocultar o no los campos en formulario de registro
    ocultar = False

    if request.method == 'POST' and "btnRegister":
        form = FormularioRegistroUsuario(request.POST)
        #Si el formulario es valido y tiene datos
        if form.is_valid():
            cd = form.cleaned_data
            #Capture correo
            email = cd["email"]
            try:
                #Consultando el usuario en la base de datos.
                email_usuario = User.objects.get(email=email)
                print("email" + str(email_usuario))

            #Si el usuario no existe, lo crea
            except User.DoesNotExist:
                    # Creando el usuario en la tabla auth_user de django
                    usuario = User()
                    usuario.first_name = cd["first_name"]
                    usuario.last_name = cd["last_name"]
                    usuario.email = cd["email"]
                    usuario.username = '12'
                    usuario.set_password(cd["password"])
                    usuario.is_active = False
                    integer = int(User.objects.latest('id').id)
                    usuario.username = integer + 1

                    #Crea el usuario en la BD si hay excepcion
                    try:
                        usuario.save()
                    except Exception as e:
                        print(e)

                    # Creando el usuario web en la base de datos de Prometeo tabla usrios_web
                    usuario_web = Usuario_Web()
                    usuario_web.nmbre_usrio = usuario.get_full_name()
                    usuario_web.email_usrio = usuario.email
                    usuario_web.clve_accso = make_password(cd["password"])
                    usuario_web.email_altrntvo = cd["email_alternativo"]
                    usuario_web.tlfno_mvil = cd["tel_movil"]
                    usuario_web.tlno_fjo = cd["tel_fijo"]


                    try:
                        usuario_web.save()
                        # Guardando información de las empresas
                        usuario_web_vinculacion_empresa = Usuario_Web_Vinculacion_Empresa()
                        usuario_web_vinculacion_empresa.id_emprsa = 10
                        usuario_web_vinculacion_empresa.email_usrio = usuario_web
                        usuario_web_vinculacion_empresa.save()
                    except Exception as e:
                        print(e)

                    #Crea la llave de activación y se envia el correo para la confirmación de registro
                    pw = make_pw_hash('123')
                    activation_key = pw[:15]
                    """  se debe de corregir datetime.datetime.today  para no generar warning"""
                    key_expires = datetime.datetime.today() + datetime.timedelta(2)


                    # Crear el perfil del usuario
                    perfil_usuario = Perfil_Usuario(usuario=usuario, activation_key=activation_key, key_expires=key_expires)
                    try:
                        perfil_usuario.save()
                    except Exception as e:
                        print("eror en perfil")
                        print (e)
                    # Enviar un email de confirmación
                    email_subject = 'Confirmación de Cuenta "PROMETEO"'
                    email_body = "Señor(a)%s, Gracias por registrarte.\n Para activar tu cuenta da click en el siguiente enlace " \
                                 "en menos de 48 horas: http://%s/activate/%s" % (usuario.get_full_name(),str(request.META['HTTP_HOST']) , activation_key)
                    send_mail(email_subject, email_body, 'settings.EMAIL_HOST_USER',[email], fail_silently=False)

                    return render_to_response('registration/registro_exitoso.html')

            else:
                form = FormularioRegistroUsuario()
                mensajeE = "Ya existe un usuario con el correo " + email +""
                return render(request, 'registrar-usuario.html', {'form': form, 'mensajeE': mensajeE,  'ocultar':ocultar})
        else:
            return render(request, 'registrar-usuario.html', {'form': form, 'mensaje': mensaje,  'ocultar':ocultar})
    else:
        form = FormularioRegistroUsuario()
    return render(request, 'registrar-usuario.html', {'form': form, 'mensaje': mensaje,  'ocultar':ocultar})

def principal(request):
    return render(request, 'index.html')


def confirmar_registro(request, activation_key=None):
    print("activation_key ---", activation_key)
    # Verifica que el usuario ya está logeado
    if request.user.is_authenticated() and not request.user.is_superuser:
        #HttpResponseRedirect('/login')
        return render(request, 'base-usuario.html')

    # Verifica que el token de activación sea válido y sino retorna un 404
    try:
        perfil_usuario = get_object_or_404(Perfil_Usuario, activation_key=activation_key)
        print("timezone ---", utc_to_local(timezone.now()))
        print("perfil_usuario.key_expires", perfil_usuario.key_expires)
        print(utc_to_local(timezone.now()))
        if perfil_usuario.key_expires < utc_to_local(timezone.now()):
            print("perfil_usuario.key_expires", perfil_usuario.key_expires)
            print("es menor a ")
            print("timezone ---", utc_to_local(timezone.now()))


            return render_to_response('registration/registro_expirado.html')

        # Si el token no ha expirado, se activa el usuario y se muestra el html de confirmación
        usuario = perfil_usuario.usuario
        print ("usuario",usuario)
        usuario.is_active = True
        usuario.save()

        usuario_web = Usuario_Web.objects.get(email_usrio=usuario.email)
        usuario_web.actvo = 1
        usuario_web.estdo_usrio = 1
        usuario_web.save()

    except Exception as e:
        print(e)

    # verifica si el token de activación ha expirado y si es así renderiza el html de registro expirado
    return render_to_response('registration/registro_confirmado.html')

# Este metodo se utiliza para el cambio de contrasena del usuario
def actualizar_usuario(request):
    mensaje = ""
    usuario = get_object_or_404(User, email=request.user.email)
    usuario_web = Usuario_Web.objects.get(email_usrio= usuario.email)


    if request.method == 'POST' and "btnUpdate":
        form = FormularioActualizarUsuario(request.POST)

        if form.is_valid():
            usuario.first_name = form.cleaned_data['first_name']
            usuario.last_name = form.cleaned_data['last_name']


            usuario_web.email_altrntvo = form.cleaned_data['email_alternativo']
            usuario_web.tlfno_mvil  = form.cleaned_data['tel_movil']
            usuario_web.tlno_fjo= form.cleaned_data['tel_fijo']

            try:
                usuario.save()
                usuario_web.save()
            except Exception as e:
                print(e)

            form = FormularioActualizarUsuario()
            mensaje = "Se ha actualizado correctamente sus datos"

        else:
            mensaje = "Formulario con campos sin diligenciar"
            print(form)
            form = FormularioActualizarUsuario()
    else:

        form = FormularioActualizarUsuario()
        form.initial = {'first_name': usuario.first_name, 'last_name': usuario.last_name , 'email': usuario.email,  'email_alternativo': usuario_web.email_altrntvo,
                        'tel_fijo': usuario_web.tlno_fjo, 'tel_movil': usuario_web.tlfno_mvil}
        form.fields['email'].widget.attrs['readonly'] = True
    return render(request, 'actualizar-usuario.html', {'form': form , 'mensaje': mensaje})
