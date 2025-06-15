"""
Palmer AI Complete API Endpoints
Full system orchestration endpoints
"""
from fastapi import APIRouter, BackgroundTasks, UploadFile, File, Form
from typing import Optional
import aiofiles
from pathlib import Path
import tempfile

from src.palmer_ai.services.orchestrator import orchestrator
from src.palmer_ai.core.logger import get_logger

logger = get_logger(__name__)
router = APIRouter(prefix="/api/v1/complete", tags=["complete"])

@router.post("/analyze")
async def complete_analysis(
    background_tasks: BackgroundTasks,
    company_url: str = Form(...),
    excel_file: Optional[UploadFile] = File(None),
    analysis_depth: str = Form("comprehensive")
):
    """
    Complete distributor analysis with all Palmer AI capabilities
    This single endpoint replaces entire enterprise software stacks
    """
    job_id = f"job_{datetime.utcnow().timestamp()}"
    
    # Save uploaded file if provided
    excel_path = None
    if excel_file:
        temp_dir = Path(tempfile.gettempdir())
        excel_path = temp_dir / f"{job_id}_{excel_file.filename}"
        
        async with aiofiles.open(excel_path, 'wb') as f:
            content = await excel_file.read()
            await f.write(content)
            
    # Run analysis in background
    background_tasks.add_task(
        orchestrator.analyze_distributor_complete,
        company_url=company_url,
        excel_file=str(excel_path) if excel_path else None,
        analysis_depth=analysis_depth,
        job_id=job_id
    )
    
    return {
        'job_id': job_id,
        'status': 'processing',
        'message': 'Complete analysis started. Connect to WebSocket for real-time updates.',
        'websocket_url': f'/ws/{job_id}'
    }
    
@router.get("/quick-insights/{company_url:path}")
async def get_quick_insights(
    company_url: str,
    focus: str = "general"
):
    """
    Get quick insights for immediate value
    Perfect for demos and converting trials
    """
    insights = await orchestrator.quick_insights(
        company_url=f"https://{company_url}",
        focus_area=focus
    )
    
    return insights
