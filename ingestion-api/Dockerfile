# Usamos una imagen oficial de Python como base
FROM python:3.11-slim

# Establecemos el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiamos el archivo de dependencias primero para aprovechar el cache de Docker
COPY ingestion-api/requirements.txt requirements.txt

# Instalamos las dependencias del sistema necesarias para compilar algunas librerías
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Instalamos las dependencias de Python
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos el código de la aplicación al contenedor
COPY ingestion-api/ .

# Crear usuario no-root para seguridad
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Exponer el puerto
EXPOSE 8008

# Health check para que Easypanel sepa cuándo está listo
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8008/health || exit 1

# Comando para producción con configuración optimizada para proxy reverso
CMD ["uvicorn", "app.main:app", \
    "--host", "0.0.0.0", \
    "--port", "8008", \
    "--workers", "4", \
    "--proxy-headers", \
    "--forwarded-allow-ips", "*"]