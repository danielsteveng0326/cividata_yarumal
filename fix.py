#!/usr/bin/env python3
"""
Configuracion minima para Railway - Sin Nixpacks
"""

from pathlib import Path
import os

def clean_nixpacks_files():
    """Elimina TODOS los archivos relacionados con nixpacks"""
    
    nixpacks_files = [
        'nixpacks.toml',
        '.nixpacks.toml', 
        'nixpacks.json',
        '.nixpacks.json'
    ]
    
    for filename in nixpacks_files:
        file_path = Path(filename)
        if file_path.exists():
            file_path.unlink()
            print(f"✓ Eliminado: {filename}")
        else:
            print(f"- No existe: {filename}")

def create_procfile():
    """Crea Procfile simple"""
    content = "web: cd app && python manage.py migrate && gunicorn app.wsgi:application --bind 0.0.0.0:$PORT"
    Path('Procfile').write_text(content, encoding='utf-8')
    print("✓ Procfile creado")

def create_runtime():
    """Especifica version de Python"""
    content = "python-3.9.18"
    Path('runtime.txt').write_text(content, encoding='utf-8')
    print("✓ runtime.txt creado")

def fix_requirements():
    """Arregla requirements.txt"""
    req_path = Path('requirements.txt')
    
    if req_path.exists():
        content = req_path.read_text(encoding='utf-8')
        
        # Cambios criticos
        changes = {
            'psycopg2==2.9.10': 'psycopg2-binary==2.9.9',
            'git-filter-repo==2.47.0': '# git-filter-repo==2.47.0'
        }
        
        for old, new in changes.items():
            if old in content:
                content = content.replace(old, new)
                print(f"✓ Cambiado: {old} -> {new}")
        
        # Agregar dependencias necesarias
        required = ['gunicorn==21.2.0', 'whitenoise==6.6.0', 'dj-database-url==2.1.0']
        
        for dep in required:
            dep_name = dep.split('==')[0]
            if dep_name not in content:
                content += f"\n{dep}"
                print(f"✓ Agregado: {dep}")
        
        req_path.write_text(content, encoding='utf-8')
        print("✓ requirements.txt actualizado")
    else:
        print("X requirements.txt no encontrado")

def main():
    print("Configurando Railway sin Nixpacks...\n")
    
    print("1. Limpiando archivos de Nixpacks:")
    clean_nixpacks_files()
    
    print("\n2. Creando Procfile:")
    create_procfile()
    
    print("\n3. Creando runtime.txt:")
    create_runtime()
    
    print("\n4. Arreglando requirements.txt:")
    fix_requirements()
    
    print("\n" + "="*50)
    print("✓ Configuracion minima completada!")
    print("\nArchivos creados:")
    print("  - Procfile (comando de inicio)")
    print("  - runtime.txt (Python 3.9.18)")
    print("  - requirements.txt (arreglado)")
    print("\nEliminados:")
    print("  - Todos los archivos nixpacks.*")
    
    print("\nProximos pasos:")
    print("1. git add .")
    print("2. git commit -m 'Remove nixpacks config - use Railway autodetection'")
    print("3. git push origin main")
    print("4. Railway redesplegara automaticamente")

if __name__ == "__main__":
    main()