"""Simple auth for the competitive intel platform"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import Optional
from datetime import datetime, timedelta
from jose import JWTError, jwt

from palmer_ai.core.config import settings

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token")

# Simplified for demo - in production use proper user model
class User(BaseModel):
    id: str
    email: str
    subscription_tier: str = "professional"

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(hours=24)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.secret_key, algorithm="HS256")

async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    """Get current user from token"""
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=["HS256"])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        # In production, load from database
        return User(id=user_id, email=f"{user_id}@example.com")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

@router.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """Simple login endpoint"""
    # In production, verify credentials
    # For now, accept any login
    access_token = create_access_token(data={"sub": form_data.username})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/signup")
async def signup(email: str, password: str):
    """Signup for Palmer AI"""
    # In production, create user in database
    access_token = create_access_token(data={"sub": email})
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "message": "Welcome to Palmer AI - Klue Killer!"
    }
