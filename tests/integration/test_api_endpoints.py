"""Integration tests for API endpoints"""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock
import json

from palmer_ai.server import app

client = TestClient(app)

def test_health_endpoint():
    """Test health endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "ai_engine" in data

@patch('palmer_ai.agents.specialized.conversational_intelligence_agent.ConversationalIntelligenceAgent.analyze')
@pytest.mark.asyncio
async def test_palmer_chat_endpoint(mock_analyze):
    """Test Palmer chat endpoint"""
    mock_analyze.return_value = AsyncMock(
        success=True,
        data={
            "palmer_response": "Test response",
            "suggestions": ["test suggestion"]
        }
    )
    
    response = client.post("/palmer/chat", json={
        "distributor_id": "test-distributor",
        "message": "Test message"
    })
    
    assert response.status_code == 200
    data = response.json()
    assert "palmer_response" in data

def test_palmer_capabilities_endpoint():
    """Test Palmer capabilities endpoint"""
    response = client.get("/palmer/capabilities")
    assert response.status_code == 200
    data = response.json()
    assert "palmer_ai_capabilities" in data

def test_invalid_chat_request():
    """Test invalid chat request"""
    response = client.post("/palmer/chat", json={
        "message": "Test without distributor_id"
    })
    assert response.status_code == 422  # Validation error
