#!/usr/bin/env python3
"""
Script para migrar el proyecto existente a Railway
"""

import os
import shutil
from pathlib import Path

def backup_original_files():
    """Hace backup de archivos originales"""
    
    files_to_backup = [
        'app/app/settings.py',
        'requirements.txt'
    ]
    
    for file_path in files_to_backup:
        if Path(file_path).exists():
            backup_path = f"{file_path}.backup"
            shutil.copy2(file_path, backup_path)
            print(f"✅ Backup creado: {backup_path}")

def update_requirements():
    """Actualiza requirements.txt con dependencias de Railway"""
    
    additional_deps = [
        "python-decouple==3.8",
        "whitenoise==6.6.0", 
        "gunicorn==21.2.0",
        "dj-database-url==2.1.0"
    ]
    
    req_path = Path('requirements.txt')
    
    if req_path.exists():
        content = req_path.read_text()
        
        # Agregar dependencias si no existen
        for dep in additional_deps:
            if dep.split('==')[0] not in content:
                content += f"\n{dep}"
        
        req_path.write_text(content)
        print("✅ requirements.txt actualizado")
    else:
        print("❌ requirements.txt no encontrado")

def create_railway_files():
    """Crea archivos específicos de Railway"""
    
    # Procfile
    procfile_content = "web: cd app && python manage.py collectstatic --noinput && python manage.py migrate && gunicorn app.wsgi:application --bind 0.0.0.0:$PORT"
    Path('Procfile').write_text(procfile_content)
    print("✅ Procfile creado")
    
    # railway.json
    railway_json = """{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "numReplicas": 1,
    "sleepApplication": false,
    "restartPolicyType": "ON_FAILURE"
  }
}"""
    Path('railway.json').write_text(railway_json)
    print("✅ railway.json creado")
    
    # nixpacks.toml
    nixpacks_content = """[phases.setup]
nixPkgs = ['python39', 'postgresql']

[phases.install]
cmds = ['pip install -r requirements.txt']

[phases.build]
cmds = [
    'cd app',
    'python manage.py collectstatic --noinput'
]

[start]
cmd = 'cd app && gunicorn app.wsgi:application --bind 0.0.0.0:$PORT'"""
    Path('nixpacks.toml').write_text(nixpacks_content)
    print("✅ nixpacks.toml creado")

def update_settings():
    """Actualiza settings.py para Railway"""
    
    settings_path = Path('app/app/settings.py')
    
    if not settings_path.exists():
        print("❌ settings.py no encontrado")
        return
    
    # Leer el contenido actual
    content = settings_path.read_text()
    
    # Agregar imports necesarios al inicio
    imports_to_add = [
        "import os",
        "import dj_database_url"
    ]
    
    # Encontrar dónde termina la sección de imports
    lines = content.split('\n')
    import_end = 0
    
    for i, line in enumerate(lines):
        if line.startswith('from pathlib import Path'):
            import_end = i + 1
            break
    
    # Insertar imports faltantes
    for imp in imports_to_add:
        if imp not in content:
            lines.insert(import_end, imp)
            import_end += 1
    
    # Actualizar configuraciones específicas
    updated_content = '\n'.join(lines)
    
    # Actualizar ALLOWED_HOSTS
    if 'ALLOWED_HOSTS = []' in updated_content:
        updated_content = updated_content.replace(
            'ALLOWED_HOSTS = []',
            """ALLOWED_HOSTS = [
    'localhost', 
    '127.0.0.1',
    '.railway.app',
    '.up.railway.app',
]

if os.environ.get('RAILWAY_PUBLIC_DOMAIN'):
    ALLOWED_HOSTS.append(os.environ.get('RAILWAY_PUBLIC_DOMAIN'))"""
        )
    
    # Agregar WhiteNoise middleware
    if "'django.middleware.security.SecurityMiddleware'," in updated_content and "'whitenoise.middleware.WhiteNoiseMiddleware'," not in updated_content:
        updated_content = updated_content.replace(
            "'django.middleware.security.SecurityMiddleware',",
            """'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',"""
        )
    
    # Actualizar configuración de base de datos
    db_config = """# Database
# Railway PostgreSQL configuration
DATABASE_URL = os.environ.get('DATABASE_URL')

if DATABASE_URL:
    # Configuración para Railway (Producción)
    DATABASES = {
        'default': dj_database_url.parse(DATABASE_URL)
    }
else:
    # Configuración local (Desarrollo)
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": "ugdb",
            "USER": "postgres", 
            "PASSWORD": "cidoli64",
            "HOST": "127.0.0.1",
            "PORT": "5432",
        }
    }"""
    
    # Reemplazar configuración de base de datos existente
    import re
    db_pattern = r'DATABASES = \{[^}]+\}[^}]*\}'
    updated_content = re.sub(db_pattern, db_config, updated_content, flags=re.DOTALL)
    
    # Agregar configuración de archivos estáticos
    if 'STATIC_ROOT' not in updated_content:
        static_config = """
# Static files configuration for Railway
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'"""
        
        # Insertar antes de DEFAULT_AUTO_FIELD
        updated_content = updated_content.replace(
            "DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'",
            static_config + "\n\nDEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'"
        )
    
    # Escribir el archivo actualizado
    settings_path.write_text(updated_content)
    print("✅ settings.py actualizado")

def update_gitignore():
    """Actualiza .gitignore"""
    
    gitignore_path = Path('.gitignore')
    
    entries_to_add = [
        '.env',
        'staticfiles/',
        '*.backup'
    ]
    
    if gitignore_path.exists():
        content = gitignore_path.read_text()
    else:
        content = ""
    
    for entry in entries_to_add:
        if entry not in content:
            content += f"\n{entry}"
    
    gitignore_path.write_text(content)
    print("✅ .gitignore actualizado")

def install_dependencies():
    """Instala dependencias nuevas"""
    
    print("\n📦 Instalando dependencias adicionales...")
    os.system("pip install python-decouple whitenoise gunicorn dj-database-url")
    print("✅ Dependencias instaladas")

def main():
    print("🚀 Migrando proyecto a Railway...\n")
    
    # 1. Backup de archivos originales
    print("📋 Creando backups...")
    backup_original_files()
    
    # 2. Actualizar requirements.txt
    print("\n📦 Actualizando requirements.txt...")
    update_requirements()
    
    # 3. Crear archivos de Railway
    print("\n📁 Creando archivos de configuración...")
    create_railway_files()
    
    # 4. Actualizar settings.py
    print("\n⚙️  Actualizando settings.py...")
    update_settings()
    
    # 5. Actualizar .gitignore
    print("\n📝 Actualizando .gitignore...")
    update_gitignore()
    
    # 6. Instalar dependencias
    install_dependencies()
    
    print("\n" + "="*50)
    print("✅ ¡Migración completada!")
    print("\n📋 Próximos pasos:")
    print("1. Revisar los cambios en settings.py")
    print("2. git add .")
    print("3. git commit -m 'Configurar para Railway'")
    print("4. git push origin main") 
    print("5. Crear proyecto en Railway")
    print("6. Configurar variables de entorno en Railway:")
    print("   - SECRET_KEY")
    print("   - DEBUG=False")
    print("   - OPENAI_API_KEY")

if __name__ == "__main__":
    main()