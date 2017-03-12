from django import forms


class FormularioVincularEmpresas(forms.Form):
    empresas = forms.MultipleChoiceField(
        widget=  forms.CheckboxSelectMultiple
    )

