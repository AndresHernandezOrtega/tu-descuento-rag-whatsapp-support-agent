# Guía de Uso - Colección Postman para Ingestion API

## 📦 Archivos Incluidos

- `Ingestion_API.postman_collection.json` - Colección completa de endpoints
- `Ingestion_API_Dev.postman_environment.json` - Entorno de desarrollo

## 🚀 Importar en Postman

### Opción 1: Importar Colección

1. Abre Postman
2. Haz clic en **Import** (esquina superior izquierda)
3. Arrastra el archivo `Ingestion_API.postman_collection.json` o selecciónalo
4. Haz clic en **Import**

### Opción 2: Importar Entorno (Opcional pero Recomendado)

1. Haz clic en **Import**
2. Arrastra el archivo `Ingestion_API_Dev.postman_environment.json`
3. Haz clic en **Import**
4. Selecciona el entorno "Ingestion API - Development" en el dropdown superior derecho

## 📋 Estructura de la Colección

### 1️⃣ Health & Status

- **Root - Welcome**: Endpoint de bienvenida
- **Health Check**: Verifica el estado de la API

### 2️⃣ Document Management

- **Ingest Document - Manual Usuario**: Ejemplo de ingesta de manual de usuario
- **Ingest Document - FAQ**: Ejemplo de ingesta de preguntas frecuentes
- **Ingest Document - Políticas**: Ejemplo de ingesta de políticas
- **List All Documents**: Lista todos los documentos almacenados
- **Delete Document by ID**: Elimina un documento específico

### 3️⃣ API Documentation

- **OpenAPI Docs (Swagger UI)**: Documentación interactiva
- **ReDoc Documentation**: Documentación alternativa
- **OpenAPI Schema (JSON)**: Esquema de la API

## 🔧 Configuración

### Variables de Colección

La colección incluye las siguientes variables:

- `base_url`: URL base de la API (default: `http://localhost:8000`)
- `document_id`: ID del documento para operaciones de eliminación

### Modificar la URL Base

Si tu API corre en otro puerto o host:

1. Ve a la colección **Ingestion API - RAG Support Agent**
2. Haz clic en **Variables**
3. Modifica el valor de `base_url`

## 📝 Flujo de Prueba Sugerido

### Paso 1: Verificar que la API está funcionando

```
GET {{base_url}}/
GET {{base_url}}/health
```

### Paso 2: Ingestar documentos de prueba

Ejecuta en orden:

1. **Ingest Document - Manual Usuario**
2. **Ingest Document - FAQ**
3. **Ingest Document - Políticas**

Cada request incluye ejemplos completos de documentos con:

- Título
- Contenido completo
- Source (origen)
- Metadata adicional

### Paso 3: Listar documentos

```
GET {{base_url}}/api/v1/documents
```

Esto te mostrará todos los documentos ingresados con:

- ID del documento
- Título
- Source
- Número de chunks generados
- Estado

### Paso 4: Eliminar un documento (Opcional)

1. Copia el `id` de un documento del paso anterior
2. Ve a **Variables** en la colección
3. Pega el ID en la variable `document_id`
4. Ejecuta: `DELETE {{base_url}}/api/v1/delete/{{document_id}}`

## 📊 Ejemplos de Respuestas

### Ingesta Exitosa

```json
{
  "id": "doc_123456",
  "title": "Manual de Usuario - TuDescuento",
  "source": "manual_usuario_v1.pdf",
  "chunks_count": 15,
  "status": "ingested"
}
```

### Lista de Documentos

```json
[
  {
    "id": "doc_123456",
    "title": "Manual de Usuario - TuDescuento",
    "source": "manual_usuario_v1.pdf",
    "chunks_count": 15,
    "status": "stored"
  },
  {
    "id": "doc_789012",
    "title": "Preguntas Frecuentes - TuDescuento",
    "source": "faq_tudescuento.txt",
    "chunks_count": 8,
    "status": "stored"
  }
]
```

### Eliminación Exitosa

```json
{
  "id": "doc_123456",
  "status": "deleted",
  "message": "Documento doc_123456 eliminado correctamente"
}
```

## 🛠️ Personalización

### Crear tu propio documento

Modifica el body de cualquier request POST para ingestar tu propio contenido:

```json
{
  "title": "Tu Título",
  "content": "Tu contenido aquí...",
  "source": "nombre_archivo.ext",
  "metadata": {
    "author": "Tu nombre",
    "category": "categoría",
    "custom_field": "valor personalizado"
  }
}
```

## 🐛 Troubleshooting

### Error: Connection Refused

- Verifica que la API esté corriendo: `uvicorn app.main:app --reload`
- Confirma que el puerto es el correcto (8000 por defecto)

### Error: ChromaDB Connection

- Asegúrate de que ChromaDB esté corriendo
- Verifica las variables de entorno en `.env`

### Error 500: Internal Server Error

- Revisa los logs de la API
- Verifica que todas las dependencias estén instaladas
- Confirma que ChromaDB esté accesible

## 📚 Recursos Adicionales

### Documentación Interactiva

Una vez que la API esté corriendo, visita:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Modificar Configuración

Edita el archivo `.env` para cambiar:

- Host y puerto de ChromaDB
- Modelo de embeddings
- Tamaño de chunks
- Overlap de chunks

## 💡 Tips

1. **Usa el entorno de desarrollo** para tener las variables pre-configuradas
2. **Guarda las respuestas** como ejemplos en Postman para referencia futura
3. **Crea tests automáticos** en la pestaña "Tests" de cada request
4. **Agrupa requests relacionados** en carpetas para mejor organización
5. **Usa variables de entorno** para diferentes ambientes (dev, staging, prod)

## 📧 Soporte

Si encuentras problemas o tienes sugerencias, contacta al equipo de desarrollo.

---

**Última actualización**: 25 de Octubre de 2025  
**Versión de la API**: 1.0.0
