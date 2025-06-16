#!/bin/bash
# Run CI/CD pipeline locally

echo "🚀 Running Palmer AI CI/CD locally..."

# Backend tests
echo "🐍 Testing backend..."
python -m pytest tests/ -v

# Frontend tests
echo "🟢 Testing frontend..."
cd frontend
npm test -- --watchAll=false
npm run build
cd ..

# Integration tests
echo "🔗 Running integration tests..."
python -m uvicorn src.palmer_ai.server:app --port 8000 &
BACKEND_PID=$!
sleep 5

cd frontend && npm run dev &
FRONTEND_PID=$!
sleep 5

# Test endpoints
curl -s http://localhost:8000/health || echo "Backend health check failed"
curl -s http://localhost:3000 || echo "Frontend check failed"

# Cleanup
kill $BACKEND_PID $FRONTEND_PID

echo "✅ Local CI/CD complete!"
