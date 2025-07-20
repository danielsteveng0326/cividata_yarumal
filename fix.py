#!/usr/bin/env python3
"""
Script para arreglar el error de build en Railway
"""

from pathlib import Path
import shutil

def backup_requirements():
    """Hace backup del requirements.txt actual"""
    req_path = Path('requirements.txt')
    if req_path.exists():
        shutil.copy2(req_path, 'requirements.txt.backup')
        print("✅ Backup de requirements.txt creado")

def fix_requirements():
    """Arregla requirements.txt para Railway"""
    
    # Contenido arreglado sin git-filter-repo y con psycopg2-binary
    fixed_content = """annotated-types==0.7.0
anyio==4.6.2.post1
asgiref==3.8.1
certifi==2024.8.30
charset-normalizer==3.4.0
colorama==0.4.6
distro==1.9.0
Django==5.1.2
h11==0.14.0
httpcore==1.0.6
httpx==0.27.2
idna==3.10
jiter==0.7.0
numpy==2.1.2
openai==1.54.1
pandas==2.2.3
psycopg2-binary==2.9.9
pydantic==2.9.2
pydantic_core==2.23.4
python-dateutil==2.9.0.post0
pytz==2024.2
requests==2.32.3
six==1.16.0
sniffio==1.3.1
sodapy==2.2.0
sqlparse==0.5.1
tqdm==4.66.6
typing_extensions==4.12.2
tzdata==2024.2
urllib3==2.2.3

# Dependencias adicionales para Railway
python-decouple==3.8
whitenoise==6.6.0
gunicorn==21.2.0
dj-database-url==2.1.0"""
    
    Path('requirements.txt').write_text(fixed_content)
    print("✅ requirements.txt arreglado")

def create_runtime_txt():
    """Crea runtime.txt para especificar versión de Python"""
    Path('runtime.txt').write_text('python-3.9.18')
    print("✅ runtime.txt creado")

def create_simple_procfile():
    """Crea Procfile simple"""
    procfile_content = "web: cd app && python manage.py migrate && gunicorn app.wsgi:application --bind 0.0.0.0:$PORT"
    Path('Procfile').write_text(procfile_content)
    print("✅ Procfile creado")

def remove_problematic_files():
    """Elimina archivos que pueden causar problemas"""
    files_to_remove = ['nixpacks.toml']
    
    for file_name in files_to_remove:
        file_path = Path(file_name)
        if file_path.exists():
            file_path.unlink()
            print(f"✅ {file_name} eliminado")

def create_minimal_railway_json():
    """Crea railway.json mínimo"""
    railway_config = """{
  "deploy": {
    "numReplicas": 1,
    "sleepApplication": false,
    "restartPolicyType": "ON_FAILURE"
  }
}"""
    Path('railway.json').write_text(railway_config)
    print("✅ railway.json creado")

def analyze_current_requirements():
    """Analiza el requirements.txt actual para identificar problemas"""
    req_path = Path('requirements.txt')
    
    if not req_path.exists():
        print("❌ requirements.txt no encontrado")
        return
    
    content = req_path.read_text()
    lines = content.strip().split('\n')
    
    problematic_packages = []
    
    for line in lines:
        line = line.strip()
        if not line or line.startswith('#'):
            continue
            
        # Identificar paquetes problemáticos
        if 'psycopg2==' in line and 'psycopg2-binary' not in line:
            problematic_packages.append(f"❌ {line} (usar psycopg2-binary)")
        elif 'git-filter-repo' in line:
            problematic_packages.append(f"❌ {line} (no necesario para web app)")
        elif '==' not in line and line:
            problematic_packages.append(f"⚠️  {line} (sin versión específica)")
    
    if problematic_packages:
        print("🔍 Paquetes problemáticos encontrados:")
        for pkg in problematic_packages:
            print(f"   {pkg}")
    else:
        print("✅ No se encontraron paquetes problemáticos obvios")

def main():
    print("🔧 Arreglando error de build en Railway...\n")
    
    # 1. Analizar requirements.txt actual
    print("🔍 Analizando requirements.txt actual:")
    analyze_current_requirements()
    
    # 2. Hacer backup
    print("\n📋 Creando backup:")
    backup_requirements()
    
    # 3. Arreglar requirements.txt
    print("\n📦 Arreglando requirements.txt:")
    fix_requirements()
    
    # 4. Crear archivos necesarios
    print("\n📁 Creando archivos de configuración:")
    create_runtime_txt()
    create_simple_procfile()
    create_minimal_railway_json()
    
    # 5. Eliminar archivos problemáticos
    print("\n🗑️  Eliminando archivos problemáticos:")
    remove_problematic_files()
    
    print("\n" + "="*60)
    print("✅ ¡Build arreglado!")
    print("\n📋 Cambios realizados:")
    print("   • psycopg2 → psycopg2-binary (precompilado)")
    print("   • git-filter-repo eliminado (no necesario)")
    print("   • runtime.txt creado (Python 3.9.18)")
    print("   • Procfile simplificado")
    print("   • nixpacks.toml eliminado")
    
    print("\n🚀 Próximos pasos:")
    print("1. git add .")
    print("2. git commit -m 'Fix Railway build errors'")
    print("3. git push origin main")
    print("4. Railway hará redeploy automático")
    
    print("\n⚠️  Si persisten errores:")
    print("   • Verifica que DATABASE_URL esté configurado en Railway")
    print("   • Agrega SECRET_KEY en variables de entorno")
    print("   • Asegúrate de que PostgreSQL esté configurado")

if __name__ == "__main__":
    main()