from django.shortcuts import render, render_to_response
from usuarios.forms import FormularioLogin, FormularioRegistroUsuario
from usuarios.models import Usuario
from django.contrib.auth import authenticate, login
from django.template.context import RequestContext
# Create your views here.

#Pagina de login
def login_user(request):
    mensaje = ""
    if request.user.is_authenticated() and not request.user.is_superuser:
        return render(request, 'base-usuario.html')

    elif request.method == 'POST':
        form = FormularioLogin(request.POST)
        if form.is_valid():
            print("entre")
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



#Vista de registro de usuarios
def registro_usuario(request):
    mensaje = ""
    llamarMensaje = ""

    form = FormularioRegistroUsuario(request.POST)

    if request.method == 'POST' and "btnRegister":
        print("ingresse")
        form = FormularioRegistroUsuario(request.POST)
        #Si el formulario es valido y tiene datos
        if form.is_valid():
            cd = form.cleaned_data
            #Capture correo
            email = cd["email"]
            try:
                #Consultando el usuario en la base de datos.
                usuario = Usuario.objects.get(email=email)

            #Si el usuario no existe, lo crea
            except Usuario.DoesNotExist:
                    # Creando el usuario
                    usuario = Usuario()
                    usuario.nombre_completo = cd["nombre_completo"]
                    usuario.email = cd["email"]
                    usuario.password = cd["password"]
                    usuario.username = cd ["nombre_usuario"]
                    usuario.email_alternativo = cd ["email_alternativo"]
                    usuario.telefono_fijo = cd ["tel_fijo"]
                    usuario.telefono_movil = cd ["tel_movil"]
                    #generando el password aleatorio.
                    password = usuario.objects.make_random_password()
                    usuario.set_password(password)

                    # Borrando los datos del formulario y enviando el mensaje de sactisfacion
                    form = FormularioRegistroUsuario()
                    mensaje = "El usuario se ha registrado satisfactoriamente, al correo" + usuario.email + "llegará un mensaje confirmando el registro"
                    llamarMensaje = "exito_usuario"

                    #Crea el usuario en la BD si hay excepcion
                    try:
                        usuario.save()
                    except Exception as e:
                        print(e)
        else:
            form = FormularioRegistroUsuario
            return render(request, 'registrar-usuario.html', {'mensaje': mensaje, 'form': form})
    else:
        form = FormularioRegistroUsuario()
        return render(request, 'registrar-usuario.html', {'mensaje': mensaje, 'form': form})


