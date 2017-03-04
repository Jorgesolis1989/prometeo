
from django.utils import timezone
from django.utils.timezone import activate
from django.conf import settings
activate(settings.TIME_ZONE)


# Create your models here
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
import hashlib, datetime, random



class Perfil_Usuario(models.Model):
    usuario = models.OneToOneField(User)
    activation_key = models.CharField(max_length=40, blank=True)
    key_expires = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.usuario.username

    class Meta:
        verbose_name_plural=u'Perfiles de Usuario'

