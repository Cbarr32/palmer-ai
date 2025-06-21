"""Competitive Intelligence Agent for market analysis"""
import asyncio
from typing import Dict, Any, List, Optional, Set
from datetime import datetime
import httpx
from urllib.parse import urlparse, quote

from ..base.agent import BaseAgent, AgentConfig, AnalysisResult, ConfidenceLevel, AgentMessage
from ...utils.logger import get_logger

logger = get_logger(__name__)

class CompetitiveIntelligenceAgent(BaseAgent):
    """Agent specialized in competitive analysis and market intelligence"""
    
    def __init__(self, config: AgentConfig):
        super().__init__(config)
        self.http_client = httpx.AsyncClient(timeout=30.0)
        self.competitor_cache: Dict[str, List[str]] = {}
        
    async def analyze(self, input_data: Dict[str, Any]) -> AnalysisResult:
        """Perform competitive intelligence analysis"""
        start_time = datetime.utcnow()
        
        try:
            url = input_data.get("url")
            domain = urlparse(url).netloc
            industry = input_data.get("industry", "general")
            
            logger.info(f"Starting competitive intelligence for {domain}")
            
            # Phase 1: Identify competitors
            competitors = await self._identify_competitors(domain, industry)
            
            # Phase 2: Analyze competitive landscape
            landscape_analysis = await self._analyze_competitive_landscape(
                domain, competitors, industry
            )
            
            # Phase 3: Market positioning
            market_position = await self._assess_market_position(
                domain, competitors, landscape_analysis
            )
            
            # Phase 4: Strategic opportunities
            opportunities = await self._identify_opportunities(
                market_position, landscape_analysis
            )
            
            # Apply UWAS reasoning
            uwas_results = await self.process_with_uwas(
                "competitive intelligence analysis",
                {
                    "competitors": competitors,
                    "landscape": landscape_analysis,
                    "position": market_position,
                    "opportunities": opportunities
                },
                techniques=["comparative_framework", "outcome_focused", "tree_of_thought"]
            )
            
            # Build evidence trail
            evidence_trail = [
                {"type": "competitor_identification", "quality_score": 0.85, "weight": 0.9},
                {"type": "landscape_analysis", "quality_score": 0.88, "weight": 1.0},
                {"type": "market_positioning", "quality_score": 0.82, "weight": 0.95},
                {"type": "opportunity_analysis", "quality_score": 0.80, "weight": 0.85}
            ]
            
            confidence = await self.calculate_confidence(evidence_trail)
            
            # Record performance
            elapsed_time = (datetime.utcnow() - start_time).total_seconds()
            self.record_performance("competitive_analysis_duration", elapsed_time)
            self.record_performance("competitors_analyzed", len(competitors))
            
            return AnalysisResult(
                success=True,
                data={
                    "target_domain": domain,
                    "industry": industry,
                    "competitors": competitors,
                    "competitive_landscape": landscape_analysis,
                    "market_position": market_position,
                    "strategic_opportunities": opportunities,
                    "uwas_insights": uwas_results
                },
                confidence=confidence,
                evidence_trail=evidence_trail,
                reasoning_path=uwas_results.get("reasoning_history", []),
                metadata={
                    "analysis_duration": elapsed_time,
                    "competitor_count": len(competitors),
                    "timestamp": datetime.utcnow().isoformat()
                }
            )
            
        except Exception as e:
            logger.error(f"Competitive intelligence failed: {str(e)}")
            return AnalysisResult(
                success=False,
                errors=[f"Competitive analysis error: {str(e)}"],
                confidence=ConfidenceLevel.LOW
            )
            
    async def collaborate(self, message: AgentMessage) -> Optional[AgentMessage]:
        """Handle collaboration with other agents"""
        if message.message_type == "request_competitor_data":
            domain = message.content.get("domain")
            competitor_data = await self._get_competitor_data(domain)
            return AgentMessage(
                sender=self.config.agent_id,
                recipient=message.sender,
                message_type="competitor_data_response",
                content={"competitors": competitor_data}
            )
        elif message.message_type == "request_market_analysis":
            industry = message.content.get("industry")
            market_data = await self._get_market_analysis(industry)
            return AgentMessage(
                sender=self.config.agent_id,
                recipient=message.sender,
                message_type="market_analysis_response",
                content={"market_analysis": market_data}
            )
        return None
        
    async def _identify_competitors(self, domain: str, industry: str) -> List[Dict[str, Any]]:
        """Identify key competitors in the market"""
        competitors = []
        
        # Check cache first
        cache_key = f"{domain}:{industry}"
        if cache_key in self.competitor_cache:
            return self.competitor_cache[cache_key]
            
        try:
            # Simulate competitor identification
            # In production, this would use search APIs, industry databases, etc.
            search_queries = [
                f"{industry} companies like {domain}",
                f"{domain} competitors",
                f"alternatives to {domain}",
                f"{industry} market leaders"
            ]
            
            # Mock competitor data
            competitors = [
                {
                    "domain": "competitor1.com",
                    "name": "Competitor One",
                    "similarity_score": 0.92,
                    "market_share": 0.28,
                    "strengths": ["market leader", "brand recognition"],
                    "weaknesses": ["high pricing", "legacy systems"]
                },
                {
                    "domain": "competitor2.com",
                    "name": "Competitor Two",
                    "similarity_score": 0.87,
                    "market_share": 0.19,
                    "strengths": ["innovation", "user experience"],
                    "weaknesses": ["limited scale", "newer player"]
                },
                {
                    "domain": "competitor3.com",
                    "name": "Competitor Three",
                    "similarity_score": 0.83,
                    "market_share": 0.15,
                    "strengths": ["cost leadership", "efficiency"],
                    "weaknesses": ["limited features", "basic UX"]
                }
            ]
            
            # Cache results
            self.competitor_cache[cache_key] = competitors
            
        except Exception as e:
            logger.error(f"Error identifying competitors: {str(e)}")
            
        return competitors
        
    async def _analyze_competitive_landscape(self, 
                                           domain: str, 
                                           competitors: List[Dict[str, Any]],
                                           industry: str) -> Dict[str, Any]:
        """Analyze the competitive landscape"""
        landscape = {
            "market_concentration": "moderate",
            "competitive_intensity": "high",
            "barriers_to_entry": ["capital requirements", "brand loyalty", "network effects"],
            "market_trends": [
                "digital transformation",
                "AI integration",
                "sustainability focus"
            ],
            "disruption_risk": "medium",
            "key_success_factors": [
                "user experience",
                "innovation speed",
                "customer service",
                "pricing strategy"
            ]
        }
        
        # Calculate market concentration (HHI)
        market_shares = [c.get("market_share", 0) for c in competitors]
        if market_shares:
            hhi = sum([(share * 100) ** 2 for share in market_shares])
            if hhi < 1500:
                landscape["market_concentration"] = "low"
            elif hhi < 2500:
                landscape["market_concentration"] = "moderate"
            else:
                landscape["market_concentration"] = "high"
                
        return landscape
        
    async def _assess_market_position(self,
                                    domain: str,
                                    competitors: List[Dict[str, Any]],
                                    landscape: Dict[str, Any]) -> Dict[str, Any]:
        """Assess target's market position"""
        position = {
            "market_share_estimate": 0.12,
            "competitive_rank": 4,
            "positioning": "challenger",
            "differentiation_factors": [
                "customer focus",
                "specialized features",
                "competitive pricing"
            ],
            "competitive_advantages": [
                "agility",
                "innovation",
                "customer satisfaction"
            ],
            "vulnerabilities": [
                "limited brand awareness",
                "resource constraints",
                "geographic coverage"
            ],
            "strategic_group": "focused differentiators"
        }
        
        return position
        
    async def _identify_opportunities(self,
                                    market_position: Dict[str, Any],
                                    landscape: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Identify strategic opportunities"""
        opportunities = []
        
        # Analyze gaps and opportunities
        if market_position.get("competitive_rank", 0) > 3:
            opportunities.append({
                "type": "market_share_growth",
                "description": "Capture market share from weaker competitors",
                "priority": "high",
                "effort": "medium",
                "potential_impact": 0.25,
                "tactics": [
                    "aggressive pricing",
                    "feature parity",
                    "targeted marketing"
                ]
            })
            
        if "innovation" in landscape.get("key_success_factors", []):
            opportunities.append({
                "type": "innovation_leadership",
                "description": "Establish innovation leadership position",
                "priority": "high",
                "effort": "high",
                "potential_impact": 0.35,
                "tactics": [
                    "R&D investment",
                    "strategic partnerships",
                    "acquisition strategy"
                ]
            })
            
        if landscape.get("market_concentration") == "low":
            opportunities.append({
                "type": "consolidation_play",
                "description": "Lead market consolidation",
                "priority": "medium",
                "effort": "very_high",
                "potential_impact": 0.45,
                "tactics": [
                    "M&A strategy",
                    "strategic alliances",
                    "market aggregation"
                ]
            })
            
        return opportunities
        
    async def _get_competitor_data(self, domain: str) -> List[Dict[str, Any]]:
        """Get cached competitor data"""
        # Implementation would retrieve from cache or database
        return []
        
    async def _get_market_analysis(self, industry: str) -> Dict[str, Any]:
        """Get market analysis for industry"""
        # Implementation would retrieve market analysis
        return {}
        
    async def __aenter__(self):
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.http_client.aclose()
