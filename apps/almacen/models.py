from django.db import models
from apps.usuarios.models import Usuario  # Para saber qué empleado movió el stock

class Insumo(models.Model):
    nombre = models.CharField(max_length=100)
    stock_actual = models.DecimalField(max_digits=10, decimal_places=2)
    unidad_medida = models.CharField(max_length=20, default='Unidades')  # Kg, Unidades, Litros

    def __str__(self):
        return f"Insumo: {self.nombre} - Stock: {self.stock_actual}"
    
    def restar_stock(self,cantidad):
        if cantidad <= 0:
            raise ValueError("No se puede tener valores negativos")
        

        if self.stock_actual >= cantidad:
            self.stock_actual -= cantidad
            self.save()
        else:
            raise ValueError(f"Stock insuficiente de {self.nombre}. Solo quedan {self.stock_actual}.")

class HistorialInventario(models.Model):
    MOVIMIENTOS = [
        ('INGRESO', 'Ingreso de Almacén'),
        ('DESPACHO', 'Despacho a Cocina'),
        ('MERMA', 'Ajuste por Pérdida/Merma'),
    ]
    
    insumo = models.ForeignKey(Insumo, on_delete=models.CASCADE)
    empleado = models.ForeignKey(Usuario, on_delete=models.PROTECT)
    tipo = models.CharField(max_length=15, choices=MOVIMIENTOS)
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_tipo_display()} - {self.insumo.nombre}"

class ControlSeguridadProducto(models.Model):
    ESTADOS_PRODUCTO = [
        ('OPTIMO', 'Óptimo / Buen Estado'),
        ('DAÑADO', 'Dañado / Vencido'),
    ]

    insumo = models.ForeignKey(Insumo, on_delete=models.CASCADE)
    administrador = models.ForeignKey(Usuario, on_delete=models.PROTECT)  # El admin que auditó
    estado_salubridad = models.CharField(max_length=20, choices=ESTADOS_PRODUCTO, default='OPTIMO')
    observaciones = models.TextField()
    fecha_verificacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Auditoría {self.insumo.nombre} - {self.get_estado_salubridad_display()}"