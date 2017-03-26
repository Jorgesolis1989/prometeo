from django import forms
from modelos_existentes.models import Formatos_Definidos
"""
Este formulario permite filtrar por certificado
"""


class FormularioEscogerCertificado(forms.Form):


    FORMATOS = Formatos_Definidos.objects.all()

    PERIODOS = [('2016-1','2016-1'), ('2016-2','2016-2')]

    tipo_certificado = forms.ModelChoiceField(widget=forms.Select(attrs={'class':'demo-chosen-select list-group-item  list-item-sm', 'data-live-search':'true',
                                                                'data-width':'100%'}), queryset=FORMATOS, empty_label=None )

    periodo = forms.ChoiceField(widget=forms.Select(attrs={'class':'demo-chosen-select list-group-item  list-item-sm', 'data-live-search':'true',
                                                                'data-width':'100%'}), choices=PERIODOS)
    #periodo = Jornada.objects.filter(is_active=True).order_by('fecha_inicio_jornada')[::-1]

    #jornada = forms.ModelChoiceField(widget=forms.Select(attrs={'class':'selectpicker', 'data-live-search':'true', 'onchange':'submit()',
    #                                                           'data-width':'100%'}),
    #                                 queryset=jornadas_elegidas, empty_label=None)