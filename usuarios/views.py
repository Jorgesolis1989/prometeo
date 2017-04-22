from django.contrib.auth.models import User
from django.shortcuts import render, render_to_response,   get_object_or_404
from usuarios.forms import FormularioLogin, FormularioRegistroUsuario , FormularioActualizarUsuario , FormularioCambiarContrasena
from modelos_existentes.models import  Usuario_Web , Usuario_Web_Vinculacion_Folder
from usuarios.models import Perfil_Usuario
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login
from carpetas.views import cargar_carpetas

from empresas.views import cargar_empresas_vinculadas


from django.utils import timezone
from django.utils.timezone import activate
from django.conf import settings
activate(settings.TIME_ZONE)

import hashlib, datetime, random
import hmac
import string
from django.core.mail import EmailMultiAlternatives

# Create your views here.
def utc_to_local(utc_dt):
    return utc_dt.replace(tzinfo=timezone.utc).astimezone(tz=None)

#Pagina de login
def login_user(request):
    mensaje = ""
    mensajeE = ""

    if request.user.is_authenticated() and not request.user.is_superuser:
        empresas_vinculadas = cargar_empresas_vinculadas(request)
        return render(request, 'base-principal.html', {'empresas_vinculadas': empresas_vinculadas  , 'carpetas': cargar_carpetas(request)})

    elif request.method == 'POST':
        form = FormularioLogin(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            usuario = authenticate(username=cd['username'], password=cd['password'])
            if usuario is not None:
                if usuario.is_active:
                    login(request, usuario)


                    #Redireccionar
                    return render(request, 'base-principal.html', {'empresas_vinculadas': cargar_empresas_vinculadas(request) , 'carpetas': cargar_carpetas(request) })
                else:
                   mensajeE = "Usuario no activado"
            else:
                   mensajeE = "Datos erróneos. Por favor, inténtelo otra vez.    "
    else:
        form = FormularioLogin()
    return render(request, 'login.html', {'mensaje': mensaje,'mensajeE': mensajeE, 'form': form })




# Este metodo se utiliza para el cambio de contrasena del usuario
def cambio_contrasena(request):

    empresas_vinculadas = cargar_empresas_vinculadas(request)
    mensaje = ""

    if request.method == 'POST' and 'btnCambiarContrasena':
        usuario = User.objects.get(email = request.user.email)
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

    return render(request, 'cambiar_contrasena.html', {'form': form , 'mensaje': mensaje , 'empresas_vinculadas': empresas_vinculadas , 'carpetas': cargar_carpetas(request) })



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
                #print("email" + str(email_usuario))

            #Si el usuario no existe, lo crea
            except User.DoesNotExist:
                    # Creando el usuario en la tabla auth_user de django
                    usuario = User()
                    usuario.first_name = cd["first_name"]
                    usuario.email = cd["email"]
                    usuario.set_password(cd["password"])
                    usuario.is_active = False

                    try:
                       integer = int(User.objects.latest('id').id)
                    except Exception as e:
                        print(e)
                        integer = 100

                    usuario.username = integer + 1

                    #Crea el usuario en la BD si hay excepcion
                    try:
                        usuario.save()
                    except Exception as e:
                        print(e)

                    # Creando el usuario web en la base de datos de Prometeo tabla usrios_web
                    usuario_web = Usuario_Web()
                    usuario_web.nmbre_usrio = usuario.first_name
                    usuario_web.email_usrio = cd["email"]
                    usuario_web.clve_accso = '123'
                    usuario_web.email_altrntvo = cd["email_alternativo"]
                    usuario_web.tlfno_mvil = cd["tel_movil"]
                    usuario_web.tlno_fjo = cd["tel_fijo"]
                    usuario_web.nit_tcro_ascdo = cd['nit_empresa']

                    try:

                        usuario_web.save()
                        # Guardando información de las empresas
                        """
                        usuario_web_vinculacion_empresa = Usuario_Web_Vinculacion_Empresa()
                        usuario_web_vinculacion_empresa.id_emprsa = 10
                        usuario_web_vinculacion_empresa.email_usrio = usuario_web
                        usuario_web_vinculacion_empresa.save()
                        """
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
                        print(e)
                    # Enviar un email de confirmación
                    #email_subject = 'Confirmación de Cuenta "PROMETEO"'
                    #email_body = "Señor(a)%s, Gracias por registrarte.\n Para activar tu cuenta da click en el siguiente enlace " \
                                 #"en menos de 48 horas: http://%s/activate/%s" % (usuario.get_full_name(),str(request.META['HTTP_HOST']) , activation_key)
                    print(usuario.email)
                    subject = 'Confirmación de Cuenta "PROMETEO"'
                    text_content = ''
                    html_content = "<!DOCTYPE>" \
                                    "<html>" \
                                    "<head>" \
                                    "    <meta charset='utf-8'> " \
                                    "    <meta name='viewport' content='width=device-width'> " \
                                    "    <meta http-equiv='X-UA-Compatible' content='IE=edge'> " \
                                    "    <title>Confirmación de Cuenta PROMETEO</title>" \
                                    "    <style type='text/css'>" \
                                    "        html," \
                                    "        body {" \
                                    "            margin: 0 auto !important;" \
                                    "            padding: 0 !important;" \
                                    "            width: 500px !important;" \
                                    "            background-color: #56ACDE;" \
                                    "        }" \
                                    "        * {" \
                                    "            -ms-text-size-adjust: 100%;" \
                                    "            -webkit-text-size-adjust: 100%;" \
                                    "        }" \
                                    "        div[style*='margin: 16px 0'] {" \
                                    "            margin:0 !important;" \
                                    "        }" \
                                    "        table," \
                                    "        td {" \
                                    "            mso-table-lspace: 0pt !important;" \
                                    "            mso-table-rspace: 0pt !important;" \
                                    "        }" \
                                    "        table {" \
                                    "            border-spacing: 0 !important;" \
                                    "            border-collapse: collapse !important;" \
                                    "            table-layout: fixed !important;" \
                                    "            Margin: 0 auto !important;" \
                                    "        }" \
                                    "        table table table {" \
                                    "            table-layout: auto;" \
                                    "        }" \
                                    "        img {" \
                                    "            -ms-interpolation-mode:bicubic;" \
                                    "        }" \
                                    "        .yshortcuts a {" \
                                    "            border-bottom: none !important;" \
                                    "        }" \
                                    "        .mobile-link--footer a," \
                                    "        a[x-apple-data-detectors] {" \
                                    "            color:inherit !important;" \
                                    "            text-decoration: underline !important;" \
                                    "        }" \
                                    "    </style>" \
                                    "    <style>" \
                                    "        @media screen and (max-width: 500px) {" \
                                    "            .email-container {" \
                                    "                width: 100% !important;" \
                                    "                margin: auto !important;" \
                                    "            }" \
                                    "        }" \
                                    "    </style>" \
                                    "</head>" \
                                    "<body>" \
                                    "<table cellpadding='0' cellspacing='0' width='500px' style='border-collapse:collapse; border-style: solid; border-width: 1px;'>" \
                                    "    <table cellspacing='0' cellpadding='0' border='0' align='center' width='500px'  class='email-container'>" \
                                    "        <tr>" \
                                    "            <td style='padding: 10px 0;'>" \
                                    "            </td>" \
                                    "        </tr>" \
                                    "    </table>" \
                                    "    <table cellspacing='0' cellpadding='0' align='center' bgcolor='#ffffff' width='500px' class='email-container'>" \
                                    "        <tr colspan=\"3\" style=\"border: hidden;\">" \
                                    "            <td colspan=\"2\" align=\"right\">" \
                                    "                <img src='http://54.200.145.159:8080/static/images/logo.png' width=\"300\" height=\"100\" alt='alt_text' border='0' align='center' >" \
                                    "            </td>" \
                                    "            <td align=\"right\" style=\"padding: 20px;\">" \
                                    "                <img src='http://54.200.145.159:8080/static/images/sql_soluciones.png' alt='alt_text' border='0' top='15px' width='60' style='top: 45px;right: -50px;'>" \
                                    "            </td>" \
                                    "        </tr>" \
                                    "        <tr>" \
                                    "            <td colspan=\"3\" style='padding: 10px; text-align: justify; font-family: sans-serif; font-size: 15px; mso-height-rule: exactly; line-height: 20px; color: #555555;'>" \
                                    "                <hr>" \
                                    "                Estimado(a) Señor(a)" + str(usuario.get_full_name())+". Gracias por registrarse."  \
                                    "                <br>" \
                                    "                <br>" \
                                    "                Para activar tu cuenta da click en el siguiente enlace en menos de 48 horas: <b>http://"+ str(request.META['HTTP_HOST'])+"/activate/"+ str(activation_key)+ "" \
                                                    "<br>" \
                                    "                <div align='center'>" \
                                    "                <br>" \
                                    "                <br>" \
                                    "                </div>" \
                                    "                En el siguiente enlace podr&aacute; conocer más sobre nosotros::" \
                                    "                <br><br>" \
                                    "                <div align='center'><b>http://"+str(request.META['HTTP_HOST'])+"</b></div>" \
                                    "                <br>" \
                                    "                Cualquier duda o informaci&oacute;n adicional escribir al correo electr&oacute;nico <a href=\"mailto:info@sqlsoluciones.com \">info@sqlsoluciones.com </a>" \
                                    "            <hr>" \
                                    "            </td>" \
                                    "        </tr>" \
                                    "    </table>" \
                                    "    <table cellspacing='0' cellpadding='0' border='0' align='center' width='500px' style='margin: auto;' class='email-container'>" \
                                    "            <tr>" \
                                    "                <td style='padding: 20px; width: 100%;font-size: 12px; font-family: sans-serif; mso-height-rule: exactly; line-height:18px; text-align: center; color: #585858; font-weight:bold;'>" \
                                    "                    PROMETEO<br>" \
                                    "                    <a href=\"http://54.200.145.159:8080\">SQL Soluciones S.A</a> - 2017" \
                                    "                </td>" \
                                    "            </tr>" \
                                    "        </table>" \
                                    "</table>" \
                                    "</body>" \
                                    "</html>"

                    from_email = '"PROMETEO" <sivore@correounivalle.edu.co>'
                    to = usuario.email
                    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
                    msg.attach_alternative(html_content, "text/html")
                    msg.send()

                    #Se valida que el email alternativo no sea usado por otro usuario
                    try:
                        email_alternativo_exist = Usuario_Web.objects.filter(email_usrio=cd["email_alternativo"], actvo=1)
                        if email_alternativo_exist is not None:
                            mensaje = "Advertencia:\n El correo alternativo ingresado ya existe para otro usuario.\n" \
                                       "Por favor actualizarlo cuando inicie sesión."
                    except Exception as e:
                        print(e, "warning email")

                    #return render_to_response('registration/registro_exitoso.html')
                    return render(request, 'registration/registro_exitoso.html', {'form': form, 'mensaje': mensaje})

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
        #print("timezone ---", utc_to_local(timezone.now()))
        #print("perfil_usuario.key_expires", perfil_usuario.key_expires)
        #print(utc_to_local(timezone.now()))
        if perfil_usuario.key_expires < utc_to_local(timezone.now()):
        #    print("perfil_usuario.key_expires", perfil_usuario.key_expires)

        #    print("timezone ---", utc_to_local(timezone.now()))
            return render_to_response('registration/registro_expirado.html')

        # Si el token no ha expirado, se activa el usuario y se muestra el html de confirmación
        usuario = perfil_usuario.usuario
        print ("usuario",usuario)
        usuario.is_active = True
        usuario.save()

        # Aquí estamos
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

    empresas_vinculadas = cargar_empresas_vinculadas(request)
    mensaje = ""
    usuario = get_object_or_404(User, email=request.user.email)
    usuario_web = Usuario_Web.objects.get(email_usrio= usuario.email)

    if request.method == 'POST' and "btnUpdate":
        form = FormularioActualizarUsuario(request.POST)

        if form.is_valid():
            usuario.first_name = form.cleaned_data['first_name']
            usuario_web.nit_tcro_ascdo = form.cleaned_data['nit_empresa']
            usuario_web.nmbre_usrio = usuario.first_name
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

            form = FormularioActualizarUsuario()
    else:

        form = FormularioActualizarUsuario()
        form.initial = {'first_name': usuario.first_name, 'nit_empresa': usuario_web.nit_tcro_ascdo , 'email': usuario.email,  'email_alternativo': usuario_web.email_altrntvo,
                        'tel_fijo': usuario_web.tlno_fjo, 'tel_movil': usuario_web.tlfno_mvil}
        form.fields['email'].widget.attrs['readonly'] = True

    return render(request, 'actualizar-usuario.html', {'form': form , 'mensaje': mensaje , 'empresas_vinculadas': empresas_vinculadas , 'carpetas': cargar_carpetas(request)})

