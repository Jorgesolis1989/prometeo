from django.shortcuts import render, render_to_response, redirect
from usuarios.forms import FormularioLogin, FormularioRegistroUsuario , FormularioActualizarUsuario , FormularioCambiarContrasena
from usuarios.models import Usuario
from django.contrib.auth import authenticate, login
from django.template.context import RequestContext

from django.core.validators import validate_email

from usuarios.models import Usuario

# Create your views here.

#Pagina de login
def login_user(request):
    mensaje = ""
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
                   mensaje = "Usuario no activado"
            else:
                   mensaje = "Datos erróneos. Por favor, inténtelo otra vez.    "
    else:
        form = FormularioLogin()
    return render(request, 'login.html', {'mensaje': mensaje, 'form': form })


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
                mensaje = "La contraseña fue cambiada exitosamente"
            else:
                form._errors["old_password"] = "Password no es igual al anterior"

    else:
        form = FormularioCambiarContrasena()
        print ()

    return  render(request, 'cambiar_contrasena.html', {'form': form , 'mensaje': mensaje})


#Vista de registro de usuarios
def registro_usuario(request):
    mensaje = ""
    llamarMensaje = ""

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

                    # Borrando los datos del formulario y enviando el mensaje de sactisfacion
                    #form = FormularioRegistroUsuario()
                    mensaje = "El usuario se ha registrado satisfactoriamente, al correo" + usuario.email + "llegará un mensaje confirmando el registro"
                    llamarMensaje = "exito_usuario"

                    #Crea el usuario en la BD si hay excepcion
                    try:
                        usuario.save()
                        return redirect("login_user")
                    except Exception as e:
                        print(e)
            else:
                form = FormularioRegistroUsuario()
                mensaje = "El usuario con email " +str(email_usuario)+ " ya esta registrado"
                print("entre ya existe")
                return render(request, 'registrar-usuario.html', {'mensaje': mensaje, 'form': form})
        else:
            print("form invalid")
            return render(request, 'registrar-usuario.html', {'mensaje': mensaje, 'form': form})
    else:
        form = FormularioRegistroUsuario()
    return render(request, 'registrar-usuario.html', {'mensaje': mensaje, 'form': form})



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

            print ("esta bien ")
            try:
                usuario.save()
            except Exception as e:
                print(e)

            form = FormularioActualizarUsuario()
            mensaje = "se ha actualizado correctamente sus datos"

        else:
            mensaje = "Formulario No valido"
            print(form)
            form = FormularioActualizarUsuario()


    else:

        form = FormularioActualizarUsuario()
        form.initial = {'first_name': usuario.first_name, 'last_name': usuario.last_name , 'email': usuario.email, 'nombre_usuario': usuario.username, 'email_alternativo': usuario.email_alternativo,
                        'tel_fijo': usuario.telefono_fijo, 'tel_movil': usuario.telefono_movil}
        form.fields['email'].widget.attrs['readonly'] = True
    return  render(request, 'actualizar-usuario.html', {'form': form , 'mensaje': mensaje})
