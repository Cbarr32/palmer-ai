#!/bin/bash

echo "🎨 Starting Palmer AI Development Environment"
echo "============================================"

# Kill any existing processes
pkill -f "next dev" 2>/dev/null || true
pkill -f "uvicorn" 2>/dev/null || true

# Start backend
echo "🔧 Starting Palmer AI Backend..."
python -m uvicorn src.palmer_ai.server:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

# Wait for backend
sleep 3

# Start frontend
echo "🎨 Starting Palmer AI Frontend..."
cd frontend
npm run dev &
FRONTEND_PID=$!

# Wait for frontend
sleep 5

echo ""
echo "🎉 Palmer AI Development Environment Ready!"
echo "=========================================="
echo "🎨 Frontend: http://localhost:3000"
echo "🔧 Backend:  http://localhost:8000"
echo "📚 API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop all services"

# Wait for user interrupt
trap 'kill $BACKEND_PID $FRONTEND_PID; exit' INT
wait
