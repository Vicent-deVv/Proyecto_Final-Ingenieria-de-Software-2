from django.urls import path
from . import views

urlpatterns = [
    path('historial/', views.historial_facturacion, name='historial_facturacion'),
]