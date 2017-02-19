from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, render_to_response, redirect,  get_object_or_404
from usuarios.forms import FormularioLogin, FormularioRegistroUsuario , FormularioActualizarUsuario , FormularioCambiarContrasena
from usuarios.models import Usuario, Perfil_Usuario
from django.contrib.auth import authenticate, login
from django.template.context import RequestContext
from django.core.mail import send_mail
from django.core.validators import validate_email
from django.utils import timezone
import hashlib, datetime, random
from usuarios.models import Usuario
import hmac
import string

# Create your views here.

#Pagina de login
def login_user(request):
    mensaje = ""
    mensajeE = ""
    if request.user.is_authenticated() and not request.user.is_superuser:
        return render(request, 'base-usuario.html')

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
                    return render(request, 'base-usuario.html')
                else:
                   mensajeE = "Usuario no activado"
            else:
                   mensajeE = "Datos erróneos. Por favor, inténtelo otra vez.    "
    else:
        form = FormularioLogin()
    return render(request, 'login.html', {'mensaje': mensaje,'mensajeE': mensajeE, 'form': form })


# Este metodo se utiliza para el cambio de contrasena del usuario
def cambio_contrasena(request):

    mensaje = ""

    if request.method == 'POST' and 'btnCambiarContrasena':
        usuario = Usuario.objects.get(username = request.user.username)
        print(usuario)
        form = FormularioCambiarContrasena(request.POST)
        #Si el formulario es valido y tiene datos

        if form.is_valid():
            if usuario.check_password(form.cleaned_data['old_password']):
                usuario.set_password(form.cleaned_data['new_password'])
                try:
                    usuario.save()
                except Exception as e:
                    print (e)
                user = authenticate(username=usuario.username, password=form.cleaned_data['new_password'])
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

    form = FormularioRegistroUsuario(request.POST)

    if request.method == 'POST' and "btnRegister":
        form = FormularioRegistroUsuario(request.POST)
        #Si el formulario es valido y tiene datos
        if form.is_valid():
            cd = form.cleaned_data
            #Capture correo
            email = cd["email"]
            try:
                #Consultando el usuario en la base de datos.
                email_usuario = Usuario.objects.get(email=email)
                print("usuario" + str(email_usuario))

            #Si el usuario no existe, lo crea
            except Usuario.DoesNotExist:
                    # Creando el usuario
                    usuario = Usuario()
                    usuario.first_name = cd["first_name"]
                    usuario.last_name = cd["last_name"]
                    usuario.email = cd["email"]
                    usuario.set_password(cd["password"])
                    usuario.username = cd["nombre_usuario"]
                    usuario.email_alternativo = cd["email_alternativo"]
                    usuario.telefono_fijo = cd["tel_fijo"]
                    usuario.telefono_movil = cd["tel_movil"]
                    usuario.is_active = False

                    #Crea el usuario en la BD si hay excepcion
                    try:
                        usuario.save()
                        #return redirect("login_user")
                        #ocultar = True
                        #return render(request, 'registrar-usuario.html', {'form': form, 'mensaje': mensaje, 'ocultar':ocultar})
                    except Exception as e:
                        print(e)

                    # Borrando los datos del formulario y enviando el mensaje de satisfacion
                    #form = FormularioRegistroUsuario()
                    mensaje = "Registro satisfactorio. Al correo " + usuario.email + " se enviará un mensaje confirmando el registro"
                    llamarMensaje = "exito_usuario"
                    # Enviando correo electronico de confirmacion de registro.
                    #mensajeC = "Señor(a) ", usuario.first_name, usuario.last_name, "\n su registro a PROMETEO fue exitoso!!\n \n ", "Estos son los datos de acceso ingresados \n \n  Nombre de usuario: " + usuario.email, "\n Contraseña: ", usuario.password
                    #send_mail("Envío de confirmación de regitro a PROMETEO", mensajeC, settings.EMAIL_HOST_USER, [usuario.email], fail_silently=False)
                    #print("send_mail -->" + send_mail)

                    pw = make_pw_hash('123')
                    print(pw)

                    activation_key = pw[:15]
                    key_expires = datetime.datetime.today() + datetime.timedelta(2)

                    # Crear el perfil del usuario
                    perfil_usuario = Perfil_Usuario(usuario=usuario, activation_key=activation_key, key_expires=key_expires)
                    perfil_usuario.save()

                    # Enviar un email de confirmación
                    email_subject = 'Confirmación de Cuenta "PROMETEO"'
                    email_body = "Señor(a)%s, Gracias por registrarte.\n Para activar tu cuenta da click en el siguiente enlace " \
                                 "en menos de 48 horas: http://127.0.0.1:8000/activate/%s" % (usuario.username, activation_key)

                    send_mail(email_subject, email_body, 'settings.EMAIL_HOST_USER',[email], fail_silently=False)

                    return HttpResponseRedirect('/register_success')
            else:
                form = FormularioRegistroUsuario()
                mensajeE = "Ya existe un usuario con el correo " + email +""
                return render(request, 'registrar-usuario.html', {'form': form, 'mensajeE': mensajeE,  'ocultar':ocultar})
        else:
            return render(request, 'registrar-usuario.html', {'form': form, 'mensaje': mensaje,  'ocultar':ocultar})
    else:
        form = FormularioRegistroUsuario()
    return render(request, 'registrar-usuario.html', {'form': form, 'mensaje': mensaje,  'ocultar':ocultar})

def confirmar_registro(request, activation_key=None):
    # Verifica que el usuario ya está logeado
    if request.user.is_authenticated():
        #HttpResponseRedirect('/login')
        return render(request, 'base-usuario.html')

    # Verifica que el token de activación sea válido y sino retorna un 404
    perfil_usuario = get_object_or_404(Perfil_Usuario, activation_key=activation_key)

    # verifica si el token de activación ha expirado y si es así renderiza el html de registro expirado
    if perfil_usuario.key_expires < timezone.now():
        return render_to_response('registration/registro_expirado.html')
    # Si el token no ha expirado, se activa el usuario y se muestra el html de confirmación
    usuario = perfil_usuario.usuario
    usuario.is_active = True
    usuario.save()
    return render_to_response('registration/registro_confirmado.html')

# Este metodo se utiliza para el cambio de contrasena del usuario
def actualizar_usuario(request):
    mensaje = ""
    usuario = Usuario.objects.get(username=request.user.username)

    if request.method == 'POST' and "btnUpdate":
        form = FormularioActualizarUsuario(request.POST)

        if form.is_valid():
            usuario.first_name = form.cleaned_data['first_name']
            usuario.last_name = form.cleaned_data['last_name']
            usuario.email_alternativo = form.cleaned_data['email_alternativo']
            usuario.telefono_movil = form.cleaned_data['tel_movil']
            usuario.telefono_fijo= form.cleaned_data['tel_fijo']

            try:
                usuario.save()
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
        form.initial = {'first_name': usuario.first_name, 'last_name': usuario.last_name , 'email': usuario.email, 'nombre_usuario': usuario.username, 'email_alternativo': usuario.email_alternativo,
                        'tel_fijo': usuario.telefono_fijo, 'tel_movil': usuario.telefono_movil}
        form.fields['email'].widget.attrs['readonly'] = True
    return render(request, 'actualizar-usuario.html', {'form': form , 'mensaje': mensaje})
