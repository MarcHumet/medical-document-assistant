"""
MCP tools implementation for medical document processing.
"""
import json
import tempfile
from pathlib import Path
from typing import Any, Dict, List

import mcp.types as types

from src.document_processor import DocumentProcessor


class DocumentTools:
    """Handles MCP tools for document operations."""
    
    def __init__(self, doc_processor: DocumentProcessor):
        """Initialize with document processor."""
        self.doc_processor = doc_processor
    
    async def list_tools(self) -> List[types.Tool]:
        """Return list of available tools."""
        return [
            types.Tool(
                name="upload_document",
                description="Upload and process a medical document (PDF or TXT) for analysis",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "content": {
                            "type": "string",
                            "description": "Base64 encoded content of the document"
                        },
                        "filename": {
                            "type": "string",
                            "description": "Name of the document file (must end in .pdf or .txt)"
                        }
                    },
                    "required": ["content", "filename"]
                }
            ),
            types.Tool(
                name="ask_document_question",
                description="Ask a question about uploaded medical documents using RAG",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "question": {
                            "type": "string",
                            "description": "Question to ask about the medical documents"
                        }
                    },
                    "required": ["question"]
                }
            ),
            types.Tool(
                name="search_documents",
                description="Search for similar content in uploaded documents",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "Search query to find relevant document sections"
                        },
                        "limit": {
                            "type": "integer",
                            "description": "Maximum number of results to return",
                            "default": 3
                        }
                    },
                    "required": ["query"]
                }
            ),
            types.Tool(
                name="summarize_document",
                description="Generate a summary of uploaded medical documents",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "focus": {
                            "type": "string",
                            "description": "Specific aspect to focus on (e.g., 'findings', 'medications', 'treatment')",
                            "default": "general"
                        }
                    }
                }
            ),
            types.Tool(
                name="extract_medical_entities",
                description="Extract medical entities (conditions, medications, procedures) from documents",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "entity_types": {
                            "type": "array",
                            "items": {
                                "type": "string",
                                "enum": ["conditions", "medications", "procedures", "all"]
                            },
                            "description": "Types of medical entities to extract",
                            "default": ["all"]
                        }
                    }
                }
            )
        ]
    
    async def call_tool(self, name: str, arguments: Dict[str, Any]) -> List[types.TextContent]:
        """Handle tool calls."""
        try:
            if name == "upload_document":
                return await self._upload_document(arguments)
            elif name == "ask_document_question":
                return await self._ask_question(arguments)
            elif name == "search_documents":
                return await self._search_documents(arguments)
            elif name == "summarize_document":
                return await self._summarize_document(arguments)
            elif name == "extract_medical_entities":
                return await self._extract_medical_entities(arguments)
            else:
                return [types.TextContent(type="text", text=f"Unknown tool: {name}")]
        except Exception as e:
            return [types.TextContent(type="text", text=f"Error: {str(e)}")]
    
    async def _upload_document(self, arguments: Dict[str, Any]) -> List[types.TextContent]:
        """Handle document upload."""
        import base64
        
        content = arguments.get("content")
        filename = arguments.get("filename")
        
        if not content or not filename:
            return [types.TextContent(type="text", text="Error: Missing content or filename")]
        
        # Validate file extension
        if not filename.lower().endswith(('.pdf', '.txt', '.text')):
            return [types.TextContent(type="text", text="Error: Only PDF and TXT files are supported")]
        
        try:
            # Decode base64 content
            file_data = base64.b64decode(content)
            
            # Create temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix=Path(filename).suffix) as temp_file:
                temp_file.write(file_data)
                temp_path = Path(temp_file.name)
            
            # Process document
            documents = self.doc_processor.process_document(temp_path)
            
            # Clean up temp file
            temp_path.unlink()
            
            result = {
                "status": "success",
                "message": f"Document '{filename}' uploaded and processed successfully",
                "chunks_created": len(documents),
                "filename": filename
            }
            
            return [types.TextContent(type="text", text=json.dumps(result, indent=2))]
            
        except Exception as e:
            return [types.TextContent(type="text", text=f"Error processing document: {str(e)}")]
    
    async def _ask_question(self, arguments: Dict[str, Any]) -> List[types.TextContent]:
        """Handle question asking."""
        question = arguments.get("question")
        
        if not question:
            return [types.TextContent(type="text", text="Error: No question provided")]
        
        try:
            result = self.doc_processor.answer_question(question)
            
            response = {
                "answer": result["answer"],
                "question": result["question"],
                "sources": result["sources"]
            }
            
            return [TextContent(type="text", text=json.dumps(response, indent=2))]
            
        except ValueError as e:
            return [types.TextContent(type="text", text=f"No documents available: {str(e)}")]
        except Exception as e:
            return [types.TextContent(type="text", text=f"Error answering question: {str(e)}")]
    
    async def _search_documents(self, arguments: Dict[str, Any]) -> List[types.TextContent]:
        """Handle document search."""
        query = arguments.get("query")
        limit = arguments.get("limit", 3)
        
        if not query:
            return [types.TextContent(type="text", text="Error: No query provided")]
        
        try:
            # Use the vector store to search
            if not hasattr(self.doc_processor, 'vector_store') or not self.doc_processor.vector_store:
                return [types.TextContent(type="text", text="Error: No documents available for search")]
            
            documents = self.doc_processor.vector_store.similarity_search(query, k=limit)
            
            results = []
            for i, doc in enumerate(documents, 1):
                result = {
                    "rank": i,
                    "content": doc.page_content[:500] + "..." if len(doc.page_content) > 500 else doc.page_content,
                    "metadata": doc.metadata,
                    "similarity_score": doc.metadata.get('score', 'N/A')
                }
                results.append(result)
            
            response = {
                "query": query,
                "results_count": len(results),
                "results": results
            }
            
            return [TextContent(type="text", text=json.dumps(response, indent=2))]
            
        except Exception as e:
            return [types.TextContent(type="text", text=f"Error searching documents: {str(e)}")]
    
    async def _summarize_document(self, arguments: Dict[str, Any]) -> List[types.TextContent]:
        """Handle document summarization."""
        focus = arguments.get("focus", "general")
        
        try:
            # Create a summarization question based on focus
            focus_questions = {
                "general": "Provide a comprehensive summary of the main content and key points in these documents.",
                "findings": "Summarize the key findings, results, and conclusions from these documents.",
                "medications": "List and summarize all medications, treatments, and therapeutic interventions mentioned.",
                "treatment": "Summarize all treatment plans, procedures, and interventions discussed.",
                "diagnosis": "Summarize any diagnoses, conditions, or medical assessments mentioned."
            }
            
            question = focus_questions.get(focus, focus_questions["general"])
            
            result = self.doc_processor.answer_question(question)
            
            response = {
                "focus": focus,
                "summary": result["answer"],
                "sources": result["sources"]
            }
            
            return [TextContent(type="text", text=json.dumps(response, indent=2))]
            
        except Exception as e:
            return [types.TextContent(type="text", text=f"Error generating summary: {str(e)}")]
    
    async def _extract_medical_entities(self, arguments: Dict[str, Any]) -> List[types.TextContent]:
        """Handle medical entity extraction."""
        entity_types = arguments.get("entity_types", ["all"])
        
        try:
            # Create entity extraction questions
            questions = []
            if "all" in entity_types or "conditions" in entity_types:
                questions.append("List all medical conditions, diseases, and diagnoses mentioned in the documents.")
            if "all" in entity_types or "medications" in entity_types:
                questions.append("List all medications, drugs, and pharmaceutical treatments mentioned.")
            if "all" in entity_types or "procedures" in entity_types:
                questions.append("List all medical procedures, surgeries, and interventions mentioned.")
            
            results = {}
            for question in questions:
                try:
                    result = self.doc_processor.answer_question(question)
                    entity_type = "conditions" if "condition" in question.lower() else \
                                  "medications" if "medication" in question.lower() else "procedures"
                    results[entity_type] = {
                        "entities": result["answer"],
                        "sources": result["sources"]
                    }
                except:
                    continue
            
            response = {
                "extracted_entities": results,
                "entity_types_requested": entity_types
            }
            
            return [TextContent(type="text", text=json.dumps(response, indent=2))]
            
        except Exception as e:
            return [types.TextContent(type="text", text=f"Error extracting entities: {str(e)}")]