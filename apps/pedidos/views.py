from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Producto, Pedido, DetallePedido
from apps.facturacion.models import Comprobante
import decimal

def agregar_al_carrito(request, producto_id):
    carrito = request.session.get('carrito', {})
    id_str = str(producto_id)
    carrito[id_str] = carrito.get(id_str, 0) + 1
    request.session['carrito'] = carrito
    messages.success(request, "Añadido a la bolsa.")
    return redirect('carta_clientes')

def ver_carrito(request):
    carrito = request.session.get('carrito', {})
    items = []
    total = decimal.Decimal('0.00')
    for p_id, cant in carrito.items():
        prod = get_object_or_404(Producto, id=int(p_id))
        sub = prod.precio * cant
        total += sub
        items.append({'producto': prod, 'cantidad': cant, 'subtotal': sub})
    return render(request, 'pedidos/carrito.html', {'items': items, 'total': total})

def confirmar_pedido(request):
    carrito = request.session.get('carrito', {})
    if not carrito: return redirect('carta_clientes')
        
    total = decimal.Decimal('0.00')
    pedido = Pedido.objects.create(usuario=request.user, estado='ENTRANTE', total=0)
    
    for p_id, cant in carrito.items():
        prod = Producto.objects.get(id=int(p_id))
        sub = prod.precio * cant
        total += sub
        DetallePedido.objects.create(pedido=pedido, producto=prod, cantidad=cant, precio_unitario=prod.precio)
        
    pedido.total = total
    pedido.save()
    
    # FACTURACIÓN AUTOMÁTICA
    subtotal = total / decimal.Decimal('1.18')
    Comprobante.objects.create(
        pedido=pedido, tipo='BOLETA', serie='B001',
        correlativo=str(pedido.id).zfill(6), subtotal=subtotal,
        igv=total - subtotal, total=total, cliente_nombre=request.user.username
    )
    
    request.session['carrito'] = {}
    messages.success(request, f"Pedido #{pedido.id} enviado a cocina.")
    return redirect('carta_clientes')

def monitor_cocina(request):
    pedidos = Pedido.objects.exclude(estado='ENTREGADO').order_by('fecha_creacion')
    return render(request, 'pedidos/monitor.html', {'pedidos': pedidos})

def cambiar_estado(request, pedido_id, nuevo_estado):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    pedido.estado = nuevo_estado
    pedido.save()
    return redirect('monitor_cocina')