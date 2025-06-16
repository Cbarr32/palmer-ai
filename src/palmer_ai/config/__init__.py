"""Palmer AI Configuration"""

from .env import load_environment

# Load environment on import
load_environment()

# Export common configurations
__all__ = ['load_environment']
