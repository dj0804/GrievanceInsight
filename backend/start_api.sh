#!/bin/bash

# AI Grievance Summarizer API - Quick Start Script

echo "🚀 Starting AI Grievance Summarizer API..."
echo "================================================"

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "❌ Virtual environment not found. Please run setup first:"
    echo "   python -m venv .venv"
    echo "   source .venv/bin/activate"
    echo "   pip install -r requirements.txt"
    exit 1
fi

# Activate virtual environment
source .venv/bin/activate

# Check if dependencies are installed
python -c "import fastapi, uvicorn, transformers, pandas" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "📦 Installing dependencies..."
    pip install -r requirements.txt
fi

echo "✅ Dependencies checked"
echo "🌐 Starting server on http://localhost:8000"
echo "📚 API Documentation: http://localhost:8000/docs"
echo "🔄 Demo endpoint: http://localhost:8000/demo"
echo ""
echo "Press Ctrl+C to stop the server"
echo "================================================"

# Start the API server
python app.py
