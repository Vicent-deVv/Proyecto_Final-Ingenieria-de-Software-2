from django.urls import path
from . import views

urlpatterns = [
    path('insumos/', views.insumo_list, name='insumo_list'),
    path('insumos/nuevo/', views.insumo_create, name='crear_insumo'),
    path('insumos/editar/<int:pk>/', views.insumo_update, name='editar_insumo'),
    path('insumos/eliminar/<int:pk>/', views.insumo_delete, name='eliminar_insumo'),
    path('movimiento/<str:tipo_movimiento>/', views.registrar_movimiento, name='registrar_movimiento'),
    path('stock/', views.consultar_stock, name='consultar_stock'),
    path('reportes/', views.panel_reportes, name='panel_reportes'),
]