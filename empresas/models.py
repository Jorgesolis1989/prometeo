from django.utils import timezone
from django.utils.timezone import activate
from django.conf import settings
activate(settings.TIME_ZONE)

from modelos_existentes.models import Empresa

# Create your models here
from django.db import models

"""
class Logo_Empresa(models.Model):
    empresa = models.OneToOneField(Empresa, unique=True)
    logo_empresa = models.CharField(max_length=100, null=False)
"""