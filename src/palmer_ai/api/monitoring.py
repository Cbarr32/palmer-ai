"""Real-time Competitive Monitoring - The Klue Killer Feature"""
from fastapi import APIRouter, HTTPException, Depends, WebSocket, WebSocketDisconnect
from typing import Dict, Any, List
import asyncio
import json
from datetime import datetime

from palmer_ai.services.competitive_intel import competitive_intel_service
from palmer_ai.api.auth import get_current_user
from palmer_ai.models.user import User
from palmer_ai.utils.logger import get_logger

logger = get_logger(__name__)
router = APIRouter()

# WebSocket connection manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
    
    async def connect(self, user_id: str, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[user_id] = websocket
        logger.info(f"User {user_id} connected to monitoring")
    
    def disconnect(self, user_id: str):
        if user_id in self.active_connections:
            del self.active_connections[user_id]
            logger.info(f"User {user_id} disconnected from monitoring")
    
    async def send_update(self, user_id: str, message: dict):
        if user_id in self.active_connections:
            websocket = self.active_connections[user_id]
            await websocket.send_json(message)

manager = ConnectionManager()

@router.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    """Real-time monitoring WebSocket"""
    await manager.connect(user_id, websocket)
    
    try:
        while True:
            # Keep connection alive
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(user_id)

@router.post("/monitor/start")
async def start_monitoring(
    current_user: User = Depends(get_current_user)
):
    """Start real-time monitoring for all user's competitors"""
    # In production, this would start background tasks
    return {
        "status": "monitoring_started",
        "user_id": current_user.id,
        "websocket_url": f"/api/v1/monitor/ws/{current_user.id}",
        "message": "Connect to WebSocket for real-time updates"
    }

@router.post("/alerts/configure")
async def configure_alerts(
    alert_config: Dict[str, Any],
    current_user: User = Depends(get_current_user)
):
    """Configure alert preferences"""
    # Alert types: pricing_change, new_feature, messaging_change, etc.
    return {
        "status": "alerts_configured",
        "config": alert_config
    }

@router.get("/changes/recent")
async def get_recent_changes(
    hours: int = 24,
    current_user: User = Depends(get_current_user)
):
    """Get recent changes across all competitors"""
    all_changes = []
    
    for comp_id, comp_data in competitive_intel_service._monitored_competitors.items():
        if comp_data["user_id"] == current_user.id:
            changes = comp_data["intel"].get("changes", [])
            for change in changes:
                change["competitor_domain"] = comp_data["domain"]
                all_changes.append(change)
    
    # Sort by recency
    all_changes.sort(key=lambda x: x.get("detected", ""), reverse=True)
    
    return {
        "recent_changes": all_changes[:20],
        "total_changes": len(all_changes),
        "time_period_hours": hours
    }
