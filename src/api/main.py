"""
FastAPI application for Medical Document Assistant.
Provides protected API endpoints for document upload and question-answering.
"""
import logging
import shutil
from datetime import timedelta
from pathlib import Path
from typing import List
from fastapi import FastAPI, File, UploadFile, Depends, HTTPException, status, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from config import settings
from src.auth import authenticate_user, create_access_token, get_current_user, Token, User
from src.document_processor import DocumentProcessor

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Medical Document Assistant API",
    description="API for uploading and querying medical documents using AI",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize document processor
doc_processor = DocumentProcessor()


# Models
class QuestionRequest(BaseModel):
    """Request model for questions."""
    question: str


class QuestionResponse(BaseModel):
    """Response model for questions."""
    answer: str
    sources: List[dict]
    question: str


class UploadResponse(BaseModel):
    """Response model for file uploads."""
    filename: str
    message: str
    chunks_created: int


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Medical Document Assistant API",
        "version": "1.0.0",
        "endpoints": {
            "auth": "/token",
            "upload": "/upload (protected)",
            "ask": "/ask (protected)",
            "health": "/health"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "llm_provider": "ollama" if settings.use_ollama else "openai",
        "embeddings_provider": "ollama" if settings.use_ollama_embeddings else "openai",
        "openai_configured": bool(settings.openai_api_key),
        "ollama_url": settings.ollama_base_url if settings.use_ollama else None
    }


@app.post("/token", response_model=Token)
async def login(username: str = Form(...), password: str = Form(...)):
    """
    Authenticate and get access token.
    
    Demo credentials (change in production):
    - username: medical_researcher
    - password: demo_password_123
    """
    logger.info(f"Login attempt for user: {username}")
    user = authenticate_user(username, password)
    if not user:
        logger.warning(f"Failed login attempt for user: {username}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    
    logger.info(f"Successful login for user: {username}")
    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/upload", response_model=UploadResponse)
async def upload_document(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user)
):
    """
    Upload and process a medical document (PDF or TXT).
    Protected endpoint - requires authentication.
    """
    logger.info(f"User {current_user.username} uploading file: {file.filename}")
    
    # Validate file type
    if not file.filename:
        raise HTTPException(status_code=400, detail="No filename provided")
    
    file_ext = Path(file.filename).suffix.lower()
    if file_ext not in ['.pdf', '.txt', '.text']:
        raise HTTPException(
            status_code=400, 
            detail=f"Unsupported file type: {file_ext}. Only PDF and TXT files are supported."
        )
    
    # Save uploaded file
    file_path = settings.upload_dir / file.filename
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        logger.info(f"Saved file: {file_path}")
    except Exception as e:
        logger.error(f"Error saving file: {e}")
        raise HTTPException(status_code=500, detail=f"Error saving file: {str(e)}")
    
    # Process document
    try:
        documents = doc_processor.process_document(file_path)
        
        logger.info(f"Processed {file.filename}: {len(documents)} chunks created")
        
        return UploadResponse(
            filename=file.filename,
            message="Document uploaded and processed successfully",
            chunks_created=len(documents)
        )
    except Exception as e:
        logger.error(f"Error processing document: {e}")
        # Clean up file if processing fails
        if file_path.exists():
            file_path.unlink()
        raise HTTPException(status_code=500, detail=f"Error processing document: {str(e)}")


@app.post("/ask", response_model=QuestionResponse)
async def ask_question(
    request: QuestionRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Ask a question about uploaded documents.
    Protected endpoint - requires authentication.
    """
    logger.info(f"User {current_user.username} asking: {request.question[:50]}...")
    
    try:
        result = doc_processor.answer_question(request.question)
        return QuestionResponse(**result)
    except ValueError as e:
        logger.warning(f"No documents available: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error answering question: {e}")
        raise HTTPException(status_code=500, detail=f"Error answering question: {str(e)}")


@app.get("/documents")
async def list_documents(current_user: User = Depends(get_current_user)):
    """
    List uploaded documents.
    Protected endpoint - requires authentication.
    """
    try:
        files = list(settings.upload_dir.glob("*"))
        documents = [
            {
                "filename": f.name,
                "size_bytes": f.stat().st_size,
                "uploaded_at": f.stat().st_mtime
            }
            for f in files if f.is_file()
        ]
        return {"documents": documents, "count": len(documents)}
    except Exception as e:
        logger.error(f"Error listing documents: {e}")
        raise HTTPException(status_code=500, detail=f"Error listing documents: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)