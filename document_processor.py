"""
Document processing utilities for handling PDFs and text files.
"""
import logging
from pathlib import Path
from typing import List
import PyPDF2
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.schema import Document

from config import settings

logger = logging.getLogger(__name__)


class DocumentProcessor:
    """Handles document processing and question-answering."""
    
    def __init__(self):
        """Initialize the document processor."""
        self.embeddings = OpenAIEmbeddings(openai_api_key=settings.openai_api_key)
        self.llm = ChatOpenAI(
            model_name="gpt-3.5-turbo",
            temperature=0,
            openai_api_key=settings.openai_api_key
        )
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )
        self.vectorstore = None
        self.qa_chain = None
    
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
    
    def create_vectorstore(self, documents: List[Document]) -> None:
        """Create a vector store from documents."""
        try:
            self.vectorstore = Chroma.from_documents(
                documents=documents,
                embedding=self.embeddings,
                collection_name="medical_docs"
            )
            
            # Create QA chain with good prompting practices
            self.qa_chain = RetrievalQA.from_chain_type(
                llm=self.llm,
                chain_type="stuff",
                retriever=self.vectorstore.as_retriever(
                    search_type="similarity",
                    search_kwargs={"k": 3}
                ),
                return_source_documents=True,
                chain_type_kwargs={
                    "prompt": self._get_qa_prompt()
                }
            )
            logger.info(f"Created vector store with {len(documents)} documents")
        except Exception as e:
            logger.error(f"Error creating vector store: {e}")
            raise
    
    def _get_qa_prompt(self):
        """Get the QA prompt template with best practices."""
        from langchain.prompts import PromptTemplate
        
        template = """You are a medical research assistant helping researchers understand clinical and medical documents.

Use the following pieces of context from medical documents to answer the question at the end.

Guidelines:
1. Be precise and cite specific information from the context when possible
2. If you're unsure or the context doesn't contain enough information, clearly state that
3. Use medical terminology accurately
4. Provide relevant context and explanations when needed
5. If the question asks about something not in the context, say "I don't have information about that in the provided documents"

Context:
{context}

Question: {question}

Answer: """
        
        return PromptTemplate(
            template=template,
            input_variables=["context", "question"]
        )
    
    def answer_question(self, question: str) -> dict:
        """Answer a question based on processed documents."""
        if not self.qa_chain:
            raise ValueError("No documents have been processed yet. Please upload documents first.")
        
        try:
            result = self.qa_chain({"query": question})
            
            # Extract source information
            sources = []
            for doc in result.get("source_documents", []):
                sources.append({
                    "source": doc.metadata.get("source", "Unknown"),
                    "chunk": doc.metadata.get("chunk", 0),
                    "content": doc.page_content[:200] + "..." if len(doc.page_content) > 200 else doc.page_content
                })
            
            logger.info(f"Answered question: {question[:50]}...")
            
            return {
                "answer": result["result"],
                "sources": sources,
                "question": question
            }
        except Exception as e:
            logger.error(f"Error answering question: {e}")
            raise
    
    def add_documents(self, documents: List[Document]) -> None:
        """Add more documents to existing vectorstore."""
        if self.vectorstore:
            self.vectorstore.add_documents(documents)
            logger.info(f"Added {len(documents)} more documents to vector store")
        else:
            self.create_vectorstore(documents)
