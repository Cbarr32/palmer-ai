#!/usr/bin/env python3
"""Test Palmer AI deployment on Railway"""
import asyncio
import httpx
import json

async def test_palmer_deployment():
    """Test Palmer AI live deployment"""
    base_url = "https://www.palmer-apps.com"
    
    print("🧪 Testing Palmer AI Live Deployment")
    print("=" * 50)
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        
        # Test 1: Health check
        print("\n1. Testing health endpoint...")
        try:
            response = await client.get(f"{base_url}/health")
            if response.status_code == 200:
                health = response.json()
                print(f"✅ Status: {health.get('status')}")
                print(f"✅ Platform: {health.get('platform', 'Palmer AI')}")
                print(f"✅ AI Engine: {health.get('ai_engine', {}).get('model', 'Claude')}")
            else:
                print(f"❌ Health check failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Health check error: {e}")
            return False
        
        # Test 2: Palmer capabilities
        print("\n2. Testing Palmer capabilities...")
        try:
            response = await client.get(f"{base_url}/palmer/capabilities")
            if response.status_code == 200:
                print("✅ Palmer capabilities loaded")
            else:
                print(f"⚠️  Capabilities endpoint: {response.status_code}")
        except Exception as e:
            print(f"⚠️  Capabilities error: {e}")
        
        # Test 3: Simple Palmer test
        print("\n3. Testing conversational Palmer...")
        try:
            test_request = {"message": "I need help with HVAC product optimization"}
            response = await client.post(f"{base_url}/test-palmer", json=test_request)
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Palmer Response: {result.get('palmer_response', '')[:100]}...")
            else:
                print(f"⚠️  Palmer test: {response.status_code}")
        except Exception as e:
            print(f"⚠️  Palmer test error: {e}")
        
        # Test 4: Real conversational chat (if working)
        print("\n4. Testing real Palmer chat...")
        try:
            chat_request = {
                "distributor_id": "test-distributor-001",
                "message": "I have 200 HVAC products that need better descriptions for contractors",
                "context": {"industry": "hvac", "target": "contractors"}
            }
            response = await client.post(f"{base_url}/palmer/chat", json=chat_request)
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Real Palmer Chat Working!")
                print(f"   Response: {result.get('palmer_response', '')[:150]}...")
            else:
                print(f"⚠️  Chat endpoint: {response.status_code}")
        except Exception as e:
            print(f"⚠️  Chat error: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 Palmer AI deployment test complete!")
    print(f"🌐 Live at: {base_url}")
    print(f"📚 API Docs: {base_url}/docs")
    return True

if __name__ == "__main__":
    asyncio.run(test_palmer_deployment())
