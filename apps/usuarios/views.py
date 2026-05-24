from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

def index(request):
    return HttpResponse("Index")

def main_clientes(request):
    return render(request, 'usuarios/main_cliente.html')

def carta_clientes(request):
    return HttpResponse("Cartaclientes")

def login_personalizado(request):
    if request.user.is_authenticated:
        # Si ya está logueado, lo redirigimos según su rol de inmediato
        if request.user.is_staff:
            return redirect('index') # Pantalla de Reportes / Empleados
        else:
            return redirect('carta_clientes') # Pantalla para Clientes
        
    error_mensaje = None

    if request.method == 'POST':
        usuario_tipeado = request.POST.get('username')
        clave_tipeada = request.POST.get('password')

        usuario_valido = authenticate(request, username=usuario_tipeado, password=clave_tipeada)

        if usuario_valido is not None:
            login(request, usuario_valido)
            
            # ─── AQUÍ REVISAMOS EL ROL RECIÉN LOGUEADO ───
            if usuario_valido.is_staff:
                # Si es administrador, supervisor o empleado con acceso al sistema
                return redirect('index') 
            else:
                # Si es un cliente común que solo compra online
                return redirect('carta_clientes') 
        else:
            error_mensaje = "Usuario o contraseña incorrectos. Inténtalo de nuevo."

    return render(request, 'usuarios/login.html', {'error': error_mensaje})

def logout_personalizado(request):
    """Cierra la sesión del supervisor y lo regresa al login"""
    logout(request)
    return redirect('login')


def registro_personalizado(request):
    if request.user.is_authenticated:
        return redirect('index')

    # ─── AQUÍ TRAEMOS TU MODELO PERSONALIZADO DE MANERA SEGURA ───
    User = get_user_model() 

    error_mensaje = None

    if request.method == 'POST':
        usuario = request.POST.get('username')
        nombre = request.POST.get('first_name')
        correo = request.POST.get('email')
        clave = request.POST.get('password')
        clave_confirm = request.POST.get('password_confirm')

        if clave != clave_confirm:
            error_mensaje = "Las contraseñas no coinciden. Inténtalo de nuevo."
        
        # Ahora estas consultas llamarán automáticamente a tu modelo 'usuarios.Usuario'
        elif User.objects.filter(username=usuario).exists():
            error_mensaje = "El nombre de usuario ya se encuentra registrado."
            
        elif User.objects.filter(email=correo).exists():
            error_mensaje = "Este correo electrónico ya está en uso."
            
        else:
            # Crea el registro en tu tabla personalizada encriptando la clave
            nuevo_usuario = User.objects.create_user(
                username=usuario,
                email=correo,
                password=clave,
                first_name=nombre
            )
            nuevo_usuario.save()
            
            login(request, nuevo_usuario)
            return redirect('carta_clientes')

    return render(request, 'usuarios/registro.html', {'error': error_mensaje})