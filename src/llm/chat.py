"""
Chat LLM implementation using OpenAI or Ollama via OpenAI-compatible API.
"""
import logging
from openai import OpenAI
from langchain_openai import ChatOpenAI

logger = logging.getLogger(__name__)


class ChatLLM:
    """Chat LLM wrapper for OpenAI or Ollama."""
    
    def __init__(self, api_key: str, model_name: str = "gpt-3.5-turbo", temperature: float = 0, base_url: str = None):
        """Initialize the chat LLM."""
        if base_url:
            # Using Ollama with OpenAI-compatible API
            self.client = OpenAI(
                base_url=base_url,
                api_key="ollama"  # required but ignored
            )
            self.llm = ChatOpenAI(
                model_name=model_name,
                temperature=temperature,
                openai_api_key="ollama",
                openai_api_base=base_url
            )
            logger.info(f"Initialized ChatLLM with Ollama model: {model_name} at {base_url}")
        else:
            # Using OpenAI
            self.client = OpenAI(api_key=api_key)
            self.llm = ChatOpenAI(
                model_name=model_name,
                temperature=temperature,
                openai_api_key=api_key
            )
            logger.info(f"Initialized ChatLLM with OpenAI model: {model_name}")
    
    def get_llm(self) -> ChatOpenAI:
        """Get the LLM instance."""
        return self.llm
    
    def invoke(self, prompt: str) -> str:
        """Invoke the LLM with a prompt."""
        response = self.client.chat.completions.create(
            model=self.llm.model_name,
            messages=[{"role": "user", "content": prompt}],
            temperature=self.llm.temperature
        )
        return response.choices[0].message.content