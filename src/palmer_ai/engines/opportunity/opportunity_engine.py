"""
Palmer AI Opportunity Intelligence Engine
Identify and win opportunities before competitors know they exist
"""
import asyncio
from typing import Dict, List, Any, Optional, Set, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum

from src.palmer_ai.core.logger import get_logger

logger = get_logger(__name__)

class OpportunityStage(Enum):
    """Opportunity stages"""
    EARLY_SIGNAL = "early_signal"
    ACTIVE_RESEARCH = "active_research"
    RFP_IMMINENT = "rfp_imminent"
    EVALUATION = "evaluation"
    DECISION = "decision"
    

@dataclass
class OpportunitySignal:
    """Single signal indicating opportunity"""
    signal_type: str
    strength: float  # 0-1
    details: str
    source: str
    detected_at: datetime
    

@dataclass
class Opportunity:
    """Identified sales opportunity"""
    id: str
    company: str
    stage: OpportunityStage
    probability: float
    estimated_value: str
    timeline: str
    signals: List[OpportunitySignal]
    decision_makers: List[Dict[str, str]]
    incumbent: Optional[str]
    requirements: List[str]
    recommended_actions: List[str]
    competition: List[str]
    

class OpportunityIntelligenceEngine:
    """
    Find opportunities 60-90 days before RFPs
    This is the ultimate competitive advantage
    """
    
    def __init__(self):
        self.signal_detector = SignalDetector()
        self.opportunity_scorer = OpportunityScorer()
        self.action_recommender = ActionRecommender()
        self.monitored_companies: Set[str] = set()
        self.active_opportunities: Dict[str, Opportunity] = {}
        
    async def monitor_market(self, target_companies: List[str]) -> Dict[str, Any]:
        """Monitor target companies for opportunity signals"""
        logger.info(f"Starting opportunity monitoring for {len(target_companies)} companies")
        
        opportunities_found = []
        
        for company in target_companies:
            self.monitored_companies.add(company)
            
            # Detect signals
            signals = await self.signal_detector.detect_signals(company)
            
            if signals:
                # Score opportunity
                opportunity = await self._create_opportunity(company, signals)
                
                if opportunity.probability > 0.5:
                    self.active_opportunities[opportunity.id] = opportunity
                    opportunities_found.append(opportunity)
                    
                    # Start tracking
                    asyncio.create_task(self._track_opportunity(opportunity))
                    
        return {
            'companies_monitored': len(target_companies),
            'opportunities_found': len(opportunities_found),
            'high_probability': len([o for o in opportunities_found if o.probability > 0.7]),
            'total_pipeline_value': self._calculate_pipeline_value(opportunities_found),
            'opportunities': opportunities_found
        }
        
    async def _create_opportunity(self, company: str, signals: List[OpportunitySignal]) -> Opportunity:
        """Create opportunity from signals"""
        
        # Score opportunity
        score = await self.opportunity_scorer.score(signals)
        
        # Determine stage
        stage = self._determine_stage(signals)
        
        # Estimate value
        estimated_value = self._estimate_value(company, signals)
        
        # Find decision makers
        decision_makers = await self._find_decision_makers(company, signals)
        
        # Identify requirements
        requirements = self._extract_requirements(signals)
        
        # Get recommended actions
        actions = await self.action_recommender.recommend(stage, signals, score)
        
        return Opportunity(
            id=f"OPP-{company}-{datetime.utcnow().strftime('%Y%m%d')}",
            company=company,
            stage=stage,
            probability=score,
            estimated_value=estimated_value,
            timeline=self._estimate_timeline(stage),
            signals=signals,
            decision_makers=decision_makers,
            incumbent=self._identify_incumbent(signals),
            requirements=requirements,
            recommended_actions=actions,
            competition=self._identify_competition(signals)
        )
        
    def _determine_stage(self, signals: List[OpportunitySignal]) -> OpportunityStage:
        """Determine opportunity stage from signals"""
        
        signal_types = [s.signal_type for s in signals]
        
        if 'rfp_mention' in signal_types or 'vendor_evaluation' in signal_types:
            return OpportunityStage.RFP_IMMINENT
        elif 'budget_approved' in signal_types or 'project_funded' in signal_types:
            return OpportunityStage.EVALUATION
        elif 'research_activity' in signal_types or 'whitepaper_download' in signal_types:
            return OpportunityStage.ACTIVE_RESEARCH
        else:
            return OpportunityStage.EARLY_SIGNAL
            
    def _estimate_timeline(self, stage: OpportunityStage) -> str:
        """Estimate timeline based on stage"""
        timelines = {
            OpportunityStage.EARLY_SIGNAL: "3-6 months",
            OpportunityStage.ACTIVE_RESEARCH: "2-3 months",
            OpportunityStage.RFP_IMMINENT: "30-60 days",
            OpportunityStage.EVALUATION: "30-45 days",
            OpportunityStage.DECISION: "0-30 days"
        }
        return timelines.get(stage, "Unknown")
        
    async def _track_opportunity(self, opportunity: Opportunity):
        """Track opportunity progression"""
        while opportunity.id in self.active_opportunities:
            try:
                await asyncio.sleep(86400)  # Daily check
                
                # Update signals
                new_signals = await self.signal_detector.detect_signals(opportunity.company)
                
                if new_signals:
                    # Update opportunity
                    opportunity.signals.extend(new_signals)
                    opportunity.stage = self._determine_stage(opportunity.signals)
                    opportunity.probability = await self.opportunity_scorer.score(opportunity.signals)
                    
                    # Check for urgent action needed
                    if opportunity.stage == OpportunityStage.RFP_IMMINENT:
                        await self._alert_sales_team(opportunity, "RFP IMMINENT - Action Required")
                        
            except Exception as e:
                logger.error(f"Error tracking opportunity {opportunity.id}: {str(e)}")
                

class SignalDetector:
    """Detect opportunity signals from various sources"""
    
    def __init__(self):
        self.signal_patterns = {
            'website_activity': [
                ('pricing page visits', 0.7),
                ('download whitepaper', 0.6),
                ('request demo', 0.9),
                ('contact form', 0.8),
                ('case study view', 0.5)
            ],
            'public_signals': [
                ('expansion announcement', 0.8),
                ('new facility', 0.9),
                ('leadership change', 0.6),
                ('merger acquisition', 0.7),
                ('earnings call mention', 0.5)
            ],
            'procurement_signals': [
                ('RFI posted', 0.8),
                ('vendor registration', 0.7),
                ('bid calendar update', 0.9),
                ('contract expiration', 0.85),
                ('budget approval', 0.9)
            ],
            'behavioral_signals': [
                ('multiple stakeholder engagement', 0.8),
                ('increased research activity', 0.6),
                ('competitor comparison', 0.7),
                ('technical documentation request', 0.8),
                ('reference check', 0.95)
            ]
        }
        
    async def detect_signals(self, company: str) -> List[OpportunitySignal]:
        """Detect all signals for a company"""
        signals = []
        
        # Check website activity
        web_signals = await self._check_website_activity(company)
        signals.extend(web_signals)
        
        # Check public sources
        public_signals = await self._check_public_sources(company)
        signals.extend(public_signals)
        
        # Check procurement sites
        procurement_signals = await self._check_procurement_sites(company)
        signals.extend(procurement_signals)
        
        # Check behavioral patterns
        behavioral_signals = await self._check_behavioral_patterns(company)
        signals.extend(behavioral_signals)
        
        return signals
        
    async def _check_website_activity(self, company: str) -> List[OpportunitySignal]:
        """Check for website activity signals"""
        # In production, would integrate with analytics
        # For now, simulate signal detection
        
        signals = []
        
        # Simulate finding pricing page visit
        signals.append(OpportunitySignal(
            signal_type='pricing_page_visit',
            strength=0.7,
            details=f"{company} visited pricing page 3 times this week",
            source='Website Analytics',
            detected_at=datetime.utcnow()
        ))
        
        return signals
        
    async def _check_public_sources(self, company: str) -> List[OpportunitySignal]:
        """Check public sources for signals"""
        # Would scrape news, social media, etc.
        return []
        
    async def _check_procurement_sites(self, company: str) -> List[OpportunitySignal]:
        """Check procurement sites for signals"""
        # Would monitor government and corporate procurement sites
        return []
        
    async def _check_behavioral_patterns(self, company: str) -> List[OpportunitySignal]:
        """Check for behavioral pattern signals"""
        # Would analyze engagement patterns
        return []
        

class OpportunityScorer:
    """Score opportunities based on signals"""
    
    async def score(self, signals: List[OpportunitySignal]) -> float:
        """Calculate opportunity probability"""
        
        if not signals:
            return 0.0
            
        # Weight signals by strength and recency
        total_weight = 0
        weighted_sum = 0
        
        for signal in signals:
            # Recency factor (signals decay over time)
            age_days = (datetime.utcnow() - signal.detected_at).days
            recency_factor = max(0, 1 - (age_days / 90))  # 90 day decay
            
            weight = signal.strength * recency_factor
            total_weight += weight
            weighted_sum += weight
            
        # Normalize
        base_score = weighted_sum / max(total_weight, 1)
        
        # Boost for multiple signals
        signal_count_boost = min(len(signals) * 0.05, 0.3)
        
        # Final score
        return min(base_score + signal_count_boost, 1.0)
        

class ActionRecommender:
    """Recommend specific actions for opportunities"""
    
    async def recommend(
        self,
        stage: OpportunityStage,
        signals: List[OpportunitySignal],
        score: float
    ) -> List[str]:
        """Generate action recommendations"""
        
        actions = []
        
        # Stage-specific actions
        if stage == OpportunityStage.EARLY_SIGNAL:
            actions.extend([
                "Add to nurture campaign",
                "Schedule quarterly check-in",
                "Create custom content for their industry"
            ])
        elif stage == OpportunityStage.ACTIVE_RESEARCH:
            actions.extend([
                "Reach out with relevant case study",
                "Invite to webinar on their pain points",
                "Offer free consultation or assessment"
            ])
        elif stage == OpportunityStage.RFP_IMMINENT:
            actions.extend([
                "Contact procurement team immediately",
                "Prepare RFP response team",
                "Gather competitive intelligence",
                "Schedule executive alignment call"
            ])
        elif stage == OpportunityStage.EVALUATION:
            actions.extend([
                "Provide ROI analysis",
                "Arrange reference calls",
                "Offer proof of concept",
                "Escalate to senior leadership"
            ])
            
        # Score-based actions
        if score > 0.8:
            actions.insert(0, "🔥 HIGH PRIORITY - Assign to senior rep immediately")
        elif score > 0.6:
            actions.insert(0, "⚡ Medium priority - Review within 48 hours")
            
        return actions
