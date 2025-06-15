#!/bin/bash
# Palmer AI Quick Start Script

echo "🚀 Starting Palmer AI with Claude Sonnet 4..."

# Check for virtual environment
if [ ! -d ".venv" ]; then
    echo "❌ No virtual environment found!"
    echo "Run: python -m venv .venv"
    exit 1
fi

# Activate it
source .venv/Scripts/activate || source .venv/bin/activate

# Set Python path
export PYTHONPATH="${PWD}/src:${PWD}:${PYTHONPATH}"

# Verify API key
if ! grep -q "ANTHROPIC_API_KEY=sk-" .env; then
    echo "❌ No Anthropic API key in .env!"
    exit 1
else
    echo "✅ Anthropic API key found"
fi

# Redis check (not required)
echo "📝 Note: Redis not required for Palmer AI"
echo "   Using in-memory caching for development"

# Start the server
echo ""
echo "🌐 Starting Palmer AI on http://localhost:8000"
echo "📚 API Docs: http://localhost:8000/docs"
echo "🎯 Frontend: http://localhost:3000 (if running)"
echo ""

python -m uvicorn src.palmer_ai.server:app \
    --reload \
    --host localhost \
    --port 8000 \
    --log-level info
