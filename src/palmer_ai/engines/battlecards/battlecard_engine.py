"""
Palmer AI Battle Cards Engine
Real-time competitive intelligence that updates before Klue knows
"""
import asyncio
from typing import Dict, List, Any, Optional, Set
from datetime import datetime, timedelta
from dataclasses import dataclass
import json

from src.palmer_ai.core.logger import get_logger
from src.palmer_ai.agents.scraper_agent import scraper_agent

logger = get_logger(__name__)

@dataclass
class CompetitiveInsight:
    """Single competitive insight"""
    competitor: str
    insight_type: str  # pricing, feature, weakness, strength
    title: str
    details: str
    talk_track: str
    proof_points: List[str]
    detected_at: datetime
    confidence: float
    sources: List[str]
    

@dataclass
class BattleCard:
    """Dynamic battle card for sales teams"""
    competitor: str
    last_updated: datetime
    win_rate_impact: float
    key_differentiators: List[Dict[str, str]]
    vulnerabilities: List[Dict[str, str]]
    talk_tracks: Dict[str, str]
    landmines: List[str]  # Topics to avoid
    proof_points: Dict[str, List[str]]
    recent_changes: List[CompetitiveInsight]
    suggested_tactics: List[Dict[str, str]]
    

class BattleCardEngine:
    """
    Creates battle cards that actually help win deals
    Updates in real-time based on market changes
    """
    
    def __init__(self):
        self.monitored_competitors: Set[str] = set()
        self.battle_cards: Dict[str, BattleCard] = {}
        self.change_detector = ChangeDetector()
        self.win_loss_analyzer = WinLossAnalyzer()
        
    async def monitor_competitor(self, domain: str) -> Dict[str, Any]:
        """Start monitoring a competitor"""
        logger.info(f"Starting real-time monitoring for {domain}")
        
        self.monitored_competitors.add(domain)
        
        # Initial deep scan
        initial_intel = await self._deep_competitor_scan(domain)
        
        # Create initial battle card
        battle_card = await self._generate_battle_card(domain, initial_intel)
        self.battle_cards[domain] = battle_card
        
        # Set up continuous monitoring
        asyncio.create_task(self._continuous_monitor(domain))
        
        return {
            'competitor': domain,
            'battle_card_created': True,
            'initial_insights': len(battle_card.recent_changes),
            'key_vulnerabilities': len(battle_card.vulnerabilities),
            'monitoring_status': 'active'
        }
        
    async def _deep_competitor_scan(self, domain: str) -> List[CompetitiveInsight]:
        """Comprehensive competitor analysis"""
        insights = []
        
        # Scrape competitor site
        competitor_data = await scraper_agent.analyze_competitor(f"https://{domain}")
        
        # Analyze pricing
        if 'pricing_intelligence' in competitor_data:
            pricing = competitor_data['pricing_intelligence']
            if 'average_discount' in pricing.get('discount_patterns', {}):
                insights.append(CompetitiveInsight(
                    competitor=domain,
                    insight_type='pricing',
                    title='Heavy Discounting Detected',
                    details=f"Competitor averaging {pricing['discount_patterns']['average_discount']:.0%} discounts",
                    talk_track="They're competing on price because they can't compete on value. Our total cost of ownership is still lower.",
                    proof_points=[
                        "Our solution includes free training worth $5K",
                        "No hidden implementation fees",
                        "Lower maintenance costs over 3 years"
                    ],
                    detected_at=datetime.utcnow(),
                    confidence=0.9,
                    sources=[domain]
                ))
                
        # Analyze technology gaps
        if 'technology_stack' in competitor_data:
            tech = competitor_data['technology_stack']
            if not tech.get('ecommerce_platform'):
                insights.append(CompetitiveInsight(
                    competitor=domain,
                    insight_type='weakness',
                    title='No Digital Commerce Platform',
                    details="Competitor lacks online ordering capabilities",
                    talk_track="While they're still taking orders by phone, we offer 24/7 self-service ordering with real-time inventory.",
                    proof_points=[
                        "Our portal reduces order errors by 67%",
                        "Customers save 2 hours per week on ordering",
                        "Mobile app for on-the-go ordering"
                    ],
                    detected_at=datetime.utcnow(),
                    confidence=0.95,
                    sources=[domain]
                ))
                
        # Analyze service gaps
        if 'unique_selling_props' in competitor_data:
            usps = competitor_data['unique_selling_props']
            if not any('24/7' in usp.lower() for usp in usps):
                insights.append(CompetitiveInsight(
                    competitor=domain,
                    insight_type='weakness',
                    title='Limited Support Hours',
                    details="No 24/7 support advertised",
                    talk_track="When your line goes down at 2 AM, you need support NOW, not at 9 AM.",
                    proof_points=[
                        "Our 24/7 support has 15-minute average response",
                        "Certified technicians always available",
                        "Remote diagnostics capability"
                    ],
                    detected_at=datetime.utcnow(),
                    confidence=0.85,
                    sources=[domain]
                ))
                
        return insights
        
    async def _generate_battle_card(self, domain: str, insights: List[CompetitiveInsight]) -> BattleCard:
        """Generate comprehensive battle card"""
        
        # Analyze win/loss data
        win_loss = await self.win_loss_analyzer.analyze(domain)
        
        # Build differentiators
        differentiators = []
        vulnerabilities = []
        talk_tracks = {}
        
        for insight in insights:
            if insight.insight_type == 'weakness':
                vulnerabilities.append({
                    'title': insight.title,
                    'details': insight.details,
                    'exploit': insight.talk_track
                })
                talk_tracks[insight.title] = insight.talk_track
                
            elif insight.insight_type == 'pricing':
                differentiators.append({
                    'area': 'Value Proposition',
                    'our_advantage': 'Total cost of ownership',
                    'their_weakness': insight.details
                })
                
        # Add standard differentiators
        differentiators.extend([
            {
                'area': 'Experience',
                'our_advantage': '25+ years serving industrial customers',
                'their_weakness': 'Limited industrial expertise'
            },
            {
                'area': 'Technology',
                'our_advantage': 'AI-powered inventory optimization',
                'their_weakness': 'Manual processes'
            }
        ])
        
        # Landmines to avoid
        landmines = [
            "Don't discuss price before value",
            "Avoid comparing feature-by-feature",
            "Don't criticize competitor directly"
        ]
        
        # Suggested tactics based on insights
        tactics = self._generate_tactics(insights, win_loss)
        
        return BattleCard(
            competitor=domain,
            last_updated=datetime.utcnow(),
            win_rate_impact=win_loss.get('win_rate_delta', 0.15),
            key_differentiators=differentiators,
            vulnerabilities=vulnerabilities,
            talk_tracks=talk_tracks,
            landmines=landmines,
            proof_points={
                'customer_success': [
                    "Acme Corp reduced costs by 23%",
                    "Widget Inc improved uptime to 99.8%"
                ],
                'service_excellence': [
                    "15-minute average response time",
                    "98% first-call resolution rate"
                ]
            },
            recent_changes=insights,
            suggested_tactics=tactics
        )
        
    def _generate_tactics(self, insights: List[CompetitiveInsight], win_loss: Dict) -> List[Dict]:
        """Generate specific sales tactics"""
        tactics = []
        
        # Tactic based on insights
        for insight in insights:
            if insight.insight_type == 'weakness':
                tactics.append({
                    'situation': f"When prospect mentions {insight.competitor}",
                    'tactic': f"Probe about {insight.title.lower()}",
                    'follow_up': insight.talk_track,
                    'success_rate': '73%'
                })
                
        # General tactics
        tactics.extend([
            {
                'situation': "Early in sales cycle",
                'tactic': "Focus on business outcomes, not features",
                'follow_up': "Share relevant case study with metrics",
                'success_rate': '81%'
            },
            {
                'situation': "Price objection",
                'tactic': "Shift to TCO and opportunity cost",
                'follow_up': "Offer ROI analysis",
                'success_rate': '67%'
            }
        ])
        
        return tactics
        
    async def _continuous_monitor(self, domain: str):
        """Continuous monitoring for changes"""
        while domain in self.monitored_competitors:
            try:
                # Check for changes every hour
                await asyncio.sleep(3600)
                
                # Detect changes
                changes = await self.change_detector.check_for_changes(domain)
                
                if changes:
                    # Update battle card
                    new_insights = await self._analyze_changes(domain, changes)
                    await self._update_battle_card(domain, new_insights)
                    
                    # Notify sales team
                    await self._notify_sales_team(domain, new_insights)
                    
            except Exception as e:
                logger.error(f"Monitoring error for {domain}: {str(e)}")
                

class ChangeDetector:
    """Detect meaningful changes in competitor data"""
    
    def __init__(self):
        self.previous_states = {}
        
    async def check_for_changes(self, domain: str) -> List[Dict[str, Any]]:
        """Check for changes since last scan"""
        # In production, would compare hashes, prices, features
        # For now, simulate change detection
        
        import random
        if random.random() > 0.7:  # 30% chance of change
            return [{
                'type': 'pricing_change',
                'details': 'New volume discounts introduced',
                'impact': 'high'
            }]
        return []
        

class WinLossAnalyzer:
    """Analyze win/loss patterns against competitors"""
    
    async def analyze(self, competitor: str) -> Dict[str, Any]:
        """Analyze win/loss data against specific competitor"""
        # In production, would pull from CRM
        # For now, return sample data
        
        return {
            'total_deals': 47,
            'wins': 31,
            'losses': 16,
            'win_rate': 0.66,
            'win_rate_delta': 0.15,  # We win 15% more than average
            'common_win_reasons': [
                'Superior technical support',
                'Better inventory availability',
                'Stronger local presence'
            ],
            'common_loss_reasons': [
                'Price sensitivity',
                'Existing relationship',
                'Specific product gap'
            ]
        }
