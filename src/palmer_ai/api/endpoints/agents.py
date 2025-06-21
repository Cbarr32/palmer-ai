"""Agent management and orchestration endpoints"""
from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
from datetime import datetime

from ...agents.coordination.coordinator import AgentCoordinator, CoordinationStrategy
from ...utils.logger import get_logger

logger = get_logger(__name__)
router = APIRouter(prefix="/agents", tags=["agents"])

# Global coordinator instance (in production, use dependency injection)
coordinator = AgentCoordinator()

class AnalysisRequest(BaseModel):
    url: str = Field(..., description="Target URL for analysis")
    analysis_type: str = Field(
        default="comprehensive",
        description="Type of analysis: comprehensive, competitive, technical"
    )
    strategy: CoordinationStrategy = Field(
        default=CoordinationStrategy.ADAPTIVE,
        description="Execution strategy: parallel, sequential, adaptive"
    )
    options: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Additional options for analysis"
    )
    
class AnalysisResponse(BaseModel):
    analysis_id: str
    status: str
    message: str
    
class AnalysisStatus(BaseModel):
    analysis_id: str
    status: str
    progress: float
    results: Optional[Dict[str, Any]] = None
    
@router.post("/analyze", response_model=AnalysisResponse)
async def start_analysis(
    request: AnalysisRequest,
    background_tasks: BackgroundTasks
) -> AnalysisResponse:
    """Start a new multi-agent analysis"""
    try:
        # Generate analysis ID
        analysis_id = f"analysis_{datetime.utcnow().timestamp()}"
        
        # Start analysis in background
        background_tasks.add_task(
            coordinator.coordinate_analysis,
            request.url,
            request.analysis_type,
            request.strategy,
            request.options
        )
        
        return AnalysisResponse(
            analysis_id=analysis_id,
            status="started",
            message=f"Analysis started for {request.url}"
        )
        
    except Exception as e:
        logger.error(f"Failed to start analysis: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
        
@router.get("/analyze/{analysis_id}", response_model=AnalysisStatus)
async def get_analysis_status(analysis_id: str) -> AnalysisStatus:
    """Get the status of an analysis"""
    if analysis_id not in coordinator.active_analyses:
        raise HTTPException(status_code=404, detail="Analysis not found")
        
    analysis = coordinator.active_analyses[analysis_id]
    
    # Calculate progress
    total_agents = len(analysis.get("agent_results", {}))
    completed_agents = sum(
        1 for result in analysis.get("agent_results", {}).values()
        if result
    )
    progress = completed_agents / total_agents if total_agents > 0 else 0
    
    return AnalysisStatus(
        analysis_id=analysis_id,
        status=analysis["status"],
        progress=progress,
        results=analysis.get("results") if analysis["status"] == "completed" else None
    )
    
@router.get("/performance", response_model=Dict[str, Dict[str, Any]])
async def get_agent_performance() -> Dict[str, Dict[str, Any]]:
    """Get performance metrics for all agents"""
    try:
        return await coordinator.get_agent_performance()
    except Exception as e:
        logger.error(f"Failed to get performance metrics: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
        
@router.get("/agents", response_model=List[Dict[str, Any]])
async def list_agents() -> List[Dict[str, Any]]:
    """List all available agents"""
    agents = []
    
    for role, agent in coordinator.agents.items():
        agents.append({
            "role": role.value,
            "agent_id": agent.config.agent_id,
            "name": agent.config.name,
            "description": agent.config.description,
            "capabilities": [cap.dict() for cap in agent.config.capabilities],
            "uwas_techniques": agent.config.uwas_techniques
        })
        
    return agents
    
@router.post("/agents/{agent_role}/message")
async def send_agent_message(
    agent_role: str,
    message: Dict[str, Any]
) -> Dict[str, Any]:
    """Send a message to a specific agent"""
    # Implementation for inter-agent messaging
    return {"status": "message_sent", "agent": agent_role}
