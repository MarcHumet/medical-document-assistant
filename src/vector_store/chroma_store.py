"""
Simple vector store implementation using basic similarity search.
"""
import logging
from typing import List, Optional, Dict, Any
import numpy as np
from langchain_core.documents import Document

logger = logging.getLogger(__name__)


class ChromaVectorStore:
    """Simple vector store implementation without ChromaDB dependency."""
    
    def __init__(self, embeddings_manager, collection_name: str = "medical_docs"):
        """Initialize the vector store."""
        self.embeddings = embeddings_manager
        self.collection_name = collection_name
        self.documents: List[Document] = []
        self.document_embeddings: List[List[float]] = []
        logger.info(f"Initialized simple vector store with collection: {collection_name}")
    
    def create_vectorstore(self, documents: List[Document]) -> None:
        """Create a vector store from documents."""
        try:
            self.documents = documents
            # Create embeddings for all documents
            texts = [doc.page_content for doc in documents]
            self.document_embeddings = self.embeddings.embed_documents(texts)
            logger.info(f"Created vector store with {len(documents)} documents")
        except Exception as e:
            logger.error(f"Error creating vector store: {e}")
            raise
    
    def add_documents(self, documents: List[Document]) -> None:
        """Add more documents to existing vectorstore."""
        if self.documents:
            texts = [doc.page_content for doc in documents]
            new_embeddings = self.embeddings.embed_documents(texts)
            self.documents.extend(documents)
            self.document_embeddings.extend(new_embeddings)
            logger.info(f"Added {len(documents)} more documents to vector store")
        else:
            self.create_vectorstore(documents)
    
    def similarity_search(self, query: str, k: int = 3) -> List[Document]:
        """Search for similar documents using cosine similarity."""
        if not self.documents:
            raise ValueError("Vector store not initialized. Please add documents first.")
        
        try:
            # Get query embedding
            query_embedding = self.embeddings.embed_query(query)
            
            # Calculate similarities
            similarities = []
            for doc_embedding in self.document_embeddings:
                similarity = self._cosine_similarity(query_embedding, doc_embedding)
                similarities.append(similarity)
            
            # Get top k most similar documents
            top_indices = np.argsort(similarities)[-k:][::-1]
            
            return [self.documents[i] for i in top_indices]
        
        except Exception as e:
            logger.error(f"Error in similarity search: {e}")
            raise
    
    def _cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """Calculate cosine similarity between two vectors."""
        vec1_np = np.array(vec1)
        vec2_np = np.array(vec2)
        
        dot_product = np.dot(vec1_np, vec2_np)
        norm1 = np.linalg.norm(vec1_np)
        norm2 = np.linalg.norm(vec2_np)
        
        if norm1 == 0 or norm2 == 0:
            return 0
        
        return dot_product / (norm1 * norm2)
    
    def as_retriever(self, search_type: str = "similarity", search_kwargs: dict = None):
        """Get a retriever for the vector store."""
        if not self.documents:
            raise ValueError("Vector store not initialized. Please add documents first.")
        
        if search_kwargs is None:
            search_kwargs = {"k": 3}
            
        class SimpleRetriever:
            def __init__(self, vector_store, k=3):
                self.vector_store = vector_store
                self.k = k
            
            def get_relevant_documents(self, query: str) -> List[Document]:
                return self.vector_store.similarity_search(query, k=self.k)
            
            def invoke(self, query: str) -> List[Document]:
                return self.get_relevant_documents(query)
                
        return SimpleRetriever(self, k=search_kwargs.get("k", 3))
    
    def get_vectorstore(self):
        """Get the underlying vector store."""
        return self