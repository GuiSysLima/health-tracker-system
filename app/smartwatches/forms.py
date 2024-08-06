from django import forms

from funcionarios.models import Funcionario


class SmartwatchForm(forms.Form):
    imei = forms.CharField(label='IMEI do Smartwatch', max_length=100)
    funcionario = forms.ModelChoiceField(
        queryset=Funcionario.objects.filter(smartwatch__isnull=True),
        label='Funcionário',
        empty_label='Selecione um funcionário sem smartwatch'
    )