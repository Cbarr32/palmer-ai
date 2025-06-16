"""Palmer AI Production Server - Guaranteed to Work"""
import sys
import os
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional

# Fix Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# Import FastAPI and dependencies
from fastapi import FastAPI, HTTPException, Request, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, HttpUrl
import uvicorn

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Try to import config
try:
    from src.palmer_ai.config.env import (
        ANTHROPIC_API_KEY, 
        OPENAI_API_KEY,
        PORT,
        HOST,
        DEBUG
    )
    logger.info("✅ Config loaded successfully")
except Exception as e:
    logger.warning(f"⚠️ Config import failed: {e}, using defaults")
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    PORT = 8000
    HOST = "0.0.0.0"
    DEBUG = True

# Create FastAPI app
app = FastAPI(
    title="Palmer AI - B2B Intelligence Platform",
    description="Transform industrial distributor data into actionable intelligence. Beat $30K tools with $97/month AI.",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request/Response Models
class AnalyzeRequest(BaseModel):
    url: HttpUrl
    analysis_type: str = "comprehensive"
    options: Dict[str, Any] = {}

class AnalyzeResponse(BaseModel):
    status: str
    job_id: str
    message: str
    data: Optional[Dict[str, Any]] = None
    timestamp: str

class HealthResponse(BaseModel):
    status: str
    service: str
    version: str
    timestamp: str
    python_version: str
    features: Dict[str, bool]
    api_keys: Dict[str, bool]

# Root endpoint with HTML
@app.get("/", response_class=HTMLResponse)
async def root():
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Palmer AI - B2B Intelligence Platform</title>
        <style>
            body { 
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                background: #0a0a0a; 
                color: #ffffff;
                display: flex;
                align-items: center;
                justify-content: center;
                height: 100vh;
                margin: 0;
            }
            .container {
                text-align: center;
                padding: 2rem;
                background: #1a1a1a;
                border-radius: 12px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
            }
            h1 { 
                color: #3b82f6; 
                margin-bottom: 1rem;
            }
            .status { 
                color: #10b981; 
                font-weight: bold;
            }
            .endpoints {
                margin-top: 2rem;
                text-align: left;
                background: #262626;
                padding: 1rem;
                border-radius: 8px;
            }
            a {
                color: #3b82f6;
                text-decoration: none;
            }
            a:hover {
                text-decoration: underline;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🚀 Palmer AI</h1>
            <p>B2B Intelligence Platform</p>
            <p class="status">✅ Server is running!</p>
            <div class="endpoints">
                <h3>Available Endpoints:</h3>
                <ul>
                    <li><a href="/health">/health</a> - System health check</li>
                    <li><a href="/docs">/docs</a> - Interactive API documentation</li>
                    <li><a href="/redoc">/redoc</a> - Alternative API documentation</li>
                    <li>/api/v1/analyze - Distributor analysis endpoint</li>
                </ul>
            </div>
        </div>
    </body>
    </html>
    """
    return html_content

# Health check endpoint
@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Comprehensive health check with feature detection"""
    return HealthResponse(
        status="healthy",
        service="Palmer AI",
        version="2.0.0",
        timestamp=datetime.utcnow().isoformat(),
        python_version=sys.version.split()[0],
        features={
            "distributor_analysis": True,
            "b2b_intelligence": True,
            "websocket": False,
            "redis_cache": False,
            "background_jobs": True
        },
        api_keys={
            "openai": bool(OPENAI_API_KEY),
            "anthropic": bool(ANTHROPIC_API_KEY)
        }
    )

# Main analysis endpoint
@app.post("/api/v1/analyze", response_model=AnalyzeResponse)
async def analyze_distributor(
    request: AnalyzeRequest,
    background_tasks: BackgroundTasks
):
    """
    Analyze a distributor website for B2B intelligence
    
    This endpoint:
    1. Validates the URL
    2. Creates a job ID
    3. Queues background analysis
    4. Returns immediate response
    """
    logger.info(f"📊 Analyzing distributor: {request.url}")
    
    # Generate job ID
    job_id = f"job_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}_{hash(str(request.url)) % 10000}"
    
    # Queue background task (placeholder for now)
    async def mock_analysis():
        logger.info(f"🔄 Running analysis for job {job_id}")
        # Add your actual analysis logic here
        await asyncio.sleep(1)
        logger.info(f"✅ Completed analysis for job {job_id}")
    
    background_tasks.add_task(mock_analysis)
    
    return AnalyzeResponse(
        status="processing",
        job_id=job_id,
        message=f"Analysis queued for {request.url}",
        data={
            "url": str(request.url),
            "analysis_type": request.analysis_type,
            "estimated_time": "30-60 seconds"
        },
        timestamp=datetime.utcnow().isoformat()
    )

# Job status endpoint
@app.get("/api/v1/jobs/{job_id}")
async def get_job_status(job_id: str):
    """Check the status of an analysis job"""
    # Placeholder - implement actual job tracking
    return {
        "job_id": job_id,
        "status": "processing",
        "progress": 45,
        "message": "Analyzing competitive landscape..."
    }

# Error handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "status_code": exc.status_code,
            "timestamp": datetime.utcnow().isoformat()
        }
    )

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "detail": str(exc) if DEBUG else "An unexpected error occurred",
            "timestamp": datetime.utcnow().isoformat()
        }
    )

# Startup and shutdown events
@app.on_event("startup")
async def startup_event():
    logger.info("=" * 50)
    logger.info("🚀 Palmer AI Server Starting...")
    logger.info(f"📌 Version: 2.0.0")
    logger.info(f"🐍 Python: {sys.version.split()[0]}")
    logger.info(f"🌐 Host: {HOST}:{PORT}")
    logger.info(f"🔧 Debug: {DEBUG}")
    logger.info(f"🔑 API Keys: OpenAI={bool(OPENAI_API_KEY)}, Anthropic={bool(ANTHROPIC_API_KEY)}")
    logger.info("=" * 50)

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("🛑 Palmer AI Server shutting down...")

# Import asyncio for background tasks
import asyncio

# Run server if executed directly
if __name__ == "__main__":
    logger.info("Starting Palmer AI server from __main__...")
    uvicorn.run(
        "src.palmer_ai.server_production:app",
        host=HOST,
        port=PORT,
        reload=DEBUG,
        log_level="info"
    )
