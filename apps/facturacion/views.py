from django.shortcuts import render
from .models import Comprobante

def historial_facturacion(request):
    comprobantes = Comprobante.objects.all().order_by('-fecha_emision')
    return render(request, 'facturacion/historial.html', {'comprobantes': comprobantes})