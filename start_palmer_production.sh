#!/bin/bash
echo "🚀 PALMER AI INTELLIGENT STARTUP"
echo "================================"
echo "Time: $(date)"
echo ""

# Function to check if port is in use
check_port() {
    netstat -an | grep -q ":$1 " && return 0 || return 1
}

# Function to find available port
find_available_port() {
    local port=$1
    while check_port $port; do
        echo "⚠️  Port $port is in use, trying $((port+1))..."
        port=$((port+1))
    done
    echo $port
}

# Kill existing processes
echo "🔄 Cleaning up existing processes..."
taskkill //F //IM python.exe 2>/dev/null || true
sleep 2

# Check frontend status
echo ""
echo "🔍 Checking service status..."
if check_port 3000; then
    echo "✅ Frontend is running on port 3000"
else
    echo "ℹ️  Frontend not detected on port 3000"
fi

# Find available port for backend
BACKEND_PORT=$(find_available_port 8000)
echo "✅ Backend will use port $BACKEND_PORT"

# Update .env with new port if needed
if [ $BACKEND_PORT -ne 8000 ]; then
    echo "📝 Updating API_BASE_URL in .env..."
    sed -i "s|API_BASE_URL=.*|API_BASE_URL=\"http://localhost:$BACKEND_PORT\"|" .env
fi

# Start backend with dynamic port
echo ""
echo "🚀 Starting Palmer AI Backend on port $BACKEND_PORT..."
PORT=$BACKEND_PORT python src/palmer_ai/server_production.py &
BACKEND_PID=$!

# Wait for backend to start
echo -n "Waiting for backend to start"
for i in {1..20}; do
    if curl -s http://localhost:$BACKEND_PORT/health > /dev/null 2>&1; then
        echo " ✅"
        break
    fi
    echo -n "."
    sleep 1
done

# Verify backend is running
echo ""
if curl -s http://localhost:$BACKEND_PORT/health | python -c "import sys, json; data=json.load(sys.stdin); print(f'✅ Backend Status: {data[\"status\"]}')" 2>/dev/null; then
    echo "✅ Backend is healthy!"
    echo ""
    echo "🎉 PALMER AI IS READY!"
    echo "===================="
    echo "📊 Backend: http://localhost:$BACKEND_PORT"
    echo "📚 API Docs: http://localhost:$BACKEND_PORT/docs"
    echo "🎨 Frontend: http://localhost:3000 (if running)"
    echo ""
    echo "📝 Test the API:"
    echo "curl -X POST http://localhost:$BACKEND_PORT/api/v1/analyze \\"
    echo "  -H \"Content-Type: application/json\" \\"
    echo "  -d '{\"url\": \"https://www.grainger.com\"}'"
else
    echo "❌ Backend failed to start!"
    echo "Check the logs above for errors."
    exit 1
fi

# Keep script running
echo ""
echo "Press Ctrl+C to stop the server..."
trap "kill $BACKEND_PID 2>/dev/null; exit" INT
wait $BACKEND_PID
