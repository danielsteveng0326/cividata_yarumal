#!/usr/bin/env python3
"""
Script para generar una SECRET_KEY segura para Django en producción
"""

import secrets
import string

def generate_secret_key(length=50):
    """Genera una SECRET_KEY segura para Django"""
    
    # Caracteres permitidos para SECRET_KEY
    chars = string.ascii_letters + string.digits + '!@#$%^&*(-_=+)'
    
    # Generar clave aleatoria
    secret_key = ''.join(secrets.choice(chars) for _ in range(length))
    
    return secret_key

def main():
    print("🔐 Generando SECRET_KEY segura para producción...\n")
    
    # Generar nueva clave
    new_secret_key = generate_secret_key()
    
    print("✅ Nueva SECRET_KEY generada:")
    print(f"SECRET_KEY={new_secret_key}")
    
    print(f"\n📋 Instrucciones:")
    print("1. Copia la SECRET_KEY de arriba")
    print("2. En Railway, ve a tu proyecto → Variables")
    print("3. Agrega una nueva variable:")
    print("   Nombre: SECRET_KEY")
    print(f"   Valor: {new_secret_key}")
    print("\n⚠️  NUNCA compartas esta clave o la subas a Git!")
    
    # Generar varias opciones
    print(f"\n🔄 Opciones adicionales (elige una):")
    for i in range(3):
        alt_key = generate_secret_key()
        print(f"Opción {i+1}: {alt_key}")

if __name__ == "__main__":
    main()