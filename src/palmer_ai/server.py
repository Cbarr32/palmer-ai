"""
Palmer AI FastAPI Server
Production-ready B2B intelligence platform
"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
import os
from datetime import datetime

from src.palmer_ai.api import analyze
from src.palmer_ai.core.logger import get_logger
from src.palmer_ai.core.websocket import ws_manager

logger = get_logger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Palmer AI",
    description="B2B Intelligence Platform for Industrial Distributors",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Add your domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
if os.path.exists("frontend/out"):
    app.mount("/static", StaticFiles(directory="frontend/out"), name="static")

# Include routers
app.include_router(analyze.router)

# WebSocket endpoint
@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket, client_id: str):
    await ws_manager.connect(websocket, client_id)
    try:
        while True:
            data = await websocket.receive_text()
            # Handle WebSocket messages
    except:
        ws_manager.disconnect(client_id)

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0",
        "service": "Palmer AI"
    }

@app.get("/api/v1/status")
async def api_status():
    """API status endpoint"""
    return {
        "api_version": "v1",
        "endpoints_available": [
            "/api/v1/analyze/distributor",
            "/api/v1/analyze/status/{job_id}",
            "/api/v1/analyze/history"
        ],
        "features": {
            "quick_analysis": True,
            "deep_analysis": True,
            "competitor_comparison": True,
            "real_time_updates": True
        }
    }

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Global exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error",
            "timestamp": datetime.utcnow().isoformat()
        }
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
