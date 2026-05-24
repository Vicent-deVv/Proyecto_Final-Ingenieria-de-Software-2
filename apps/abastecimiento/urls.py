from django.urls import path
from . import views

urlpatterns = [
    path('proveedores/', views.proveedor_list, name='proveedor_list'),
    path('proveedores/nuevo/', views.proveedor_create, name='crear_proveedor'),
    path('proveedores/editar/<int:pk>/', views.proveedor_update, name='editar_proveedor'), # ¡NUEVA RUTA!
]