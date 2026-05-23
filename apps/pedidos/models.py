from django.db import models
from apps.usuarios.models import Usuario  # Jalamos a tu usuario personalizado

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

class Pedido(models.Model):
    ESTADOS = [
        ('ENTRANTE', 'Entrante'),
        ('ACEPTADO', 'Aceptado'),
        ('EN_PREPARACION', 'En Preparación'),
        ('ENVIADO', 'Enviado'),
        ('ENTREGADO', 'Entregado'),
        ('CANCELADO', 'Cancelado'),
    ]
    
    # Relaciones obligatorias
    cliente = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='mis_pedidos')
    empleado_asignado = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, blank=True, related_name='pedidos_gestionados')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='ENTRANTE')
    tiempo_estimado_minutos = models.IntegerField(default=30)  # Para la vista del cliente

    def __str__(self):
        return f"Pedido #{self.id} - {self.cliente.username} ({self.get_estado_display()})"
    
    def cambiar_estado(self, nuevo_estado):
        estados_validos = []

        for tupla in self.ESTADOS:
            estados_validos.append(tupla[0])

        if nuevo_estado in estados_validos:
            self.estado = nuevo_estado
            self.save()
        else:
            raise ValueError("Error: Ese estado no está permitido en Bembos.")
        
    def calcular_total(self):
        total = 0
        detalles = self.detalles.all()

        for detallePedido in detalles:
            total = total + detallePedido.calcular_subtotal()

        return total


        

class DetallePedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='detalles')
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT)
    cantidad = models.PositiveIntegerField(default=1)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    def calcular_subtotal(self):
        return self.cantidad * self.precio_unitario