"""
Embeddings manager for document vectorization using OpenAI or Ollama.
"""
import logging
from typing import List
from openai import OpenAI
from langchain_openai import OpenAIEmbeddings

logger = logging.getLogger(__name__)


class EmbeddingsManager:
    """Manages document embeddings using OpenAI or Ollama."""
    
    def __init__(self, api_key: str, model: str = "text-embedding-ada-002", base_url: str = None):
        """Initialize embeddings manager."""
        if base_url:
            # Using Ollama with OpenAI-compatible API
            self.client = OpenAI(
                base_url=base_url,
                api_key="ollama"  # required but ignored
            )
            self.embeddings = OpenAIEmbeddings(
                openai_api_key="ollama",
                openai_api_base=base_url,
                model=model
            )
            logger.info(f"Initialized embeddings manager with Ollama model: {model} at {base_url}")
        else:
            # Using OpenAI
            self.client = OpenAI(api_key=api_key)
            self.embeddings = OpenAIEmbeddings(
                openai_api_key=api_key,
                model=model
            )
            logger.info(f"Initialized embeddings manager with OpenAI model: {model}")
    
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Embed a list of documents."""
        return self.embeddings.embed_documents(texts)
    
    def embed_query(self, text: str) -> List[float]:
        """Embed a single query."""
        return self.embeddings.embed_query(text)
    
    def get_embeddings(self) -> OpenAIEmbeddings:
        """Get the embeddings instance."""
        return self.embeddings