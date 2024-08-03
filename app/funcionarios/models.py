from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models

class Funcionario(models.Model):

    def validate_idade(idade):
        if idade < 18 or idade > 114:
            raise ValidationError(f'Idade {idade} não permitida. Deve estar entre 18 e 114 anos.')

    def validate_peso(peso):
        if peso < 30 or peso > 300:
            raise ValidationError(f'Peso {peso} não é permitido. Deve estar entre 30 e 300 kg.')

    def validate_altura(altura):
        if altura < 0.5 or altura > 2.5:
            raise ValidationError(f'Altura {altura} não é permitida. Deve estar entre 0.5 e 2.5 metros.')

    nome_completo = models.CharField(max_length=255, validators=[
            RegexValidator(
                regex=r'^[a-zA-ZÀ-ÿ\s]*$',
                message='Nome completo deve conter apenas letras e espaços.'
            )
        ]) # Nome completo em 255 caracteres não numéricos
    email = models.EmailField(unique=True)
    idade = models.PositiveIntegerField(validators=[validate_idade]) # Idade em Inteiros Positivos
    altura = models.FloatField(validators=[validate_altura])  # Altura em metros
    peso = models.FloatField(validators=[validate_peso])  # Peso em quilogramas

    def __str__(self):
        return self.nome_completo