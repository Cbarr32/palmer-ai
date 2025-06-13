"""Test Palmer AI Conversational B2B Platform"""
import asyncio
import httpx
import json

async def test_palmer_platform():
    """Test the complete Palmer AI platform"""
    base_url = "http://localhost:8000"
    
    print("🤖 Testing Palmer AI Conversational B2B Platform")
    print("=" * 60)
    
    async with httpx.AsyncClient() as client:
        
        # Test 1: Platform health
        print("\n1. Testing platform health...")
        try:
            response = await client.get(f"{base_url}/health")
            health = response.json()
            print(f"✅ Status: {health['status']}")
            print(f"✅ AI Engine: {health['ai_engine']['model']}")
            print(f"✅ Features: {health['features']}")
        except Exception as e:
            print(f"❌ Health check failed: {e}")
            return
        
        # Test 2: Palmer capabilities
        print("\n2. Testing Palmer capabilities...")
        try:
            response = await client.get(f"{base_url}/palmer/capabilities")
            capabilities = response.json()
            print("✅ Palmer AI Capabilities loaded")
            for category in capabilities["palmer_ai_capabilities"]:
                print(f"   • {category}")
        except Exception as e:
            print(f"❌ Capabilities test failed: {e}")
        
        # Test 3: Conversational chat
        print("\n3. Testing conversational chat...")
        try:
            chat_request = {
                "distributor_id": "test-distributor-123",
                "message": "I need help optimizing my HVAC product catalog for contractors",
                "context": {"industry": "hvac", "target": "contractors"}
            }
            
            response = await client.post(f"{base_url}/palmer/chat", json=chat_request)
            chat_result = response.json()
            
            print("✅ Palmer Chat Response:")
            print(f"   Palmer: {chat_result.get('palmer_response', '')[:100]}...")
            print(f"   Suggestions: {len(chat_result.get('suggestions', []))}")
            
        except Exception as e:
            print(f"❌ Chat test failed: {e}")
        
        # Test 4: Quick help
        print("\n4. Testing quick help...")
        try:
            help_request = {"question": "How do I upload an Excel file?"}
            response = await client.post(f"{base_url}/palmer/quick-help", json=help_request)
            help_result = response.json()
            
            print("✅ Quick Help Response:")
            print(f"   Answer: {help_result.get('palmer_response', '')[:80]}...")
            
        except Exception as e:
            print(f"❌ Quick help failed: {e}")
        
        # Test 5: B2B manufacturer analysis
        print("\n5. Testing B2B manufacturer analysis...")
        try:
            analysis_request = {
                "manufacturer_url": "https://example-manufacturer.com",
                "company_name": "Example Manufacturing",
                "distributor_id": "test-distributor-123"
            }
            
            response = await client.post(f"{base_url}/b2b/manufacturers/analyze", json=analysis_request)
            analysis_result = response.json()
            
            print("✅ Manufacturer Analysis:")
            print(f"   Estimated Products: {analysis_result['site_analysis']['estimated_product_count']}")
            print(f"   Estimated Time: {analysis_result['extraction_estimate']['estimated_time_hours']} hours")
            
        except Exception as e:
            print(f"❌ Manufacturer analysis failed: {e}")
        
        # Test 6: Simple Palmer test
        print("\n6. Testing simple Palmer interaction...")
        try:
            test_request = {"message": "help"}
            response = await client.post(f"{base_url}/test-palmer", json=test_request)
            test_result = response.json()
            
            print("✅ Palmer Test Response:")
            print(f"   User: {test_result['user_message']}")
            print(f"   Palmer: {test_result['palmer_response'][:80]}...")
            
        except Exception as e:
            print(f"❌ Palmer test failed: {e}")
    
    print("\n" + "=" * 60)
    print("🎉 Palmer AI Platform Testing Complete!")
    print("\n📋 Next Steps:")
    print("1. Visit http://localhost:8000 for platform overview")
    print("2. Check http://localhost:8000/docs for API documentation")
    print("3. Try conversational chat at /palmer/chat")
    print("4. Upload files at /palmer/upload-and-chat")
    print("5. Test B2B endpoints at /b2b/*")

if __name__ == "__main__":
    asyncio.run(test_palmer_platform())
