# Solución al Error de ImportError con sentence-transformers

## 🔴 Problema

```
ImportError: cannot import name 'cached_download' from 'huggingface_hub'
```

Este error ocurre por incompatibilidad de versiones entre `sentence-transformers` y `huggingface_hub`.

## ✅ Solución Aplicada

### 1. Actualización de `requirements.txt`

Se especificaron versiones compatibles:

```txt
sentence-transformers>=2.2.0
transformers>=4.34.0
torch>=2.0.0
```

### 2. Lazy Loading del Modelo

El modelo de embeddings ahora se carga solo cuando se necesita (no al inicio de la app):

```python
def _get_embedding_model(self):
    """Lazy loading del modelo de embeddings"""
    if self._embedding_model is None:
        from sentence_transformers import SentenceTransformer
        self._embedding_model = SentenceTransformer(self.settings.embedding_model)
    return self._embedding_model
```

**Ventajas:**

- ✅ La API inicia más rápido
- ✅ El modelo solo se carga cuando se ingresa el primer documento
- ✅ Mejor manejo de errores
- ✅ Menos memoria usada si no se usa el servicio

## 🐳 Pasos para Aplicar los Cambios

### Si estás usando Docker Compose:

```powershell
# 1. Detener los contenedores actuales
docker-compose down

# 2. Reconstruir la imagen con las nuevas dependencias
docker-compose build --no-cache ingestion-api

# 3. Iniciar los servicios nuevamente
docker-compose up -d

# 4. Ver los logs para verificar
docker-compose logs -f ingestion-api
```

### Si estás ejecutando localmente:

```powershell
# 1. Desinstalar las versiones antiguas
pip uninstall -y sentence-transformers transformers torch

# 2. Instalar las nuevas dependencias
pip install -r requirements.txt

# 3. Ejecutar la API
uvicorn app.main:app --reload
```

## 🔍 Verificación

### 1. Verifica que la API inicie correctamente:

```powershell
curl http://localhost:8000/health
```

Debería responder:

```json
{
  "status": "healthy",
  "service": "Ingestion API",
  "version": "1.0.0"
}
```

### 2. Prueba la ingesta de un documento:

Usa Postman o curl:

```powershell
curl -X POST http://localhost:8000/api/v1/ingest `
  -H "Content-Type: application/json" `
  -d '{
    "title": "Test Document",
    "content": "Este es un documento de prueba para verificar que el modelo de embeddings funciona correctamente.",
    "source": "test.txt",
    "metadata": {}
  }'
```

### 3. Verifica en los logs:

Deberías ver:

```
Conectando a ChromaDB...
Host: chroma, Port: 8000
Cargando modelo de embeddings: sentence-transformers/all-MiniLM-L6-v2
Modelo de embeddings cargado exitosamente
Documento dividido en X chunks
Documento XXXXX ingresado exitosamente
```

## 🐛 Troubleshooting

### Error: "No module named 'sentence_transformers'"

```powershell
# Reinstalar dependencias
pip install sentence-transformers>=2.2.0
```

### Error: "Connection refused" a ChromaDB

```powershell
# Verificar que ChromaDB esté corriendo
docker-compose ps

# Si no está corriendo, iniciarlo
docker-compose up -d chromadb
```

### Error: "Out of memory" al cargar el modelo

El modelo `all-MiniLM-L6-v2` requiere ~100MB. Si tienes problemas:

**Opción 1**: Usar un modelo más pequeño en `.env`:

```env
EMBEDDING_MODEL=sentence-transformers/paraphrase-MiniLM-L3-v2
```

**Opción 2**: Aumentar memoria del contenedor en `docker-compose.yml`:

```yaml
services:
  ingestion-api:
    deploy:
      resources:
        limits:
          memory: 2G
```

## 📝 Cambios en el Código

### Antes:

```python
def __init__(self):
    self.settings = settings
    self._initialize_chroma()
    self._initialize_embeddings()  # ← Carga inmediata

def _initialize_embeddings(self):
    from sentence_transformers import SentenceTransformer
    self.embedding_model = SentenceTransformer(...)
```

### Después:

```python
def __init__(self):
    self.settings = settings
    self._embedding_model: Optional[Any] = None  # ← Variable privada
    self._initialize_chroma()  # Solo conecta a ChromaDB

def _get_embedding_model(self):  # ← Lazy loading
    if self._embedding_model is None:
        from sentence_transformers import SentenceTransformer
        self._embedding_model = SentenceTransformer(...)
    return self._embedding_model
```

## ✅ Resultado Final

- ✅ API inicia correctamente sin errores
- ✅ Modelo se carga solo cuando se necesita
- ✅ Versiones compatibles entre todas las librerías
- ✅ Mejor rendimiento y uso de memoria
- ✅ Funcionalidad completa mantenida

## 📚 Información Adicional

### Versiones Actuales Recomendadas:

- `sentence-transformers`: >= 2.2.0
- `transformers`: >= 4.34.0
- `torch`: >= 2.0.0
- `chromadb`: Latest (compatible con todas)

### Modelo de Embeddings por Defecto:

- **Nombre**: `sentence-transformers/all-MiniLM-L6-v2`
- **Tamaño**: ~100MB
- **Dimensiones**: 384
- **Rendimiento**: Excelente balance velocidad/calidad

---

**Fecha**: 26 de Octubre de 2025  
**Estado**: ✅ Resuelto
