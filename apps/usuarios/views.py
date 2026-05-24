from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .models import Usuario
from apps.pedidos.models import Producto

def login_personalizado(request):
    if request.method == 'POST':
        u = request.POST.get('username')
        p = request.POST.get('password')
        user = authenticate(request, username=u, password=p)
        if user is not None:
            login(request, user)
            # Validamos si es Admin de Django (superusuario) o si es personal de tienda
            if user.is_superuser or user.rol in ['COCINERO', 'ALMACENERO', 'SUPERVISOR']:
                return redirect('index') # Al panel de control/gestión
            return redirect('carta') # CORREGIDO: Clientes van a la ruta 'carta'
        else:
            messages.error(request, "Credenciales inválidas.")
    return render(request, 'usuarios/login.html')

def logout_personalizado(request):
    logout(request)
    return redirect('login')

def registro_personalizado(request):
    if request.method == 'POST':
        u = request.POST.get('username')
        e = request.POST.get('email')
        p = request.POST.get('password')
        # Por defecto, el que se registra por la web es CLIENTE
        if Usuario.objects.filter(username=u).exists():
            messages.error(request, "Ese nombre de usuario ya está en uso.")
        else:
            user = Usuario.objects.create_user(username=u, email=e, password=p, rol='CLIENTE')
            messages.success(request, "Registro exitoso. Ya puedes iniciar sesión.")
            return redirect('login')
    return render(request, 'usuarios/registro.html')

def index(request):
    return render(request, 'usuarios/gestion.html')

def carta_clientes(request):
    productos = Producto.objects.filter(activo=True)
    return render(request, 'usuarios/carta.html', {'productos': productos})

# ¡NUEVA FUNCIÓN AÑADIDA PARA EL CARRITO!
def ver_carrito(request):
    return render(request, 'usuarios/carrito.html')