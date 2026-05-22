from django.db import models
from apps.usuarios.models import Usuario
from apps.almacen.models import Insumo

class Proveedor(models.Model):
    ruc = models.CharField(max_length=11, unique=True)
    nombre_empresa = models.CharField(max_length=150)

    def __str__(self):
        return self.nombre_empresa

class OrdenAbastecimiento(models.Model):
    administrador = models.ForeignKey(Usuario, on_delete=models.PROTECT)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.PROTECT)
    fecha_pedido = models.DateTimeField(auto_now_add=True)
    completado = models.BooleanField(default=False)

    def __str__(self):
        return f"Orden #{self.id} - {self.proveedor.nombre_empresa}"