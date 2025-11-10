#!/bin/bash

echo "🚀 Starting Hostel Grievance Application..."

# Start backend in background
echo "📡 Starting backend server..."
./backend/start_backend.sh &
BACKEND_PID=$!

# Wait a moment for backend to initialize
sleep 3

# Start frontend
echo "🎨 Starting frontend server..."
./start_frontend.sh &
FRONTEND_PID=$!

echo ""
echo "✅ Application started!"
echo "🔗 Backend running at: http://localhost:8000"
echo "🌐 Frontend running at: http://localhost:3000"
echo ""
echo "Press Ctrl+C to stop both servers"

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "🛑 Shutting down servers..."
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    echo "✅ Cleanup complete"
    exit 0
}

# Set trap to cleanup on Ctrl+C
trap cleanup SIGINT

# Wait for processes
wait