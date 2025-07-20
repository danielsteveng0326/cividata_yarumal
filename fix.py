#!/usr/bin/env python3
"""
Solucion definitiva para Railway - Compatible con Windows
"""

from pathlib import Path
import shutil

def remove_nixpacks():
    """Elimina nixpacks.toml para usar autodeteccion"""
    nixpacks_path = Path('nixpacks.toml')
    if nixpacks_path.exists():
        nixpacks_path.unlink()
        print("✓ nixpacks.toml eliminado")
    else:
        print("i nixpacks.toml ya no existe")

def create_minimal_config():
    """Crea configuracion minima que funciona"""
    
    # Procfile simple
    procfile = "web: cd app && python manage.py migrate && gunicorn app.wsgi:application --bind 0.0.0.0:$PORT"
    Path('Procfile').write_text(procfile, encoding='utf-8')
    print("✓ Procfile creado")
    
    # Runtime para Python
    runtime = "python-3.9.18"
    Path('runtime.txt').write_text(runtime, encoding='utf-8')
    print("✓ runtime.txt creado")
    
    # Railway.json minimo
    railway_config = """{
  "deploy": {
    "numReplicas": 1,
    "sleepApplication": false,
    "restartPolicyType": "ON_FAILURE"
  }
}"""
    Path('railway.json').write_text(railway_config, encoding='utf-8')
    print("✓ railway.json minimo creado")

def fix_requirements_final():
    """Arregla requirements.txt de forma definitiva"""
    
    req_path = Path('requirements.txt')
    if not req_path.exists():
        print("X requirements.txt no encontrado")
        return
    
    # Leer contenido actual
    content = req_path.read_text(encoding='utf-8')
    
    # Reemplazos necesarios
    replacements = {
        'psycopg2==2.9.10': 'psycopg2-binary==2.9.9',
        'git-filter-repo==2.47.0': '# git-filter-repo==2.47.0  # No necesario para web app'
    }
    
    # Aplicar reemplazos
    for old, new in replacements.items():
        if old in content:
            content = content.replace(old, new)
            print(f"✓ Reemplazado: {old} -> {new}")
    
    # Asegurar dependencias de Railway
    railway_deps = [
        'python-decouple==3.8',
        'whitenoise==6.6.0',
        'gunicorn==21.2.0',
        'dj-database-url==2.1.0'
    ]
    
    for dep in railway_deps:
        dep_name = dep.split('==')[0]
        if dep_name not in content:
            content += f"\n{dep}"
            print(f"✓ Agregado: {dep}")
    
    # Escribir archivo actualizado
    req_path.write_text(content, encoding='utf-8')
    print("✓ requirements.txt actualizado")

def create_aptfile():
    """Crea Aptfile para dependencias del sistema"""
    
    aptfile_content = """postgresql-dev
libpq-dev"""
    
    Path('Aptfile').write_text(aptfile_content, encoding='utf-8')
    print("✓ Aptfile creado (para dependencias de PostgreSQL)")

def create_build_script():
    """Crea script de build personalizado sin emojis"""
    
    build_script = """#!/bin/bash
set -e

echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "Collecting static files..."
cd app
python manage.py collectstatic --noinput --clear

echo "Build completed!"
"""
    
    build_path = Path('build.sh')
    build_path.write_text(build_script, encoding='utf-8')
    print("✓ build.sh creado")

def verify_files():
    """Verifica que todos los archivos necesarios existan"""
    
    required_files = {
        'Procfile': 'Comando de inicio',
        'runtime.txt': 'Version de Python',
        'railway.json': 'Configuracion Railway',
        'requirements.txt': 'Dependencias Python',
        'Aptfile': 'Dependencias sistema',
        'build.sh': 'Script de build'
    }
    
    print("\nVerificando archivos:")
    all_good = True
    
    for filename, description in required_files.items():
        if Path(filename).exists():
            print(f"✓ {filename} - {description}")
        else:
            print(f"X {filename} - {description} - FALTANTE")
            all_good = False
    
    return all_good

def main():
    print("Aplicando solucion definitiva para Railway...\n")
    
    # 1. Eliminar configuraciones problematicas
    print("Eliminando configuraciones problematicas:")
    remove_nixpacks()
    
    # 2. Crear configuracion minima
    print("\nCreando configuracion minima:")
    create_minimal_config()
    
    # 3. Arreglar requirements.txt
    print("\nArreglando requirements.txt:")
    fix_requirements_final()
    
    # 4. Crear Aptfile para dependencias del sistema
    print("\nCreando Aptfile:")
    create_aptfile()
    
    # 5. Crear script de build
    print("\nCreando script de build:")
    create_build_script()
    
    # 6. Verificar archivos
    files_ok = verify_files()
    
    print("\n" + "="*60)
    if files_ok:
        print("✓ Solucion aplicada correctamente!")
    else:
        print("! Algunos archivos no se crearon correctamente")
    
    print("\nArchivos creados/modificados:")
    print("   • Procfile (comando de inicio)")
    print("   • runtime.txt (Python 3.9.18)")
    print("   • railway.json (configuracion minima)")
    print("   • requirements.txt (arreglado)")
    print("   • Aptfile (dependencias PostgreSQL)")
    print("   • build.sh (script de build)")
    print("   • nixpacks.toml (eliminado)")
    
    print("\nProximos pasos:")
    print("1. git add .")
    print("2. git commit -m 'Fix Railway deployment - remove nixpacks'")
    print("3. git push origin main")
    
    print("\nVariables de entorno en Railway:")
    print("   SECRET_KEY=tu-clave-secreta")
    print("   DEBUG=False")
    print("   OPENAI_API_KEY=tu-openai-key")
    
    print("\nEsta configuracion usa:")
    print("   • Autodeteccion de Railway (sin nixpacks.toml)")
    print("   • psycopg2-binary (precompilado)")
    print("   • Aptfile para dependencias del sistema")
    print("   • Configuracion minima que funciona")

if __name__ == "__main__":
    main()