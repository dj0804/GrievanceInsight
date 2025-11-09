#!/bin/bash

# Backend API Startup Script for Hostel Grievance Summarizer

echo "🚀 Starting Hostel Grievance Backend API..."

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "📦 Creating Python virtual environment..."
    python3 -m venv .venv
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source .venv/bin/activate

# Install dependencies
echo "📥 Installing Python dependencies..."
pip install -r requirements.txt

# Load environment variables
if [ -f "../.env" ]; then
    echo "🔑 Loading environment variables..."
    export $(cat ../.env | xargs)
fi

# Start the API server
echo "🌟 Starting API server on http://localhost:8000"
echo "📊 Backend is ready to process grievance analysis requests"
echo "🔗 Frontend should be running on http://localhost:3000"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python app.py
