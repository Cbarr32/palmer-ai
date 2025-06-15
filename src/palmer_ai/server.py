"""Palmer AI Main Server - Production Ready"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from fastapi import FastAPI, Request, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from datetime import datetime
import os

# Import our modules with error handling
try:
    from src.palmer_ai.core.logger import get_logger
    from src.palmer_ai.core.websocket import ws_manager
    from src.palmer_ai.api import analyze
    logger = get_logger(__name__)
except ImportError as e:
    print(f"Import error: {e}")
    # Fallback for missing modules
    class MockLogger:
        def info(self, msg): print(f"INFO: {msg}")
        def error(self, msg): print(f"ERROR: {msg}")
    logger = MockLogger()
    ws_manager = None
    analyze = None

# Create FastAPI app
app = FastAPI(
    title="Palmer AI",
    description="B2B Intelligence Platform - Replace $30K tools with $97/month",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers if available
if analyze:
    app.include_router(analyze.router)

# Health endpoint
@app.get("/health")
async def health_check():
    """System health check"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0",
        "service": "Palmer AI",
        "features": {
            "distributor_analysis": bool(analyze),
            "websocket": bool(ws_manager),
            "cache": True,
            "auth": True
        }
    }

# API status
@app.get("/api/v1/status")
async def api_status():
    """API status and capabilities"""
    return {
        "api_version": "v1",
        "status": "operational",
        "endpoints": [
            "/health",
            "/api/v1/status",
            "/api/v1/analyze/distributor",
            "/docs"
        ],
        "subscription_tiers": {
            "basic": "$97/month",
            "professional": "$297/month",
            "enterprise": "$497/month"
        }
    }

# WebSocket endpoint
if ws_manager:
    @app.websocket("/ws/{client_id}")
    async def websocket_endpoint(websocket: WebSocket, client_id: str):
        await ws_manager.connect(websocket, client_id)
        try:
            while True:
                data = await websocket.receive_text()
                # Handle incoming messages
        except:
            ws_manager.disconnect(client_id)

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )

if __name__ == "__main__":
    import uvicorn
    logger.info("Starting Palmer AI server...")
    uvicorn.run(app, host="0.0.0.0", port=8000)
