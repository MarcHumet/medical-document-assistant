"""
Embeddings manager for document vectorization using OpenAI or Ollama.
"""
import os
import sys
from typing import List
from openai import OpenAI
from dotenv import load_dotenv
from loguru import logger

load_dotenv()

# Configure loguru
logger.remove()  # Remove default handler
logger.add(
    "./logs/embeddings.log",
    rotation="500 MB",
    retention="6 months",
    level="DEBUG",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}"
)
logger.add(sys.stdout, level="INFO")

def get_embeddings_client():
    """Get embeddings client based on provider configuration."""
    provider = os.getenv("LLM_PROVIDER", "ollama")
    logger.info(f"Initializing embeddings client with provider: {provider}")
    
    try:
        if provider == "openai":
            api_key = os.getenv("OPENAI_API_KEY")
            logger.debug(f"Using OpenAI embeddings with API key: {'***' if api_key else 'None'}")
            
            client = OpenAI(api_key=api_key)
            logger.success("OpenAI embeddings client initialized successfully")
            return client
        else:
            # Configuration for Ollama
            endpoint = os.getenv("LLM_ENDPOINT", "http://localhost:11434/v1")
            api_key = os.getenv("OPENAI_API_KEY", "ollama")
            
            logger.debug(f"Using Ollama embeddings endpoint: {endpoint}")
            logger.debug(f"Using API key: {'***' if api_key != 'ollama' else 'ollama'}")
            
            client = OpenAI(
                base_url=endpoint,
                api_key=api_key
            )
            logger.success(f"Ollama embeddings client initialized successfully at {endpoint}")
            return client
            
    except Exception as e:
        logger.error(f"Failed to initialize embeddings client: {e}")
        logger.exception("Full exception details:")
        raise

class EmbeddingsManager:
    """Manages document embeddings using OpenAI or Ollama."""
    
    def __init__(self, model: str = None):
        """Initialize embeddings manager."""
        logger.info("Initializing EmbeddingsManager")
        
        self.provider = os.getenv("LLM_PROVIDER", "ollama")
        logger.debug(f"Provider: {self.provider}")
        
        if model:
            self.model = model
            logger.debug(f"Using provided model: {model}")
        else:
            # Set default model based on provider
            if self.provider == "openai":
                self.model = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-ada-002")
            else:
                self.model = os.getenv("OLLAMA_EMBEDDING_MODEL", "nomic-embed-text")
            logger.debug(f"Using default model for {self.provider}: {self.model}")
        
        try:
            logger.info(f"Attempting to create {self.provider} embeddings client...")
            self.client = get_embeddings_client()
            logger.success(f"EmbeddingsManager initialized successfully with {self.provider} provider using model: {self.model}")
        except Exception as e:
            logger.critical(f"Failed to initialize EmbeddingsManager: {e}")
            raise
    
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Embed a list of documents."""
        try:
            response = self.client.embeddings.create(
                model=self.model,
                input=texts
            )
            return [embedding.embedding for embedding in response.data]
        except Exception as e:
            logger.error(f"Error embedding documents: {e}")
            raise
    
    def embed_query(self, text: str) -> List[float]:
        """Embed a single query."""
        try:
            response = self.client.embeddings.create(
                model=self.model,
                input=[text]
            )
            return response.data[0].embedding
        except Exception as e:
            logger.error(f"Error embedding query: {e}")
            raise