from django.contrib import admin
from usuarios.models import Usuario_Web, Perfil_Usuario , Usuario_Web_Vinculacion_Empresa

# Register your models here.
admin.site.register(Usuario_Web)
admin.site.register(Perfil_Usuario)
admin.site.register(Usuario_Web_Vinculacion_Empresa)
