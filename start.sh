#!/bin/bash
# Startup script for Medical Document Assistant

echo "🏥 Starting Medical Document Assistant..."
echo ""

# Function to start with Docker
start_docker() {
    echo "🐳 Starting with Docker..."
    
    # Check if .env file exists
    if [ ! -f ".env" ]; then
        echo "⚠️  .env file not found. Creating from template..."
        if [ -f ".env.template" ]; then
            cp .env.template .env
            echo "✅ Created .env from template. Please update it with your OpenAI API key!"
        else
            echo "❌ No .env template found. Please create a .env file manually."
            exit 1
        fi
    fi
    
    # Build and start services
    echo "🔨 Building Docker images..."
    docker-compose build
    
    echo "🚀 Starting services..."
    docker-compose up -d
    
    echo "✅ Services started!"
    echo "📍 API: http://localhost:8000"
    echo "📍 Frontend: http://localhost:8501"
    echo "📍 API Documentation: http://localhost:8000/docs"
    
    # Follow logs
    echo ""
    echo "📋 Following logs (Ctrl+C to stop):"
    docker-compose logs -f
}

# Function to start with virtual environment (development)
start_venv() {
    echo "🛠️  Starting in development mode..."
    
    # Check if virtual environment exists
    if [ ! -d "venv" ]; then
        echo "⚠️  Virtual environment not found. Creating one..."
        python3 -m venv venv
        echo "✅ Virtual environment created"
    fi

    # Activate virtual environment
    source venv/bin/activate

    # Check if dependencies are installed
    if ! python -c "import fastapi" &> /dev/null; then
        echo "📦 Installing dependencies..."
        pip install -r requirements.txt
        echo "✅ Dependencies installed"
    fi

    # Check if .env exists
    if [ ! -f ".env" ]; then
        echo "⚠️  .env file not found. Copying from template..."
        if [ -f ".env.template" ]; then
            cp .env.template .env
            echo "✅ Created .env from template. Please update it with your OpenAI API key!"
        else
            echo "❌ No .env template found. Please create a .env file manually."
        fi
    fi

    # Start API server in background
    echo "🚀 Starting API server on http://localhost:8000..."
    python -m uvicorn src.api.main:app --host 0.0.0.0 --port 8000 --reload &
    API_PID=$!

    # Wait for API to start
    sleep 3

    # Start Streamlit app
    echo "🎨 Starting Streamlit app on http://localhost:8501..."
    streamlit run app.py &
    STREAMLIT_PID=$!

    echo ""
    echo "✅ Both services are running!"
    echo "   - API: http://localhost:8000"
    echo "   - App: http://localhost:8501"
    echo "   - API Documentation: http://localhost:8000/docs"
    echo ""
    echo "Press Ctrl+C to stop all services..."

    # Wait for user interrupt
    trap "kill $API_PID $STREAMLIT_PID; exit" INT
    wait
}

# Parse command line arguments
case "$1" in
    docker|d)
        start_docker
        ;;
    dev|development|venv|v)
        start_venv
        ;;
    *)
        echo "Usage: $0 [docker|dev]"
        echo ""
        echo "Options:"
        echo "  docker, d      Start with Docker (recommended for production)"
        echo "  dev, venv, v   Start with virtual environment (development)"
        echo ""
        echo "If no option is provided, Docker will be used by default."
        echo ""
        start_docker
        ;;
esac
