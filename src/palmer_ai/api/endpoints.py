"""API Endpoints for Palmer AI - Real Implementation"""
from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import Dict, Any
import asyncio

from ..config import settings
from ..core import PalmerAICore
from ..utils.logger import get_logger

logger = get_logger(__name__)
router = APIRouter(prefix="/api/v1", tags=["analysis"])

# Initialize Palmer AI Core
palmer_core = PalmerAICore()

@router.post("/analyze")
async def analyze_company(request: Dict[str, Any]):
    """Real company analysis using Claude AI"""
    try:
        company_name = request.get("company_name", "Unknown Company")
        logger.info(f"Starting analysis for: {company_name}")
        
        # Prepare company data for analysis
        company_data = {
            "name": company_name,
            "website": request.get("website", ""),
            "industry": request.get("industry", ""),
            "size": request.get("size", ""),
            "description": request.get("description", ""),
            **request  # Include any additional data
        }
        
        # Perform real AI analysis
        analysis_result = await palmer_core.analyze_with_love(company_data)
        
        logger.info(f"Analysis completed for {company_name}")
        return analysis_result
        
    except Exception as e:
        logger.error(f"Analysis endpoint error: {e}")
        raise HTTPException(
            status_code=500, 
            detail=f"Analysis failed: {str(e)}"
        )

@router.post("/analyze-batch")
async def analyze_multiple_companies(request: Dict[str, Any]):
    """Analyze multiple companies in batch"""
    companies = request.get("companies", [])
    if not companies:
        raise HTTPException(status_code=400, detail="No companies provided")
    
    if len(companies) > 10:
        raise HTTPException(status_code=400, detail="Maximum 10 companies per batch")
    
    results = []
    for company in companies:
        try:
            result = await palmer_core.analyze_with_love(company)
            results.append(result)
        except Exception as e:
            results.append({
                "status": "error",
                "company_name": company.get("name", "Unknown"),
                "error": str(e)
            })
    
    return {
        "batch_analysis": True,
        "total_companies": len(companies),
        "results": results
    }

@router.get("/status")
async def get_status():
    """Enhanced API status with Claude connectivity"""
    try:
        health_check = await palmer_core.quick_health_check()
        return {
            "api_status": "ready",
            "model": settings.anthropic_model,
            "version": settings.app_version,
            "elite_mode": settings.elite_mode,
            **health_check
        }
    except Exception as e:
        return {
            "api_status": "degraded",
            "model": settings.anthropic_model,
            "version": settings.app_version,
            "error": str(e)
        }

@router.get("/health")
async def detailed_health():
    """Detailed health check for monitoring"""
    health_data = await palmer_core.quick_health_check()
    
    return {
        "timestamp": "2025-06-11T22:00:00Z",
        "palmer_ai": {
            "core": health_data.get("core_status", "unknown"),
            "claude_api": health_data.get("claude_api", "unknown"),
            "version": settings.app_version
        },
        "system": {
            "environment": settings.environment,
            "debug": settings.debug,
            "elite_mode": settings.elite_mode
        },
        "mia_dedication": "💜 Every heartbeat of this system honors Mia's memory 💜"
    }

@router.post("/analyze-website")
async def analyze_website_url(request: Dict[str, Any]):
    """Analyze a company by website URL"""
    website_url = request.get("url", "").strip()
    if not website_url:
        raise HTTPException(status_code=400, detail="Website URL required")
    
    # Extract company name from URL
    company_name = website_url.replace("https://", "").replace("http://", "").replace("www.", "").split(".")[0].title()
    
    company_data = {
        "name": company_name,
        "website": website_url,
        "analysis_type": "website_url"
    }
    
    return await palmer_core.analyze_with_love(company_data)
