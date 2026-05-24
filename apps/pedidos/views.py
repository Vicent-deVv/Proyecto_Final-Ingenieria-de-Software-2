from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Producto, Pedido

# Create your views here.
def menu(request):
    return render(request,'pedidos/menu.html')

def listar_productos(request):
    #Listamos todos los productos activos
    productos = Producto.objects.filter(activo = True)
    return HttpResponse(productos)

def lista_ordenes(request):
    estados_deseados = ['ENTRANTE','ACEPTADO','EN_PREPARACION']

    ordenes = Pedido.objects.filter(estado__in = estados_deseados)
    
    return HttpResponse(ordenes)