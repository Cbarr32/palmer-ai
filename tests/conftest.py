"""Pytest configuration and fixtures for Palmer AI"""
import pytest
import asyncio
from unittest.mock import AsyncMock, Mock
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from palmer_ai.agents.base.agent import AgentConfig, AgentRole
from palmer_ai.agents.base.production_agent import ProductionAgent

@pytest.fixture
def event_loop():
    """Create event loop for async tests"""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()

@pytest.fixture
def mock_agent_config():
    """Mock agent configuration"""
    return AgentConfig(
        agent_id="test_agent",
        name="Test Agent",
        role=AgentRole.RECONNAISSANCE,
        description="Test agent for unit tests",
        capabilities=[],
        uwas_techniques=["chain_of_thought"]
    )

@pytest.fixture
def mock_anthropic_client():
    """Mock Anthropic client"""
    mock_client = AsyncMock()
    mock_client.messages.create.return_value = Mock(
        content=[Mock(text="Mock AI response")]
    )
    return mock_client

@pytest.fixture
def sample_product_data():
    """Sample product data for testing"""
    return {
        "url": "https://example.com/product",
        "distributor_id": "test-distributor",
        "file_content": b"SKU,Name,Description\nP001,Pump,Industrial pump",
        "file_name": "products.csv"
    }

class MockAgent(ProductionAgent):
    """Mock agent for testing"""
    
    async def analyze(self, input_data):
        return {
            "success": True,
            "data": {"enhanced_data": "mock_enhanced"},
            "confidence": 0.9
        }
        
    async def collaborate(self, message):
        return None
