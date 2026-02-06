# 🧪 Testing Guide for Medical Document Assistant

This document provides comprehensive information about all testing files in the project, explaining how, when, and why to use each test.

## 📂 Test Organization

All test files are organized in the `test/` directory for better project structure:
- Python test scripts
- Shell test scripts  
- FastAPI test routes
- Test utilities and helpers

**Note**: Run tests from the project root directory using `./test/filename` or navigate to the test directory first with `cd test`.

## 📁 Test Files Overview

The project contains the following test files:

| File | Type | Purpose | Location |
|------|------|---------|----------|
| `test_ollama.py` | Python Script | Standalone Ollama LLM testing | `test/` directory |
| `test_routes.py` | FastAPI Routes | API endpoint testing | `test/` directory |
| `test_ollama.sh` | Shell Script | Docker-based Ollama testing | `test/` directory |
| `test_pdf_upload.sh` | Shell Script | End-to-end PDF upload testing | `test/` directory |

---

## 🐍 Python Test Files

### 1. `test_ollama.py` - Standalone Ollama LLM Testing

**📍 Location**: `/test/test_ollama.py`

**🎯 Purpose**: 
Standalone test script to verify Ollama LLM functionality without running the full application stack.

**⚙️ What it tests**:
- Basic Ollama LLM connectivity
- Simple question-answer functionality
- Medical-specific questions
- Multiple question handling
- Error handling and recovery

**🔧 How to use**:
```bash
# From project root directory
cd test
python test_ollama.py

# Or with specific Python environment
cd test && python3 test_ollama.py

# With environment variables for local testing
cd test && LLM_PROVIDER=ollama LLM_ENDPOINT=http://localhost:11434/v1 python test_ollama.py
```

**📅 When to use**:
- Before starting development to verify Ollama is working
- After Ollama model updates or changes
- During debugging LLM connectivity issues
- For quick LLM functionality verification
- When testing different Ollama models

**✅ Expected output**:
```
🧪 Ollama LLM Test Suite
============================================================

1️⃣ Testing simple question...
🤖 Testing Ollama LLM...
📝 Question: What is the capital of France?
⚙️ Provider: ollama
🔗 Endpoint: http://localhost:11434/v1
🎯 Model: llama3.2:1b
------------------------------------------------------------
🚀 Sending question to Ollama...
✅ Response received!
💬 Answer: [LLM Response]
```

**🚨 Prerequisites**:
- Ollama service running (local or Docker)
- Environment variables configured (.env file)
- Python dependencies installed

---

### 2. `test_routes.py` - FastAPI Testing Routes

**📍 Location**: `/test/test_routes.py`

**🎯 Purpose**: 
Provides FastAPI endpoints specifically for testing LLM functionality through HTTP requests.

**⚙️ What it provides**:
- `/test-llm` (POST): Test with custom questions
- `/test-llm-simple` (GET): Quick test with predefined question

**🔧 How to use**:

**Via HTTP POST**:
```bash
curl -X POST "http://localhost:8000/api/test-llm" \
  -H "Content-Type: application/json" \
  -d '{"question": "What is machine learning?"}'
```

**Via HTTP GET** (simple test):
```bash
curl -X GET "http://localhost:8000/api/test-llm-simple"
```

**Via API Documentation**:
1. Start the application: `./start.sh`
2. Go to: http://localhost:8000/docs
3. Find `/test-llm` endpoints in the documentation
4. Use the "Try it out" feature

**📅 When to use**:
- Testing LLM through the actual API endpoints
- Verifying API integration with LLM
- During API development and debugging
- For automated API testing
- When testing authentication is not required

**✅ Expected JSON response**:
```json
{
  "success": true,
  "question": "What is 2 + 2?",
  "response": "2 + 2 equals 4.",
  "error": null,
  "provider": "ollama",
  "model": "llama3.2:1b"
}
```

---

## 🐚 Shell Script Tests

### 3. `test_ollama.sh` - Docker-based Ollama Testing

**📍 Location**: `/test/test_ollama.sh`

**🎯 Purpose**: 
Tests Ollama LLM functionality from within the Docker container environment.

**⚙️ What it tests**:
- Container-to-container communication (api → ollama)
- Internal Docker network connectivity
- Environment variable configuration in containers

**🔧 How to use**:
```bash
# From project root directory
# Make executable (if needed)
chmod +x test/test_ollama.sh

# Run the test
./test/test_ollama.sh

# Or from test directory
cd test && ./test_ollama.sh
```

**📅 When to use**:
- After starting Docker services (`docker-compose up`)
- To verify inter-container communication
- When debugging Docker networking issues
- Before running the full application
- When Ollama container connectivity seems problematic

**🚨 Prerequisites**:
- Docker and Docker Compose installed
- Containers running: `docker-compose up -d`
- Ollama container accessible as `ollama` in Docker network

**✅ Expected output**:
```
🤖 Testing Ollama LLM with correct endpoint...
Provider: ollama
Endpoint: http://ollama:11434/v1
Question: What is 2 + 2?
✅ Response: 2 + 2 equals 4.
```

---

### 4. `test_pdf_upload.sh` - End-to-End PDF Upload Testing

**📍 Location**: `/test/test_pdf_upload.sh`

**🎯 Purpose**: 
Comprehensive end-to-end test of the complete document upload and question-answering workflow.

**⚙️ What it tests**:
- API authentication flow
- PDF document upload
- Document processing and embedding
- Document listing functionality
- Question-answering on uploaded documents
- Complete RAG (Retrieval-Augmented Generation) pipeline

**🔧 How to use**:
```bash
# From project root directory
# Make executable (if needed)
chmod +x test/test_pdf_upload.sh

# Run the test
./test/test_pdf_upload.sh

# Or from test directory
cd test && ./test_pdf_upload.sh
```

**📋 Test workflow**:
1. **Authentication**: Gets JWT token
2. **File Validation**: Checks for existing PDF document
3. **Upload**: Sends PDF to `/upload` endpoint
4. **Verification**: Lists uploaded documents
5. **Q&A Testing**: Asks questions about the uploaded document
6. **Cleanup**: Maintains original files

**📅 When to use**:
- Testing the complete application workflow
- Before deployment or releases
- After making changes to document processing
- For integration testing
- When verifying the full RAG pipeline
- During development of new features

**🚨 Prerequisites**:
- Full application stack running (`./start.sh`)
- PDF file: "DA Technical Challenge.pdf" in project root directory
- API accessible on localhost:8000
- Authentication credentials configured

**✅ Expected output sections**:
```bash
🧪 Testing PDF Document Upload Functionality
==============================================
📍 Step 1: Getting authentication token...
✅ Authentication token obtained

📍 Step 2: Using existing PDF document...
✅ Found PDF document: DA Technical Challenge.pdf

📍 Step 3: Uploading document to API...
✅ Upload response:
{
  "message": "Document uploaded and processed successfully",
  "filename": "DA Technical Challenge.pdf",
  "chunks": 42
}

📍 Step 4: Listing uploaded documents...
✅ Documents list:
[
  {
    "filename": "DA Technical Challenge.pdf",
    "upload_date": "2026-02-06T10:30:00Z",
    "size": "1.2MB"
  }
]

📍 Step 5: Testing question about the document...
✅ Question response:
{
  "answer": "This document appears to be...",
  "sources": ["chunk_1", "chunk_3"],
  "confidence": 0.85
}

📍 Step 6: Cleanup...
✅ Test completed! (Original PDF preserved)
```

---

## 🎯 Testing Strategy

### Development Workflow

1. **Local Development**:
   ```bash
   # 1. Test Ollama connectivity
   cd test && LLM_PROVIDER=ollama LLM_ENDPOINT=http://localhost:11434/v1 python test_ollama.py
   
   # 2. Start application
   ./start.sh
   
   # 3. Test API endpoints
   curl http://localhost:8000/api/test-llm-simple
   
   # 4. Test full workflow
   ./test/test_pdf_upload.sh
   ```

2. **Docker Development**:
   ```bash
   # 1. Start services
   docker-compose up -d
   
   # 2. Test inter-container communication
   ./test/test_ollama.sh
   
   # 3. Test full workflow
   ./test/test_pdf_upload.sh
   ```

3. **From Test Directory**:
   ```bash
   cd test
   
   # Run individual tests
   LLM_PROVIDER=ollama LLM_ENDPOINT=http://localhost:11434/v1 python test_ollama.py
   ./test_ollama.sh
   ./test_pdf_upload.sh
   ```

### 🔍 Troubleshooting with Tests

| Problem | Use This Test | What It Reveals |
|---------|---------------|-----------------|
| "LLM not responding" | `python test_ollama.py` | Ollama service status, model availability |
| "API endpoints failing" | `curl localhost:8000/test-llm-simple` | API service status, routing issues |
| "Docker networking issues" | `./test_ollama.sh` | Container communication problems |
| "Document upload not working" | `./test_pdf_upload.sh` | Full pipeline issues, authentication problems |
| "Q&A returning wrong answers" | `./test_pdf_upload.sh` | RAG pipeline, embedding quality |

### ⚠️ **Environment Configuration Issues**

**Problem**: Some tests require different endpoint configurations for local vs Docker environments.

**Details**:
- **Local Testing**: Ollama accessible at `http://localhost:11434/v1`
- **Docker Environment**: Ollama accessible at `http://ollama:11434/v1` (internal Docker networking)
- **Impact**: `test_ollama.py` may fail if run locally without adjusting the endpoint

**Solutions**:

1. **For Local Testing** (outside Docker):
   ```bash
   cd test && LLM_PROVIDER=ollama LLM_ENDPOINT=http://localhost:11434/v1 python test_ollama.py
   ```

2. **For Docker Environment** (inside containers):
   ```bash
   ./test/test_ollama.sh  # Uses internal Docker networking automatically
   ```

3. **Environment-Aware Configuration** (recommended):
   ```bash
   # Check if running inside Docker
   if [ -f /.dockerenv ]; then
       export LLM_ENDPOINT="http://ollama:11434/v1"
   else
       export LLM_ENDPOINT="http://localhost:11434/v1"
   fi
   ```

**Files Affected**:
- `test_ollama.py`: Requires correct endpoint configuration
- `.env` file: Contains Docker-specific endpoints by default
- Any local testing that imports LLM components

**Recommended Fix**: Update test scripts to auto-detect environment or provide clear instructions for local vs Docker testing.

### 🚀 Continuous Integration

For CI/CD pipelines, run tests in this order:

```bash
# 1. Unit tests (fastest)
cd test && python test_ollama.py

# 2. API tests (medium speed)
curl http://localhost:8000/health
curl http://localhost:8000/api/test-llm-simple

# 3. Integration tests (slowest)
./test/test_pdf_upload.sh
```

---

## 📈 Performance Benchmarking

Use these tests for performance monitoring:

- **`test_ollama.py`**: Measure raw LLM response times
- **`test_pdf_upload.sh`**: Measure end-to-end processing times
- **`test_routes.py`**: Measure API response times

---

## 🛠️ Extending the Tests

### Adding New Test Cases

1. **For new LLM providers**: Extend `test_ollama.py`
2. **For new API endpoints**: Add routes to `test_routes.py`
3. **For new document formats**: Extend `test_pdf_upload.sh`
4. **For performance testing**: Create new shell scripts

### Best Practices

- ✅ Run tests before committing code
- ✅ Use tests to verify bug fixes
- ✅ Update tests when adding features
- ✅ Include tests in deployment workflows
- ✅ Document expected outcomes
- ✅ Handle error cases gracefully

---

**📝 Note**: These tests are designed for development and testing environments. For production deployment, implement proper monitoring, logging, and health checks beyond these basic test scripts.