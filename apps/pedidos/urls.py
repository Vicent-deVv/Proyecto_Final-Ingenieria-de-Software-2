from django.urls import path
from . import views

urlpatterns = [
    path('carrito/agregar/<int:producto_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('carrito/', views.ver_carrito, name='ver_carrito'),
    path('carrito/confirmar/', views.confirmar_pedido, name='confirmar_pedido'),
    path('cocina/monitor/', views.monitor_cocina, name='monitor_cocina'),
    path('cocina/estado/<int:pedido_id>/<str:nuevo_estado>/', views.cambiar_estado, name='cambiar_estado'),
]