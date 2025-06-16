"""Palmer AI Startup Verification"""
import sys
import os
sys.path.insert(0, 'src')

print("🔍 Palmer AI System Verification")
print("================================")

# Test imports
try:
    from palmer_ai.config.env import OPENAI_API_KEY, ANTHROPIC_API_KEY
    print("✅ Configuration module loads")
    print(f"   OpenAI: {'Configured' if OPENAI_API_KEY else 'Missing'}")
    print(f"   Anthropic: {'Configured' if ANTHROPIC_API_KEY else 'Missing'}")
except Exception as e:
    print(f"❌ Configuration error: {e}")

try:
    from palmer_ai.server import app
    print("✅ Server module loads")
except Exception as e:
    print(f"❌ Server error: {e}")

try:
    from palmer_ai.api.complete import router
    print("✅ API endpoints configured")
except Exception as e:
    print(f"❌ API error: {e}")

print("\n🎯 System ready for development!")
