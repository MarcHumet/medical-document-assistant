"""
Vector store module for document embeddings and similarity search.
"""
from .chroma_store import ChromaVectorStore
from .embeddings import EmbeddingsManager

__all__ = ["ChromaVectorStore", "EmbeddingsManager"]