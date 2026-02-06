"""
MCP server implementation for Medical Document Assistant.
Provides tools and resources for AI assistants to process medical documents.
"""
import asyncio
import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence

from mcp.server.models import InitializationOptions
import mcp.types as types
from mcp.server import NotificationOptions, Server
from mcp.server.stdio import stdio_server

from src.document_processor import DocumentProcessor
from .tools import DocumentTools
from .resources import DocumentResources
from config import settings


class MedicalDocumentMCPServer:
    """MCP server for medical document processing capabilities."""
    
    def __init__(self):
        """Initialize the MCP server."""
        self.server = Server("medical-document-assistant")
        self.doc_processor = DocumentProcessor()
        self.tools_handler = DocumentTools(self.doc_processor)
        self.resources_handler = DocumentResources(self.doc_processor)
        
        self._register_handlers()
    
    def _register_handlers(self):
        """Register MCP handlers."""
        
        @self.server.list_tools()
        async def handle_list_tools() -> List[types.Tool]:
            """List available tools."""
            return await self.tools_handler.list_tools()
        
        @self.server.call_tool()
        async def handle_call_tool(name: str, arguments: Dict[str, Any] | None) -> List[types.TextContent]:
            """Handle tool calls."""
            return await self.tools_handler.call_tool(name, arguments or {})
        
        @self.server.list_resources()
        async def handle_list_resources() -> List[types.Resource]:
            """List available resources."""
            return await self.resources_handler.list_resources()
        
        @self.server.read_resource()
        async def handle_read_resource(uri: str) -> str:
            """Read a specific resource."""
            return await self.resources_handler.read_resource(uri)
    
    async def run(self):
        """Run the MCP server."""
        async with stdio_server() as (read_stream, write_stream):
            await self.server.run(
                read_stream,
                write_stream,
                InitializationOptions(
                    server_name="medical-document-assistant",
                    server_version="0.1.0",
                    capabilities=self.server.get_capabilities(
                        notification_options=NotificationOptions(),
                        experimental_capabilities={}
                    )
                )
            )


def main():
    """Main entry point for the MCP server."""
    server = MedicalDocumentMCPServer()
    asyncio.run(server.run())


if __name__ == "__main__":
    main()