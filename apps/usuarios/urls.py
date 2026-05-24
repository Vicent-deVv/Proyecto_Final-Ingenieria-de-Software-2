# apps/usuarios/urls.py
from django.urls import path
from apps.usuarios import views

urlpatterns = [
    path('',views.main_clientes,name='main_cliente'),
    # El formulario único de login
    path('login/', views.login_personalizado, name='login'),
    path('logout/', views.logout_personalizado, name='logout'),
    path('registro/', views.registro_personalizado, name='registro'),

    # RUTA 1: Si es Empleado/Supervisor, la vista lo manda aquí
    path('gestion/', views.index, name='index'), 
    
    # RUTA 2: Si es Cliente, la vista lo manda aquí
    path('carta/', views.carta_clientes, name='carta_clientes'), 
]