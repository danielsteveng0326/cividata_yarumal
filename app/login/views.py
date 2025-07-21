# app/login/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponseRedirect
from django.urls import reverse

@never_cache
@csrf_protect
def login_view(request):
    """Vista de login con diseño AdminLTE"""
    
    # Si el usuario ya está autenticado, redirigir directamente al index de contratación
    if request.user.is_authenticated:
        return redirect('/contratacion/index/')  # ← CAMBIO AQUÍ
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if username and password:
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, f'¡Bienvenido {user.get_full_name() or user.username}!')
                
                # Redirigir a la página solicitada o al dashboard
                next_url = request.GET.get('next', '/contratacion/index/')
                return HttpResponseRedirect(next_url)
            else:
                messages.error(request, 'Usuario o contraseña incorrectos')
        else:
            messages.error(request, 'Por favor complete todos los campos')
    
    return render(request, 'login/login.html')

@login_required
def logout_view(request):
    """Vista de logout"""
    user_name = request.user.get_full_name() or request.user.username
    logout(request)
    messages.info(request, f'Sesión cerrada correctamente. ¡Hasta pronto {user_name}!')
    return redirect('login:login')

def check_auth_status(request):
    """Vista para verificar estado de autenticación via AJAX"""
    from django.http import JsonResponse
    return JsonResponse({
        'authenticated': request.user.is_authenticated,
        'username': request.user.username if request.user.is_authenticated else None
    })