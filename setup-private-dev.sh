#!/bin/bash
# Palmer AI Private Development Setup

echo "Setting up private Palmer AI development..."

# Check if private_core exists
if [ ! -d "private_core" ]; then
    echo "⚠️ Private core missing! You're running public version."
    echo "Contact Chris Barr for private module access."
    exit 1
fi

# Set environment for private features
export PALMER_AI_MODE="private"
export ENABLE_PROPRIETARY_FEATURES="true"

echo "✅ Private Palmer AI activated!"
echo "🔒 Proprietary features enabled"
echo "⚠️ Remember: NEVER commit private_core/ to public repo!"
