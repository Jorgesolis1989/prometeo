from django import forms
from captcha.fields import ReCaptchaField

class FormularioLogin(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={ 'class': 'form-control', 'placeholder': 'Escriba aquí su nombre de usuario' , 'required':'true' 'autofocus'  }))

    #<input type="password" class="form-control" placeholder="Password">
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Escriba aquí su contraseña' , 'required':'true'}))