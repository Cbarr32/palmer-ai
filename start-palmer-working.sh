#!/bin/bash
# Palmer AI Working Launcher

echo "🚀 Starting Palmer AI (Fixed Version)"
echo "===================================="

# Activate Python 3.12 venv
source .venv/Scripts/activate

# Set Python path
export PYTHONPATH="${PWD}/src:${PWD}:${PYTHONPATH}"

# Start backend
echo "🐍 Starting backend on http://localhost:8000"
python -m uvicorn src.palmer_ai.server:app --reload --host localhost --port 8000 &
BACKEND_PID=$!

# Wait a bit
sleep 5

# Start frontend
echo "⚛️ Starting frontend on http://localhost:3000"
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

# Cleanup function
cleanup() {
    echo "Stopping services..."
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
    exit
}
trap cleanup EXIT

echo ""
echo "✅ Palmer AI is running!"
echo "Frontend: http://localhost:3000"
echo "Backend: http://localhost:8000"
echo "API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop"

# Keep running
wait
