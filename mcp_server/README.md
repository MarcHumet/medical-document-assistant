# MCP Server Directory

This directory contains all Model Context Protocol (MCP) related files for the Medical Document Assistant.

## Directory Structure

```
mcp_server/
├── __init__.py                 # Package initialization
├── mcp_server.py              # CLI entry point for MCP server
├── mcp_config.json            # MCP server configuration
├── MCP_SETUP.md              # MCP setup and integration guide
├── test_integration.py        # Integration tests
├── test_comprehensive.py      # Comprehensive functionality tests
└── src/
    ├── __init__.py            # MCP source package init
    ├── server.py              # Main MCP server implementation
    ├── tools.py               # MCP tools (5 medical document tools)
    └── resources.py           # MCP resources (3 information resources)
```

## Usage

### From Project Root
```bash
# Using module approach
python3 -m mcp_server.mcp_server --help

# Using pip script (if installed)
medical-mcp-server --help
```

### From MCP Directory
```bash
cd mcp_server
python3 mcp_server.py --help
```

### Running Tests

#### Prerequisites
Before running tests, ensure you have:
1. Activated the Python virtual environment
2. Docker services are running (for integration tests)

#### Test Files Available
- **test_integration.py**: Tests both MCP server and Docker services integration
- **test_comprehensive.py**: Tests MCP tools and resources functionality

#### Running Tests

**Option 1: From project root directory**
```bash
cd /home/marc/project/medical-document-assistant

# Activate virtual environment
source .venv/bin/activate

# Run integration tests (tests MCP + Docker services)
cd mcp_server && python3 test_integration.py

# Run comprehensive tests (tests MCP functionality)
python3 test_comprehensive.py
```

**Option 2: From mcp_server directory**
```bash
cd mcp_server

# Activate virtual environment (adjust path as needed)
source ../.venv/bin/activate

# Run integration tests
python3 test_integration.py

# Run comprehensive MCP functionality tests  
python3 test_comprehensive.py
```

#### Expected Test Output
- **✅ All tests passed**: Both MCP server and Docker services working
- **❌ Tests failed**: Check Docker services status and virtual environment

#### Test Dependencies
- Docker services must be running for integration tests
- Virtual environment must be activated
- All MCP dependencies must be installed (`mcp>=0.9.0`, `click>=8.0.0`, etc.)

## Available Tools
- **upload_document**: Upload and process medical documents
- **ask_document_question**: Ask questions using RAG
- **search_documents**: Search for similar content
- **summarize_document**: Generate document summaries
- **extract_medical_entities**: Extract medical entities

## Available Resources
- **medical-docs://uploaded-documents**: List uploaded documents
- **medical-docs://vector-store-info**: Vector store status
- **medical-docs://system-status**: System configuration info