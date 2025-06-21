"""WebSocket support for real-time analysis updates"""
from fastapi import WebSocket, WebSocketDisconnect
from typing import Dict, Set, Any
import json
import asyncio

from ..utils.logger import get_logger
from ..frameworks.canvas.collaboration import CanvasUpdate

logger = get_logger(__name__)

class ConnectionManager:
    """Manages WebSocket connections for real-time updates"""
    
    def __init__(self):
        self.active_connections: Dict[str, Set[WebSocket]] = {}
        self.analysis_subscriptions: Dict[str, Set[str]] = {}
        
    async def connect(self, websocket: WebSocket, client_id: str):
        """Accept new WebSocket connection"""
        await websocket.accept()
        
        if client_id not in self.active_connections:
            self.active_connections[client_id] = set()
            
        self.active_connections[client_id].add(websocket)
        logger.info(f"Client {client_id} connected")
        
    def disconnect(self, websocket: WebSocket, client_id: str):
        """Remove WebSocket connection"""
        if client_id in self.active_connections:
            self.active_connections[client_id].discard(websocket)
            
            if not self.active_connections[client_id]:
                del self.active_connections[client_id]
                
                # Clean up subscriptions
                for analysis_id in list(self.analysis_subscriptions.keys()):
                    self.analysis_subscriptions[analysis_id].discard(client_id)
                    if not self.analysis_subscriptions[analysis_id]:
                        del self.analysis_subscriptions[analysis_id]
                        
        logger.info(f"Client {client_id} disconnected")
        
    async def subscribe_to_analysis(self, client_id: str, analysis_id: str):
        """Subscribe client to analysis updates"""
        if analysis_id not in self.analysis_subscriptions:
            self.analysis_subscriptions[analysis_id] = set()
            
        self.analysis_subscriptions[analysis_id].add(client_id)
        logger.info(f"Client {client_id} subscribed to analysis {analysis_id}")
        
    async def send_personal_message(self, message: str, websocket: WebSocket):
        """Send message to specific WebSocket"""
        try:
            await websocket.send_text(message)
        except Exception as e:
            logger.error(f"Error sending message: {str(e)}")
            
    async def send_to_client(self, client_id: str, message: Dict[str, Any]):
        """Send message to all connections for a client"""
        if client_id in self.active_connections:
            message_text = json.dumps(message)
            
            # Send to all connections for this client
            disconnected = []
            for websocket in self.active_connections[client_id]:
                try:
                    await websocket.send_text(message_text)
                except Exception as e:
                    logger.error(f"Error sending to client {client_id}: {str(e)}")
                    disconnected.append(websocket)
                    
            # Clean up disconnected websockets
            for websocket in disconnected:
                self.active_connections[client_id].discard(websocket)
                
    async def broadcast_analysis_update(self, 
                                      analysis_id: str, 
                                      update_type: str,
                                      data: Dict[str, Any]):
        """Broadcast update to all subscribed clients"""
        if analysis_id in self.analysis_subscriptions:
            message = {
                "type": "analysis_update",
                "analysis_id": analysis_id,
                "update_type": update_type,
                "data": data,
                "timestamp": data.get("timestamp", "")
            }
            
            # Send to all subscribed clients
            for client_id in self.analysis_subscriptions[analysis_id]:
                await self.send_to_client(client_id, message)
                
    async def broadcast_canvas_update(self, 
                                    canvas_id: str,
                                    update: CanvasUpdate):
        """Broadcast canvas update to subscribed clients"""
        # Extract analysis_id from canvas_id
        analysis_id = canvas_id.replace("canvas_", "")
        
        if analysis_id in self.analysis_subscriptions:
            message = {
                "type": "canvas_update",
                "canvas_id": canvas_id,
                "element_id": update.element_id,
                "element_type": update.element_type.value,
                "content": update.content,
                "metadata": update.metadata,
                "timestamp": update.timestamp.isoformat()
            }
            
            # Send to all subscribed clients
            for client_id in self.analysis_subscriptions[analysis_id]:
                await self.send_to_client(client_id, message)
                
# Global connection manager
manager = ConnectionManager()

async def websocket_endpoint(websocket: WebSocket, client_id: str):
    """WebSocket endpoint handler"""
    await manager.connect(websocket, client_id)
    
    try:
        while True:
            # Receive message from client
            data = await websocket.receive_text()
            
            try:
                message = json.loads(data)
                
                if message["type"] == "subscribe":
                    analysis_id = message["analysis_id"]
                    await manager.subscribe_to_analysis(client_id, analysis_id)
                    
                    # Send confirmation
                    await manager.send_personal_message(
                        json.dumps({
                            "type": "subscription_confirmed",
                            "analysis_id": analysis_id
                        }),
                        websocket
                    )
                    
                elif message["type"] == "ping":
                    # Respond to ping
                    await manager.send_personal_message(
                        json.dumps({"type": "pong"}),
                        websocket
                    )
                    
            except json.JSONDecodeError:
                logger.error(f"Invalid JSON from client {client_id}: {data}")
                
    except WebSocketDisconnect:
        manager.disconnect(websocket, client_id)
