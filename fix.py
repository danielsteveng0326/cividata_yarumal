#!/usr/bin/env python3
"""
Cambiar a Dockerfile para evitar problemas con Nixpacks
"""

from pathlib import Path
import shutil

def remove_nixpacks_files():
    """Elimina todos los archivos relacionados con Nixpacks"""
    
    files_to_remove = [
        'nixpacks.toml',
        '.nixpacks.toml',
        'nixpacks.json',
        '.nixpacks.json',
        'railway.json',  # También eliminar esto para usar Dockerfile
        'Procfile',      # No necesario con Dockerfile
        'runtime.txt',   # Especificado en Dockerfile
        'Aptfile'        # Especificado en Dockerfile
    ]
    
    for filename in files_to_remove:
        file_path = Path(filename)
        if file_path.exists():
            file_path.unlink()
            print(f"✓ Eliminado: {filename}")

def create_dockerfile():
    """Crea Dockerfile optimizado para Railway"""
    
    dockerfile_content = """# Dockerfile para Railway
FROM python:3.9-slim

# Variables de entorno
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=8000

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \\
    postgresql-client \\
    libpq-dev \\
    gcc \\
    && rm -rf /var/lib/apt/lists/*

# Crear directorio de trabajo
WORKDIR /app

# Copiar requirements y instalar dependencias Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código de la aplicación
COPY . .

# Crear directorio para archivos estáticos
RUN mkdir -p staticfiles

# Recopilar archivos estáticos
RUN cd app && python manage.py collectstatic --noinput

# Exponer puerto
EXPOSE $PORT

# Comando de inicio
CMD cd app && python manage.py migrate && gunicorn app.wsgi:application --bind 0.0.0.0:$PORT"""
    
    Path('Dockerfile').write_text(dockerfile_content, encoding='utf-8')
    print("✓ Dockerfile creado")

def create_dockerignore():
    """Crea .dockerignore para optimizar build"""
    
    dockerignore_content = """.git
.gitignore
README.md
*.md
.env
.venv
venv/
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
pip-log.txt
pip-delete-this-directory.txt
.coverage
.pytest_cache/
.mypy_cache/
staticfiles/
.DS_Store
Thumbs.db
nixpacks.toml
.nixpacks.toml
railway.json"""
    
    Path('.dockerignore').write_text(dockerignore_content, encoding='utf-8')
    print("✓ .dockerignore creado")

def fix_requirements():
    """Asegura que requirements.txt esté correcto"""
    
    req_path = Path('requirements.txt')
    if not req_path.exists():
        print("X requirements.txt no encontrado")
        return
    
    content = req_path.read_text(encoding='utf-8')
    
    # Cambios críticos
    replacements = {
        'psycopg2==2.9.10': 'psycopg2-binary==2.9.9',
        'git-filter-repo==2.47.0': '# git-filter-repo==2.47.0  # No necesario'
    }
    
    for old, new in replacements.items():
        if old in content:
            content = content.replace(old, new)
            print(f"✓ Reemplazado: {old}")
    
    # Asegurar dependencias
    required = [
        'gunicorn==21.2.0',
        'whitenoise==6.6.0', 
        'dj-database-url==2.1.0'
    ]
    
    for dep in required:
        dep_name = dep.split('==')[0]
        if dep_name not in content:
            content += f"\n{dep}"
            print(f"✓ Agregado: {dep}")
    
    req_path.write_text(content, encoding='utf-8')
    print("✓ requirements.txt verificado")

def verify_settings():
    """Verifica configuraciones básicas en settings.py"""
    
    settings_path = Path('app/app/settings.py')
    if not settings_path.exists():
        print("! settings.py no encontrado")
        return
    
    content = settings_path.read_text(encoding='utf-8')
    
    checks = [
        ('DATABASE_URL', 'Configuración de BD'),
        ('STATIC_ROOT', 'Archivos estáticos'),
        ('WhiteNoiseMiddleware', 'WhiteNoise'),
        ('.railway.app', 'ALLOWED_HOSTS')
    ]
    
    print("\nVerificando settings.py:")
    for check, desc in checks:
        if check in content:
            print(f"✓ {desc}")
        else:
            print(f"! {desc} - puede necesitar configuración")

def main():
    print("Cambiando a Dockerfile para evitar Nixpacks...\n")
    
    print("1. Eliminando archivos de Nixpacks:")
    remove_nixpacks_files()
    
    print("\n2. Creando Dockerfile:")
    create_dockerfile()
    
    print("\n3. Creando .dockerignore:")
    create_dockerignore()
    
    print("\n4. Verificando requirements.txt:")
    fix_requirements()
    
    print("\n5. Verificando settings.py:")
    verify_settings()
    
    print("\n" + "="*60)
    print("✓ Migración a Dockerfile completada!")
    
    print("\nArchivos creados:")
    print("  - Dockerfile (configuración completa)")
    print("  - .dockerignore (optimización)")
    
    print("\nArchivos eliminados:")
    print("  - nixpacks.toml, railway.json, Procfile, etc.")
    
    print("\nVentajas del Dockerfile:")
    print("  - Control total sobre el entorno")
    print("  - Sin problemas de Nixpacks")
    print("  - Build más predecible")
    print("  - Fácil debugging")
    
    print("\nPróximos pasos:")
    print("1. git add .")
    print("2. git commit -m 'Switch to Dockerfile - avoid Nixpacks issues'")
    print("3. git push origin main")
    print("4. Railway detectará automáticamente el Dockerfile")
    
    print("\nVariables de entorno necesarias en Railway:")
    print("  SECRET_KEY=tu-clave-secreta")
    print("  DEBUG=False")
    print("  OPENAI_API_KEY=tu-openai-key")

if __name__ == "__main__":
    main()