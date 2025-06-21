"""API endpoint initialization"""
from fastapi import APIRouter
from .agents import router as agents_router

# Create main API router
router = APIRouter(prefix="/api/v1")

# Include all endpoint routers
router.include_router(agents_router)

# Health check endpoint
@router.get("/health")
async def health_check():
    return {"status": "healthy", "service": "palmer-ai-agents"}
