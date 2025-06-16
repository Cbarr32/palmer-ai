"""Palmer AI Environment Configuration - Complete Fix"""
import os
import sys
import logging
from pathlib import Path
from typing import Optional

# Try to import dotenv, fallback if not available
try:
    from dotenv import load_dotenv
except ImportError:
    print("Warning: python-dotenv not installed, using environment variables only")
    load_dotenv = None

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('logs/server.log', mode='a')
    ]
)
logger = logging.getLogger(__name__)

def find_env_file() -> Optional[Path]:
    """Search for .env file in project hierarchy"""
    current = Path(__file__).parent
    for _ in range(5):
        env_path = current / '.env'
        if env_path.exists():
            return env_path
        current = current.parent
    return None

def load_environment() -> bool:
    """Load environment variables from .env file"""
    if load_dotenv is None:
        logger.warning("python-dotenv not available, skipping .env loading")
        return False
        
    env_path = find_env_file()
    if env_path:
        load_dotenv(env_path, override=True)
        logger.info(f"✅ Loaded environment from: {env_path}")
        return True
    else:
        logger.warning("⚠️ No .env file found, using system environment")
        return False

# Auto-load environment
load_environment()

# Core Configuration
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
DEBUG = ENVIRONMENT == "development"
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")

# API Keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")

# Log API key status
if OPENAI_API_KEY:
    logger.info(f"✅ OpenAI API key loaded ({len(OPENAI_API_KEY)} chars)")
else:
    logger.warning("⚠️ No OpenAI API key found")

if ANTHROPIC_API_KEY:
    logger.info(f"✅ Anthropic API key loaded ({len(ANTHROPIC_API_KEY)} chars)")
else:
    logger.warning("⚠️ No Anthropic API key found")

# Server Configuration
PORT = int(os.getenv("PORT", "8000"))
HOST = os.getenv("HOST", "0.0.0.0")

# Database Configuration
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./palmer_ai.db")
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")

# Security
SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "dev-jwt-secret-change-in-production")

# Feature Flags
ENABLE_WEBSOCKET = os.getenv("ENABLE_WEBSOCKET", "true").lower() == "true"
ENABLE_CACHE = os.getenv("ENABLE_CACHE", "true").lower() == "true"

# Export all
__all__ = [
    "load_environment",
    "ENVIRONMENT",
    "DEBUG",
    "API_BASE_URL",
    "OPENAI_API_KEY",
    "ANTHROPIC_API_KEY",
    "PORT",
    "HOST",
    "DATABASE_URL",
    "REDIS_URL",
    "SECRET_KEY",
    "JWT_SECRET_KEY",
    "ENABLE_WEBSOCKET",
    "ENABLE_CACHE"
]
