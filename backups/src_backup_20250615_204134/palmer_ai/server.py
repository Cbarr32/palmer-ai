"""Palmer AI Main Server - B2B Intelligence Platform"""
import os
import sys
import asyncio
import logging
from datetime import datetime
from pathlib import Path

# Add src to Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
import uvicorn

# Import configurations
from palmer_ai.config.env import (
    OPENAI_API_KEY, 
    ANTHROPIC_API_KEY, 
    API_BASE_URL, 
    DEBUG
)

# Import routers
from palmer_ai.api.complete import router as complete_router
from palmer_ai.api.gtm_suite import router as gtm_router
from palmer_ai.api.working_api import router as working_router

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('data/logs/palmer_ai.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Palmer AI - B2B Intelligence Platform",
    description="AI-powered business analysis platform that beats $30K enterprise tools",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount routers
app.include_router(complete_router, prefix="/api/v1", tags=["Complete"])
app.include_router(gtm_router, prefix="/api/v1/gtm", tags=["GTM Suite"])
app.include_router(working_router, prefix="/api/v1/working", tags=["Working"])

# Health check endpoint
@app.get("/health")
async def health_check():
    """System health check with service status"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "services": {
            "api": "running",
            "openai": "configured" if OPENAI_API_KEY else "missing",
            "anthropic": "configured" if ANTHROPIC_API_KEY else "missing",
            "version": "1.0.0"
        }
    }

# Root endpoint
@app.get("/")
async def root():
    """Palmer AI API root endpoint"""
    return {
        "message": "Palmer AI - B2B Intelligence Platform",
        "documentation": f"{API_BASE_URL}/docs",
        "health": f"{API_BASE_URL}/health",
        "tagline": "Beat $30K enterprise tools with $97/month AI"
    }

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Global exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "message": str(exc) if DEBUG else "An error occurred",
            "timestamp": datetime.now().isoformat()
        }
    )

# Startup event
@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    logger.info("🚀 Palmer AI starting up...")
    
    # Create necessary directories
    os.makedirs("data/logs", exist_ok=True)
    os.makedirs("data/cache", exist_ok=True)
    os.makedirs("data/excel", exist_ok=True)
    os.makedirs("data/reports", exist_ok=True)
    
    # Log configuration status
    logger.info(f"✅ OpenAI API: {'Configured' if OPENAI_API_KEY else 'Missing'}")
    logger.info(f"✅ Anthropic API: {'Configured' if ANTHROPIC_API_KEY else 'Missing'}")
    logger.info(f"✅ Debug mode: {DEBUG}")
    
    logger.info("🎯 Palmer AI ready to beat enterprise tools!")

# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    logger.info("👋 Palmer AI shutting down...")

if __name__ == "__main__":
    # Ensure data directories exist
    os.makedirs("data/logs", exist_ok=True)
    
    # Start server
    logger.info("Starting Palmer AI server...")
    uvicorn.run(
        "palmer_ai.server:app",
        host="0.0.0.0",
        port=8000,
        reload=DEBUG,
        log_level="info"
    )
