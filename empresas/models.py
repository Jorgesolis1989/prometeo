from django.utils import timezone
from django.utils.timezone import activate
from django.conf import settings
activate(settings.TIME_ZONE)

# Create your models here
from django.db import models

class Empresa(models.Model):
    """
        id_clnte numeric(15,0) NOT NULL,
        id_emprsa numeric(15,0) NOT NULL,
        nmbre_rzon_scial character varying(80),
        cdgo_pais integer,
        cdgo_dpto integer,
        cdgo_mncpio integer,
        cdgo_pstal character varying(6),
        drccion character varying(50),
        web_site character varying(100),
        lgtpo_emprsa bytea,
        fcha_crcion date,
        actvo integer,
    """

    id_clnte = models.BigIntegerField()
    id_emprsa = models.BigIntegerField(primary_key=True, unique=True)
    nmbre_rzon_scial = models.CharField(max_length=80)
    cdgo_pais = models.IntegerField(default=57)
    cdgo_dpto = models.IntegerField(null=True)
    cdgo_mncpio = models.IntegerField(null=True)
    cdgo_pstal = models.CharField(max_length=6, null=True)
    drccion = models.CharField(max_length=50)
    web_site = models.CharField(max_length=100 , null=True)
    lgtpo_emprsa = models.ImageField(upload_to='logosEmpresas/', null=True)
    fcha_crcion = models.DateTimeField(default=timezone.now , null=True)
    actvo = models.IntegerField(default=1)

    def __str__(self):
        return self.nmbre_rzon_scial

    class Meta:
        verbose_name_plural=u'Empresas'
        db_table = 'emprsas'


