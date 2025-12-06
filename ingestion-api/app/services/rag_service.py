"""
Servicio RAG para gestionar la ingesta de documentos
Implementa: Cargar -> Dividir -> Vectorizar -> Almacenar
"""
from typing import List, Dict, Any, Optional
import uuid
import chromadb

from app.core.config import settings
from app.schemas.document import DocumentCreate, DocumentResponse


class RAGService:
    """
    Servicio para gestionar la ingesta y procesamiento de documentos
    """
    
    def __init__(self):
        self.settings = settings
        self._embedding_model: Optional[Any] = None
        self._initialize_chroma()
    
    def _initialize_chroma(self):
        """Inicializa la conexión con ChromaDB"""
        print("Conectando a ChromaDB...")
        print(f"Host: {self.settings.chroma_host}, Port: {self.settings.chroma_port}")
        self.chroma_client = chromadb.HttpClient(
            host=self.settings.chroma_host,
            port=self.settings.chroma_port
        )
        
    def _get_embedding_model(self):
        """Lazy loading del modelo de embeddings"""
        if self._embedding_model is None:
            print(f"Cargando modelo de embeddings: {self.settings.embedding_model}")
            try:
                from sentence_transformers import SentenceTransformer
                self._embedding_model = SentenceTransformer(self.settings.embedding_model)
                print("Modelo de embeddings cargado exitosamente")
            except Exception as e:
                print(f"Error al cargar modelo de embeddings: {e}")
                raise
        return self._embedding_model
    
    def _split_text(self, text: str, chunk_size: int, chunk_overlap: int) -> List[str]:
        """
        Divide el texto en chunks con overlap
        """
        chunks = []
        start = 0
        text_length = len(text)
        
        while start < text_length:
            end = start + chunk_size
            chunk = text[start:end]
            
            # Si no es el último chunk y hay más texto, intenta cortar en un espacio
            if end < text_length:
                last_space = chunk.rfind(' ')
                if last_space > chunk_size // 2:  # Solo ajusta si el espacio está en la segunda mitad
                    end = start + last_space + 1
                    chunk = text[start:end]
            
            chunks.append(chunk.strip())
            start = end - chunk_overlap if end < text_length else end
        
        return chunks
    
    async def ingest_document(self, document: DocumentCreate) -> DocumentResponse:
        """
        Ingesta un documento completo:
        1. Cargar el contenido
        2. Dividir en chunks
        3. Vectorizar
        4. Almacenar en ChromaDB
        """
        # Dividir el contenido en chunks
        text_chunks = self._split_text(
            document.content,
            self.settings.chunk_size,
            self.settings.chunk_overlap
        )
        
        print(f"Documento dividido en {len(text_chunks)} chunks")
        
        # Obtener el modelo de embeddings (lazy loading)
        embedding_model = self._get_embedding_model()
        
        # Generar embeddings para cada chunk
        embeddings = embedding_model.encode(text_chunks).tolist()
        
        # Generar IDs únicos para cada chunk
        document_id = str(uuid.uuid4())
        chunk_ids = [f"{document_id}_chunk_{i}" for i in range(len(text_chunks))]
        
        # Preparar metadata para cada chunk
        metadatas = []
        for i in range(len(text_chunks)):
            metadata = {
                "source": document.source,
                "title": document.title,
                "document_id": document_id,
                "chunk_index": i,
                "total_chunks": len(text_chunks),
                **document.metadata
            }
            metadatas.append(metadata)
        
        # Obtener o crear la colección
        try:
            collection = self.chroma_client.get_or_create_collection(
                name=self.settings.chroma_collection_name
            )
        except Exception as e:
            print(f"Error al obtener/crear colección: {e}")
            raise
        
        # Almacenar en ChromaDB
        collection.add(
            ids=chunk_ids,
            embeddings=embeddings,
            documents=text_chunks,
            metadatas=metadatas
        )
        
        print(f"Documento {document_id} ingresado exitosamente")
        
        return DocumentResponse(
            id=document_id,
            title=document.title,
            source=document.source,
            chunks_count=len(text_chunks),
            status="ingested"
        )
    
    async def delete_document(self, document_id: str) -> Dict[str, Any]:
        """
        Elimina un documento y todos sus chunks de ChromaDB
        """
        try:
            collection = self.chroma_client.get_collection(
                name=self.settings.chroma_collection_name
            )
            
            # Obtener todos los chunks del documento
            results = collection.get(
                where={"document_id": document_id}
            )
            
            if not results['ids']:
                return {
                    "id": document_id,
                    "status": "not_found",
                    "message": f"Documento {document_id} no encontrado"
                }
            
            # Eliminar todos los chunks del documento
            collection.delete(ids=results['ids'])
            
            print(f"Documento {document_id} eliminado ({len(results['ids'])} chunks)")
            
            return {
                "id": document_id,
                "status": "deleted",
                "chunks_deleted": len(results['ids']),
                "message": f"Documento {document_id} eliminado correctamente"
            }
        except Exception as e:
            print(f"Error al eliminar documento: {e}")
            raise
    
    async def list_documents(self) -> List[DocumentResponse]:
        """
        Lista todos los documentos almacenados
        """
        try:
            collection = self.chroma_client.get_collection(
                name=self.settings.chroma_collection_name
            )
        except Exception:
            # Si la colección no existe, retornar lista vacía
            return []
        
        # Obtener todos los documentos
        results = collection.get()
        
        if not results['metadatas']:
            return []
        
        # Agrupar por document_id para evitar duplicados de chunks
        documents_dict = {}
        for i, metadata in enumerate(results['metadatas']):
            doc_id = metadata.get('document_id', results['ids'][i])
            
            if doc_id not in documents_dict:
                documents_dict[doc_id] = DocumentResponse(
                    id=doc_id,
                    title=metadata.get('title', 'Sin título'),
                    source=metadata.get('source', 'unknown'),
                    chunks_count=1,
                    status="stored"
                )
            else:
                documents_dict[doc_id].chunks_count += 1
        
        return list(documents_dict.values())
