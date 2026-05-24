from django.db import models

class Proveedor(models.Model):
    ESTADOS = (('ACTIVO', 'Activo'), ('INACTIVO', 'Inactivo'))
    ruc = models.CharField(max_length=11, unique=True)
    razon_social = models.CharField(max_length=100)
    contacto = models.CharField(max_length=100, blank=True, null=True)
    telefono = models.CharField(max_length=15, blank=True, null=True)
    correo = models.EmailField(blank=True, null=True)
    direccion = models.CharField(max_length=200, blank=True, null=True)
    categoria = models.CharField(max_length=50, default='Alimentos')
    estado = models.CharField(max_length=10, choices=ESTADOS, default='ACTIVO')

    def __str__(self):
        return self.razon_social