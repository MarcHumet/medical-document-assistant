# 🏥 Medical Document Assistant

A containerized AI-powered assistant for medical document analysis and question-answering. Built with FastAPI, Streamlit, and OpenAI's language models.

# 💻 System Requirements

## Hardware Requirements

### Minimum Specifications
- **CPU**: x86_64 processor (Intel/AMD) or ARM64 (Apple Silicon, ARM-based systems)
- **RAM**: 8 GB (for small 1B-3B models)
- **Storage**: 20 GB free disk space (10 GB for Docker base + models)
- **GPU** (optional): NVIDIA GPU with 4 GB VRAM or Apple Silicon

### Recommended Specifications
- **CPU**: Modern multi-core processor (Intel Core i5/i7, AMD Ryzen 5/7+, Apple M1/M2+)
- **RAM**: 16 GB or more
- **Storage**: 50+ GB SSD for multiple models
- **GPU**: NVIDIA GPU with 8+ GB VRAM for optimal performance

## Memory Requirements by Model Size

| Model Size | RAM (CPU-only) | VRAM (GPU) | Disk Space | Example Models |
|------------|----------------|------------|------------|----------------|
| 1B-3B | 4-8 GB | 4-6 GB | 1-3 GB | llama3.2:1b, phi-3.5-mini, smollm |
| 7B-8B | 8-16 GB | 8-12 GB | 4-5 GB | llama3.1, mistral, medllama2 |
| 13B-14B | 16-24 GB | 12-16 GB | 8-10 GB | phi4, vicuna-13b |
| 30B-40B | 32-64 GB | 24+ GB | 20-30 GB | Larger specialized models |
| 70B+ | 64-128 GB | 48+ GB | 40-80 GB | llama3.3:70b |

*Note: Quantized models (Q4, Q5) use 30-50% less memory than listed values.*

## Performance: CPU vs GPU

### CPU-Only Inference
- **Speed**: 3-6 tokens/second (modern processors)
- **Use cases**: Batch processing, development, non-interactive applications
- **Pros**: No GPU required, works on any system
- **Cons**: 10-20x slower than GPU inference

### GPU-Accelerated Inference
- **Speed**: 40-100+ tokens/second (depending on GPU and model)
- **Use cases**: Interactive chatbots, real-time applications, production RAG systems
- **Pros**: Fast response times, handles concurrent requests
- **Cons**: Requires compatible NVIDIA GPU or Apple Silicon

### Performance Benchmarks
| Hardware | Model Size | Tokens/Second |
|----------|------------|---------------|
| Ryzen 5 3600 (CPU) | 7B | 3-6 t/s |
| NVIDIA GTX 1070 (8GB) | 7B | 40-45 t/s |
| NVIDIA RTX 3090 (24GB) | 7B | 80-100 t/s |
| Apple M1 | 7B | 25-35 t/s |


## 🏗️ Architecture

The project follows a modular architecture with clear separation of concerns:

```
medical-document-assistant/
├── src/                           # Source code
│   ├── api/                       # FastAPI application
│   │   ├── __init__.py
│   │   └── main.py               # API routes and endpoints
│   ├── auth/                     # Authentication module
│   │   ├── __init__.py
│   │   └── auth.py              # JWT authentication
│   ├── document_digestion/       # Document processing
│   │   ├── __init__.py
│   │   └── processor.py         # PDF/TXT extraction & chunking
│   ├── llm/                      # Language model integration
│   │   ├── __init__.py
│   │   ├── chat.py              # OpenAI chat wrapper
│   │   └── qa_chain.py          # Question-answering chain
│   ├── vector_store/             # Vector database
│   │   ├── __init__.py
│   │   ├── chroma_store.py      # ChromaDB implementation
│   │   ├── chroma_store_persistent.py # Persistent ChromaDB
│   │   └── embeddings.py       # OpenAI embeddings
│   ├── __init__.py
│   └── document_processor.py    # Main orchestrator
├── test/                         # Testing files
│   ├── test_ollama.py           # Standalone LLM tests
│   ├── test_ollama.sh           # Docker-based LLM tests
│   ├── test_pdf_upload.sh       # End-to-end workflow tests
│   └── test_routes.py           # FastAPI test routes
├── app.py                        # Streamlit frontend
├── config.py                     # Configuration management
├── requirements.txt              # Python dependencies
├── Dockerfile                    # Container definition
├── docker-compose.yml           # Multi-service orchestration
├── docker-compose.ollama.yml    # Ollama-specific compose
├── start.sh                     # Startup script
├── setup-ollama.sh              # Ollama setup script
├── .env.template                # Environment variables template
├── .env.example                 # Environment example
├── pyproject.toml               # Project metadata
├── TESTING_GUIDE.md             # Testing documentation
├── uploads/                     # Document upload directory
├── logs/                        # Application logs
└── README.md                    # This file
```

## 🚀 Quick Start

### Option 1: Docker (Recommended)

1. **Clone the repository:**
   ```bash
   git clone https://github.com/MarcHumet/medical-document-assistant.git
   cd medical-document-assistant
   ```

2. **Configure environment:**
   use provided .env (in the repo) or change it according your LLM configuration
   ```bash
   nano .env
   # Edit .env and add your OPENAI_API_KEY
   ```
   If no changes, Ollama should be installed 

3. **Start the application:**
   ```bash
   ./start.sh docker
   # or simply
   ./start.sh
   ```

4. **Access the application:**
   - Frontend: http://localhost:8501
   - API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

### Using Local LLM with Ollama (Optional)
Although this code should work with an openai valid api key set in the .env file, I strongly recomment using local LLM with Ollama, since i don't have a openai account i do no have a proper api-hey and it was not tested!!

To use a local LLM instead of OpenAI's API:

1. **Start Ollama service:**
   ```bash
   docker compose -f docker-compose.yml -f docker-compose.ollama.yml up -d
   ```

2. **Load models:**
   ```bash
   ./setup-ollama.sh
   ```

3. **Verify models are loaded:**
   Visit [http://localhost:11434/api/tags](http://localhost:11434/api/tags) in your browser and two models should appear in a json format.

**Note:** Model download can take 10-15 minutes depending on your internet speed and the model size. Make sure you have sufficient disk space and memory for the selected models.   

### Option 2: MCP Server (AI Assistant Integration)

The Medical Document Assistant includes a fully functional **Model Context Protocol (MCP) server** that enables AI assistants like Claude Desktop to directly access medical document processing capabilities.

- **Status**: ✅ Fully developed and operational
- **Features**: 5 medical document tools + 3 information resources
- **Documentation**: Complete setup and usage instructions available
- **Testing**: Comprehensive test suite included

👉 **[See MCP Server Documentation](mcp_server/README.md)** for detailed setup instructions and usage guide.

### Option 3: Development Mode

## 📋 Features

### Core Functionality
- 📄 **Document Processing**: Upload and process PDF and TXT medical documents
- 🤖 **AI-Powered Q&A**: Ask questions and get contextual answers from your documents
- 🔍 **Source Attribution**: See exactly where answers come from in your documents
- 🔐 **Secure API**: JWT-based authentication for all operations

### Technical Features
- 🐳 **Containerized**: Fully containerized with Docker and Docker Compose
- 🏗️ **Modular Architecture**: Clean separation of concerns across modules
- 📊 **Vector Search**: Efficient similarity search using ChromaDB and OpenAI embeddings
- 🔄 **Hot Reload**: Development mode with auto-reload capabilities
- 📝 **API Documentation**: Auto-generated OpenAPI/Swagger documentation
- 🤖 **MCP Server**: Model Context Protocol server for AI assistant integration ([see MCP documentation](mcp_server/README.md))

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | Your OpenAI API key | **Required** |
| `API_SECRET_KEY` | JWT signing secret | `dev-secret-key-change-in-production` |
| `DEMO_USERNAME` | Demo username | `medical_researcher` |
| `DEMO_PASSWORD` | Demo password | `demo_password_123` |
| `UPLOAD_DIR` | Document upload directory | `uploads` |
| `MAX_FILE_SIZE_MB` | Maximum file size in MB | `10` |

### Production Considerations

For production deployment:

1. **Security**: Change default credentials and JWT secret
2. **API Key**: Use secure secret management for OpenAI API key
3. **Volumes**: Ensure persistent storage for uploads and vector database
4. **Networking**: Configure proper firewall and SSL termination
5. **Scaling**: Consider using load balancers for high availability

## 📚 API Documentation

### Authentication

The API uses JWT Bearer token authentication. Get a token by posting credentials to `/token`:

```bash
curl -X POST "http://localhost:8000/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=medical_researcher&password=demo_password_123"
```

### Main Endpoints

- `POST /token` - Get authentication token
- `POST /upload` - Upload and process a document (auth required)
- `POST /ask` - Ask a question about documents (auth required)
- `GET /documents` - List uploaded documents (auth required)
- `GET /health` - Health check endpoint

Full API documentation is available at http://localhost:8000/docs when running.

## 🔍 Usage Examples

### Uploading a Document

```python
import requests

# Get token
auth_response = requests.post(
    "http://localhost:8000/token",
    data={"username": "medical_researcher", "password": "demo_password_123"}
)
token = auth_response.json()["access_token"]

# Upload document
files = {"file": ("document.pdf", open("document.pdf", "rb"), "application/pdf")}
headers = {"Authorization": f"Bearer {token}"}

response = requests.post(
    "http://localhost:8000/upload",
    headers=headers,
    files=files
)
```

### Asking Questions

```python
# Ask a question
question_data = {"question": "What are the main findings of this study?"}
response = requests.post(
    "http://localhost:8000/ask",
    headers=headers,
    json=question_data
)

result = response.json()
print(f"Answer: {result['answer']}")
print(f"Sources: {result['sources']}")
```

## 🛠️ Development

### Project Structure

The modular architecture allows for easy maintenance and testing:

- **`src/document_digestion/`**: Handles PDF/TXT parsing and text chunking
- **`src/vector_store/`**: Manages document embeddings and similarity search
- **`src/llm/`**: Integrates with OpenAI's language models
- **`src/api/`**: FastAPI application with protected endpoints
- **`src/auth/`**: JWT authentication and user management

### Adding New Features

1. **New document formats**: Extend `src/document_digestion/processor.py`
2. **Different LLM providers**: Implement new classes in `src/llm/`
3. **Alternative vector stores**: Add implementations in `src/vector_store/`
4. **New API endpoints**: Extend `src/api/main.py`
5. **New test scenarios**: Add tests to `test/` directory

### Development path
AI assistance was used heavily to avoid 
heavy coding to:
1. create an initial folder structure and initial documentation of the repo
2. generate docker structure

3. Improving documentation.
For instance a prompt to improve further developments:
   ```
   please complete the readme file (do not change any line of code!) for "further development" section. Include these points:

   implement user's feedback for response (tumb up/down)
   implement ddbb to store user info, feedback, history,...
   optimise chunking strategy
   optimise vector store search (reranking models, metadata graphs)
   optimise chunking strategy
   search and test for edge cases and safety
   semantic search
   set a KPI (rate of feedback, times LM answer s"no references found") to monitor performance
   Provide your additional suggestion separated, to be ckecked before joining them.
   ```
4. Develope MCP server
5. Generate unit&integrate testing code and also testing services inside dockers.
6. Agent testing of full project and checking for inconsistencies.

### Testing

```bash
# Run in development mode
./start.sh dev

# Test API endpoints
curl http://localhost:8000/health

# Access interactive documentation
open http://localhost:8000/docs
```

For comprehensive testing instructions, see [TESTING_GUIDE.md](TESTING_GUIDE.md).

## 🐳 Docker Services

The application runs as two services:

1. **API Service** (`medical-assistant-api`):
   - FastAPI application with document processing
   - Exposed on port 8000
   - Handles authentication, file uploads, and Q&A

2. **Frontend Service** (`medical-assistant-frontend`):
   - Streamlit web interface
   - Exposed on port 8501
   - Provides user-friendly chat interface

### Docker Commands

```bash
# Build and start services
docker compose up -d

# View logs
docker compose logs -f

# Stop services
docker compose down

# Rebuild services
docker compose build --no-cache
```
## 🔧 Troubleshooting

### Common Issues

1. **OpenAI API Key Error**:
   - Ensure your `.env` file contains a valid `OPENAI_API_KEY`
   - Check API key permissions and billing status

2. **Port Conflicts**:
   - Change ports in `docker-compose.yml` if 8000/8501 are in use
   - Update `API_URL` environment variable accordingly

3. **Docker Build Issues**:
   - Clear Docker cache: `docker system prune -a`
   - Ensure Docker and Docker Compose are installed and running

4. **File Upload Errors**:
   - Check file size limits (default 10MB)
   - Ensure upload directory permissions are correct
   - Verify supported file formats (PDF, TXT)

## 📄 License

This project is intended for educational and research purposes. Please ensure compliance with OpenAI's usage policies and your organization's data handling requirements when processing medical documents.

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Follow the existing code style and architecture
4. Add tests for new functionality
5. Submit a pull request

---

**Note**: This application is designed for research and educational purposes. For production use with real medical data, ensure proper security measures, data privacy compliance, and regulatory adherence.

## 🚀 Future Enhancements

### Core Features & User Experience
- [ ] **User Feedback System**: Implement thumbs up/down feedback mechanism for AI responses
  - Add feedback endpoints to track response quality
  - Store feedback data for model improvement insights
  - Create user interface components for rating responses

- [ ] **Database Implementation**: Set up comprehensive database system to store:
  - User information and profiles
  - User feedback and ratings
  - Conversation history and sessions
  - Document metadata and processing logs
  - Analytics and usage patterns

- [ ] **Document Management**: Delete, list, and search uploaded documents
- [ ] **Conversation History Persistence**: Store and retrieve previous chat sessions

### File Format & Integration Support
- [ ] Support for more file formats (DOCX, HTML)
- [ ] **MCP Server Integration**: Model Context Protocol server implementation
- [ ] **EHR System Integration**: Connect with Electronic Health Record systems
- [ ] **Medical Database APIs**: Integration with PubMed, clinical trial databases

### Performance Optimization
- [ ] **Chunking Strategy Enhancement**: 
  - Implement adaptive chunking based on document type and content structure
  - Test different chunk sizes and overlap strategies
  - Add semantic chunking to preserve context boundaries
  - Consider hierarchical chunking for better information retrieval

- [ ] **Vector Store Search Optimization**:
  - Integrate reranking models (e.g., Cohere, sentence-transformers)
  - Implement metadata-based filtering and graph relationships
  - Add hybrid search (dense + sparse retrieval)
  - Optimize embedding model selection for medical domain


- [ ] **Semantic Search Implementation**:
  - Add advanced semantic search capabilities beyond simple similarity
  - Implement query expansion and reformulation
  - Add multi-modal search for documents with images/tables
  - Create domain-specific search filters for medical specialties

### Advanced AI Features
- [ ] **Multi-Agent RAG System**: Implement specialized agents for different medical domains
- [ ] **Citation Quality Scoring**: Rank and score the relevance of source citations
- [ ] **Medical Entity Recognition**: Extract and link medical entities (drugs, conditions, procedures)
- [ ] **Temporal Analysis**: Track changes in medical conditions over time across documents

### Quality Assurance & Monitoring
- [ ] **Edge Cases & Safety Testing**:
  - Test with malformed/corrupted documents
  - Handle edge cases in document parsing and text extraction
  - Implement content safety filters for inappropriate queries
  - Add input validation and sanitization
  - Test with various document sizes and formats

- [ ] **Performance Monitoring & KPIs**:
  - **Feedback Rate**: Track percentage of responses receiving user feedback
  - **"No References Found" Rate**: Monitor frequency of LM responses without source citations
  - **Response Time Metrics**: Track query processing and response generation times
  - **User Engagement**: Monitor session duration and query frequency
  - **Document Processing Success Rate**: Track successful vs failed document uploads
  - **Search Accuracy**: Measure relevance of retrieved chunks to user queries

### Technical Infrastructure
- [ ] **API Rate Limiting**: Control API usage and prevent abuse
- [ ] **Batch Processing**: Handle multiple documents simultaneously
- [ ] **Caching Layer**: Implement Redis for frequently asked questions and document embeddings
- [ ] **API Versioning**: Support multiple API versions for backward compatibility
- [ ] **Background Job Processing**: Queue system for heavy document processing tasks
- [ ] **Auto-scaling**: Kubernetes deployment with horizontal pod autoscaling

### Security & Compliance
- [ ] **HIPAA Compliance Features**: Implement audit logging, data encryption at rest, and access controls
- [ ] **Role-based Access Control (RBAC)**: Different permission levels for researchers, clinicians, administrators
- [ ] **Data Anonymization**: Automatic PII detection and redaction in medical documents
- [ ] **Secure Multi-tenancy**: Isolation between different organizations or departments

### Analytics & Insights
- [ ] **Usage Analytics Dashboard**: Visual insights into user behavior and system performance
- [ ] **Medical Terminology Insights**: Track most queried medical terms and concepts
- [ ] **Document Utilization**: Identify which documents are most/least referenced
- [ ] **A/B Testing Framework**: Test different RAG strategies and UI improvements

### Deployment & Operations
- [ ] **Deployment Guides**: Documentation for Docker and cloud deployments
- [ ] **Plugin Architecture**: Allow third-party extensions for specialized medical tools
