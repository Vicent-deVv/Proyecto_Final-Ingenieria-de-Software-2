from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Insumo, MovimientoAlmacen
from apps.abastecimiento.models import Proveedor

def insumo_list(request):
    insumos = Insumo.objects.all().order_by('id')
    return render(request, 'almacen/insumo_list.html', {'insumos': insumos})

def insumo_create(request):
    if request.method == 'POST':
        nom = request.POST.get('nombre')
        cat = request.POST.get('categoria')
        stk = request.POST.get('stock', 0)
        unid = request.POST.get('unidad_medida')
        prec = request.POST.get('precio', 0)
        prov_id = request.POST.get('proveedor')
        
        prov = Proveedor.objects.get(id=prov_id) if prov_id else None
        Insumo.objects.create(nombre=nom, categoria=cat, stock=stk, unidad_medida=unid, precio=prec, proveedor=prov)
        messages.success(request, "Nuevo insumo registrado en el catálogo.")
        return redirect('insumo_list')
        
    return render(request, 'almacen/insumo_form.html', {
        'titulo_formulario': 'Nuevo Insumo',
        'proveedores': Proveedor.objects.filter(estado='ACTIVO')
    })

def insumo_update(request, pk):
    insumo = get_object_or_404(Insumo, id=pk)
    if request.method == 'POST':
        insumo.nombre = request.POST.get('nombre')
        insumo.categoria = request.POST.get('categoria')
        insumo.stock = request.POST.get('stock')
        insumo.unidad_medida = request.POST.get('unidad_medida')
        insumo.precio = request.POST.get('precio')
        prov_id = request.POST.get('proveedor')
        insumo.proveedor = Proveedor.objects.get(id=prov_id) if prov_id else None
        insumo.save()
        messages.success(request, f"Insumo {insumo.nombre} modificado correctamente.")
        return redirect('insumo_list')
        
    return render(request, 'almacen/insumo_form.html', {
        'insumo': insumo,
        'titulo_formulario': f'Editar Insumo: {insumo.nombre}',
        'proveedores': Proveedor.objects.filter(estado='ACTIVO')
    })

def insumo_delete(request, pk):
    insumo = get_object_or_404(Insumo, id=pk)
    # Simulación de eliminación lógica para no romper llaves foráneas históricas
    insumo.delete()
    messages.success(request, "Insumo dado de baja del catálogo.")
    return redirect('insumo_list')

def registrar_movimiento(request, tipo_movimiento):
    if request.method == 'POST':
        ins_id = request.POST.get('insumo_id')
        cant = float(request.POST.get('cantidad', 0))
        
        insumo = get_object_or_404(Insumo, id=ins_id)
        
        if tipo_movimiento in ['SALIDA', 'MERMA']:
            if float(insumo.stock) < cant:
                messages.error(request, f"Error: Stock insuficiente de {insumo.nombre}.")
                return redirect('index')
            insumo.stock = float(insumo.stock) - cant
        else:
            insumo.stock = float(insumo.stock) + cant
            
        insumo.save()
        
        MovimientoAlmacen.objects.create(
            insumo=insumo,
            tipo=tipo_movimiento,
            cantidad=cant,
            guia_remision=request.POST.get('guia_remision'),
            area_destino=request.POST.get('area_destino'),
            operario=request.POST.get('operario'),
            motivo_merma=request.POST.get('motivo_merma'),
            observacion=request.POST.get('observacion')
        )
        messages.success(request, f"Registro de {tipo_movimiento} completado.")
        return redirect('index')
        
    return render(request, 'almacen/form_movimientos.html', {
        'insumos': Insumo.objects.all(),
        'proveedores': Proveedor.objects.filter(estado='ACTIVO'),
        'tipo_movimiento': tipo_movimiento
    })

def consultar_stock(request):
    return render(request, 'almacen/stock.html', {'insumos': Insumo.objects.all()})

def panel_reportes(request):
    # Capturamos todos los movimientos para la vista previa de auditoría
    movimientos = MovimientoAlmacen.objects.all().order_by('-fecha')
    return render(request, 'almacen/reportes.html', {'movimientos': movimientos})

def panel_reportes(request):
    # 1. Traemos todos los movimientos por defecto
    movimientos = MovimientoAlmacen.objects.all().order_by('-fecha')
    
    # 2. Capturamos lo que el usuario seleccionó en la interfaz
    tipo_reporte = request.GET.get('tipo_reporte', '')
    fecha_filtro = request.GET.get('fecha', '')
    
    titulo_reporte = "REPORTE GENERAL DE MOVIMIENTOS Y AUDITORÍA"
    
    # 3. Aplicamos los filtros lógicos
    if tipo_reporte:
        if tipo_reporte == 'ENTRADAS':
            movimientos = movimientos.filter(tipo='ENTRADA')
            titulo_reporte = "REPORTE DE INGRESO Y REABASTECIMIENTO (LOTES)"
        elif tipo_reporte == 'SALIDAS':
            movimientos = movimientos.filter(tipo='SALIDA')
            titulo_reporte = "REPORTE DE DESPACHO INTERNO (CONSUMO DE COCINA)"
        elif tipo_reporte == 'MERMAS':
            movimientos = movimientos.filter(tipo='MERMA')
            titulo_reporte = "REPORTE DE ALERTA: MERMAS Y DESECHOS"

    if fecha_filtro:
        # Filtramos exactamente por el día seleccionado
        movimientos = movimientos.filter(fecha__date=fecha_filtro)
        
    return render(request, 'almacen/reportes.html', {
        'movimientos': movimientos,
        'tipo_reporte': tipo_reporte,
        'fecha_filtro': fecha_filtro,
        'titulo_reporte': titulo_reporte
    })