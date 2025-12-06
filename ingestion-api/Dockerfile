# Usamos una imagen oficial de Python como base
FROM python:3.11-slim

# Establecemos el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiamos el archivo de dependencias primero para aprovechar el cache de Docker
COPY requirements.txt requirements.txt

# Instalamos las dependencias
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos el resto del código de nuestra aplicación al contenedor
COPY . .

# El comando para iniciar la app se define en docker-compose.yml,
# por lo que no es necesario un CMD aquí.