"""Production middleware for Palmer AI API"""
import time
import uuid
from typing import Callable
from fastapi import Request, Response
from fastapi.middleware.base import BaseHTTPMiddleware

from ..utils.logger import get_logger
from ..utils.metrics import metrics_collector
from ..utils.security import security_validator

logger = get_logger(__name__)

class MetricsMiddleware(BaseHTTPMiddleware):
    """Middleware to collect API metrics"""
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        start_time = time.time()
        request_id = str(uuid.uuid4())
        
        # Add request ID to headers
        request.state.request_id = request_id
        
        # Process request
        response = await call_next(request)
        
        # Record metrics
        duration = time.time() - start_time
        metrics_collector.record_api_request(
            endpoint=request.url.path,
            method=request.method,
            status_code=response.status_code,
            duration=duration
        )
        
        # Add response headers
        response.headers["X-Request-ID"] = request_id
        response.headers["X-Response-Time"] = f"{duration:.3f}s"
        
        # Log request
        logger.info(
            f"API Request: {request.method} {request.url.path} "
            f"Status: {response.status_code} Duration: {duration:.3f}s "
            f"Request-ID: {request_id}"
        )
        
        return response

class SecurityMiddleware(BaseHTTPMiddleware):
    """Security middleware for input validation"""
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Validate request size
        if hasattr(request, 'headers') and 'content-length' in request.headers:
            content_length = int(request.headers['content-length'])
            if content_length > 50 * 1024 * 1024:  # 50MB limit
                return Response(
                    content="Request too large",
                    status_code=413
                )
        
        # Add security headers to response
        response = await call_next(request)
        
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        
        return response
