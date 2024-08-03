from django import forms

from funcionarios.models import Funcionario


class SmartwatchForm(forms.Form):
    porta_url = forms.CharField(label='URL da Porta do Smartwatch', max_length=100)
    funcionario = forms.ModelChoiceField(
        queryset=Funcionario.objects.filter(smartwatch__isnull=True),
        label='Funcionário',
        empty_label='Selecione um funcionário sem smartwatch'
    )