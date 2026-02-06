#!/bin/bash
# Setup script for Ollama models

echo "🦙 Setting up Ollama models for Medical Document Assistant..."

# Load environment variables from .env file
if [ -f .env ]; then
    export $(grep -v '^#' .env | xargs)
else
    echo "❌ .env file not found. Please create one based on .env.example"
    exit 1
fi

# Set default values if not specified in .env
OLLAMA_MODEL=${OLLAMA_MODEL:-"llama2"}
OLLAMA_EMBEDDING_MODEL=${OLLAMA_EMBEDDING_MODEL:-"nomic-embed-text"}

# Check if Ollama is running
if ! curl -s http://localhost:11434/api/tags > /dev/null; then
    echo "❌ Ollama is not running. Please start it with: docker compose up ollama"
    exit 1
fi

echo "✅ Ollama is running"

# Pull required models
echo "📥 Pulling $OLLAMA_MODEL model (this may take a while)..."
docker exec -it ollama ollama pull "$OLLAMA_MODEL"

echo "📥 Pulling $OLLAMA_EMBEDDING_MODEL model for embeddings..."
docker exec -it ollama ollama pull "$OLLAMA_EMBEDDING_MODEL"

echo "✅ Ollama models are ready!"
echo ""
echo "💡 Current configuration from .env:"
echo "   LLM_PROVIDER=${LLM_PROVIDER:-ollama}"
echo "   OLLAMA_BASE_URL=${LLM_ENDPOINT:-http://localhost:11434}"
echo "   OLLAMA_MODEL=$OLLAMA_MODEL"
echo "   USE_OLLAMA_EMBEDDINGS=${USE_OLLAMA_EMBEDDINGS:-false}"
echo "   OLLAMA_EMBEDDING_MODEL=$OLLAMA_EMBEDDING_MODEL"