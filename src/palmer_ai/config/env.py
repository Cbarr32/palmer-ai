"""Palmer AI Enhanced Environment Configuration"""
import os
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
project_root = Path(__file__).parent.parent.parent.parent
env_path = project_root / '.env'

if env_path.exists():
    load_dotenv(env_path)
    logger.info(f"✅ Loaded environment from: {env_path}")
else:
    logger.warning(f"⚠️  No .env file found at: {env_path}")

# API Keys
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')

# Validate API keys
if not OPENAI_API_KEY:
    logger.warning("⚠️  OPENAI_API_KEY not configured")
else:
    logger.info(f"✅ OpenAI API key loaded ({len(OPENAI_API_KEY)} chars)")

if not ANTHROPIC_API_KEY:
    logger.warning("⚠️  ANTHROPIC_API_KEY not configured")
else:
    logger.info(f"✅ Anthropic API key loaded ({len(ANTHROPIC_API_KEY)} chars)")

# Application Configuration
API_BASE_URL = os.getenv('API_BASE_URL', 'http://localhost:8000')
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')

# Database Configuration
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://palmer:palmer123@localhost/palmer_ai')
REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379')

# Security
SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'dev-jwt-secret')

# Export all configuration
__all__ = [
    'OPENAI_API_KEY', 'ANTHROPIC_API_KEY', 'API_BASE_URL', 'DEBUG',
    'ENVIRONMENT', 'DATABASE_URL', 'REDIS_URL', 'SECRET_KEY', 'JWT_SECRET_KEY'
]

def get_ai_client(provider: str = "openai"):
    """Get configured AI client based on provider"""
    if provider == "openai":
        if not OPENAI_API_KEY:
            raise ValueError("OpenAI API key not configured")
        import openai
        return openai.Client(api_key=OPENAI_API_KEY)
    elif provider == "anthropic":
        if not ANTHROPIC_API_KEY:
            raise ValueError("Anthropic API key not configured")
        import anthropic
        return anthropic.Client(api_key=ANTHROPIC_API_KEY)
    else:
        raise ValueError(f"Unknown AI provider: {provider}")
