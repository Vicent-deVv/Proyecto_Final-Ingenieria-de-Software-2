from django.db import models
from django.conf import settings

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=6, decimal_places=2)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

class Pedido(models.Model):
    ESTADOS = (
        ('ENTRANTE', 'Entrante'),
        ('ACEPTADO', 'Aceptado'),
        ('PREPARACION', 'En Preparación'),
        ('LISTO', 'Listo para Entrega'),
        ('ENTREGADO', 'Entregado'),
    )
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='ENTRANTE')
    total = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)

class DetallePedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='detalles')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=1)
    precio_unitario = models.DecimalField(max_digits=6, decimal_places=2)