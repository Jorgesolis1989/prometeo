from django.db import models

# Create your models here
from django.db import models
from django.contrib.auth.models import User

class Usuario(User):
    email_alternativo = models.EmailField(blank=True)
    telefono_fijo = models.CharField(max_length=100)
    telefono_movil = models.CharField(max_length=100)
    codigo_perfil = models.CharField(max_length=100)

    class Meta:
        ordering = ["first_name"]
        verbose_name_plural = "Usuarios_Prometeo"


    def __str__(self):
        return '%s - %s  ' %( self.first_name , self.email)