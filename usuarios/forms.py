from django import forms
from captcha.fields import ReCaptchaField
from django.contrib.auth.models import User

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

    first_name = forms.CharField(
        widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Escriba aquí sus nombres', 'required':'true'}))

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Escriba aquí su correo electrónico', 'required':'true'}))

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Escriba aquí su contraseña' , 'required':'true','id': 'password1', 'min':'4'}))

    nit_empresa = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Escriba aquí el NIT de empresa sin digito de verificacion', 'required':'true'}))

    email_alternativo = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Escriba aquí un correo electrónico alternativo', 'required':'true'}))

    tel_fijo = forms.IntegerField(
       widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Escriba aquí un teléfono fijo', 'min':'1' , 'required':'true'}))

    tel_movil = forms.IntegerField(
       widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Escriba aquí un teléfono móvil', 'min':'1' , 'required':'true'}))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'password')

"""
    #clean email field
    def clean_email(self):
        email = self.cleaned_data["email"]
        try:
            User._default_manager.get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError('email duplicado')

    #modificamos el método save() así podemos definir  user.is_active a False la primera vez que se registra
    def save(self, commit=True):
        usuario = super(FormularioRegistroUsuario, self).save(commit=False)
        usuario.email = self.cleaned_data['email']
        if commit:
            usuario.is_active = False # No está activo hasta que active el vínculo de verificación
            usuario.save()

        return usuario
"""

"""
formulario para editar usuario
"""
class FormularioActualizarUsuario(forms.Form):


    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Escriba aquí su nombre', 'required':'true'}))


    nit_empresa = forms.IntegerField(
       widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Escriba aquí el NIT sin digito de Verficación   ', 'min':'1' , 'required':'true'}))


    email = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Escriba aquí su correo electrónico'}), required= False)


    email_alternativo = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Escriba aquí un correo electrónico alternativo', 'required':'true'}))

    tel_fijo = forms.IntegerField(
       widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Escriba aquí un teléfono fijo', 'min':'1' , 'required':'true'}))

    tel_movil = forms.IntegerField(
       widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Escriba aquí un teléfono móvil', 'min':'1' , 'required':'true'}))


class FormularioCambiarContrasena(forms.Form):

    old_password = forms.CharField(
        widget= forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Escriba aquí su contraseña anterior', 'required':'true'}))

    new_password = forms.CharField(
        widget= forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Escriba aquí su contraseña nueva', 'required':'true'}))

    confirm_password = forms.CharField(
        widget= forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirme su contraseña nueva    ', 'required':'true'}))

    def clean(self):
        new_password = self.cleaned_data['new_password']
        confirm_password = self.cleaned_data['confirm_password']

        if new_password != confirm_password:
            self._errors["new_password"] = "Las contraseñas no coinciden" # Will raise a error message
            #del form_data['new_password']
        return self.cleaned_data

