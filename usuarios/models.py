
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
    key_expires = models.DateTimeField()

    def __str__(self):
        return self.usuario.username

    class Meta:
        verbose_name_plural=u'Perfiles de Usuario'

class Usuario_Web(models.Model):
    email_usrio = models.CharField( primary_key=True , max_length=80 , null= False)
    clve_accso = models.CharField(max_length=128 , null= False)
    nmbre_usrio = models.CharField(max_length=60)
    email_altrntvo = models.CharField(max_length=80)
    tlno_fjo = models.CharField(max_length=20)
    tlfno_mvil = models.CharField(max_length=20)
    cdgo_prfil = models.IntegerField(null=True)
    nit_empresa = models.IntegerField(default=0, null=False)
    estdo_usrio = models.IntegerField(null=False , default= 0)
    fcha_crcion_date = models.DateTimeField( default=timezone.now)
    actvo = models.IntegerField(null=False, default= 0)

    def __str__(self):
        return self.email_usrio

    class Meta:
        verbose_name_plural= u'Usuarios_Web'
        db_table = 'usrios_web'


class Usuario_Web_Vinculacion_Empresa(models.Model):
    email_usrio = models.ForeignKey(Usuario_Web, db_column='email_usrio' , null=False)
    id_emprsa = models.IntegerField(primary_key=True)
    fcha_crcion = models.DateTimeField( default=timezone.now)
    actvo = models.IntegerField(null=False, default=1)

    class Meta:
        verbose_name_plural= u'Usuarios_Web_Vinculacion_Empresas'
        db_table = 'usrios_web_vnclcnes_emprsas'

    def __str__(self):
        return '%s - %s'  %(self.email_usrio, self.id_emprsa)