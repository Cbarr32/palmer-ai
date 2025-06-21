"""Tests for production agent resilience"""
import pytest
import asyncio
from unittest.mock import AsyncMock, patch

from palmer_ai.agents.base.production_agent import ProductionAgent, CircuitBreaker
from palmer_ai.agents.base.agent import AnalysisResult, ConfidenceLevel

@pytest.mark.asyncio
async def test_circuit_breaker_closed_state():
    """Test circuit breaker in closed state"""
    cb = CircuitBreaker(failure_threshold=3)
    
    async def successful_operation():
        return "success"
    
    result = await cb.call(successful_operation)
    assert result == "success"
    assert cb.state.value == "closed"

@pytest.mark.asyncio
async def test_circuit_breaker_opens_after_failures():
    """Test circuit breaker opens after threshold failures"""
    cb = CircuitBreaker(failure_threshold=2)
    
    async def failing_operation():
        raise Exception("Operation failed")
    
    # First failure
    with pytest.raises(Exception):
        await cb.call(failing_operation)
    assert cb.failure_count == 1
    
    # Second failure - should open circuit
    with pytest.raises(Exception):
        await cb.call(failing_operation)
    assert cb.state.value == "open"

@pytest.mark.asyncio
async def test_production_agent_retry_mechanism(mock_agent_config):
    """Test production agent retry logic"""
    agent = ProductionAgent(mock_agent_config)
    
    # Mock analyze method to fail twice then succeed
    call_count = 0
    async def mock_analyze(input_data):
        nonlocal call_count
        call_count += 1
        if call_count < 3:
            raise Exception("Temporary failure")
        return AnalysisResult(
            success=True,
            data={"result": "success"},
            confidence=ConfidenceLevel.HIGH
        )
    
    agent.analyze = mock_analyze
    
    result = await agent.analyze_with_resilience({"test": "data"})
    assert result.success
    assert call_count == 3  # Failed twice, succeeded on third attempt

@pytest.mark.asyncio
async def test_production_agent_fallback(mock_agent_config):
    """Test production agent fallback mechanism"""
    agent = ProductionAgent(mock_agent_config)
    
    # Mock analyze to always fail
    async def mock_analyze(input_data):
        raise Exception("Persistent failure")
    
    agent.analyze = mock_analyze
    
    result = await agent.analyze_with_resilience({"test": "data"})
    assert not result.success
    assert "Agent temporarily unavailable" in result.errors[0]
    assert result.metadata["fallback_triggered"] is True

@pytest.mark.asyncio
async def test_agent_health_check(mock_agent_config):
    """Test agent health check"""
    agent = ProductionAgent(mock_agent_config)
    
    health = await agent.health_check()
    assert health["agent_id"] == "test_agent"
    assert health["status"] == "healthy"
    assert "circuit_breaker_state" in health
