#!/bin/bash
# Palmer AI Debug Startup Script

echo "🔍 Palmer AI Debug Startup"
echo "========================="

# Clean up any existing processes
echo "Cleaning up existing processes..."
taskkill //F //IM python.exe 2>/dev/null || true
taskkill //F //IM node.exe 2>/dev/null || true
sleep 2

# Check Python environment
echo ""
echo "Python environment:"
python --version
pip show fastapi uvicorn httpx beautifulsoup4 pandas pydantic | grep "Name\|Version" || echo "⚠️ Some packages missing"

# Start backend with full output
echo ""
echo "Starting backend with debug output..."
cd ~/dev/palmerai
python -m uvicorn src.palmer_ai.server:app --reload --host 0.0.0.0 --port 8000 --log-level debug
