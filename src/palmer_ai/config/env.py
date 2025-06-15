"""Environment configuration with secure API key management"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
project_root = Path(__file__).parent.parent.parent.parent
env_path = project_root / '.env'

# Load the .env file if it exists
if env_path.exists():
    load_dotenv(env_path)
else:
    print(f"Warning: .env file not found at {env_path}")

# API Keys
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Validate critical environment variables
if not OPENAI_API_KEY:
    print("Warning: OPENAI_API_KEY not found in environment variables")
    print("Please ensure .env file exists with OPENAI_API_KEY set")

# Other configuration
API_BASE_URL = os.getenv('API_BASE_URL', 'http://localhost:8000')
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'

# Export for easy access
__all__ = ['OPENAI_API_KEY', 'API_BASE_URL', 'DEBUG']
