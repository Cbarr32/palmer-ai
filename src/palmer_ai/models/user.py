"""User model"""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class User(BaseModel):
    id: str
    email: str
    subscription_tier: str = "starter"
    created_at: Optional[datetime] = None
    is_active: bool = True
