"""
Palmer AI Server - Working Version
Real intelligence that actually works
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime

from src.palmer_ai.api.working_api import router
from src.palmer_ai.core.logger import get_logger

logger = get_logger(__name__)

app = FastAPI(
    title="Palmer AI - Working Intelligence",
    description="""
    Real competitive intelligence that actually works.
    
    What it does:
    - Scrapes competitor websites
    - Extracts insights using AI
    - Finds patterns in historical data  
    - Generates actionable recommendations
    
    Simple. Practical. Valuable.
    """,
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

@app.get("/")
async def root():
    return {
        "message": "Palmer AI Working Intelligence",
        "status": "ready",
        "endpoints": [
            "/api/v1/analyze - Analyze a competitor",
            "/api/v1/setup - Configure AI",
            "/api/v1/health - Check system health",
            "/docs - API documentation"
        ]
    }

if __name__ == "__main__":
    import uvicorn
    logger.info("Starting Palmer AI...")
    uvicorn.run(app, host="0.0.0.0", port=8000)
