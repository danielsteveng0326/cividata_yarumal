# app/app/urls.py - Versión actualizada con login
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

# Vistas de error personalizadas
def custom_404(request, exception):
    from django.shortcuts import render
    return render(request, 'error.html', status=404)

def custom_500(request):
    from django.shortcuts import render
    return render(request, 'error.html', status=500)

def custom_403(request, exception):
    from django.shortcuts import render
    return render(request, 'error.html', status=403)

def custom_400(request, exception):
    from django.shortcuts import render
    return render(request, 'error.html', status=400)

urlpatterns = [
    # Login como página principal
    path('', RedirectView.as_view(url='/login/', permanent=False)),
    
    # URLs principales
    path('admin/', admin.site.urls),
    path('login/', include('login.urls')),  # ← ACTIVADO
    path('contratacion/', include('dashboard.urls')),
    path('chat/', include('chatbot.urls')),
]

# Manejo de errores
handler404 = custom_404
handler500 = custom_500
handler403 = custom_403
handler400 = custom_400