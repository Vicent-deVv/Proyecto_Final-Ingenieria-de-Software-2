from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Insumo

# Create your views here.
def listar_insumo(request):
    insumos = Insumo.objects.all()

    return HttpResponse(insumos)