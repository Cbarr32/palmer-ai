"""Production Palmer AI Server with Enhanced Middleware"""
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, PlainTextResponse
from contextlib import asynccontextmanager
import uvicorn

from .config import settings
from .utils.logger import get_logger, setup_logging
from .utils.metrics import metrics_collector
from .api.middleware import MetricsMiddleware, SecurityMiddleware
from .api.endpoints import router as api_router
from .api.endpoints.b2b_distributors import router as b2b_router
from .api.endpoints.conversational_b2b import router as palmer_router

# Setup logging
setup_logging()
logger = get_logger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Enhanced application lifecycle management"""
    logger.info(f"🚀 Palmer AI Production Server {settings.app_version}")
    logger.info(f"🤖 AI Engine: {settings.anthropic_model}")
    logger.info(f"🔧 Environment: {settings.environment}")
    logger.info(f"🛡️ Security: Enhanced")
    logger.info(f"📊 Metrics: Enabled")
    
    # Initialize metrics collection
    await metrics_collector.start() if hasattr(metrics_collector, 'start') else None
    
    yield
    
    logger.info("🛑 Palmer AI Production Server shutting down")
    await metrics_collector.stop() if hasattr(metrics_collector, 'stop') else None

# Create FastAPI app with production configuration
app = FastAPI(
    title="Palmer AI Production Platform",
    description="🤖 **Production AI-Powered B2B Intelligence Platform**\n\n"
                "Powered by Claude Sonnet 4 with enterprise-grade reliability",
    version=settings.app_version,
    lifespan=lifespan,
    docs_url="/docs" if settings.debug else None,
    redoc_url="/redoc" if settings.debug else None
)

# Add production middleware
app.add_middleware(SecurityMiddleware)
app.add_middleware(MetricsMiddleware)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(api_router)
app.include_router(b2b_router)
app.include_router(palmer_router)

@app.get("/")
async def root():
    """Production root endpoint"""
    return {
        "service": "Palmer AI Production Platform",
        "version": settings.app_version,
        "status": "operational",
        "ai_engine": f"Claude Sonnet 4 ({settings.anthropic_model})",
        "features": [
            "🤖 Conversational AI with production reliability",
            "📊 Real-time metrics and monitoring", 
            "🛡️ Enterprise security and validation",
            "⚡ Circuit breaker and retry patterns",
            "🔍 Comprehensive health monitoring"
        ],
        "endpoints": {
            "health": "/health",
            "metrics": "/metrics",
            "chat": "/palmer/chat",
            "upload": "/palmer/upload-and-chat",
            "docs": "/docs" if settings.debug else "disabled"
        }
    }

@app.get("/health")
async def enhanced_health():
    """Comprehensive health check"""
    from .agents.coordination.coordinator import coordinator
    
    try:
        # Check agent health
        agent_health = await coordinator.get_agent_performance()
        
        health_data = {
            "status": "healthy",
            "timestamp": "2025-06-13T22:00:00Z",
            "version": settings.app_version,
            "environment": settings.environment,
            "components": {
                "api": "healthy",
                "agents": "healthy" if agent_health else "degraded",
                "ai_engine": "healthy",
                "metrics": "enabled",
                "security": "enabled"
            },
            "metrics_summary": metrics_collector.get_summary(),
            "agent_status": agent_health
        }
        
        return health_data
        
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return JSONResponse(
            status_code=503,
            content={
                "status": "unhealthy",
                "error": str(e),
                "timestamp": "2025-06-13T22:00:00Z"
            }
        )

@app.get("/metrics", response_class=PlainTextResponse)
async def metrics_endpoint():
    """Prometheus metrics endpoint"""
    return metrics_collector.get_prometheus_metrics()

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler with metrics"""
    request_id = getattr(request.state, 'request_id', 'unknown')
    
    logger.error(f"Unhandled exception for request {request_id}: {str(exc)}")
    metrics_collector.increment_counter("palmer_ai_unhandled_exceptions")
    
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "request_id": request_id,
            "message": "An unexpected error occurred"
        }
    )

if __name__ == "__main__":
    uvicorn.run(
        "palmer_ai.server_production:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug,
        log_level=settings.log_level.lower()
    )
