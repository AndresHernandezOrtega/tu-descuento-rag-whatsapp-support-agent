"""
Endpoints para la gestión de ingesta de documentos
"""
from fastapi import APIRouter, HTTPException, status
from typing import List

from app.schemas.document import DocumentCreate, DocumentResponse, DocumentDelete
from app.services.rag_service import RAGService

router = APIRouter()
rag_service = RAGService()


@router.post("/ingest", response_model=DocumentResponse, status_code=status.HTTP_201_CREATED)
async def ingest_document(document: DocumentCreate):
    """
    Ingesta un nuevo documento en ChromaDB
    """
    try:
        result = await rag_service.ingest_document(document)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al ingestar documento: {str(e)}"
        )


@router.delete("/delete/{document_id}", response_model=dict)
async def delete_document(document_id: str):
    """
    Elimina un documento de ChromaDB
    """
    try:
        result = await rag_service.delete_document(document_id)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar documento: {str(e)}"
        )


@router.get("/documents", response_model=List[DocumentResponse])
async def list_documents():
    """
    Lista todos los documentos ingresados
    """
    try:
        documents = await rag_service.list_documents()
        return documents
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al listar documentos: {str(e)}"
        )
