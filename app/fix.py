# css_fix_script.py - Script para crear archivos CSS faltantes

import os

# Crear directorios y archivos CSS básicos si no existen
css_files = [
    'app/static/lib/adminlt320/plugins/tempusdominus-bootstrap-4/css/tempusdominus-bootstrap-4.min.css',
    'app/static/lib/adminlt320/plugins/icheck-bootstrap/icheck-bootstrap.min.css',
    'app/static/lib/adminlt320/plugins/jqvmap/jqvmap.min.css',
    'app/static/lib/adminlt320/plugins/daterangepicker/daterangepicker.css',
    'app/static/lib/adminlt320/plugins/summernote/summernote-bs4.min.css'
]

# CSS básico para archivos faltantes
basic_css = """/* Archivo CSS básico para evitar errores 404 */
/* Este archivo se puede reemplazar con el contenido real más tarde */
"""

def create_missing_css():
    for css_file in css_files:
        # Crear directorio si no existe
        directory = os.path.dirname(css_file)
        os.makedirs(directory, exist_ok=True)
        
        # Crear archivo si no existe
        if not os.path.exists(css_file):
            with open(css_file, 'w') as f:
                f.write(basic_css)
            print(f"✅ Creado: {css_file}")
        else:
            print(f"📁 Ya existe: {css_file}")

if __name__ == "__main__":
    print("🔧 Creando archivos CSS faltantes...")
    create_missing_css()
    print("✅ ¡Archivos CSS creados!")
    print("\n📋 Próximos pasos:")
    print("1. Ejecutar: python manage.py collectstatic --noinput")
    print("2. Reiniciar el servidor: python manage.py runserver")
    print("3. Verificar que los gráficos cargan correctamente")