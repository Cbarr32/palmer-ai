#!/bin/bash
# Test Working Palmer AI

cd ~/dev/palmerai || exit 1

echo "🧪 Testing Working Palmer AI"
echo "==========================="

# Start server
echo "Starting server..."
python -m uvicorn src.palmer_ai.server:app --reload --host 0.0.0.0 --port 8000 > server.log 2>&1 &
SERVER_PID=$!
sleep 5

# Check health
echo ""
echo "1️⃣ Checking system health..."
curl -s http://localhost:8000/api/v1/health | python -m json.tool

# Test analysis
echo ""
echo "2️⃣ Testing competitor analysis..."
curl -X POST http://localhost:8000/api/v1/analyze \
  -H "Content-Type: application/json" \
  -d '{"domain": "grainger.com"}' | python -m json.tool

echo ""
echo "✅ Test complete!"
echo ""
echo "To use with OpenAI:"
echo "1. Get API key from https://platform.openai.com"
echo "2. Configure: curl -X POST http://localhost:8000/api/v1/setup -d '{\"openai_api_key\": \"YOUR_KEY\"}'"
echo ""
echo "Server running at http://localhost:8000"
echo "API docs at http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop..."
wait $SERVER_PID
