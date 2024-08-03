from django.db import models

from funcionarios.models import Funcionario


class Smartwatch(models.Model):
    imei = models.CharField(max_length=255, primary_key=True)
    data = models.DateField()
    hora = models.TimeField()
    bpm = models.IntegerField()
    mmhg = models.CharField(max_length=10)
    temperatura_corporal = models.CharField(max_length=8)
    funcionario = models.OneToOneField(Funcionario, on_delete=models.CASCADE, related_name='smartwatch')

    def __str__(self):
        return self.imei


class SmartwatchHistory(models.Model):
    smartwatch = models.ForeignKey(Smartwatch, on_delete=models.CASCADE, related_name='historico')
    data = models.DateField()
    hora = models.TimeField()
    bpm = models.IntegerField()
    mmhg = models.CharField(max_length=10)
    temperatura_corporal = models.CharField(max_length=8)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.smartwatch.imei} - {self.timestamp}"