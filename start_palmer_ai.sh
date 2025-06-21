#!/bin/bash
echo "🚀 Starting Palmer AI B2B Intelligence Platform"
echo "============================================="

cd ~/dev/palmerai

# Ensure we're using the right Python
PYTHON_CMD="/c/Users/chris/AppData/Local/Programs/Python/Python312/python.exe"

# Verify system
echo -e "\n🔍 Running system verification..."
$PYTHON_CMD verify_palmer.py

# Start the server
echo -e "\n🌐 Starting API server..."
$PYTHON_CMD src/palmer_ai/server.py
