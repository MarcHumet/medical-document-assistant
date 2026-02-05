#!/bin/bash
# Startup script for Medical Document Assistant

echo "🏥 Starting Medical Document Assistant..."
echo ""

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
    echo "⚠️  .env file not found. Copying from .env.example..."
    cp .env.example .env
    echo "⚠️  Please edit .env and add your OPENAI_API_KEY"
    echo ""
fi

# Start API server in background
echo "🚀 Starting API server on http://localhost:8000..."
python api.py &
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
echo ""
echo "Press Ctrl+C to stop all services..."

# Wait for user interrupt
trap "kill $API_PID $STREAMLIT_PID; exit" INT
wait
