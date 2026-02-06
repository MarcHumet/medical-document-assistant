"""
Question-Answering chain implementation for medical documents.
"""
import logging
from typing import List, Dict, Any
from langchain_core.documents import Document

logger = logging.getLogger(__name__)


class QAChain:
    """Simple Question-Answering chain for medical documents."""
    
    def __init__(self, llm):
        """Initialize the QA chain."""
        self.llm = llm
        self.retriever = None
        logger.info("Initialized simple QA chain")
    
    def create_qa_chain(self, retriever) -> None:
        """Set the retriever for the QA chain."""
        self.retriever = retriever
        logger.info("Set retriever for QA chain")
    
    def _get_qa_prompt(self, context: str, question: str) -> str:
        """Get the QA prompt template with best practices."""
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
        
        return template.format(context=context, question=question)
    
    def answer_question(self, question: str) -> Dict[str, Any]:
        """Answer a question based on processed documents."""
        if not self.retriever:
            raise ValueError("QA chain not initialized. Please create the chain first.")
        
        try:
            # Get relevant documents
            relevant_docs = self.retriever.get_relevant_documents(question)
            
            # Prepare context
            context = "\n\n".join([doc.page_content for doc in relevant_docs])
            
            # Create prompt
            prompt = self._get_qa_prompt(context, question)
            
            # Get answer from LLM
            answer = self.llm.invoke(prompt)
            
            # Extract source information
            sources = []
            for doc in relevant_docs:
                sources.append({
                    "source": doc.metadata.get("source", "Unknown"),
                    "chunk": doc.metadata.get("chunk", 0),
                    "content": doc.page_content[:200] + "..." if len(doc.page_content) > 200 else doc.page_content
                })
            
            logger.info(f"Answered question: {question[:50]}...")
            
            return {
                "answer": answer,
                "sources": sources,
                "question": question
            }
        except Exception as e:
            logger.error(f"Error answering question: {e}")
            raise