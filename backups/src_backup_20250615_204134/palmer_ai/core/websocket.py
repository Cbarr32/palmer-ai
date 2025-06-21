"""Palmer AI Real-time WebSocket System"""
from typing import Dict, Any
from fastapi import WebSocket
import json

class WebSocketManager:
    """Manage real-time connections"""
    
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
        self.job_connections: Dict[str, str] = {}
        
    async def connect(self, websocket: WebSocket, client_id: str):
        """Accept new connection"""
        await websocket.accept()
        self.active_connections[client_id] = websocket
        
    def disconnect(self, client_id: str):
        """Remove connection"""
        if client_id in self.active_connections:
            del self.active_connections[client_id]
            
    async def send_to_job(self, job_id: str, data: Dict[str, Any]):
        """Send update to job client"""
        if job_id in self.job_connections:
            client_id = self.job_connections[job_id]
            if client_id in self.active_connections:
                try:
                    await self.active_connections[client_id].send_json(data)
                except:
                    self.disconnect(client_id)

ws_manager = WebSocketManager()
