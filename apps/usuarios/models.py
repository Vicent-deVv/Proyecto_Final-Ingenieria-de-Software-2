from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
    ROLES = (
        ('CLIENTE', 'Cliente'),
        ('COCINERO', 'Cocinero'),
        ('ALMACENERO', 'Almacenero'),
        ('SUPERVISOR', 'Supervisor'),
    )
    rol = models.CharField(max_length=20, choices=ROLES, default='CLIENTE')
    telefono = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return f"{self.username} - {self.rol}"