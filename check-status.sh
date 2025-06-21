#!/bin/bash
echo "🔍 Palmer AI System Status"
echo "========================="

# Check backend
echo ""
echo "Backend Status:"
curl -s http://localhost:8000/health | jq . 2>/dev/null && echo "✅ Backend Online" || echo "❌ Backend Offline"

# Check frontend
echo ""
echo "Frontend Status:"
curl -s http://localhost:3000 > /dev/null && echo "✅ Frontend Online" || echo "❌ Frontend Offline"

# Check API key
echo ""
echo "Configuration:"
grep -q "ANTHROPIC_API_KEY=sk-ant-" .env && echo "✅ API Key Configured" || echo "❌ API Key Missing"

# Show running processes
echo ""
echo "Running Processes:"
ps aux | grep -E "(uvicorn|next)" | grep -v grep | wc -l | xargs -I {} echo "{} Palmer AI processes running"
