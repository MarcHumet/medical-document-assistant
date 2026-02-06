# Medical Document Assistant MCP Server

This directory contains the Model Context Protocol (MCP) server implementation for the Medical Document Assistant.

## Overview

The MCP server provides AI assistants with access to medical document processing capabilities through a standardized protocol.

## Features

### 🛠️ Available Tools

1. **upload_document** - Upload and process medical documents (PDF/TXT)
2. **ask_document_question** - Ask questions about documents using RAG
3. **search_documents** - Search for similar content in documents
4. **summarize_document** - Generate document summaries
5. **extract_medical_entities** - Extract medical entities from documents

### 📁 Available Resources

1. **uploaded-documents** - List all uploaded documents
2. **vector-store-info** - Vector store status and information
3. **system-status** - System configuration and capabilities
4. **document/[filename]** - Individual document content

## Quick Start

### 1. Install Dependencies

```bash
pip install mcp mcp-server-stdio click
```

### 2. Run MCP Server

```bash
# Basic usage
python mcp_server.py

# With custom settings
python mcp_server.py --upload-dir /path/to/docs --llm-provider openai --verbose
```

### 3. Configure in Claude Desktop

Add to your Claude Desktop configuration:

```json
{
  "mcpServers": {
    "medical-document-assistant": {
      "command": "python",
      "args": ["mcp_server.py"],
      "cwd": "/path/to/medical-document-assistant",
      "env": {
        "OPENAI_API_KEY": "your-api-key",
        "LLM_PROVIDER": "ollama",
        "UPLOAD_DIR": "uploads"
      }
    }
  }
}
```

## Usage Examples

### Upload a Document
```python
# AI Assistant will call:
upload_document(
    content="base64_encoded_pdf_content",
    filename="medical_report.pdf"
)
```

### Ask Questions
```python
# AI Assistant will call:
ask_document_question(
    question="What are the key findings in this medical report?"
)
```

### Search Documents
```python
# AI Assistant will call:
search_documents(
    query="blood pressure medications",
    limit=5
)
```

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `LLM_PROVIDER` | LLM provider (openai/ollama) | `ollama` |
| `OPENAI_API_KEY` | OpenAI API key | None |
| `LLM_ENDPOINT` | Ollama endpoint | `http://localhost:11434/v1` |
| `OLLAMA_MODEL` | Ollama model name | `llama3.2:1b` |
| `UPLOAD_DIR` | Document storage directory | `uploads` |

### Command Line Options

```bash
python mcp_server.py --help

Options:
  -c, --config-file PATH          Path to configuration file
  -u, --upload-dir PATH          Directory for uploaded documents
  -p, --llm-provider [openai|ollama]  LLM provider to use
  -v, --verbose                  Enable verbose logging
```

## Integration with AI Assistants

Once configured, AI assistants (like Claude Desktop) can:

1. **Upload documents**: Process medical documents by encoding them as base64
2. **Query documents**: Ask natural language questions about uploaded content
3. **Search content**: Find specific information within documents
4. **Generate summaries**: Create focused summaries of medical content
5. **Extract entities**: Identify medical terms, conditions, and treatments

## Architecture

```
MCP Server
├── Tools (Function calls)
│   ├── Document upload/processing
│   ├── Question answering (RAG)
│   ├── Document search
│   ├── Summarization
│   └── Entity extraction
└── Resources (Data access)
    ├── Document listings
    ├── System status
    └── Document content
```

## Security Considerations

- Documents are processed locally
- No data is sent to external services (except LLM provider)
- Base64 encoding for document transfer
- File type validation (PDF/TXT only)
- Temporary file handling with automatic cleanup

## Troubleshooting

### Common Issues

1. **MCP Server not starting**:
   ```bash
   # Check Python path and dependencies
   python -c "import mcp; print('MCP installed')"
   ```

2. **LLM not responding**:
   ```bash
   # Test Ollama connection
   curl http://localhost:11434/api/tags
   ```

3. **Document processing errors**:
   ```bash
   # Check upload directory permissions
   ls -la uploads/
   ```

## Development

To extend the MCP server:

1. **Add new tools**: Modify `src/mcp/tools.py`
2. **Add new resources**: Modify `src/mcp/resources.py`
3. **Update schemas**: Update tool input schemas as needed

## Integration Examples

### With Claude Desktop

1. Configure `mcp_config.json`
2. Start the MCP server
3. Claude can now process medical documents

### With Other AI Systems

The MCP protocol is standardized, so any MCP-compatible AI system can use this server.

## Performance

- **Document Processing**: 1-5 seconds per document
- **Question Answering**: 2-10 seconds depending on LLM
- **Search Operations**: <1 second
- **Memory Usage**: ~100-500MB depending on document size

## Limitations

- PDF/TXT files only
- 10MB file size limit (configurable)
- Single-user operation
- No authentication (suitable for local use)

---

For more information, see the main [README.md](../README.md) file.