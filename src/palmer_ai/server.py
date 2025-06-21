"""Palmer AI - Direct Klue Competitor
Competitive Intelligence at 1/300th the cost
"""
import os
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import our focused modules
from palmer_ai.core.config import settings
from palmer_ai.api.intelligence import router as intelligence_router
from palmer_ai.api.monitoring import router as monitoring_router
from palmer_ai.api.auth import router as auth_router, get_current_user
from palmer_ai.services.competitive_intel import CompetitiveIntelService

# Lifespan management
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("🚀 Palmer AI Competitive Intelligence starting...")
    yield
    # Shutdown
    logger.info("👋 Palmer AI shutting down...")

# Create focused app
app = FastAPI(
    title="Palmer AI - Competitive Intelligence Platform",
    description="Beat Klue at 1/300th the price. Real-time competitive intelligence for B2B companies.",
    version="2.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://palmer-apps.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount routers
app.include_router(auth_router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(intelligence_router, prefix="/api/v1/intel", tags=["Intelligence"])
app.include_router(monitoring_router, prefix="/api/v1/monitor", tags=["Monitoring"])

@app.get("/")
async def root():
    """Root endpoint with product focus"""
    return {
        "product": "Palmer AI Competitive Intelligence",
        "tagline": "Beat Klue at 1/300th the price",
        "value_props": [
            "Real-time competitor monitoring",
            "AI-powered insight extraction",
            "Zero integration required",
            "Start in 5 minutes"
        ],
        "pricing": {
            "starter": "$97/month",
            "professional": "$297/month",
            "enterprise": "$497/month"
        },
        "vs_klue": {
            "klue_price": "$30,000+/year",
            "palmer_price": "$1,164/year",
            "savings": "96%"
        }
    }

@app.get("/health")
async def health_check():
    """Health check with service status"""
    return {
        "status": "healthy",
        "service": "Palmer AI Competitive Intelligence",
        "timestamp": datetime.utcnow().isoformat(),
        "capabilities": {
            "competitor_monitoring": "active",
            "insight_extraction": "active",
            "alert_system": "active",
            "api_access": "active"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
