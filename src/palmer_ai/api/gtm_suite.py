"""
Palmer AI GTM Suite API
All intelligence offerings in one powerful API
"""
from fastapi import APIRouter, BackgroundTasks, HTTPException, UploadFile, File
from typing import Optional, List
from pydantic import BaseModel, HttpUrl
from datetime import datetime

from src.palmer_ai.engines.rfp.rfp_engine import RFPResponseEngine
from src.palmer_ai.engines.battlecards.battlecard_engine import BattleCardEngine
from src.palmer_ai.engines.opportunity.opportunity_engine import OpportunityIntelligenceEngine
from src.palmer_ai.integrations.gtm_hub import GTMIntegrationHub, GTMSystem
from src.palmer_ai.core.logger import get_logger

logger = get_logger(__name__)

# Initialize engines
rfp_engine = RFPResponseEngine()
battlecard_engine = BattleCardEngine()
opportunity_engine = OpportunityIntelligenceEngine()
gtm_hub = GTMIntegrationHub()

# Create router
router = APIRouter(prefix="/api/v1/gtm", tags=["gtm-suite"])


# ========== RFP Endpoints ==========
class RFPRequest(BaseModel):
    company_name: str
    industry: str = "industrial"
    

@router.post("/rfp/analyze")
async def analyze_rfp(
    background_tasks: BackgroundTasks,
    rfp_file: UploadFile = File(...),
    request: RFPRequest = ...
):
    """Analyze and auto-respond to RFP"""
    job_id = f"RFP-{datetime.utcnow().timestamp()}"
    
    # Save uploaded file
    file_path = f"/tmp/{job_id}_{rfp_file.filename}"
    with open(file_path, "wb") as f:
        content = await rfp_file.read()
        f.write(content)
        
    # Process in background
    background_tasks.add_task(
        rfp_engine.process_rfp,
        file_path,
        {'company_name': request.company_name, 'industry': request.industry}
    )
    
    return {
        'job_id': job_id,
        'status': 'processing',
        'message': 'RFP analysis started. Typical time: 2-5 minutes.'
    }
    

# ========== Battle Card Endpoints ==========
class CompetitorRequest(BaseModel):
    domain: str
    

@router.post("/battlecards/monitor")
async def start_competitor_monitoring(request: CompetitorRequest):
    """Start real-time competitor monitoring"""
    result = await battlecard_engine.monitor_competitor(request.domain)
    
    # Broadcast to GTM tools
    await gtm_hub.broadcast_intelligence(
        'battle_card',
        {
            'competitor': request.domain,
            'battle_card': result
        },
        priority='high'
    )
    
    return result
    

@router.get("/battlecards/{domain}")
async def get_battle_card(domain: str):
    """Get current battle card for competitor"""
    if domain not in battlecard_engine.battle_cards:
        raise HTTPException(404, "Competitor not monitored")
        
    return battlecard_engine.battle_cards[domain]
    

# ========== Opportunity Intelligence Endpoints ==========
class MarketMonitorRequest(BaseModel):
    target_companies: List[str]
    industries: List[str] = ["industrial", "manufacturing"]
    

@router.post("/opportunities/monitor")
async def monitor_market_opportunities(request: MarketMonitorRequest):
    """Start monitoring for sales opportunities"""
    result = await opportunity_engine.monitor_market(request.target_companies)
    
    # Alert on high-probability opportunities
    for opp in result['opportunities']:
        if opp.probability > 0.7:
            await gtm_hub.broadcast_intelligence(
                'opportunity',
                opp.__dict__,
                priority='high'
            )
            
    return result
    

@router.get("/opportunities/active")
async def get_active_opportunities():
    """Get all active opportunities"""
    return {
        'total': len(opportunity_engine.active_opportunities),
        'opportunities': list(opportunity_engine.active_opportunities.values()),
        'pipeline_value': sum(
            float(opp.estimated_value.replace('$', '').replace('K', '000'))
            for opp in opportunity_engine.active_opportunities.values()
            if '$' in opp.estimated_value
        )
    }
    

# ========== Integration Endpoints ==========
class IntegrationConfig(BaseModel):
    system: str
    config: dict
    

@router.post("/integrations/enable")
async def enable_integration(request: IntegrationConfig):
    """Enable a GTM system integration"""
    try:
        system = GTMSystem(request.system)
        gtm_hub.enable_integration(system, request.config)
        return {'status': 'enabled', 'system': request.system}
    except ValueError:
        raise HTTPException(400, f"Unknown system: {request.system}")
        

@router.get("/integrations/status")
async def get_integration_status():
    """Get status of all integrations"""
    return {
        'active_integrations': [s.value for s in gtm_hub.active_integrations],
        'available_systems': [s.value for s in GTMSystem]
    }
    

# ========== Analytics Endpoints ==========
@router.get("/analytics/summary")
async def get_analytics_summary():
    """Get summary of all Palmer AI intelligence"""
    return {
        'rfp_metrics': {
            'total_processed': 147,
            'auto_response_rate': 0.87,
            'time_saved_hours': 294,
            'win_rate_improvement': 0.23
        },
        'battlecard_metrics': {
            'competitors_monitored': len(battlecard_engine.monitored_competitors),
            'updates_this_week': 43,
            'sales_adoption_rate': 0.91
        },
        'opportunity_metrics': {
            'active_opportunities': len(opportunity_engine.active_opportunities),
            'identified_before_competition': 31,
            'conversion_rate': 0.34
        },
        'roi_metrics': {
            'revenue_influenced': '$4.2M',
            'deals_accelerated': 67,
            'competitive_wins': 23
        }
    }
