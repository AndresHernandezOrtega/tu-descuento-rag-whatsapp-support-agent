"""
Esquemas Pydantic para validación de documentos
"""
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List


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


class QueryRequest(BaseModel):
    """
    Esquema para realizar una consulta a la base de datos vectorial
    """
    query: str = Field(..., description="Texto de la consulta", min_length=1)
    n_results: int = Field(default=5, description="Número de resultados a retornar", ge=1, le=20)
    filter_metadata: Optional[Dict[str, Any]] = Field(default=None, description="Filtros de metadata opcionales")
    
    class Config:
        json_schema_extra = {
            "example": {
                "query": "¿Cómo puedo registrarme en TuDescuento?",
                "n_results": 5,
                "filter_metadata": {
                    "category": "soporte"
                }
            }
        }


class QueryResult(BaseModel):
    """
    Esquema para un resultado individual de la búsqueda
    """
    id: str = Field(..., description="ID del chunk")
    content: str = Field(..., description="Contenido del chunk")
    score: float = Field(..., description="Score de similitud (menor es más similar)")
    metadata: Dict[str, Any] = Field(..., description="Metadata del documento")
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": "doc_123456_chunk_0",
                "content": "Para registrarte en TuDescuento, sigue estos pasos...",
                "score": 0.234,
                "metadata": {
                    "title": "Manual de Usuario",
                    "source": "manual_usuario.pdf",
                    "category": "soporte"
                }
            }
        }


class QueryResponse(BaseModel):
    """
    Esquema para la respuesta de una consulta
    """
    query: str = Field(..., description="Consulta realizada")
    results: List[QueryResult] = Field(..., description="Resultados de la búsqueda")
    total_results: int = Field(..., description="Número total de resultados retornados")
    
    class Config:
        json_schema_extra = {
            "example": {
                "query": "¿Cómo puedo registrarme?",
                "results": [
                    {
                        "id": "doc_123456_chunk_0",
                        "content": "Para registrarte...",
                        "score": 0.234,
                        "metadata": {"title": "Manual", "source": "manual.pdf"}
                    }
                ],
                "total_results": 1
            }
        }
