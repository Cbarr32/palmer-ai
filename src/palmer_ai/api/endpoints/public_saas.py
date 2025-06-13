# src/palmer_ai/api/endpoints/public_saas.py
"""Public SaaS endpoints for self-service Palmer AI platform"""
from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field, EmailStr
from datetime import datetime, timedelta
import uuid
import stripe
from passlib.context import CryptContext
from jose import JWTError, jwt

from ...config import settings
from ...utils.logger import get_logger

logger = get_logger(__name__)
router = APIRouter(prefix="/public", tags=["Public SaaS Platform"])

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Stripe configuration
stripe.api_key = settings.stripe_api_key

class UserSignup(BaseModel):
    email: EmailStr
    company_name: str
    industry: Optional[str] = None
    how_did_you_hear: Optional[str] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class TrialRequest(BaseModel):
    trial_type: str = Field(..., description="file_upload, url_extraction, or guided_tour")
    sample_data: Optional[Dict[str, Any]] = None

@router.post("/signup")
async def public_signup(signup: UserSignup) -> Dict[str, Any]:
    """Public self-service signup for Palmer AI"""
    try:
        # Generate user ID and API key
        user_id = str(uuid.uuid4())
        api_key = f"pk_live_{uuid.uuid4().hex[:32]}"
        
        # Create free trial account
        user_account = {
            "user_id": user_id,
            "email": signup.email,
            "company_name": signup.company_name,
            "industry": signup.industry,
            "plan": "free_trial",
            "api_key": api_key,
            "trial_expires": (datetime.utcnow() + timedelta(days=14)).isoformat(),
            "usage_limits": {
                "products_remaining": 50,
                "manufacturers_remaining": 1,
                "api_calls_remaining": 100
            },
            "created_at": datetime.utcnow().isoformat(),
            "onboarding_completed": False
        }
        
        # In production: Save to database
        logger.info(f"New signup: {signup.email} from {signup.company_name}")
        
        # Send welcome email (placeholder)
        await send_welcome_email(signup.email, user_account)
        
        return {
            "success": True,
            "user_id": user_id,
            "message": f"Welcome to Palmer AI, {signup.company_name}!",
            "trial_info": {
                "plan": "Free Trial",
                "expires": user_account["trial_expires"],
                "products_included": 50,
                "manufacturers_included": 1
            },
            "next_steps": [
                "Check your email for login credentials",
                "Try uploading a product file",
                "Extract products from a manufacturer website",
                "Explore AI enhancement features"
            ],
            "getting_started_url": "/public/getting-started",
            "dashboard_url": f"/dashboard?user_id={user_id}"
        }
        
    except Exception as e:
        logger.error(f"Signup failed: {str(e)}")
        raise HTTPException(status_code=500, detail="Signup failed. Please try again.")

@router.post("/trial/start")
async def start_trial(trial_request: TrialRequest, user_id: str) -> Dict[str, Any]:
    """Start a specific trial experience"""
    try:
        if trial_request.trial_type == "file_upload":
            return {
                "trial_type": "file_upload",
                "instructions": "Upload your Excel or CSV file below",
                "sample_file_url": "/samples/sample_product_catalog.xlsx",
                "expected_outcome": "See your products enhanced with AI-powered B2B descriptions",
                "time_estimate": "2-3 minutes",
                "upload_endpoint": "/palmer/upload-