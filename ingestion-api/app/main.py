"""
Punto de entrada principal de la aplicación FastAPI
Ingestion API para gestión de documentos en ChromaDB
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api.v1.endpoints import ingestion

# Crear instancia de FastAPI
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="API para la ingesta y gestión de documentos en ChromaDB",
    debug=settings.debug
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(
    ingestion.router,
    prefix="/api/v1",
    tags=["ingestion"]
)


@app.get("/")
async def root():
    """
    Endpoint raíz de bienvenida
    """
    return {
        "message": f"Bienvenido a {settings.app_name}",
        "version": settings.app_version,
        "status": "running"
    }


@app.get("/health")
async def health_check():
    """
    Endpoint de health check
    """
    return {
        "status": "healthy",
        "service": settings.app_name,
        "version": settings.app_version
    }

