#!/bin/bash

# Frontend Startup Script for Hostel Grievance Summarizer

echo "🚀 Starting Hostel Grievance Frontend..."

# Navigate to the frontend directory
cd "$(dirname "$0")/hostel-portal"

# Install dependencies if needed
if [ ! -d "node_modules" ]; then
    echo "📦 Installing Node.js dependencies..."
    npm install
fi

# Check environment variables
if [ ! -f ".env.local" ]; then
    echo "⚠️  Warning: .env.local file not found"
    echo "Please create .env.local with your Neon database URL"
fi

# Start the development server
echo "🌟 Starting Next.js development server..."
echo "📊 Frontend will be available at http://localhost:3000"
echo "🔗 Make sure backend is running at http://localhost:8000 for AI features"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

npm run dev
