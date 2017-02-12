from django import forms
from captcha.fields import ReCaptchaField

class FormularioLogin(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={ 'class': 'form-control', 'placeholder': 'Escriba aquí su nombre de usuario' , 'required':'true' 'autofocus'  }))

    #<input type="password" class="form-control" placeholder="Password">
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Escriba aquí su contraseña' , 'required':'true'}))


"""
formulario para registrar usuario
"""
class FormularioRegistroUsuario(forms.Form):

    nombre_completo = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Escriba aquí su nombre y apellido', 'required':'true'}))

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Escriba aquí su correo electrónico', 'required':'true'}))

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Escriba aquí su contraseña' , 'required':'true'}))

    nombre_usuario = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Escriba aquí el nombre del usuario', 'required':'true'}))

    email_alternativo = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Escriba aquí un correo electrónico alternativo', 'required':'true'}))

    tel_fijo = forms.IntegerField(
       widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Escriba aquí un teléfono fijo', 'min':'1' , 'required':'true'}))

    tel_movil = forms.IntegerField(
       widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Escriba aquí un teléfono móvil', 'min':'1' , 'required':'true'}))
