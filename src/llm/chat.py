"""
Chat LLM implementation using OpenAI or Ollama via OpenAI-compatible API.
"""
import os
import sys
from openai import OpenAI
from dotenv import load_dotenv
from loguru import logger

load_dotenv()

# Configure loguru
logger.remove()  # Remove default handler
log_path = os.getenv("LOG_PATH", "/app/logs/chat_llm.log")
# Create directory if it doesn't exist
os.makedirs(os.path.dirname(log_path), exist_ok=True)
logger.add(
    log_path,
    rotation="500 MB",
    retention="6 months",
    level="DEBUG",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}"
)
logger.add(sys.stdout, level="INFO")

def get_llm_client():
    """Get LLM client based on provider configuration."""
    provider = os.getenv("LLM_PROVIDER", "ollama")
    logger.info(f"Initializing LLM client with provider: {provider}")
    
    try:
        if provider == "openai":
            api_key = os.getenv("OPENAI_API_KEY")
            logger.debug(f"Using OpenAI with API key: {'***' if api_key else 'None'}")
            
            client = OpenAI(api_key=api_key)
            logger.success("OpenAI client initialized successfully")
            return client
        else:
            # Configuration for Ollama
            endpoint = os.getenv("LLM_ENDPOINT", "http://localhost:11434/v1")
            api_key = os.getenv("OPENAI_API_KEY", "ollama")
            
            logger.debug(f"Using Ollama endpoint: {endpoint}")
            logger.debug(f"Using API key: {'***' if api_key != 'ollama' else 'ollama'}")
            
            client = OpenAI(
                base_url=endpoint,
                api_key=api_key
            )
            logger.success(f"Ollama client initialized successfully at {endpoint}")
            return client
            
    except Exception as e:
        logger.error(f"Failed to initialize LLM client: {e}")
        logger.exception("Full exception details:")
        raise

class ChatLLM:
    """Chat LLM wrapper for OpenAI or Ollama."""
    
    def __init__(self, model_name: str = None, temperature: float = 0.7):
        """Initialize the chat LLM."""
        logger.info("Initializing ChatLLM")
        
        self.provider = os.getenv("LLM_PROVIDER", "ollama")
        self.temperature = temperature
        
        logger.debug(f"Provider: {self.provider}, Temperature: {temperature}")
        
        if model_name:
            self.model_name = model_name
            logger.debug(f"Using provided model: {model_name}")
        else:
            # Set default model based on provider
            if self.provider == "openai":
                self.model_name = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
            else:
                self.model_name = os.getenv("OLLAMA_MODEL", "llama3.2:1b")
            logger.debug(f"Using default model for {self.provider}: {self.model_name}")
        
        try:
            logger.info(f"Attempting to create {self.provider} client...")
            self.client = get_llm_client()
            logger.success(f"ChatLLM initialized successfully with {self.provider} provider using model: {self.model_name}")
        except Exception as e:
            logger.critical(f"Failed to initialize ChatLLM: {e}")
            raise
    
    def invoke(self, prompt: str) -> str:
        """Invoke the LLM with a prompt."""
        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[{"role": "user", "content": prompt}],
                temperature=self.temperature
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Error invoking LLM: {e}")
            raise