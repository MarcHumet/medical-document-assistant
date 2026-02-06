"""
Integrated document processor combining all modules.
"""
import os
import sys
from pathlib import Path
from typing import List
from loguru import logger

from src.document_digestion import DocumentProcessor as DocProcessor
from src.llm import ChatLLM, QAChain
from src.vector_store import ChromaVectorStore, EmbeddingsManager
from config import settings

# Configure loguru
logger.remove()  # Remove default handler
logger.add(
    "./logs/document_processor.log",
    rotation="500 MB",
    retention="6 months",
    level="DEBUG",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}"
)
logger.add(sys.stdout, level="INFO")


class DocumentProcessor:
    """Main document processor that orchestrates all components."""
    
    def __init__(self):
        """Initialize the integrated document processor."""
        logger.info("Starting DocumentProcessor initialization")
        
        # Initialize components
        try:
            logger.debug("Initializing DocProcessor")
            self.doc_processor = DocProcessor()
            logger.success("DocProcessor initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize DocProcessor: {e}")
            raise
        
        # Initialize LLM and embeddings using unified approach
        provider = os.getenv("LLM_PROVIDER", "ollama")
        logger.info(f"Using {provider} for LLM and embeddings")
        
        try:
            logger.debug("Initializing ChatLLM")
            self.chat_llm = ChatLLM()
            logger.success("ChatLLM initialized successfully")
        except Exception as e:
            logger.critical(f"Failed to initialize ChatLLM: {e}")
            logger.exception("ChatLLM initialization error details:")
            raise
        
        try:
            logger.debug("Initializing EmbeddingsManager")
            embeddings_manager = EmbeddingsManager()
            logger.success("EmbeddingsManager initialized successfully")
        except Exception as e:
            logger.critical(f"Failed to initialize EmbeddingsManager: {e}")
            logger.exception("EmbeddingsManager initialization error details:")
            raise
        
        try:
            logger.debug("Initializing ChromaVectorStore")
            self.vector_store = ChromaVectorStore(embeddings_manager)
            logger.success("ChromaVectorStore initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize ChromaVectorStore: {e}")
            raise
        
        try:
            logger.debug("Initializing QAChain")
            self.qa_chain = QAChain(self.chat_llm)
            logger.success("QAChain initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize QAChain: {e}")
            raise
        
        logger.success("DocumentProcessor initialization completed successfully")
    
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