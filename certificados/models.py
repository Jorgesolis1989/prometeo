from __future__ import unicode_literals

from django.db import models
from datetime import datetime
from django.utils import timezone
from django.utils.timezone import activate
from django.conf import settings
activate(settings.TIME_ZONE)

class Documentos(models.Model):
    id_dcmnto = models.IntegerField(primary_key=True)
    documento = models.FileField(upload_to="/documentos")

    class Meta:
        verbose_name_plural= u'documentos_correo'

    def __str__(self):
        return '%s' %(self.asnto_dcmnto)