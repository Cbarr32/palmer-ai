#!/bin/bash
# Palmer AI Quick Launch - WORKING VERSION

echo "🚀 PALMER AI LAUNCHER"
echo "===================="

# Kill any existing processes on our ports
echo "🧹 Cleaning up old processes..."
lsof -ti:8000 | xargs kill -9 2>/dev/null
lsof -ti:3000 | xargs kill -9 2>/dev/null

# Start Backend
echo ""
echo "🐍 Starting Backend..."
source .venv/Scripts/activate
export PYTHONPATH="${PWD}/src:${PYTHONPATH}"
python -m uvicorn src.palmer_ai.server:app --reload --host localhost --port 8000 &
BACKEND_PID=$!

# Give backend time to start
sleep 3

# Start Frontend in dev mode (always works)
echo ""
echo "⚛️ Starting Frontend..."
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

# Function to stop everything
cleanup() {
    echo -e "\n\n🛑 Shutting down Palmer AI..."
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
    exit 0
}
trap cleanup EXIT INT TERM

# Show success
echo ""
echo "✅ PALMER AI IS RUNNING!"
echo "========================"
echo ""
echo "🌐 Frontend: http://localhost:3000"
echo "🔧 Backend: http://localhost:8000"
echo "📚 API Docs: http://localhost:8000/docs"
echo ""
echo "💡 Test the API:"
echo "   curl http://localhost:8000/health"
echo ""
echo "Press Ctrl+C to stop everything"
echo ""

# Keep running
wait
