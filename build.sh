#!/bin/bash

# build.sh - Script de build para Railway

set -e

echo "🔧 Instalando dependencias..."
pip install -r requirements.txt

echo "📁 Recolectando archivos estáticos..."
cd app
python manage.py collectstatic --noinput

echo "✅ Build completado!"