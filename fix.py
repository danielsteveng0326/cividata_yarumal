#!/usr/bin/env python3
"""
Diagnosticar problemas de deployment en Railway
"""

from pathlib import Path

def check_urls_configuration():
    """Verifica la configuración de URLs"""
    
    main_urls_path = Path('app/app/urls.py')
    dashboard_urls_path = Path('app/dashboard/urls.py')
    
    print("=== VERIFICANDO CONFIGURACIÓN DE URLs ===\n")
    
    # Verificar URLs principales
    if main_urls_path.exists():
        content = main_urls_path.read_text(encoding='utf-8')
        print("✓ app/app/urls.py encontrado")
        print("Contenido:")
        print("-" * 40)
        print(content)
        print("-" * 40)
        
        # Verificar si hay una ruta para '/'
        if "path(''" in content:
            print("✓ Ruta raíz configurada")
        else:
            print("❌ NO hay ruta para '/' configurada")
    else:
        print("❌ app/app/urls.py NO encontrado")
    
    print("\n" + "="*50 + "\n")
    
    # Verificar URLs de dashboard
    if dashboard_urls_path.exists():
        content = dashboard_urls_path.read_text(encoding='utf-8')
        print("✓ app/dashboard/urls.py encontrado")
        print("Contenido:")
        print("-" * 40)
        print(content)
        print("-" * 40)
    else:
        print("❌ app/dashboard/urls.py NO encontrado")

def check_views():
    """Verifica las vistas de dashboard"""
    
    views_path = Path('app/dashboard/views.py')
    
    print("\n=== VERIFICANDO VISTAS ===\n")
    
    if views_path.exists():
        content = views_path.read_text(encoding='utf-8')
        print("✓ app/dashboard/views.py encontrado")
        
        # Verificar funciones principales
        functions = ['home', 'dashboard', 'expired', 'api']
        
        for func in functions:
            if f"def {func}(" in content:
                print(f"✓ Función {func} encontrada")
            else:
                print(f"❌ Función {func} NO encontrada")
    else:
        print("❌ app/dashboard/views.py NO encontrado")

def check_templates():
    """Verifica que existan los templates necesarios"""
    
    print("\n=== VERIFICANDO TEMPLATES ===\n")
    
    template_paths = [
        'app/templates/navbar.html',
        'app/templates/contract_dash.html',
        'app/templates/home/home.html',
        'app/templates/index.html'
    ]
    
    for template_path in template_paths:
        path = Path(template_path)
        if path.exists():
            print(f"✓ {template_path}")
        else:
            print(f"❌ {template_path} NO encontrado")

def check_static_files():
    """Verifica configuración de archivos estáticos"""
    
    print("\n=== VERIFICANDO ARCHIVOS ESTÁTICOS ===\n")
    
    static_dirs = [
        'app/static',
        'app/staticfiles',
        'staticfiles'
    ]
    
    for static_dir in static_dirs:
        path = Path(static_dir)
        if path.exists():
            print(f"✓ {static_dir} existe")
            # Contar archivos
            files = list(path.rglob('*'))
            print(f"  - {len(files)} archivos encontrados")
        else:
            print(f"❌ {static_dir} NO existe")

def generate_fixed_urls():
    """Genera configuración de URLs corregida"""
    
    print("\n=== CONFIGURACIÓN DE URLs SUGERIDA ===\n")
    
    main_urls_fixed = '''"""
URL configuration for app project.
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('dashboard.urls')),  # Ruta raíz apunta a dashboard
    path('contratacion/', include('dashboard.urls')),
    path('chat/', include('chatbot.urls')),
]'''
    
    dashboard_urls_fixed = '''from django.urls import path
from . import views
from .views import ContratoListView

urlpatterns = [
    path('', views.dashboard, name="dashboard"),  # Ruta raíz
    path('dashboard/', views.dashboard, name="dashboard"),
    path('expired/', views.expired, name="expired"),
    path('expired-edur/', views.expirededur, name="expirededur"),
    path('report/', ContratoListView.as_view(), name='contratos_list'),
    path('api/', views.api, name="api"),
    path('emilia/', views.emilia, name="emilia"),
]'''
    
    print("📁 app/app/urls.py debería contener:")
    print("-" * 40)
    print(main_urls_fixed)
    print("-" * 40)
    
    print("\n📁 app/dashboard/urls.py debería contener:")
    print("-" * 40)
    print(dashboard_urls_fixed)
    print("-" * 40)

def railway_debugging_commands():
    """Comandos para debuggear en Railway"""
    
    print("\n=== COMANDOS PARA DEBUGGEAR EN RAILWAY ===\n")
    
    commands = [
        "# 1. Ver logs completos:",
        "Railway → Deploy → View Logs",
        "",
        "# 2. Acceder a shell de Railway:",
        "Railway → Deploy → Shell",
        "",
        "# 3. Comandos útiles en el shell:",
        "cd app",
        "python manage.py check",
        "python manage.py showmigrations", 
        "python manage.py collectstatic --noinput",
        "python manage.py runserver 0.0.0.0:8080 --insecure",
        "",
        "# 4. Verificar variables de entorno:",
        "env | grep DATABASE",
        "env | grep SECRET",
        "",
        "# 5. Probar URLs específicas:",
        "curl http://localhost:8080/",
        "curl http://localhost:8080/dashboard/",
        "curl http://localhost:8080/admin/"
    ]
    
    for cmd in commands:
        print(cmd)

def main():
    print("🔍 DIAGNOSTICANDO DEPLOYMENT EN RAILWAY...\n")
    
    check_urls_configuration()
    check_views()
    check_templates()
    check_static_files()
    generate_fixed_urls()
    railway_debugging_commands()
    
    print("\n" + "="*60)
    print("🎯 POSIBLES CAUSAS DEL PROBLEMA:")
    print("="*60)
    print("1. ❌ No hay ruta configurada para '/'")
    print("2. ❌ Error en las vistas de dashboard")
    print("3. ❌ Templates faltantes")
    print("4. ❌ Archivos estáticos no encontrados")
    print("5. ❌ Variables de entorno mal configuradas")
    
    print("\n🔧 PRÓXIMOS PASOS:")
    print("1. Ejecutar este diagnóstico")
    print("2. Revisar logs de Railway")
    print("3. Verificar configuración de URLs")
    print("4. Probar en shell de Railway")
    print("5. Corregir y redesplegar")

if __name__ == "__main__":
    main()