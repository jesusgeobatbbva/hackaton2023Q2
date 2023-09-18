from django.db import models

# Create your models here.
from django.contrib.auth.models import User 
import random

class InformacionBancaria(models.Model):
    usuario             = models.OneToOneField(User, on_delete=models.CASCADE)
    numero_cuenta       = models.CharField(max_length=20, unique=True, null=True, blank=True)  
    saldo               = models.DecimalField(max_digits=15, decimal_places=2)

    def __str__(self):
        return f'Información de {self.usuario.username} - con cuenta {self.numero_cuenta}'

    def generar_numero_cuenta(self):
        return f'{self.usuario.id:04d}{random.randint(10, 99)}{random.randint(10, 99)}'

    def save(self, *args, **kwargs):
        if not self.numero_cuenta:
            self.numero_cuenta = self.generar_numero_cuenta()
        super().save(*args, **kwargs)


class Transaccion(models.Model):
    usuario     = models.ForeignKey(User, on_delete=models.CASCADE)
    tipo        = models.CharField(max_length=50)
    monto       = models.DecimalField(max_digits=10, decimal_places=2)
    fecha       = models.DateTimeField()

    def __str__(self):
        return f'Transacción de {self.usuario.username} - Tipo: {self.tipo}, Monto: {self.monto}, Fecha: {self.fecha}'
