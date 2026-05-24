from django.urls import path
from . import views

urlpatterns = [
    path('menu/',views.menu)
    #Paths de testing
    #path('', views.listar_productos),
    #path('lista_ordenes/',views.lista_ordenes)
]