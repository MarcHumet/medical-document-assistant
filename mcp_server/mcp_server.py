#!/usr/bin/env python3
"""
MCP Server CLI entry point for Medical Document Assistant.
"""
import click
import asyncio
from pathlib import Path
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from mcp_server.src.server import MedicalDocumentMCPServer


@click.command()
@click.option('--config-file', '-c', type=click.Path(exists=True), 
              help='Path to configuration file')
@click.option('--upload-dir', '-u', type=click.Path(), 
              help='Directory for uploaded documents', default='uploads')
@click.option('--llm-provider', '-p', type=click.Choice(['openai', 'ollama']), 
              help='LLM provider to use', default='ollama')
@click.option('--verbose', '-v', is_flag=True, help='Enable verbose logging')
def main(config_file, upload_dir, llm_provider, verbose):
    """Start the Medical Document Assistant MCP server."""
    if verbose:
        import logging
        logging.basicConfig(level=logging.DEBUG)
    
    # Set environment variables if provided
    import os
    if upload_dir:
        os.environ['UPLOAD_DIR'] = str(upload_dir)
    if llm_provider:
        os.environ['LLM_PROVIDER'] = llm_provider
    
    # Ensure upload directory exists
    Path(upload_dir).mkdir(parents=True, exist_ok=True)
    
    click.echo(f"Starting Medical Document Assistant MCP Server...")
    click.echo(f"Upload directory: {upload_dir}")
    click.echo(f"LLM provider: {llm_provider}")
    
    # Create and run server
    server = MedicalDocumentMCPServer()
    asyncio.run(server.run())


if __name__ == "__main__":
    main()