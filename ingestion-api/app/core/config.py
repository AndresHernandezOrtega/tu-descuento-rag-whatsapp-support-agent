"""
Configuración central de la aplicación
Carga variables de entorno y configuraciones generales
"""
from pydantic_settings import BaseSettings
from typing import Optional



class Settings(BaseSettings):
    """
    Configuración de la aplicación usando Pydantic Settings
    """
    # API Settings
    app_name: str = "Ingestion API"
    app_version: str = "1.0.0"
    debug: bool = False
    
    # ChromaDB Settings
    chroma_host: str = "chroma"
    chroma_port: int = 8000
    chroma_collection_name: str = "documents"
    
    # Embedding Settings
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    
    # Document Processing
    chunk_size: int = 1000
    chunk_overlap: int = 200
    
    # CORS Settings
    cors_origins: list = ["*"]
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Instancia global de configuración
settings = Settings()
