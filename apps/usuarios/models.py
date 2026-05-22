from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
    ROLES = [
        ('ADMINISTRADOR', 'Administrador'),
        ('EMPLEADO_ALMACEN', 'Empleado de Almacén'),
        ('EMPLEADO_PEDIDO', 'Empleado de Pedido'),
        ('CLIENTE', 'Cliente'),
    ]
    
    rol = models.CharField(max_length=20, choices=ROLES, default='CLIENTE')
    telefono = models.CharField(max_length=15, blank=True, null=True)
    direccion = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.username} - {self.get_rol_display()}"