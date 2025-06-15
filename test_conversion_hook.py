"""Test Palmer AI 3-Message Conversion Hook"""
import asyncio
import httpx
import json
from datetime import datetime

async def test_hook():
    base_url = "http://localhost:8000"
    headers = {
        "X-Forwarded-For": "192.168.1.100",
        "User-Agent": "Mozilla/5.0 Test Client"
    }
    
    print("🧪 Palmer AI Conversion Hook Test")
    print("=" * 50)
    
    companies = [
        {"company_name": "TechCorp Solutions", "url": "techcorp.com"},
        {"company_name": "Industrial Supply Co", "url": "industrialsupply.com"},
        {"company_name": "HVAC Masters Inc", "url": "hvacmasters.com"},
        {"company_name": "Global Machinery Ltd", "url": "globalmachinery.com"}
    ]
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        for i, company in enumerate(companies):
            print(f"\n📊 Message {i+1}/4 - Analyzing: {company['company_name']}")
            print("-" * 40)
            
            try:
                response = await client.post(
                    f"{base_url}/palmer/analyze-with-hook",
                    json=company,
                    headers=headers
                )
                
                if response.status_code == 200:
                    data = response.json()
                    hook = data.get("conversion_hook", {})
                    analysis = data.get("analysis", {})
                    
                    print(f"✅ Success!")
                    print(f"📈 Message Count: {hook.get('message_count')}/3")
                    print(f"🎯 Stage: {hook.get('hook_data', {}).get('stage', 'unknown').upper()}")
                    print(f"💬 Message: {hook.get('hook_data', {}).get('message', '')}")
                    
                    if analysis.get("insights"):
                        print(f"\n🔍 Analysis Preview:")
                        print(analysis["insights"][:200] + "...")
                    
                    if hook.get('hook_data', {}).get('upgrade_prompt'):
                        print(f"\n🎊 CONVERSION TRIGGER ACTIVATED!")
                        print(f"💰 CTA: {hook['hook_data']['upgrade_prompt']['cta']}")
                        print(f"🔥 {hook['hook_data']['upgrade_prompt']['urgency']}")
                        
                elif response.status_code == 403:
                    error_data = response.json()
                    print(f"🚫 Rate Limit Reached!")
                    print(f"📢 {error_data['detail']['message']}")
                    print(f"💳 {error_data['detail']['cta']}")
                    break
                else:
                    print(f"❌ Error: {response.status_code}")
                    print(response.text)
                    
            except Exception as e:
                print(f"❌ Request failed: {str(e)}")
    
    print("\n" + "=" * 50)
    print("✅ Conversion Hook Test Complete!")
    print("\n💡 Next Steps:")
    print("1. Check frontend at http://localhost:3000")
    print("2. Try the same test from browser")
    print("3. Monitor conversion metrics in logs")

if __name__ == "__main__":
    asyncio.run(test_hook())
