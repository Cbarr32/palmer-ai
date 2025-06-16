#!/bin/bash
# Start Palmer AI Competitive Intelligence Platform

echo "🚀 Starting Palmer AI - The Klue Killer"
echo "====================================="
echo "Competitive Intelligence at 1/300th the price"
echo ""

# Kill any existing processes
echo "🔄 Cleaning up existing processes..."
taskkill //F //IM python.exe 2>/dev/null || true
sleep 2

# Start the server
echo "🎯 Starting competitive intelligence server..."
python -m uvicorn src.palmer_ai.server:app --reload --host 0.0.0.0 --port 8000
