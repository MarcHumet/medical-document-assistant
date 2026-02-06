# MCP Server Directory

This directory contains all Model Context Protocol (MCP) related files for the Medical Document Assistant.

## Directory Structure

```
mcp_server/
├── __init__.py                 # Package initialization
├── mcp_server.py              # CLI entry point for MCP server
├── mcp_config.json            # MCP server configuration
├── MCP_SETUP.md              # MCP setup and integration guide
├── README.md                 # This documentation file
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
1. **Python virtual environment activated**
2. **Docker services running** (required for integration tests)
3. **All dependencies installed** in the virtual environment

#### Step-by-Step Testing Instructions

**Step 1: Verify Docker Services**
```bash
# From project root directory
cd /path_to_repository/medical-document-assistant

# Check Docker services status
docker compose ps

# If services are not running, start them:
docker compose up -d

# Wait for services to be healthy (about 30 seconds)
# Verify API health
curl -s http://localhost:8000/health
```

**Step 2: Activate Virtual Environment**
```bash
# From project root directory
source .venv/bin/activate

# Verify MCP dependencies are installed
python3 -c "import mcp; print('MCP package available')"
```

**Step 3: Run Tests**

**Option A: Run from project root**
```bash
# Navigate to MCP server directory
cd mcp_server

# Run integration tests (tests both MCP server and Docker services)
python3 test_integration.py

# Expected output should show:
# 🎉 ALL TESTS PASSED - Both MCP and Docker functionality working!

# Run comprehensive functionality tests
python3 test_comprehensive.py

# Expected output should show:
# 🎉 COMPREHENSIVE TEST PASSED
```

**Option B: Run from MCP server directory**
```bash
# Navigate directly to MCP server directory
cd /home/marc/project/medical-document-assistant/mcp_server

# Activate virtual environment (adjust path if different)
source ../.venv/bin/activate

# Run integration tests
python3 test_integration.py

# Run comprehensive tests
python3 test_comprehensive.py
```

#### Test Details

**test_integration.py** verifies:
- ✅ MCP CLI help functionality
- ✅ MCP server initialization 
- ✅ Configuration file validation
- ✅ Docker API service health (port 8000)
- ✅ Streamlit frontend availability (port 8501)

**test_comprehensive.py** verifies:
- ✅ MCP modules import correctly
- ✅ DocumentProcessor initialization
- ✅ All 5 MCP tools are available and functional
- ✅ All 3 MCP resources are available and functional
- ✅ Full component integration

#### Troubleshooting Test Failures

**If Docker tests fail:**
```bash
# Check Docker service status
docker compose ps
docker compose logs api
docker compose logs frontend

# Restart if needed
docker compose down && docker compose up -d
```

**If MCP tests fail:**
```bash
# Verify virtual environment
which python3
pip list | grep mcp

# Check import paths
python3 -c "from mcp_server.src.server import MedicalDocumentMCPServer; print('Import OK')"
```

**If permission errors occur:**
```bash
# Check log directory permissions
ls -la ../logs/
mkdir -p ../logs
chmod 755 ../logs
```

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