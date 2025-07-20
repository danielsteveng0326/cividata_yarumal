# Dockerfile para Railway
FROM python:3.9-slim

# Variables de entorno
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=8000

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    postgresql-client \
    libpq-dev \
    gcc \
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
CMD cd app && python manage.py migrate && gunicorn app.wsgi:application --bind 0.0.0.0:$PORT