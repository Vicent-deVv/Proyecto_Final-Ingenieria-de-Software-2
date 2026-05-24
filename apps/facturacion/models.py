from django.db import models
from apps.pedidos.models import Pedido

class Comprobante(models.Model):
    pedido = models.OneToOneField(Pedido, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=20, default='BOLETA')
    serie = models.CharField(max_length=4, default='B001')
    correlativo = models.CharField(max_length=8)
    fecha_emision = models.DateTimeField(auto_now_add=True)
    subtotal = models.DecimalField(max_digits=8, decimal_places=2)
    igv = models.DecimalField(max_digits=8, decimal_places=2)
    total = models.DecimalField(max_digits=8, decimal_places=2)
    cliente_nombre = models.CharField(max_length=100)