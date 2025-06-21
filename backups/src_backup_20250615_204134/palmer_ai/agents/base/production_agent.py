"""Production-Ready Agent Base with Resilience Patterns"""
import asyncio
import time
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional, Callable
from datetime import datetime, timedelta
from enum import Enum
from dataclasses import dataclass
import json

from .agent import BaseAgent, AgentConfig, AnalysisResult, ConfidenceLevel
from ...utils.logger import get_logger
from ...utils.metrics import metrics_collector

logger = get_logger(__name__)

class CircuitBreakerState(Enum):
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"

@dataclass
class RetryConfig:
    max_attempts: int = 3
    base_delay: float = 1.0
    max_delay: float = 60.0
    exponential_base: float = 2.0

class CircuitBreaker:
    def __init__(self, failure_threshold: int = 5, recovery_timeout: int = 60):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.state = CircuitBreakerState.CLOSED
        self.failure_count = 0
        self.last_failure_time = None
        
    async def call(self, func: Callable, *args, **kwargs):
        if self.state == CircuitBreakerState.OPEN:
            if time.time() - self.last_failure_time < self.recovery_timeout:
                raise Exception("Circuit breaker is OPEN")
            else:
                self.state = CircuitBreakerState.HALF_OPEN
                
        try:
            result = await func(*args, **kwargs)
            if self.state == CircuitBreakerState.HALF_OPEN:
                self.state = CircuitBreakerState.CLOSED
                self.failure_count = 0
            return result
        except Exception as e:
            self.failure_count += 1
            self.last_failure_time = time.time()
            
            if self.failure_count >= self.failure_threshold:
                self.state = CircuitBreakerState.OPEN
            raise e

class ProductionAgent(BaseAgent):
    """Production-ready agent with resilience patterns"""
    
    def __init__(self, config: AgentConfig):
        super().__init__(config)
        self.circuit_breaker = CircuitBreaker()
        self.retry_config = RetryConfig()
        
    async def analyze_with_resilience(self, input_data: Dict[str, Any]) -> AnalysisResult:
        """Analyze with circuit breaker and retry logic"""
        start_time = time.time()
        
        try:
            result = await self.circuit_breaker.call(
                self._analyze_with_retry, input_data
            )
            
            # Record success metrics
            duration = time.time() - start_time
            metrics_collector.record_analysis_duration(duration)
            metrics_collector.increment_counter(f"agent_{self.config.agent_id}_success")
            
            return result
            
        except Exception as e:
            # Record failure metrics
            metrics_collector.increment_counter(f"agent_{self.config.agent_id}_failure")
            
            # Attempt fallback analysis
            return await self.fallback_analysis(input_data, str(e))
            
    async def _analyze_with_retry(self, input_data: Dict[str, Any]) -> AnalysisResult:
        """Retry logic with exponential backoff"""
        last_exception = None
        
        for attempt in range(self.retry_config.max_attempts):
            try:
                return await self.analyze(input_data)
            except Exception as e:
                last_exception = e
                
                if attempt < self.retry_config.max_attempts - 1:
                    delay = min(
                        self.retry_config.base_delay * (self.retry_config.exponential_base ** attempt),
                        self.retry_config.max_delay
                    )
                    logger.warning(f"Agent {self.config.agent_id} attempt {attempt + 1} failed, retrying in {delay}s")
                    await asyncio.sleep(delay)
                    
        raise last_exception
        
    async def fallback_analysis(self, input_data: Dict[str, Any], error: str) -> AnalysisResult:
        """Fallback when all retries fail"""
        logger.error(f"Agent {self.config.agent_id} entering fallback mode: {error}")
        
        return AnalysisResult(
            success=False,
            errors=[f"Agent temporarily unavailable: {error}"],
            confidence=ConfidenceLevel.LOW,
            metadata={
                "fallback_triggered": True,
                "original_error": error,
                "fallback_timestamp": datetime.utcnow().isoformat()
            }
        )
        
    async def health_check(self) -> Dict[str, Any]:
        """Agent health check endpoint"""
        return {
            "agent_id": self.config.agent_id,
            "status": "healthy" if self.circuit_breaker.state == CircuitBreakerState.CLOSED else "degraded",
            "circuit_breaker_state": self.circuit_breaker.state.value,
            "failure_count": self.circuit_breaker.failure_count,
            "performance_metrics": await self.get_performance_summary()
        }
