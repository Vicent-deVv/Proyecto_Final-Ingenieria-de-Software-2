from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Proveedor
from django.shortcuts import render, redirect, get_object_or_404

def proveedor_list(request):
    proveedores = Proveedor.objects.all().order_by('razon_social')
    return render(request, 'abastecimiento/proveedor_list.html', {'proveedores': proveedores})

def proveedor_create(request):
    if request.method == 'POST':
        prov = request.POST.get('proveedor')
        ruc_num = request.POST.get('ruc')
        cont = request.POST.get('contacto')
        cat = request.POST.get('categoria')
        mail = request.POST.get('correo')
        dir_fisc = request.POST.get('direccion')
        
        Proveedor.objects.create(
            razon_social=prov, ruc=ruc_num, contacto=cont,
            categoria=cat, correo=mail, direccion=dir_fisc, estado='ACTIVO'
        )
        messages.success(request, "Proveedor homologado con éxito.")
        return redirect('proveedor_list')
    # Reutiliza una vista simple o renderiza el formulario del Figma
    return render(request, 'abastecimiento/proveedor_form.html')

def proveedor_update(request, pk):
    # Buscamos el proveedor que el usuario quiere editar
    proveedor = get_object_or_404(Proveedor, id=pk)
    
    if request.method == 'POST':
        # Sobreescribimos con los datos nuevos
        proveedor.razon_social = request.POST.get('proveedor')
        proveedor.ruc = request.POST.get('ruc')
        proveedor.contacto = request.POST.get('contacto')
        proveedor.categoria = request.POST.get('categoria')
        proveedor.correo = request.POST.get('correo')
        proveedor.direccion = request.POST.get('direccion')
        proveedor.save()
        
        messages.success(request, f"Proveedor {proveedor.razon_social} modificado correctamente.")
        return redirect('proveedor_list')
        
    # Reutilizamos el mismo formulario HTML, pero le pasamos los datos del proveedor
    return render(request, 'abastecimiento/proveedor_form.html', {
        'proveedor': proveedor,
        'titulo_formulario': f'Editar Proveedor: {proveedor.razon_social}'
    })