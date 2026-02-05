# Medical Document Assistant

A local prototype assistant that helps researchers interact with clinical and medical documents using AI-powered question-answering.

## Features

- 📄 **Document Upload**: Support for PDF and text files
- 💬 **Intelligent Q&A**: Ask questions and get contextual answers using OpenAI
- 🔐 **Protected API**: Secure endpoints with JWT authentication
- 🎯 **Context-Aware**: Answers include source citations
- 📊 **Observability**: Built-in logging for monitoring
- 🚀 **Extensible**: Designed for future MCP (Model Context Protocol) integration

## Architecture

### Backend (FastAPI)
- Protected REST API with JWT authentication
- Document processing (PDF, TXT)
- Vector-based document search using ChromaDB
- OpenAI integration for question-answering
- Comprehensive logging

### Frontend (Streamlit)
- User-friendly chat interface
- Document upload functionality
- Source citation display
- Session management

## Prerequisites

- Python 3.8+
- OpenAI API key

## Installation

1. **Clone the repository**
```bash
git clone https://github.com/MarcHumet/medical-document-assistant.git
cd medical-document-assistant
```

2. **Create a virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**
```bash
cp .env.example .env
```

Edit `.env` and add your OpenAI API key:
```
OPENAI_API_KEY=your_openai_api_key_here
```

## Usage

### Running the Application

**Option 1: Run both services**

Terminal 1 - Start the API server:
```bash
python api.py
```
The API will be available at http://localhost:8000

Terminal 2 - Start the Streamlit app:
```bash
streamlit run app.py
```
The web interface will open at http://localhost:8501

**Option 2: Use the startup script (Unix/Linux/Mac)**
```bash
chmod +x start.sh
./start.sh
```

### Using the Application

1. **Login**: Use the demo credentials (pre-filled):
   - Username: `medical_researcher`
   - Password: `demo_password_123`

2. **Upload Documents**: 
   - Click "Browse files" in the sidebar
   - Select a PDF or TXT medical document
   - Click "Process Document"

3. **Ask Questions**:
   - Type your question in the chat input
   - Review the AI-generated answer
   - Expand "View Sources" to see citations

### API Usage

#### Get Access Token
```bash
curl -X POST "http://localhost:8000/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=medical_researcher&password=demo_password_123"
```

#### Upload Document
```bash
curl -X POST "http://localhost:8000/upload" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "file=@path/to/document.pdf"
```

#### Ask Question
```bash
curl -X POST "http://localhost:8000/ask" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"question": "What are the main findings?"}'
```

## API Documentation

Once the API is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Project Structure

```
medical-document-assistant/
├── api.py                  # FastAPI application
├── app.py                  # Streamlit frontend
├── auth.py                 # Authentication utilities
├── config.py              # Configuration management
├── document_processor.py  # Document processing and Q&A
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
├── .gitignore            # Git ignore rules
└── README.md             # This file
```

## Configuration

Environment variables in `.env`:

- `OPENAI_API_KEY`: Your OpenAI API key (required)
- `API_SECRET_KEY`: Secret key for JWT tokens
- `API_ALGORITHM`: JWT algorithm (default: HS256)
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Token expiration time
- `UPLOAD_DIR`: Directory for uploaded files
- `MAX_FILE_SIZE_MB`: Maximum file size limit
- `DEMO_USERNAME`: Demo user username
- `DEMO_PASSWORD`: Demo user password

## Security Considerations

⚠️ **Important for Production:**

1. **Change default credentials** in `.env`
2. **Use strong secret keys** for JWT
3. **Implement proper user management** (replace demo auth)
4. **Add HTTPS** for production deployment
5. **Validate and sanitize** all file uploads
6. **Set up rate limiting** to prevent abuse
7. **Store secrets** in secure vaults (not .env files)

## Good Prompting Practices

The system uses carefully crafted prompts for:

1. **Medical Domain Expertise**: Instructions for handling medical terminology
2. **Source Attribution**: Always cite sources for answers
3. **Uncertainty Handling**: Explicitly state when information is unavailable
4. **Context Awareness**: Use document context effectively
5. **Accuracy Priority**: Prioritize correctness over speculation

See `document_processor.py` for the prompt template.

## Extensibility & MCP Integration

The codebase is designed for extensibility:

- **Modular Architecture**: Separate concerns (auth, processing, API)
- **Vector Store**: ChromaDB for flexible document retrieval
- **LangChain Integration**: Easy to add new chains and agents
- **MCP Ready**: Structure supports future Model Context Protocol integration
- **Pluggable LLMs**: Easy to swap OpenAI for other providers

## Observability

The system includes:

- **Structured Logging**: All operations logged with context
- **Request Tracking**: User actions and API calls tracked
- **Error Handling**: Comprehensive error logging
- **Performance Metrics**: Document processing statistics

Logs include:
- User authentication events
- Document upload and processing
- Question-answering operations
- Errors and exceptions

## Troubleshooting

**API Connection Error**
- Ensure the API server is running on port 8000
- Check firewall settings

**OpenAI API Error**
- Verify your API key in `.env`
- Check your OpenAI account has credits

**Document Processing Error**
- Ensure file is valid PDF or TXT
- Check file size is under limit
- Verify file is not corrupted

**Authentication Error**
- Check credentials match `.env` settings
- Ensure token hasn't expired

## Development

### Adding New Document Types

1. Add extraction method in `document_processor.py`
2. Update file type validation in `api.py`
3. Add file type to Streamlit uploader in `app.py`

### Customizing the LLM

Edit `document_processor.py`:
```python
self.llm = ChatOpenAI(
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
