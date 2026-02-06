"""
MCP resources implementation for medical document management.
"""
import json
from pathlib import Path
from typing import List

import mcp.types as types

from src.document_processor import DocumentProcessor
from config import settings


class DocumentResources:
    """Handles MCP resources for document management."""
    
    def __init__(self, doc_processor: DocumentProcessor):
        """Initialize with document processor."""
        self.doc_processor = doc_processor
    
    async def list_resources(self) -> List[types.Resource]:
        """Return list of available resources."""
        resources = [
            types.Resource(
                uri="medical-docs://uploaded-documents",
                name="Uploaded Documents",
                description="List of all uploaded medical documents",
                mimeType="application/json"
            ),
            types.Resource(
                uri="medical-docs://vector-store-info",
                name="Vector Store Information", 
                description="Information about the current vector store status",
                mimeType="application/json"
            ),
            types.Resource(
                uri="medical-docs://system-status",
                name="System Status",
                description="Current system configuration and status",
                mimeType="application/json"
            )
        ]
        
        # Add individual document resources
        try:
            uploaded_files = list(settings.upload_dir.glob("*"))
            for file_path in uploaded_files:
                if file_path.is_file() and file_path.suffix.lower() in ['.pdf', '.txt', '.text']:
                    resources.append(
                        types.Resource(
                            uri=f"medical-docs://document/{file_path.name}",
                            name=f"Document: {file_path.name}",
                            description=f"Individual medical document: {file_path.name}",
                            mimeType="text/plain" if file_path.suffix.lower() in ['.txt', '.text'] else "application/pdf"
                        )
                    )
        except Exception:
            pass  # If upload directory doesn't exist, skip individual documents
        
        return resources
    
    async def read_resource(self, uri: str) -> str:
        """Read a specific resource."""
        try:
            if uri == "medical-docs://uploaded-documents":
                return await self._get_uploaded_documents()
            elif uri == "medical-docs://vector-store-info":
                return await self._get_vector_store_info()
            elif uri == "medical-docs://system-status":
                return await self._get_system_status()
            elif uri.startswith("medical-docs://document/"):
                filename = uri.replace("medical-docs://document/", "")
                return await self._get_document_content(filename)
            else:
                return json.dumps({"error": f"Unknown resource URI: {uri}"})
        except Exception as e:
            return json.dumps({"error": f"Error reading resource: {str(e)}"})
    
    async def _get_uploaded_documents(self) -> str:
        """Get list of uploaded documents."""
        try:
            documents = []
            if settings.upload_dir.exists():
                for file_path in settings.upload_dir.glob("*"):
                    if file_path.is_file() and file_path.suffix.lower() in ['.pdf', '.txt', '.text']:
                        stat = file_path.stat()
                        documents.append({
                            "filename": file_path.name,
                            "size_bytes": stat.st_size,
                            "size_human": self._format_size(stat.st_size),
                            "modified": stat.st_mtime,
                            "type": file_path.suffix.lower(),
                            "uri": f"medical-docs://document/{file_path.name}"
                        })
            
            result = {
                "document_count": len(documents),
                "upload_directory": str(settings.upload_dir),
                "documents": documents
            }
            
            return json.dumps(result, indent=2)
        except Exception as e:
            return json.dumps({"error": f"Error listing documents: {str(e)}"})
    
    async def _get_vector_store_info(self) -> str:
        """Get vector store information."""
        try:
            info = {
                "vector_store_type": "ChromaDB",
                "status": "unknown"
            }
            
            # Try to get vector store info
            if hasattr(self.doc_processor, 'vector_store') and self.doc_processor.vector_store:
                try:
                    if hasattr(self.doc_processor.vector_store, 'get_collection_info'):
                        collection_info = self.doc_processor.vector_store.get_collection_info()
                        info.update(collection_info)
                        info["status"] = "active"
                    elif hasattr(self.doc_processor.vector_store, 'documents'):
                        info["document_count"] = len(self.doc_processor.vector_store.documents)
                        info["status"] = "active"
                    else:
                        info["status"] = "initialized"
                except:
                    info["status"] = "error"
            else:
                info["status"] = "not_initialized"
            
            return json.dumps(info, indent=2)
        except Exception as e:
            return json.dumps({"error": f"Error getting vector store info: {str(e)}"})
    
    async def _get_system_status(self) -> str:
        """Get system status information."""
        try:
            status = {
                "llm_provider": settings.use_ollama and "ollama" or "openai",
                "embeddings_provider": settings.use_ollama_embeddings and "ollama" or "openai",
                "configuration": {
                    "openai_configured": bool(settings.openai_api_key),
                    "ollama_base_url": settings.ollama_base_url if settings.use_ollama else None,
                    "ollama_model": settings.ollama_model if settings.use_ollama else None,
                    "upload_dir": str(settings.upload_dir),
                    "max_file_size_mb": settings.max_file_size_mb
                },
                "capabilities": {
                    "document_formats": ["PDF", "TXT"],
                    "llm_providers": ["OpenAI", "Ollama"],
                    "vector_store": "ChromaDB",
                    "features": [
                        "Document upload and processing",
                        "Question answering (RAG)",
                        "Document search",
                        "Medical entity extraction",
                        "Document summarization"
                    ]
                }
            }
            
            return json.dumps(status, indent=2)
        except Exception as e:
            return json.dumps({"error": f"Error getting system status: {str(e)}"})
    
    async def _get_document_content(self, filename: str) -> str:
        """Get content of a specific document."""
        try:
            file_path = settings.upload_dir / filename
            
            if not file_path.exists():
                return json.dumps({"error": f"Document not found: {filename}"})
            
            if not file_path.is_file():
                return json.dumps({"error": f"Not a file: {filename}"})
            
            if file_path.suffix.lower() in ['.txt', '.text']:
                # Return text content directly
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                result = {
                    "filename": filename,
                    "type": "text",
                    "content": content[:10000] + "..." if len(content) > 10000 else content,
                    "size": len(content),
                    "truncated": len(content) > 10000
                }
                
                return json.dumps(result, indent=2)
            
            elif file_path.suffix.lower() == '.pdf':
                # For PDF, return metadata and first page text
                from src.document_digestion.processor import DocumentProcessor as DocProcessor
                
                processor = DocProcessor()
                try:
                    full_text = processor.extract_text_from_pdf(file_path)
                    preview = full_text[:2000] + "..." if len(full_text) > 2000 else full_text
                    
                    result = {
                        "filename": filename,
                        "type": "pdf",
                        "preview": preview,
                        "total_characters": len(full_text),
                        "truncated": len(full_text) > 2000
                    }
                    
                    return json.dumps(result, indent=2)
                except Exception as e:
                    return json.dumps({"error": f"Error reading PDF: {str(e)}"})
            
            else:
                return json.dumps({"error": f"Unsupported file type: {file_path.suffix}"})
                
        except Exception as e:
            return json.dumps({"error": f"Error reading document: {str(e)}"})
    
    def _format_size(self, bytes_size: int) -> str:
        """Format file size in human readable format."""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if bytes_size < 1024.0:
                return f"{bytes_size:.1f}{unit}"
            bytes_size /= 1024.0
        return f"{bytes_size:.1f}TB"