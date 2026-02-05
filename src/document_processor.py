"""
Integrated document processor combining all modules.
"""
import logging
from pathlib import Path
from typing import List

from src.document_digestion import DocumentProcessor as DocProcessor
from src.llm import ChatLLM, QAChain
from src.vector_store import ChromaVectorStore, EmbeddingsManager
from config import settings

logger = logging.getLogger(__name__)


class DocumentProcessor:
    """Main document processor that orchestrates all components."""
    
    def __init__(self):
        """Initialize the integrated document processor."""
        # Initialize components
        self.doc_processor = DocProcessor()
        
        # Determine base URLs and models
        if settings.use_ollama:
            logger.info("Using Ollama for LLM and embeddings")
            base_url = f"{settings.ollama_base_url}/v1/"
            
            self.chat_llm = ChatLLM(
                api_key=settings.openai_api_key or "ollama",
                model_name=settings.ollama_model,
                base_url=base_url
            )
            
            embedding_model = settings.ollama_embedding_model if settings.use_ollama_embeddings else "text-embedding-ada-002"
            embedding_base_url = base_url if settings.use_ollama_embeddings else None
            
            self.embeddings_manager = EmbeddingsManager(
                api_key=settings.openai_api_key or "ollama",
                model=embedding_model,
                base_url=embedding_base_url
            )
        else:
            logger.info("Using OpenAI for LLM and embeddings")
            self.chat_llm = ChatLLM(settings.openai_api_key)
            self.embeddings_manager = EmbeddingsManager(settings.openai_api_key)
        
        # Initialize vector store and QA chain
        self.vector_store = ChromaVectorStore(self.embeddings_manager.get_embeddings())
        self.qa_chain = QAChain(self.chat_llm.get_llm())
        
        logger.info("Initialized integrated document processor")
    
    def process_document(self, file_path: Path):
        """Process a document and add to vector store."""
        documents = self.doc_processor.process_document(file_path)
        self.vector_store.add_documents(documents)
        
        # Update QA chain with new retriever
        retriever = self.vector_store.as_retriever(
            search_type="similarity",
            search_kwargs={"k": 3}
        )
        self.qa_chain.create_qa_chain(retriever)
        
        return documents
    
    def answer_question(self, question: str):
        """Answer a question using the QA chain."""
        return self.qa_chain.answer_question(question)