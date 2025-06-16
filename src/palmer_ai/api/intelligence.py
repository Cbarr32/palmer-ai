"""Competitive Intelligence API - This is what users actually use"""
from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, HttpUrl
from datetime import datetime

from palmer_ai.services.competitive_intel import competitive_intel_service
from palmer_ai.api.auth import get_current_user
from palmer_ai.models.user import User
from palmer_ai.utils.logger import get_logger

logger = get_logger(__name__)
router = APIRouter()

class AddCompetitorRequest(BaseModel):
    competitor_url: HttpUrl
    monitor: bool = True

class CompetitorResponse(BaseModel):
    competitor_id: str
    domain: str
    status: str
    intel_summary: Dict[str, Any]

@router.post("/competitors", response_model=CompetitorResponse)
async def add_competitor(
    request: AddCompetitorRequest,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user)
):
    """Add a competitor to track - This is the entry point"""
    try:
        # Check user limits
        user_tier = current_user.subscription_tier
        # (In production, check against tier limits)
        
        result = await competitive_intel_service.add_competitor(
            user_id=current_user.id,
            competitor_url=str(request.competitor_url)
        )
        
        if request.monitor:
            # Schedule monitoring
            background_tasks.add_task(
                competitive_intel_service.monitor_changes,
                result["competitor_id"]
            )
        
        return CompetitorResponse(
            competitor_id=result["competitor_id"],
            domain=result["domain"],
            status="monitoring_active" if request.monitor else "analyzed",
            intel_summary={
                "headlines": result["initial_intel"]["messaging"]["headlines"][:3],
                "features_count": len(result["initial_intel"]["features"]),
                "has_pricing": len(result["initial_intel"]["pricing"]["plans"]) > 0,
                "insights_count": len(result["initial_intel"]["insights"])
            }
        )
        
    except Exception as e:
        logger.error(f"Failed to add competitor: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/competitors/{competitor_id}")
async def get_competitor_intel(
    competitor_id: str,
    current_user: User = Depends(get_current_user)
):
    """Get full intelligence on a competitor"""
    try:
        report = await competitive_intel_service.get_competitor_report(competitor_id)
        return report
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Failed to get competitor intel: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/competitors/{competitor_id}/refresh")
async def refresh_competitor_intel(
    competitor_id: str,
    current_user: User = Depends(get_current_user)
):
    """Manually refresh competitor intelligence"""
    try:
        result = await competitive_intel_service.monitor_changes(competitor_id)
        return {
            "status": "refreshed",
            "changes_detected": result["changes_detected"],
            "changes": result["changes"],
            "last_scan": datetime.utcnow().isoformat()
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Failed to refresh competitor: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/competitors")
async def list_competitors(
    current_user: User = Depends(get_current_user)
):
    """List all tracked competitors"""
    # In production, this would query from database
    # For now, return from in-memory store
    competitors = []
    
    for comp_id, comp_data in competitive_intel_service._monitored_competitors.items():
        if comp_data["user_id"] == current_user.id:
            competitors.append({
                "competitor_id": comp_id,
                "domain": comp_data["domain"],
                "url": comp_data["url"],
                "monitoring_since": comp_data["added"].isoformat(),
                "last_scan": comp_data["last_scan"].isoformat(),
                "changes_count": len(comp_data["intel"].get("changes", []))
            })
    
    return {
        "competitors": competitors,
        "total": len(competitors),
        "tier_limit": 20  # Would come from user tier
    }

@router.get("/insights/trending")
async def get_trending_insights(
    current_user: User = Depends(get_current_user)
):
    """Get trending insights across all competitors"""
    # Aggregate insights across user's competitors
    all_insights = []
    
    for comp_id, comp_data in competitive_intel_service._monitored_competitors.items():
        if comp_data["user_id"] == current_user.id:
            insights = comp_data["intel"].get("insights", [])
            for insight in insights:
                insight["competitor_domain"] = comp_data["domain"]
                all_insights.append(insight)
    
    # Sort by importance/recency
    return {
        "trending_insights": all_insights[:10],
        "total_insights": len(all_insights),
        "generated_at": datetime.utcnow().isoformat()
    }
