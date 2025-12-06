# 📚 Ingestion API + ChromaDB

API de ingesta de documentos y generación de embeddings desarrollada en **FastAPI**, conectada a una instancia de **ChromaDB** para almacenar y gestionar vectores.

Este proyecto provee una API REST capaz de:

- Recibir archivos o texto.
- Generar _embeddings_ utilizando un proveedor externo (ej. OpenAI).
- Almacenar embeddings y metadatos dentro de **ChromaDB**.
- Mantener un flujo de ingesta escalable, modular y listo para producción.

Incluye un entorno Docker listo para ejecutar tanto la API como la base vectorial.

---

## 🚀 Características principales

- API desarrollada con **FastAPI**
- Conexión directa a **ChromaDB**
- Proceso automatizado de ingesta y generación de embeddings
- Arquitectura lista para entornos **RAG**
- Despliegue sencillo mediante **Docker Compose**
- Hot-reload habilitado para desarrollo

---

## 📁 Estructura del proyecto

```
    /ingestion-api
    │── app/
    │ ├── main.py
    │ ├── routers/
    │ ├── services/
    │ └── utils/
    │── Dockerfile
    docker-compose.yml
    README.md
```

---

# 🐳 Deploy con Docker

A continuación se explica cómo levantar todo el entorno usando **Docker Compose**, incluyendo la instancia de ChromaDB y la API.

---

## 1️⃣ Requisitos

Antes de comenzar, asegúrate de tener instalado:

- **Docker**
- **Docker Compose**
- Una clave válida de **OpenAI API Key**, exportada en tu sistema:

```bash
export OPENAI_API_KEY="tu_llave_aquí"\

```

## Estructura DockerCompose

```yaml
services:
chroma:
  image: chromadb/chroma:latest
  restart: always
  environment:
    - CHROMA_SERVER_CORS_ALLOW_ORIGINS=*
    - ANONYMIZED_TELEMETRY=False
  ports:
    - '8002:8000'
  volumes:
    - chroma_data:/chroma/.chroma/index

ingestion-api:
  build:
  context: ./ingestion-api
  restart: always
  ports:
    - '8001:8008'
  volumes:
    - ./ingestion-api:/app
  environment:
    - CHROMA_HOST=chroma
    - CHROMA_PORT=8000
    - OPENAI_API_KEY=${OPENAI_API_KEY}
  command: uvicorn app.main:app --host 0.0.0.0 --port 8008 --reload
  depends_on:
    - chroma

volumes:
chroma_data:
```

## 3️⃣ Construcción y ejecución

Para levantar todo el entorno:

```bash
docker compose up --build
```

Esto:

- Descargará la imagen oficial de ChromaDB
- Construirá la imagen local de la API
- Levantará ambos servicios

## 4️⃣ Verificación de servicios

```bash
Servicio	URL de acceso	Descripción
ChromaDB	http://localhost:8002
	Motor vectorial HTTP
Ingestion API	http://localhost:8001/docs
	Documentación Swagger

```

Una vez ejecutado, deberías ver la interfaz de documentación automática de FastAPI en: 👉 http://localhost:8001/docs

## 5️⃣ Uso básico

### 📤 Ingesta de documentos

Ejemplo de petición POST:

```bash
curl -X POST "http://localhost:8001/ingest" \
 -H "Content-Type: multipart/form-data" \
 -F "file=@documento.pdf"

📄 Ingesta de texto curl -X POST "http://localhost:8001/ingest-text" \
 -H "Content-Type: application/json" \
 -d '{"content": "Texto para embedder"}'
```

6️⃣ Detener servicios docker compose down

Para eliminar volúmenes:

docker compose down -v

## 🧱 Roadmap

- Agregar soporte para múltiples modelos de embedding

- Procesamiento en batch

- Metrics & logging avanzado

- Autenticación para la API

🤝 Contribuciones ¡Las contribuciones son bienvenidas! Puedes abrir un issue, proponer mejoras o enviar un pull request.
