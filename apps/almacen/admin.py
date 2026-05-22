from django.contrib import admin
from .models import Insumo, HistorialInventario, ControlSeguridadProducto

# Register your models here.
admin.site.register(Insumo)
admin.site.register(HistorialInventario)
admin.site.register(ControlSeguridadProducto)