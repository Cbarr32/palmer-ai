"""3-Message Conversion Hook - Core Business Logic"""
from typing import Dict, Any, Optional
from datetime import datetime, timedelta
import json
import hashlib
from fastapi import HTTPException

from ..utils.logger import get_logger
from ..config import settings

logger = get_logger(__name__)

class ConversionHookService:
    """Implements the 3-message hook to convert free users"""
    
    def __init__(self):
        # In production, use Redis. For now, in-memory
        self._message_counts: Dict[str, Dict[str, Any]] = {}
        self._conversion_triggers = {
            1: self._first_message_hook,
            2: self._second_message_hook,
            3: self._third_message_hook
        }
    
    def get_session_id(self, identifier: str) -> str:
        """Generate consistent session ID from email/IP/etc"""
        return hashlib.md5(identifier.encode()).hexdigest()
    
    async def track_message(self, session_id: str, message_type: str = "analysis") -> Dict[str, Any]:
        """Track message and return hook data"""
        if session_id not in self._message_counts:
            self._message_counts[session_id] = {
                "count": 0,
                "first_seen": datetime.utcnow(),
                "last_seen": datetime.utcnow(),
                "converted": False,
                "messages": []
            }
        
        session = self._message_counts[session_id]
        session["count"] += 1
        session["last_seen"] = datetime.utcnow()
        session["messages"].append({
            "type": message_type,
            "timestamp": datetime.utcnow().isoformat()
        })
        
        logger.info(f"Session {session_id}: Message {session['count']}/3")
        
        # Get appropriate hook
        hook_func = self._conversion_triggers.get(session["count"], self._beyond_third_message)
        hook_data = await hook_func(session_id, session)
        
        return {
            "message_count": session["count"],
            "max_free_messages": 3,
            "hook_data": hook_data,
            "session_id": session_id
        }
    
    async def _first_message_hook(self, session_id: str, session: Dict[str, Any]) -> Dict[str, Any]:
        """First message: Shock with impressive intelligence"""
        return {
            "stage": "shock",
            "message": "Impressive intelligence delivered! You have 2 more free analyses today.",
            "show_value": True,
            "upgrade_prompt": None,
            "features_shown": ["basic_analysis", "competitor_identification"],
            "next_teaser": "Next analysis will include pricing intelligence..."
        }
    
    async def _second_message_hook(self, session_id: str, session: Dict[str, Any]) -> Dict[str, Any]:
        """Second message: Deeper value + urgency"""
        return {
            "stage": "deeper_value",
            "message": "Enhanced intelligence with pricing insights! 1 free analysis remaining.",
            "show_value": True,
            "upgrade_prompt": None,
            "features_shown": ["pricing_intelligence", "market_positioning", "growth_indicators"],
            "next_teaser": "Final analysis unlocks decision-maker contacts and strategic recommendations..."
        }
    
    async def _third_message_hook(self, session_id: str, session: Dict[str, Any]) -> Dict[str, Any]:
        """Third message: Maximum value + conversion trigger"""
        return {
            "stage": "conversion",
            "message": "⚡ You've experienced Palmer AI's full power!",
            "show_value": True,
            "upgrade_prompt": {
                "title": "Unlock Unlimited Intelligence",
                "message": "Get unlimited company analyses, API access, and priority support.",
                "cta": "Upgrade Now - $97/month",
                "benefits": [
                    "Unlimited company analyses",
                    "Real-time monitoring",
                    "API access for integrations",
                    "Bulk analysis tools",
                    "Priority support"
                ],
                "urgency": "🔥 Special offer: 20% off first month with code INTELLIGENCE20"
            },
            "features_shown": ["decision_makers", "strategic_recommendations", "integration_options"],
            "conversion_required": True
        }
    
    async def _beyond_third_message(self, session_id: str, session: Dict[str, Any]) -> Dict[str, Any]:
        """Beyond third message: Require upgrade"""
        if not session.get("converted"):
            raise HTTPException(
                status_code=403,
                detail={
                    "error": "Free analysis limit reached",
                    "message": "You've used all 3 free analyses for today.",
                    "upgrade_required": True,
                    "upgrade_url": "/pricing",
                    "cta": "Upgrade to Palmer AI Pro for unlimited access"
                }
            )
        return {
            "stage": "paid_user",
            "message": "Welcome to Palmer AI Pro!",
            "unlimited": True
        }
    
    def check_rate_limit(self, session_id: str) -> bool:
        """Check if user has messages remaining"""
        if session_id not in self._message_counts:
            return True
        
        session = self._message_counts[session_id]
        if session.get("converted"):
            return True
            
        # Reset count if last message was >24 hours ago
        if session["last_seen"] < datetime.utcnow() - timedelta(hours=24):
            session["count"] = 0
            return True
            
        return session["count"] < 3

# Singleton instance
conversion_hook = ConversionHookService()
