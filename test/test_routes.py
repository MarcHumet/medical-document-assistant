"""
Test endpoint for Ollama LLM functionality
"""
import os
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from src.llm.chat import ChatLLM
from loguru import logger

router = APIRouter()

class TestRequest(BaseModel):
    question: str = "What is the capital of France?"

class TestResponse(BaseModel):
    success: bool
    question: str
    response: str = None
    error: str = None
    provider: str
    model: str = None

@router.post("/test-llm", response_model=TestResponse)
async def test_llm(request: TestRequest):
    """Test the LLM with a simple question."""
    try:
        # Ensure we're using Ollama
        provider = os.getenv("LLM_PROVIDER", "ollama")
        
        logger.info(f"Testing LLM with provider: {provider}")
        logger.info(f"Question: {request.question}")
        
        # Initialize ChatLLM
        chat_llm = ChatLLM()
        
        # Ask the question
        logger.info("Sending question to LLM...")
        response = chat_llm.invoke(request.question)
        
        logger.success("Response received!")
        logger.info(f"Response: {response}")
        
        return TestResponse(
            success=True,
            question=request.question,
            response=response,
            provider=provider,
            model=chat_llm.model_name
        )
        
    except Exception as e:
        error_msg = str(e)
        logger.error(f"Error testing LLM: {error_msg}")
        
        return TestResponse(
            success=False,
            question=request.question,
            error=error_msg,
            provider=os.getenv("LLM_PROVIDER", "ollama")
        )

@router.get("/test-llm-simple")
async def test_llm_simple():
    """Simple GET endpoint to test LLM quickly."""
    request = TestRequest(question="What is 2 + 2?")
    return await test_llm(request)