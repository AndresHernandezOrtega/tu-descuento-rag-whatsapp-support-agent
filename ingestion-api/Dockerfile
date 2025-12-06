# Usamos una imagen oficial de Python como base
FROM python:3.11-slim

# Establecemos el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiamos el archivo de dependencias primero para aprovechar el cache de Docker
COPY ingestion-api/requirements.txt requirements.txt

# Instalamos las dependencias
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos el código de la aplicación al contenedor
COPY ingestion-api/ .

# Exponer el puerto
EXPOSE 8008

# Comando para iniciar la aplicación
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8008"]