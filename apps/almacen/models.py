from django.db import models
from apps.abastecimiento.models import Proveedor

class Insumo(models.Model):
    nombre = models.CharField(max_length=100)
    categoria = models.CharField(max_length=50, default='Otros')
    stock = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    unidad_medida = models.CharField(max_length=20, default='kg')
    precio = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.SET_NULL, null=True, blank=True)
    fecha_vencimiento = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.nombre} ({self.stock} {self.unidad_medida})"

class MovimientoAlmacen(models.Model):
    TIPOS = (('ENTRADA', 'Entrada'), ('SALIDA', 'Salida'), ('MERMA', 'Merma'))
    insumo = models.ForeignKey(Insumo, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=15, choices=TIPOS)
    cantidad = models.DecimalField(max_digits=8, decimal_places=2)
    fecha = models.DateTimeField(auto_now_add=True)
    guia_remision = models.CharField(max_length=50, blank=True, null=True)
    area_destino = models.CharField(max_length=50, blank=True, null=True)
    operario = models.CharField(max_length=100, blank=True, null=True)
    motivo_merma = models.CharField(max_length=50, blank=True, null=True)
    observacion = models.TextField(blank=True, null=True)