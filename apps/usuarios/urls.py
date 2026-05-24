from django.urls import path
from . import views

urlpatterns = [
    # Rutas de autenticación y panel
    path('', views.login_personalizado, name='login'),
    path('registro/', views.registro_personalizado, name='registro'),
    path('logout/', views.logout_personalizado, name='logout'),
    path('gestion/', views.index, name='index'),
    
    # Rutas para el cliente (ESTAS SON LAS QUE FALTABAN)
    path('carta/', views.carta_clientes, name='carta'),
    path('carrito/', views.ver_carrito, name='ver_carrito'),
]