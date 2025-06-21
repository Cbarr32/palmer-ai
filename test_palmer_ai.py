"""Test Palmer AI Multi-Agent System"""
import asyncio
import httpx
import json
from datetime import datetime

async def test_palmer_ai():
    """Test the Palmer AI system"""
    base_url = "http://localhost:8000"
    
    async with httpx.AsyncClient() as client:
        # Test health endpoint
        print("Testing health endpoint...")
        response = await client.get(f"{base_url}/health")
        print(f"Health: {response.json()}")
        
        # List available agents
        print("\nListing available agents...")
        response = await client.get(f"{base_url}/api/v1/agents")
        agents = response.json()
        print(f"Available agents: {len(agents)}")
        for agent in agents:
            print(f"  - {agent['name']} ({agent['role']})")
            
        # Start analysis
        print("\nStarting comprehensive analysis...")
        analysis_request = {
            "url": "https://example.com",
            "analysis_type": "comprehensive",
            "strategy": "adaptive"
        }
        
        response = await client.post(
            f"{base_url}/api/v1/agents/analyze",
            json=analysis_request
        )
        
        result = response.json()
        print(f"Analysis started: {result}")
        
        analysis_id = result["analysis_id"]
        
        # Poll for results
        print("\nPolling for results...")
        for i in range(30):  # Poll for up to 30 seconds
            await asyncio.sleep(1)
            
            response = await client.get(
                f"{base_url}/api/v1/agents/analyze/{analysis_id}"
            )
            
            status = response.json()
            print(f"Progress: {status['progress']*100:.0f}% - Status: {status['status']}")
            
            if status["status"] == "completed":
                print("\nAnalysis completed!")
                print(json.dumps(status["results"], indent=2))
                break
                
        # Get performance metrics
        print("\nFetching performance metrics...")
        response = await client.get(f"{base_url}/api/v1/agents/performance")
        performance = response.json()
        print(f"Performance metrics: {json.dumps(performance, indent=2)}")

if __name__ == "__main__":
    asyncio.run(test_palmer_ai())
