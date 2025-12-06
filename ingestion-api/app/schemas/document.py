"""
Esquemas Pydantic para validación de documentos
"""
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any


class DocumentCreate(BaseModel):
    """
    Esquema para crear un nuevo documento
    """
    title: str = Field(..., description="Título del documento")
    content: str = Field(..., description="Contenido del documento")
    source: str = Field(..., description="Fuente o URL del documento")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Metadata adicional del documento")
    
    class Config:
        json_schema_extra = {
            "example": {
                "title": "Manual de Usuario",
                "content": "Este es el contenido del documento...",
                "source": "manual_usuario.pdf",
                "metadata": {
                    "author": "TuDescuento",
                    "category": "soporte"
                }
            }
        }


class DocumentResponse(BaseModel):
    """
    Esquema para la respuesta de un documento
    """
    id: str = Field(..., description="ID único del documento")
    title: str = Field(..., description="Título del documento")
    source: str = Field(..., description="Fuente del documento")
    chunks_count: int = Field(..., description="Número de chunks generados")
    status: str = Field(..., description="Estado del documento")
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": "doc_123456",
                "title": "Manual de Usuario",
                "source": "manual_usuario.pdf",
                "chunks_count": 15,
                "status": "ingested"
            }
        }


class DocumentDelete(BaseModel):
    """
    Esquema para eliminar un documento
    """
    id: str = Field(..., description="ID del documento a eliminar")
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": "doc_123456"
            }
        }
