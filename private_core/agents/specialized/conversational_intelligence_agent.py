"""Conversational Intelligence Agent for flexible distributor interactions"""
import asyncio
from typing import Dict, Any, List, Optional, Union
from datetime import datetime
import json
import pandas as pd
import io
from anthropic import Anthropic

from ..base.agent import BaseAgent, AgentConfig, AnalysisResult, ConfidenceLevel, AgentMessage
from ...utils.logger import get_logger
from ...config import settings

logger = get_logger(__name__)

class ConversationalIntelligenceAgent(BaseAgent):
    """Conversational AI agent that understands distributor needs"""
    
    def __init__(self, config: AgentConfig):
        super().__init__(config)
        self.anthropic_client = Anthropic(api_key=settings.anthropic_api_key)
        self.conversation_history: List[Dict[str, Any]] = []
        
    async def analyze(self, input_data: Dict[str, Any]) -> AnalysisResult:
        """Handle flexible distributor requests through conversation"""
        start_time = datetime.utcnow()
        
        try:
            # Identify input type
            input_type = self._identify_input_type(input_data)
            distributor_id = input_data.get("distributor_id")
            
            logger.info(f"Processing {input_type} request for distributor {distributor_id}")
            
            # Route to appropriate handler
            if input_type == "file_upload":
                result = await self._handle_file_upload(input_data)
            elif input_type == "conversational_request":
                result = await self._handle_conversational_request(input_data)
            elif input_type == "mixed_input":
                result = await self._handle_mixed_input(input_data)
            else:
                result = await self._handle_conversational_request(input_data)
            
            elapsed_time = (datetime.utcnow() - start_time).total_seconds()
            
            return AnalysisResult(
                success=True,
                data=result,
                confidence=ConfidenceLevel.HIGH,
                metadata={
                    "input_type": input_type,
                    "processing_time": elapsed_time,
                    "timestamp": datetime.utcnow().isoformat()
                }
            )
            
        except Exception as e:
            logger.error(f"Conversational intelligence failed: {str(e)}")
            return AnalysisResult(
                success=False,
                errors=[f"Processing error: {str(e)}"],
                confidence=ConfidenceLevel.LOW
            )
    
    def _identify_input_type(self, input_data: Dict[str, Any]) -> str:
        """Identify what type of input the distributor provided"""
        if input_data.get("file_content"):
            return "file_upload"
        elif input_data.get("natural_language_request"):
            return "conversational_request"
        elif len([k for k in input_data.keys() if k in ["file_content", "manufacturer_urls", "product_list"]]) > 1:
            return "mixed_input"
        else:
            return "conversational_request"
    
    async def _handle_file_upload(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle Excel, CSV, or other file uploads"""
        file_content = input_data.get("file_content")
        file_name = input_data.get("file_name", "uploaded_file")
        
        # Parse the file
        try:
            if file_name.endswith((".xlsx", ".xls")):
                df = pd.read_excel(io.BytesIO(file_content))
            else:
                df = pd.read_csv(io.StringIO(file_content.decode('utf-8')))
        except Exception as e:
            return {
                "error": f"Could not parse file: {str(e)}",
                "suggestions": ["Try uploading an Excel (.xlsx) or CSV file"]
            }
        
        # Analyze the file
        file_analysis = await self._analyze_file_structure(df, file_name)
        
        return {
            "input_type": "file_upload",
            "file_info": {
                "name": file_name,
                "rows": len(df),
                "columns": list(df.columns),
                "sample_data": df.head(3).to_dict('records')
            },
            "analysis": file_analysis,
            "next_steps": "I've analyzed your file. What would you like me to help you with?"
        }
    
    async def _handle_conversational_request(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle natural language requests"""
        user_request = input_data.get("natural_language_request", "")
        
        conversation_response = await self._process_conversational_request(user_request)
        
        return {
            "input_type": "conversational_request",
            "user_request": user_request,
            "palmer_response": conversation_response.get("palmer_response", ""),
            "suggested_actions": conversation_response.get("suggested_actions", []),
            "next_steps": conversation_response.get("next_steps", "")
        }
    
    async def _handle_mixed_input(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle complex requests with multiple input types"""
        results = {}
        
        if input_data.get("file_content"):
            results["file_processing"] = await self._handle_file_upload(input_data)
        
        if input_data.get("natural_language_request"):
            results["conversation"] = await self._handle_conversational_request(input_data)
        
        return {
            "input_type": "mixed_input",
            "individual_results": results,
            "next_steps": "I've processed your combined request. What would you like to focus on first?"
        }
    
    async def _analyze_file_structure(self, df: pd.DataFrame, file_name: str) -> Dict[str, Any]:
        """Analyze uploaded file structure"""
        file_summary = {
            "file_name": file_name,
            "total_rows": len(df),
            "columns": list(df.columns),
            "sample_data": df.head(3).to_dict('records')
        }
        
        prompt = f"""Analyze this distributor's product file and provide recommendations:

FILE DATA: {json.dumps(file_summary, indent=2, default=str)}

Provide analysis in JSON format:
{{
  "file_assessment": {{
    "quality": "HIGH/MEDIUM/LOW",
    "completeness": 0.0-1.0,
    "issues_found": ["list of issues"]
  }},
  "enhancement_opportunities": [
    "specific improvements possible"
  ],
  "recommended_actions": [
    "actionable next steps"
  ]
}}"""

        try:
            response = await self.anthropic_client.messages.create(
                model=settings.anthropic_model,
                max_tokens=1500,
                messages=[{"role": "user", "content": prompt}]
            )
            
            content = response.content[0].text
            json_start = content.find('{')
            json_end = content.rfind('}') + 1
            
            if json_start != -1 and json_end != -1:
                return json.loads(content[json_start:json_end])
            else:
                return self._fallback_file_analysis(df)
                
        except Exception as e:
            logger.error(f"File analysis failed: {str(e)}")
            return self._fallback_file_analysis(df)
    
    async def _process_conversational_request(self, user_request: str) -> Dict[str, Any]:
        """Process natural language requests"""
        prompt = f"""You are Palmer AI, a helpful B2B product intelligence assistant.

USER REQUEST: "{user_request}"

Respond as Palmer AI with helpful guidance. Provide JSON format:

{{
  "palmer_response": "Helpful response to their request",
  "suggested_actions": [
    "specific actions Palmer can take"
  ],
  "next_steps": "What should happen next"
}}

Be conversational and helpful."""

        try:
            response = await self.anthropic_client.messages.create(
                model=settings.anthropic_model,
                max_tokens=1000,
                messages=[{"role": "user", "content": prompt}]
            )
            
            content = response.content[0].text
            json_start = content.find('{')
            json_end = content.rfind('}') + 1
            
            if json_start != -1 and json_end != -1:
                return json.loads(content[json_start:json_end])
            else:
                return self._fallback_conversation_response(user_request)
                
        except Exception as e:
            logger.error(f"Conversation processing failed: {str(e)}")
            return self._fallback_conversation_response(user_request)
    
    def _fallback_file_analysis(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Fallback file analysis"""
        return {
            "file_assessment": {
                "quality": "MEDIUM",
                "completeness": 0.5,
                "issues_found": ["Analysis pending"]
            },
            "enhancement_opportunities": ["File structure analysis needed"],
            "recommended_actions": ["Manual review recommended"]
        }
    
    def _fallback_conversation_response(self, user_request: str) -> Dict[str, Any]:
        """Fallback conversation response"""
        return {
            "palmer_response": f"I understand you're asking about: '{user_request}'. Let me help you with that!",
            "suggested_actions": ["clarify_request"],
            "next_steps": "Could you provide more details about what you need?"
        }
    
    async def collaborate(self, message: AgentMessage) -> Optional[AgentMessage]:
        """Handle collaboration with other agents"""
        return None
