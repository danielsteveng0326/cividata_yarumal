#!/bin/bash
set -e

echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "Collecting static files..."
cd app
python manage.py collectstatic --noinput --clear

echo "Build completed!"
