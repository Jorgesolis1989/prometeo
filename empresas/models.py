from django.utils import timezone
from django.utils.timezone import activate
from django.conf import settings

from django.db import models
from modelos_existentes.models import Empresa

class Empresa_Con_Logo(models.Model):
    id_emprsa = models.BigIntegerField(unique=True)
    lgtpo_emprsa = models.ImageField(upload_to='logosEmpresas/', null=True)
    activo = models.IntegerField(default=1)

    def __str__(self):
        return str(self.id_emprsa)