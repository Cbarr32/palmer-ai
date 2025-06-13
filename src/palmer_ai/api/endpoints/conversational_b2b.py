"""Conversational B2B API endpoints for flexible distributor interactions"""
from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
from datetime import datetime
import uuid
import json

from ...agents.specialized.conversational_intelligence_agent import ConversationalIntelligenceAgent
from ...agents.base.agent import AgentConfig, AgentRole
from ...utils.logger import get_logger

logger = get_logger(__name__)
router = APIRouter(prefix="/palmer", tags=["Conversational Palmer AI"])

# Initialize conversational agent
conversational_config = AgentConfig(
    agent_id="palmer_conversational",
    name="Palmer AI Conversational Intelligence",
    role=AgentRole.SUPERVISOR,
    description="Conversational AI for flexible distributor interactions",
    capabilities=[],
    uwas_techniques=["chain_of_thought", "expert_persona"]
)
palmer_agent = ConversationalIntelligenceAgent(conversational_config)

class ConversationalRequest(BaseModel):
    distributor_id: str
    message: str = Field(..., description="Natural language request")
    context: Optional[Dict[str, Any]] = Field(default={})

@router.post("/chat")
async def chat_with_palmer(request: ConversationalRequest) -> Dict[str, Any]:
    """Natural language conversation with Palmer AI"""
    try:
        logger.info(f"Palmer chat from {request.distributor_id}: {request.message[:100]}...")
        
        analysis_result = await palmer_agent.analyze({
            "natural_language_request": request.message,
            "distributor_id": request.distributor_id,
            "context": request.context
        })
        
        if analysis_result.success:
            response_data = analysis_result.data
            
            return {
                "session_id": str(uuid.uuid4()),
                "palmer_response": response_data.get("palmer_response", ""),
                "suggestions": response_data.get("suggested_actions", []),
                "next_steps": response_data.get("next_steps", "")
            }
        else:
            raise HTTPException(status_code=500, detail="Failed to process conversation")
            
    except Exception as e:
        logger.error(f"Palmer chat failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/upload-and-chat")
async def upload_file_and_chat(
    file: UploadFile = File(...),
    distributor_id: str = Form(...),
    message: str = Form(default="Please analyze this file")
) -> Dict[str, Any]:
    """Upload a file and chat about it"""
    try:
        file_content = await file.read()
        
        logger.info(f"File upload from {distributor_id}: {file.filename}")
        
        analysis_result = await palmer_agent.analyze({
            "file_content": file_content,
            "file_name": file.filename,
            "distributor_id": distributor_id,
            "natural_language_request": message
        })
        
        if analysis_result.success:
            response_data = analysis_result.data
            
            return {
                "upload_successful": True,
                "file_info": response_data.get("file_info", {}),
                "palmer_response": response_data.get("next_steps", ""),
                "analysis": response_data.get("analysis", {}),
                "session_id": str(uuid.uuid4())
            }
        else:
            raise HTTPException(status_code=500, detail="Failed to process file")
            
    except Exception as e:
        logger.error(f"File upload failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/capabilities")
async def palmer_capabilities() -> Dict[str, Any]:
    """Get Palmer AI capabilities"""
    return {
        "palmer_ai_capabilities": {
            "file_processing": {
                "supported_formats": ["Excel (.xlsx, .xls)", "CSV"],
                "capabilities": [
                    "Analyze product catalogs",
                    "Enhance descriptions", 
                    "Identify opportunities"
                ]
            },
            "conversational_intelligence": {
                "capabilities": [
                    "Natural language requests",
                    "Business guidance", 
                    "Strategic insights"
                ]
            }
        }
    }

@router.post("/quick-help")
async def quick_help(request: Dict[str, Any]) -> Dict[str, Any]:
    """Quick help for common questions"""
    question = request.get("question", "").lower()
    
    if "upload" in question:
        return {
            "palmer_response": "You can upload Excel (.xlsx) or CSV files. I'll analyze and enhance your product data.",
            "next_steps": "Use /palmer/upload-and-chat to get started."
        }
    elif "enhance" in question:
        return {
            "palmer_response": "I can enhance product descriptions, add specifications, and optimize for your target market.",
            "next_steps": "Share your product data and tell me about your customers."
        }
    
    return {
        "palmer_response": "I'm here to help with product intelligence! Ask me about uploading files or enhancing catalogs.",
        "suggested_questions": ["How do I upload files?", "Can you enhance descriptions?"]
    }
