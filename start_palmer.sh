#!/bin/bash
# Palmer AI Production Startup Script

echo "🚀 Palmer AI Startup Sequence"
echo "============================"

# Change to project directory
cd ~/dev/palmerai || exit 1

# Kill any existing services
echo "🔄 Cleaning up existing processes..."
taskkill //F //IM python.exe 2>/dev/null || true
taskkill //F //IM node.exe 2>/dev/null || true
sleep 2

# Start backend
echo ""
echo "🔧 Starting Palmer AI Backend..."
python -m uvicorn src.palmer_ai.server:app --reload --host 0.0.0.0 --port 8000 > backend.log 2>&1 &
BACKEND_PID=$!
echo "Backend PID: $BACKEND_PID"

# Wait for backend
echo -n "Waiting for backend to start"
for i in {1..15}; do
    if curl -s http://localhost:8000/health > /dev/null 2>&1; then
        echo " ✅"
        break
    fi
    echo -n "."
    sleep 1
done

# Verify backend
if curl -s http://localhost:8000/health | python -m json.tool; then
    echo ""
    echo "✅ Backend is healthy!"
else
    echo ""
    echo "❌ Backend failed to start. Check backend.log"
    exit 1
fi

# Start frontend if it exists
if [ -d "frontend" ]; then
    echo ""
    echo "🎨 Starting Frontend..."
    cd frontend
    npm run dev > ../frontend.log 2>&1 &
    FRONTEND_PID=$!
    echo "Frontend PID: $FRONTEND_PID"
    cd ..
    sleep 3
fi

echo ""
echo "🎉 Palmer AI is running!"
echo "======================="
echo "🔧 Backend:  http://localhost:8000"
echo "📚 API Docs: http://localhost:8000/docs"
echo "💾 Health:   http://localhost:8000/health"
echo "🎨 Frontend: http://localhost:3000 (if available)"
echo ""
echo "📊 Test the distributor analyzer:"
echo 'curl -X POST http://localhost:8000/api/v1/analyze/distributor \'
echo '  -H "Content-Type: application/json" \'
echo '  -d "{\"url\": \"https://www.grainger.com\"}"'
echo ""
echo "📝 Logs:"
echo "  tail -f backend.log"
echo "  tail -f frontend.log"
