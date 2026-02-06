"""
Document processing utilities for handling PDFs and text files.
"""
import logging
from pathlib import Path
from typing import List
import PyPDF2
from langchain_core.documents import Document

logger = logging.getLogger(__name__)


class SimpleTextSplitter:
    """Simple text splitter that mimics RecursiveCharacterTextSplitter."""
    
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
    
    def split_text(self, text: str) -> List[str]:
        """Split text into chunks."""
        chunks = []
        start = 0
        
        while start < len(text):
            end = start + self.chunk_size
            chunk = text[start:end]
            chunks.append(chunk)
            
            # Move start position accounting for overlap
            start = end - self.chunk_overlap
            if start >= len(text):
                break
        
        return chunks


class DocumentProcessor:
    """Handles document text extraction and chunking."""
    
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        """Initialize the document processor."""
        self.text_splitter = SimpleTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )
    
    def extract_text_from_pdf(self, file_path: Path) -> str:
        """Extract text from a PDF file."""
        try:
            text = ""
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
            logger.info(f"Extracted {len(text)} characters from PDF: {file_path.name}")
            return text
        except Exception as e:
            logger.error(f"Error extracting text from PDF {file_path}: {e}")
            raise
    
    def extract_text_from_txt(self, file_path: Path) -> str:
        """Extract text from a text file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()
            logger.info(f"Extracted {len(text)} characters from text file: {file_path.name}")
            return text
        except Exception as e:
            logger.error(f"Error reading text file {file_path}: {e}")
            raise
    
    def process_document(self, file_path: Path) -> List[Document]:
        """Process a document and create text chunks."""
        # Extract text based on file type
        if file_path.suffix.lower() == '.pdf':
            text = self.extract_text_from_pdf(file_path)
        elif file_path.suffix.lower() in ['.txt', '.text']:
            text = self.extract_text_from_txt(file_path)
        else:
            raise ValueError(f"Unsupported file type: {file_path.suffix}")
        
        # Split text into chunks
        chunks = self.text_splitter.split_text(text)
        
        # Create Document objects
        documents = [
            Document(
                page_content=chunk,
                metadata={"source": file_path.name, "chunk": i}
            )
            for i, chunk in enumerate(chunks)
        ]
        
        logger.info(f"Created {len(documents)} chunks from {file_path.name}")
        return documents