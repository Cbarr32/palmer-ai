"""Test the competitive intelligence system"""
import asyncio
import httpx

async def test_palmer_ai():
    """Test Palmer AI competitive intelligence"""
    base_url = "http://localhost:8000"
    
    async with httpx.AsyncClient() as client:
        # Test health
        print("Testing health endpoint...")
        response = await client.get(f"{base_url}/health")
        print(f"Health: {response.json()}")
        
        # Test root
        print("\nTesting root endpoint...")
        response = await client.get(f"{base_url}/")
        print(f"Root: {response.json()}")
        
        print("\n✅ Palmer AI Competitive Intelligence is ready!")
        print("📊 Visit http://localhost:8000/docs for API documentation")

if __name__ == "__main__":
    asyncio.run(test_palmer_ai())
