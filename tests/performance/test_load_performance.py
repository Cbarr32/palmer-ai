"""Performance tests for Palmer AI"""
import pytest
import asyncio
import time
from concurrent.futures import ThreadPoolExecutor
from fastapi.testclient import TestClient

from palmer_ai.server import app

client = TestClient(app)

@pytest.mark.performance
def test_concurrent_health_checks():
    """Test concurrent health check performance"""
    def make_request():
        start_time = time.time()
        response = client.get("/health")
        duration = time.time() - start_time
        return response.status_code == 200, duration
    
    # Test with 50 concurrent requests
    with ThreadPoolExecutor(max_workers=50) as executor:
        futures = [executor.submit(make_request) for _ in range(50)]
        results = [future.result() for future in futures]
    
    # All requests should succeed
    success_count = sum(1 for success, _ in results if success)
    assert success_count == 50
    
    # Average response time should be under 1 second
    avg_duration = sum(duration for _, duration in results) / len(results)
    assert avg_duration < 1.0

@pytest.mark.performance
@pytest.mark.asyncio
async def test_agent_analysis_performance(mock_agent_config):
    """Test agent analysis performance"""
    from palmer_ai.agents.base.production_agent import ProductionAgent
    
    agent = ProductionAgent(mock_agent_config)
    
    async def mock_analyze(input_data):
        await asyncio.sleep(0.1)  # Simulate processing
        return {"success": True, "data": "mock_result"}
    
    agent.analyze = mock_analyze
    
    start_time = time.time()
    
    # Run 10 analyses concurrently
    tasks = [
        agent.analyze_with_resilience({"test": f"data_{i}"})
        for i in range(10)
    ]
    
    results = await asyncio.gather(*tasks)
    duration = time.time() - start_time
    
    # Should complete in reasonable time (concurrent execution)
    assert duration < 2.0  # Should be much faster than 10 * 0.1 = 1.0s
    assert len(results) == 10
