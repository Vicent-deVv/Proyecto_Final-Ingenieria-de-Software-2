from django.db import models
from apps.pedidos.models import Pedido  # Conectamos con la orden de compra

class Comprobante(models.Model):
    TIPOS = [
        ('BOLETA', 'Boleta'),
        ('FACTURA', 'Factura'),
    ]
    METODOS_PAGO = [
        ('EFECTIVO', 'Efectivo'),
        ('TARJETA', 'Tarjeta'),
        ('YAPE_PLIN', 'Yape / Plin'),
    ]

    # Un pedido tiene un único comprobante (Relación Uno a Uno)
    pedido = models.OneToOneField(Pedido, on_delete=models.CASCADE, related_name='comprobante')
    tipo = models.CharField(max_length=10, choices=TIPOS, default='BOLETA')
    numero_serie = models.CharField(max_length=20, unique=True)  # Ej: B001-000001
    monto_total = models.DecimalField(max_digits=10, decimal_places=2)
    metodo_pago = models.CharField(max_length=15, choices=METODOS_PAGO)
    fecha_emision = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_tipo_display()} {self.numero_serie}"

class GestionDevolucion(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.PROTECT)
    motivo = models.TextField()
    fecha_procesado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Devolución Pedido #{self.pedido.id}"