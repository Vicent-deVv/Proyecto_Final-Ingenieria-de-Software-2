from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_personalizado, name='login'),
    path('logout/', views.logout_personalizado, name='logout'),
    path('registro/', views.registro_personalizado, name='registro'),
    path('gestion/', views.index, name='index'),
    path('carta/', views.carta_clientes, name='carta_clientes'),
]