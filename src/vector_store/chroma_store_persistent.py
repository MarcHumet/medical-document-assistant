"""
Persistent vector store implementation using ChromaDB.
"""
import os
from pathlib import Path
from typing import List, Optional, Dict, Any
import chromadb
from chromadb.config import Settings
from langchain_core.documents import Document
from loguru import logger

class ChromaVectorStore:
    """Persistent vector store implementation using ChromaDB."""
    
    def __init__(self, embeddings_manager, collection_name: str = "medical_docs"):
        """Initialize the persistent vector store."""
        self.embeddings = embeddings_manager
        self.collection_name = collection_name
        
        # Set up ChromaDB persistence path
        self.persist_directory = os.getenv("VECTOR_STORE_PATH", "./chroma_db")
        Path(self.persist_directory).mkdir(parents=True, exist_ok=True)
        
        logger.info(f"Initializing ChromaDB with persistence at: {self.persist_directory}")
        
        try:
            # Initialize ChromaDB with persistence
            self.client = chromadb.PersistentClient(
                path=self.persist_directory,
                settings=Settings(
                    anonymized_telemetry=False,
                    allow_reset=True
                )
            )
            
            # Get or create collection
            self.collection = self.client.get_or_create_collection(
                name=self.collection_name,
                metadata={"hnsw:space": "cosine"}
            )
            
            logger.success(f"ChromaDB collection '{self.collection_name}' initialized successfully")
            logger.info(f"Collection contains {self.collection.count()} documents")
            
        except Exception as e:
            logger.error(f"Failed to initialize ChromaDB: {e}")
            raise
    
    def create_vectorstore(self, documents: List[Document]) -> None:
        """Create a vector store from documents."""
        try:
            if not documents:
                logger.warning("No documents provided to create vector store")
                return
                
            logger.info(f"Creating vector store with {len(documents)} documents")
            
            # Prepare document data
            texts = [doc.page_content for doc in documents]
            metadatas = [doc.metadata for doc in documents]
            ids = [f"doc_{i}_{hash(doc.page_content[:100])}" for i, doc in enumerate(documents)]
            
            # Create embeddings
            logger.info("Generating embeddings...")
            embeddings = self.embeddings.embed_documents(texts)
            
            # Clear existing documents and add new ones
            existing_count = self.collection.count()
            if existing_count > 0:
                logger.info(f"Clearing {existing_count} existing documents")
                # Get all existing IDs and delete them
                results = self.collection.get()
                if results['ids']:
                    self.collection.delete(ids=results['ids'])
            
            # Add documents to ChromaDB
            logger.info("Adding documents to ChromaDB...")
            self.collection.add(
                embeddings=embeddings,
                documents=texts,
                metadatas=metadatas,
                ids=ids
            )
            
            logger.success(f"Successfully stored {len(documents)} documents in ChromaDB")
            logger.info(f"Vector store now contains {self.collection.count()} documents")
            
        except Exception as e:
            logger.error(f"Error creating vector store: {e}")
            raise
    
    def add_documents(self, documents: List[Document]) -> None:
        """Add more documents to existing vectorstore."""
        if self.collection.count() == 0:
            self.create_vectorstore(documents)
        else:
            try:
                logger.info(f"Adding {len(documents)} documents to existing vector store")
                
                # Prepare document data
                texts = [doc.page_content for doc in documents]
                metadatas = [doc.metadata for doc in documents]
                
                # Generate unique IDs for new documents
                existing_count = self.collection.count()
                ids = [f"doc_{existing_count + i}_{hash(doc.page_content[:100])}" for i, doc in enumerate(documents)]
                
                # Create embeddings
                embeddings = self.embeddings.embed_documents(texts)
                
                # Add to ChromaDB
                self.collection.add(
                    embeddings=embeddings,
                    documents=texts,
                    metadatas=metadatas,
                    ids=ids
                )
                
                logger.success(f"Added {len(documents)} documents. Total: {self.collection.count()}")
                
            except Exception as e:
                logger.error(f"Error adding documents: {e}")
                raise
    
    def similarity_search(self, query: str, k: int = 3) -> List[Document]:
        """Perform similarity search on the vector store."""
        try:
            if self.collection.count() == 0:
                raise ValueError("Vector store not initialized. Please add documents first.")
                
            logger.debug(f"Performing similarity search for: {query[:50]}...")
            
            # Create query embedding
            query_embedding = self.embeddings.embed_query(query)
            
            # Search ChromaDB
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=min(k, self.collection.count())
            )
            
            # Convert results to Document objects
            documents = []
            if results['documents'] and results['documents'][0]:
                for i, doc_text in enumerate(results['documents'][0]):
                    metadata = results['metadatas'][0][i] if results['metadatas'] and results['metadatas'][0] else {}
                    # Add distance score to metadata
                    if results['distances'] and results['distances'][0]:
                        metadata['score'] = 1 - results['distances'][0][i]  # Convert distance to similarity
                    
                    documents.append(Document(
                        page_content=doc_text,
                        metadata=metadata
                    ))
            
            logger.debug(f"Found {len(documents)} similar documents")
            return documents
            
        except Exception as e:
            logger.error(f"Error performing similarity search: {e}")
            return []
    
    def get_collection_info(self) -> Dict[str, Any]:
        """Get information about the collection."""
        try:
            count = self.collection.count()
            return {
                "collection_name": self.collection_name,
                "document_count": count,
                "persist_directory": self.persist_directory
            }
        except Exception as e:
            logger.error(f"Error getting collection info: {e}")
            return {}
    
    def delete_collection(self) -> bool:
        """Delete the entire collection."""
        try:
            self.client.delete_collection(name=self.collection_name)
            logger.info(f"Deleted collection: {self.collection_name}")
            return True
        except Exception as e:
            logger.error(f"Error deleting collection: {e}")
            return False