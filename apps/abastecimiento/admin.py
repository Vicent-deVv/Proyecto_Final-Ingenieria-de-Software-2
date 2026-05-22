from django.contrib import admin
from .models import Proveedor, OrdenAbastecimiento

# Register your models here.
admin.site.register(Proveedor)
admin.site.register(OrdenAbastecimiento)