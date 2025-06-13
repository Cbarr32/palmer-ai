"""Palmer AI Conversational B2B Platform - Powered by Claude Sonnet 4"""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager

from .config import settings
from .utils.logger import get_logger, setup_logging
from .api.endpoints import router as api_router
from .api.endpoints.b2b_distributors import router as b2b_router
from .api.endpoints.conversational_b2b import router as palmer_router

# Setup logging
setup_logging()
logger = get_logger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifecycle"""
    logger.info(f"Starting Palmer AI B2B Platform {settings.app_version}")
    logger.info(f"Powered by Claude Sonnet 4: {settings.anthropic_model}")
    logger.info(f"Conversational Intelligence: ENABLED")
    print("🤖 Palmer AI Conversational B2B Platform - Ready for distributors!")
    yield
    logger.info("Shutting down Palmer AI B2B Platform")

# Create FastAPI app
app = FastAPI(
    title="Palmer AI Conversational B2B Intelligence Platform",
    description=(
        "🤖 **Conversational AI-Powered Product Intelligence for B2B Distributors**\n\n"
        "**Powered by Claude Sonnet 4** - Advanced conversational AI for business\n\n"
        "**Flexible Input Methods:**\n"
        "• 💬 Natural language conversations\n"
        "• 📊 Excel/CSV file uploads\n"
        "• 🔗 Manufacturer website extraction\n"
        "• 📝 Product lists and mixed requests\n\n"
        "**Target Market**: $7.6 trillion wholesale trade opportunity\n\n"
        "Built with love in memory of Mia Palmer Barreto 💜"
    ),
    version=settings.app_version,
    lifespan=lifespan
)

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
    """Welcome to Palmer AI Conversational B2B Platform"""
    return {
        "message": "Welcome to Palmer AI Conversational B2B Intelligence Platform",
        "tagline": "Flexible AI-Powered Product Intelligence for Distributors",
        "version": settings.app_version,
        "ai_engine": f"Claude Sonnet 4 ({settings.anthropic_model})",
        "key_features": [
            "🤖 Conversational AI that adapts to your workflow",
            "📊 Upload Excel/CSV files for instant enhancement",
            "🔗 Extract from manufacturer websites", 
            "💬 Natural language product intelligence",
            "🎯 Industry-specific optimization"
        ],
        "target_market": "$7.6 trillion wholesale trade opportunity",
        "subscription_tiers": {
            "starter": f"${settings.subscription_tiers['starter']['monthly_price']}/month",
            "professional": f"${settings.subscription_tiers['professional']['monthly_price']}/month", 
            "enterprise": f"${settings.subscription_tiers['enterprise']['monthly_price']}/month"
        },
        "documentation": "/docs",
        "conversational_ai": "/palmer"
    }

@app.get("/health")
async def health():
    """Health check endpoint"""
    return {
        "status": "healthy", 
        "platform": "Palmer AI Conversational B2B Intelligence",
        "ai_engine": {
            "model": settings.anthropic_model,
            "version": "Claude Sonnet 4"
        },
        "features": {
            "conversational_ai": True,
            "file_uploads": True,
            "url_extraction": True,
            "b2b_optimization": True
        }
    }

@app.post("/test-palmer")
async def test_palmer_conversation(request: dict):
    """Quick test endpoint"""
    message = request.get("message", "Hello!")
    
    responses = {
        "hello": "Hello! I'm Palmer AI. I can help with Excel uploads, manufacturer extraction, and product optimization.",
        "help": "I can help with: 📊 Excel/CSV analysis, 🔗 Website extraction, 💬 Product optimization, 🎯 Strategic guidance.",
        "upload": "Upload Excel (.xlsx) or CSV files and I'll enhance your product data instantly!"
    }
    
    for keyword, response in responses.items():
        if keyword in message.lower():
            return {
                "user_message": message,
                "palmer_response": response,
                "next_steps": "Try /palmer/chat or /palmer/upload-and-chat"
            }
    
    return {
        "user_message": message,
        "palmer_response": f"Thanks for saying: '{message}'. I'm here to help with product intelligence!",
        "suggested_messages": ["help", "upload file", "extract from website"]
    }
