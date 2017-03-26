from django import forms
"""
Este formulario permite filtrar por certificado
"""


class FormularioEscogerCertificado(forms.Form):

    FORMATOS = []

    FORMATOS = [('1','Retefuente'), ('2','Reteica')]

    PERIODOS = [('1','Retefuente'), ('2','Reteica')]

    tipo_certificado = forms.ChoiceField(widget=forms.Select(attrs={'class':'demo-chosen-select list-group-item  list-item-sm', 'data-live-search':'true',
                                                                'data-width':'100%'}), choices=FORMATOS, initial='retefuente')

    periodo = forms.ChoiceField(widget=forms.Select(attrs={'class':'demo-chosen-select list-group-item  list-item-sm', 'data-live-search':'true',
                                                                'data-width':'100%'}), choices=PERIODOS, initial='retefuente')
    #periodo = Jornada.objects.filter(is_active=True).order_by('fecha_inicio_jornada')[::-1]

    #jornada = forms.ModelChoiceField(widget=forms.Select(attrs={'class':'selectpicker', 'data-live-search':'true', 'onchange':'submit()',
    #                                                           'data-width':'100%'}),
    #                                 queryset=jornadas_elegidas, empty_label=None)