#!/usr/bin/env python
"""Test Palmer AI Setup"""
import os
import sys

print("🧪 Testing Palmer AI Setup...")
print("-" * 50)

# Check Python version
print(f"✅ Python: {sys.version.split()[0]}")

# Check environment
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv("ANTHROPIC_API_KEY", "")
if api_key.startswith("sk-ant-"):
    print(f"✅ Anthropic API Key: {api_key[:20]}...")
else:
    print("❌ Anthropic API Key not found!")

# Test imports
try:
    import anthropic
    print("✅ Anthropic SDK installed")
    
    # Test API connection
    client = anthropic.Anthropic(api_key=api_key)
    print("✅ Anthropic client initialized")
except Exception as e:
    print(f"❌ Anthropic error: {e}")

try:
    import fastapi
    print("✅ FastAPI installed")
except:
    print("❌ FastAPI not installed")

try:
    from src.palmer_ai.server import app
    print("✅ Palmer AI server importable")
except Exception as e:
    print(f"⚠️  Palmer AI import issue: {e}")

print("-" * 50)
print("Redis: Not required for Palmer AI! ✅")
print("Ready to start with: ./start-palmer.sh")
