#!/bin/bash
echo "🚀 Launching Palmer AI with Beautiful UI"
echo "====================================="

# Start backend
source .venv/Scripts/activate
export PYTHONPATH="${PWD}/src:${PYTHONPATH}"
python -m uvicorn src.palmer_ai.server:app --reload --host localhost --port 8000 &
BACKEND=$!

sleep 3

# Start frontend
cd frontend && npm run dev &
FRONTEND=$!

cleanup() {
    kill $BACKEND $FRONTEND 2>/dev/null
}
trap cleanup EXIT

echo ""
echo "✅ Palmer AI is running!"
echo "🌐 Beautiful UI: http://localhost:3000"
echo "🔧 API: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop"

wait
