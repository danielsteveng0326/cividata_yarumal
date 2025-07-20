"""
URL configuration for app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

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
    path('', include('dashboard.urls')),
    path('admin/', admin.site.urls),
    path('contratacion/', include('dashboard.urls')),
    path('chat/', include('chatbot.urls')),
]

# Manejo de errores
handler404 = custom_404
handler500 = custom_500
handler403 = custom_403
handler400 = custom_400