"""Palmer AI Configuration - Focused on Competitive Intelligence"""
from pydantic_settings import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    # App
    app_name: str = "Palmer AI"
    app_version: str = "2.0.0"
    environment: str = "development"
    
    # API Keys
    anthropic_api_key: str = os.getenv("ANTHROPIC_API_KEY", "")
    openai_api_key: Optional[str] = os.getenv("OPENAI_API_KEY", "")
    
    # Database
    database_url: str = "sqlite:///./palmer_competitive_intel.db"
    redis_url: str = "redis://localhost:6379"
    
    # Security
    secret_key: str = os.getenv("SECRET_KEY", "your-secret-key-change-this")
    
    # Competitive Intelligence Settings
    monitoring_interval: int = 300  # 5 minutes
    max_competitors_per_user: int = 20
    insight_cache_ttl: int = 3600  # 1 hour
    
    # Pricing Tiers
    tier_limits: dict = {
        "starter": {"competitors": 5, "checks_per_day": 24},
        "professional": {"competitors": 20, "checks_per_day": 144},
        "enterprise": {"competitors": -1, "checks_per_day": -1}
    }
    
    class Config:
        env_file = ".env"

settings = Settings()
