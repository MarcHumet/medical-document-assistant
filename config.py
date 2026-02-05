"""
Configuration management for the Medical Document Assistant.
"""
import os
from pathlib import Path
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    """Application settings."""
    
    # LLM Configuration
    use_ollama: bool = os.getenv("USE_OLLAMA", "false").lower() == "true"
    
    # OpenAI Configuration
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    
    # Ollama Configuration
    ollama_base_url: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    ollama_model: str = os.getenv("OLLAMA_MODEL", "llama2")
    
    # Embedding Configuration
    use_ollama_embeddings: bool = os.getenv("USE_OLLAMA_EMBEDDINGS", "false").lower() == "true"
    ollama_embedding_model: str = os.getenv("OLLAMA_EMBEDDING_MODEL", "nomic-embed-text")
    
    # API Security
    api_secret_key: str = os.getenv("API_SECRET_KEY", "dev-secret-key-change-in-production")
    api_algorithm: str = os.getenv("API_ALGORITHM", "HS256")
    access_token_expire_minutes: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    
    # Application
    upload_dir: Path = Path(os.getenv("UPLOAD_DIR", "uploads"))
    max_file_size_mb: int = int(os.getenv("MAX_FILE_SIZE_MB", "10"))
    
    # Demo credentials
    demo_username: str = os.getenv("DEMO_USERNAME", "medical_researcher")
    demo_password: str = os.getenv("DEMO_PASSWORD", "demo_password_123")
    
    class Config:
        env_file = ".env"
        extra = "ignore"  # Ignore extra fields in .env


settings = Settings()

# Create upload directory if it doesn't exist
settings.upload_dir.mkdir(exist_ok=True)
