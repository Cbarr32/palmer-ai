"""Palmer AI Product Description Optimizer Server"""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, HTMLResponse
from contextlib import asynccontextmanager

from .config import settings
from .utils.logger import get_logger, setup_logging
from .api.endpoints.b2b_distributors import router as b2b_router
from .api.endpoints.conversational_b2b import router as palmer_router
from .api.endpoints.product_descriptions import router as products_router

# Setup logging
setup_logging()
logger = get_logger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifecycle"""
    logger.info(f"Starting Palmer AI Product Description Optimizer")
    logger.info(f"Version: {settings.app_version}")
    print("🤖 Palmer AI - Ready to optimize product descriptions!")
    yield
    logger.info("Shutting down Palmer AI")

# Create FastAPI app
app = FastAPI(
    title="Palmer AI Product Description Optimizer",
    description="Transform product data into descriptions that sell",
    version=settings.app_version,
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(b2b_router)
app.include_router(palmer_router)
app.include_router(products_router)

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Palmer AI Product Description Optimizer",
        "description": "Transform boring product data into compelling descriptions",
        "endpoints": {
            "optimize_single": "/api/v1/products/optimize",
            "upload_excel": "/api/v1/products/upload-excel",
            "chat": "/palmer/chat",
            "docs": "/docs"
        }
    }

@app.get("/health")
async def health():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "Palmer AI",
        "version": settings.app_version
    }
