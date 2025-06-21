#!/bin/bash
# Palmer AI Full Stack Launcher

echo "🚀 Palmer AI Full Stack Launch Sequence"
echo "======================================"

# Function to kill processes on exit
cleanup() {
    echo ""
    echo "🛑 Shutting down Palmer AI..."
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
    exit
}
trap cleanup EXIT

# Start Backend
echo ""
echo "🐍 Starting Backend (Port 8000)..."
source .venv/Scripts/activate
export PYTHONPATH="${PWD}/src:${PYTHONPATH}"
python -m uvicorn src.palmer_ai.server:app --reload --host localhost --port 8000 &
BACKEND_PID=$!

# Wait for backend to start
sleep 5

# Start Frontend
echo ""
echo "⚛️ Starting Frontend (Port 3000)..."
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

# Show access URLs
echo ""
echo "✅ Palmer AI Full Stack Running!"
echo "================================"
echo "🌐 Frontend: http://localhost:3000"
echo "🔧 Backend API: http://localhost:8000"
echo "📚 API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop all services"

# Keep script running
wait
