# 🏥 Medical Document Assistant

A containerized AI-powered assistant for medical document analysis and question-answering. Built with FastAPI, Streamlit, and OpenAI's language models.

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
│   │   └── embeddings.py       # OpenAI embeddings
│   ├── __init__.py
│   └── document_processor.py    # Main orchestrator
├── app.py                        # Streamlit frontend
├── config.py                     # Configuration management
├── requirements.txt              # Python dependencies
├── Dockerfile                    # Container definition
├── docker-compose.yml           # Multi-service orchestration
├── start.sh                     # Startup script
├── .env.template                # Environment variables template
└── README.md                    # This file
```

## 🚀 Quick Start

### Option 1: Docker (Recommended)

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd medical-document-assistant
   ```

2. **Configure environment:**
   ```bash
   cp .env.template .env
   # Edit .env and add your OPENAI_API_KEY
   ```

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

### Option 2: Development Mode

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

### Testing

```bash
# Run in development mode
./start.sh dev

# Test API endpoints
curl http://localhost:8000/health

# Access interactive documentation
open http://localhost:8000/docs
```

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
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Rebuild services
docker-compose build -:
-no-cache
```
In case, local LLM it is desired, install Ollama localy and proceed to charge LLM with the following steps:



```bash
docker-compose up ollama -d
```

And load model defined in .env
```bash
./setup-ollama.sh
```


```bash
docker-compose up ollama -d
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
    model_name="gpt-4",  # Change model
    temperature=0.3,     # Adjust creativity
    ...
)
```

### Modifying the Prompt

Update `_get_qa_prompt()` in `document_processor.py` to customize how the AI responds.

## Future Enhancements

- [ ] Support for more file formats (DOCX, HTML)
- [ ] Multi-user database for authentication
- [ ] Document management (delete, list, search)
- [ ] Conversation history persistence
- [ ] Advanced RAG techniques
- [ ] MCP server integration
- [ ] Batch processing
- [ ] API rate limiting
- [ ] Deployment guides (Docker, cloud)

## License

This project is open source and available under the MIT License.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For issues and questions, please use the GitHub issue tracker.

---

**Note**: This is a prototype for local development and research purposes. For production use, implement proper security, scalability, and compliance measures appropriate for handling medical data.
