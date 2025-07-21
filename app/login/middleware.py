# app/login/middleware.py
from django.shortcuts import redirect
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.conf import settings

class LoginRequiredMiddleware:
    """
    Middleware que requiere login para todas las páginas excepto las públicas
    """
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # URLs que no requieren autenticación
        public_urls = [
            '/login/',
            '/admin/login/',
            '/admin/',
            '/static/',
            '/media/',
        ]
        
        # Verificar si la URL actual es pública
        is_public = any(request.path.startswith(url) for url in public_urls)
        
        # Si no es una URL pública y el usuario no está autenticado
        if not is_public and not request.user.is_authenticated:
            # Redirigir al login con next parameter
            login_url = '/login/'
            return HttpResponseRedirect(f"{login_url}?next={request.path}")
        
        response = self.get_response(request)
        return response