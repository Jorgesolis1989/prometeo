from __future__ import unicode_literals

from django.db import models
from datetime import datetime
from django.utils import timezone
from django.utils.timezone import activate
from django.conf import settings
activate(settings.TIME_ZONE)

# Usuario
class Usuario_Web(models.Model):
    email_usrio = models.CharField(primary_key=True , max_length=80 , null= False)
    clve_accso = models.CharField(max_length=10 , null= False)
    nmbre_usrio = models.CharField(max_length=60, null=True)
    email_altrntvo = models.CharField(max_length=80, null=True)
    tlno_fjo = models.CharField(max_length=20, null=True)
    tlfno_mvil = models.CharField(max_length=20, null=True)
    cdgo_prfil = models.IntegerField(null=True)
    nit_tcro_ascdo = models.CharField(max_length=13)
    estdo_usrio = models.IntegerField(null=False, default= 0)
    fcha_crcion = models.DateField(default=datetime.now, null=True)
    actvo = models.IntegerField(null=False, default= 0)

    def __str__(self):
        return self.email_usrio

    class Meta:
        verbose_name_plural= u'Usuarios_Web'
        db_table = 'usrios_web'


class Usuario_Web_Vinculacion_Empresa(models.Model):
    email_usrio = models.ForeignKey(Usuario_Web, db_column='email_usrio' , null=False)
    id_emprsa = models.IntegerField(primary_key=True)
    fcha_crcion = models.DateTimeField(default=timezone.now)
    actvo = models.IntegerField(null=False, default=1)

    class Meta:
        verbose_name_plural= u'Usuarios_Web_Vinculacion_Empresas'
        db_table = 'usrios_web_vnclcnes_emprsas'

    def __str__(self):
        return '%s - %s'  %(self.email_usrio, self.id_emprsa)

class Empresa(models.Model):
    id_clnte = models.BigIntegerField()
    id_emprsa = models.BigIntegerField(primary_key=True)
    nmbre_rzon_scial = models.CharField(max_length=80)
    cdgo_pais = models.IntegerField(default=57)
    cdgo_dpto = models.IntegerField(null=True)
    cdgo_mncpio = models.IntegerField(null=True)
    cdgo_pstal = models.CharField(max_length=6, null=True)
    drccion = models.CharField(max_length=50)
    web_site = models.CharField(max_length=100 , null=True)
    lgtpo_emprsa = models.BinaryField( null=True)
    fcha_crcion = models.DateField(default=datetime.now, null=True)
    actvo = models.IntegerField(default=1)


    def __str__(self):
        return self.nmbre_rzon_scial

    class Meta:
        verbose_name_plural=u'Empresas'
        db_table = 'emprsas'
        unique_together = (('id_clnte', 'id_emprsa'),)


class Usuario_Web_Vinculacion_Folder(models.Model):
    email_usrio = models.ForeignKey(Usuario_Web, db_column='email_usrio' , null=False)
    nmro_flder =  models.AutoField(primary_key=True)
    nmbre_flder = models.CharField(max_length=60)
    nmro_orden =  models.IntegerField()

    class Meta:
        verbose_name_plural= u'Usuarios_Web_Vinculacion_Folders'
        db_table = 'usrios_web_mnjo_flders_enc'
        unique_together = (('email_usrio', 'nmro_flder'),)

    def __str__(self):
        return '%s - Folder  %s'  %(self.email_usrio, self.nmro_flder)

class movimientos_formato_concepto(models.Model):
    id_clnte = models.BigIntegerField()
    id_emprsa = models.BigIntegerField(primary_key=True)
    cdgo_frmto =  models.IntegerField()
    cdgo_cncpto = models.IntegerField()
    nmro_scncial = models.IntegerField()
    ano_mes = models.CharField(max_length=7)
    cnta_cntble = models.CharField(max_length=16)
    id_trcro = models.CharField(max_length=7)
    vlor_grvble = models.IntegerField()
    cmpo_1 = models.IntegerField()
    cmpo_2 = models.IntegerField()
    cmpo_3 = models.IntegerField()
    cmpo_4 = models.CharField(max_length=20)
    cmpo_5 = models.CharField(max_length=20)
    cmpo_6 = models.CharField(max_length=20)
    fcha_prcso = models.DateTimeField()

    class Meta:
        verbose_name_plural= u'Mvmnto_Frmto_Cncpto'
        db_table = 'mvmnto_frmto_cncpto'
        unique_together = (('id_clnte', 'id_emprsa', 'cdgo_frmto', 'cdgo_cncpto', 'nmro_scncial', 'ano_mes'))

    def __str__(self):
        return '%s - Movimientos  %s' %(self.id_clnte, self.id_emprsa,self.cdgo_frmto, self.cdgo_cncpto,self.nmro_scncial,self.ano_mes)


class Paises(models.Model):
    cdgo_pais = models.IntegerField(primary_key=True)
    nmbre_pais = models.CharField(max_length=40)
    id_mnda = models.CharField(max_length=4)
    id_idioma =  models.CharField(max_length=4)
    fcha_crcion = models.DateField()
    actvo = models.IntegerField(default=1)

    class Meta:
        verbose_name_plural= u'Paises'
        db_table = 'paises'

    def __str__(self):
        return 'Pais  %s' %(self.nmbre_pais)


class Departamentos(models.Model):
    cdgo_pais = models.IntegerField()
    cdgo_dpto = models.IntegerField(primary_key=True)
    nmbre_dpto = models.CharField(max_length=40)
    fcha_crcion = models.DateField()
    actvo = models.IntegerField(default=1)

    class Meta:
        verbose_name_plural= u'Departamentos'
        db_table = 'dptos'
     #   unique_together = (('cdgo_pais', 'cdgo_dpto'))

    def __str__(self):
        return 'Departamento %s' %(self.nmbre_dpto)

class Municipios(models.Model):
      cdgo_pais = models.IntegerField()
      cdgo_dpto = models.IntegerField()
      cdgo_mncpio = models.IntegerField(primary_key=True)
      nmbre_mncpio = models.CharField(max_length=40)
      fcha_crcion = models.DateField()
      actvo = models.IntegerField(default=1)

      class Meta:
        verbose_name_plural= u'municipios'
        db_table = 'mncpios'
      #  unique_together = (('cdgo_pais', 'cdgo_dpto' ,'cdgo_mncpio' ))

        def __str__(self):
            return '%s - Municipio' %(self.nmbre_mncpio)


class Formatos_Definidos (models.Model):
    id_clnte = models.IntegerField()
    id_emprsa = models.IntegerField()
    cdgo_frmto = models.IntegerField(primary_key=True)
    nmbre_frmto = models.CharField(max_length=80)
    fcha_crcion = models.DateField()
    actvo= models.IntegerField(default=1)

    class Meta:
        verbose_name_plural= u'formatos definidos'
        db_table = 'frmtos_dfndos'
        unique_together = (('id_clnte', 'id_emprsa' ,'cdgo_frmto' ))

    def __str__(self):
        return '%s' %(self.nmbre_frmto)
