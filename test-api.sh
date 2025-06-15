#!/bin/bash
# Test Palmer AI API

echo "🧪 Testing Palmer AI API..."

# Test root endpoint
echo "Testing root endpoint..."
curl -s http://localhost:8000/ | jq . 2>/dev/null || curl http://localhost:8000/

# Test health endpoint
echo -e "\n\nTesting health endpoint..."
curl -s http://localhost:8000/health | jq . 2>/dev/null || curl http://localhost:8000/health

# Test Claude connection
echo -e "\n\nTesting Claude integration..."
curl -X POST http://localhost:8000/api/v1/analyze \
  -H "Content-Type: application/json" \
  -d '{"company_name": "Test Company", "description": "Testing Palmer AI"}' \
  | jq . 2>/dev/null || echo "Run ./start-palmer.sh first!"
