# app/create_admin_user.py
# Script para crear usuario administrador rápidamente

import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')
django.setup()

from django.contrib.auth.models import User

def create_admin_user():
    """Crear usuario administrador"""
    
    # Datos del usuario (cámbialo por tus datos)
    username = "admin"
    email = "admin@municipio.gov.co"
    password = "admin123"  # Cambia por una contraseña segura
    first_name = "Administrador"
    last_name = "Sistema"
    
    # Verificar si ya existe
    if User.objects.filter(username=username).exists():
        print(f"❌ El usuario '{username}' ya existe")
        user = User.objects.get(username=username)
        print(f"📋 Usuario existente: {user.get_full_name()} ({user.email})")
        return
    
    # Crear usuario
    user = User.objects.create_user(
        username=username,
        email=email,
        password=password,
        first_name=first_name,
        last_name=last_name,
        is_staff=True,      # Puede acceder al admin
        is_superuser=True   # Permisos totales
    )
    
    print("✅ Usuario administrador creado exitosamente!")
    print(f"👤 Usuario: {username}")
    print(f"🔑 Contraseña: {password}")
    print(f"📧 Email: {email}")
    print(f"🏷️  Nombre: {user.get_full_name()}")
    print("\n🚀 Ya puedes usar estos datos para iniciar sesión")

def create_regular_user():
    """Crear usuario regular para pruebas"""
    
    username = "usuario"
    email = "usuario@municipio.gov.co" 
    password = "usuario123"
    first_name = "Usuario"
    last_name = "Prueba"
    
    if User.objects.filter(username=username).exists():
        print(f"❌ El usuario '{username}' ya existe")
        return
        
    user = User.objects.create_user(
        username=username,
        email=email,
        password=password,
        first_name=first_name,
        last_name=last_name,
        is_staff=False,
        is_superuser=False
    )
    
    print("✅ Usuario regular creado exitosamente!")
    print(f"👤 Usuario: {username}")
    print(f"🔑 Contraseña: {password}")

if __name__ == "__main__":
    print("🔧 Creando usuarios del sistema...\n")
    
    # Crear admin
    create_admin_user()