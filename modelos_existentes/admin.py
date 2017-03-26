from django.contrib import admin

from modelos_existentes.models import Usuario_Web_Vinculacion_Empresa, Usuario_Web, Empresa , Paises , Municipios , Departamentos
# Register your models here.
admin.site.register(Usuario_Web_Vinculacion_Empresa)
admin.site.register(Usuario_Web)
admin.site.register(Empresa)
admin.site.register(Paises)