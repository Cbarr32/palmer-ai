"""
Palmer AI Analysis Agent
The brain that turns data into decisions
"""
import json
from typing import Dict, List, Any, Optional
from datetime import datetime
import numpy as np
from dataclasses import dataclass

from src.palmer_ai.core.logger import get_logger

logger = get_logger(__name__)

@dataclass
class InsightScore:
    """Score and rank insights by business impact"""
    insight: Dict[str, Any]
    impact_score: float
    confidence: float
    urgency: str
    

class DistributorAnalysisAgent:
    """
    The AI brain that analyzes all data and generates actionable intelligence
    This is what makes Palmer AI worth $497/month
    """
    
    def __init__(self):
        self.analysis_patterns = {
            'inventory_health': self._analyze_inventory_health,
            'pricing_optimization': self._analyze_pricing_opportunities,
            'customer_patterns': self._analyze_customer_patterns,
            'competitive_position': self._analyze_competitive_position,
            'growth_opportunities': self._identify_growth_opportunities
        }
        
    async def generate_intelligence_report(
        self,
        excel_data: Optional[Dict] = None,
        competitor_data: Optional[Dict] = None,
        historical_data: Optional[List[Dict]] = None
    ) -> Dict[str, Any]:
        """Generate comprehensive intelligence report"""
        logger.info("Generating intelligence report")
        
        analyses = {}
        
        for analysis_type, analyzer in self.analysis_patterns.items():
            try:
                result = await analyzer(excel_data, competitor_data, historical_data)
                analyses[analysis_type] = result
            except Exception as e:
                logger.error(f"Analysis {analysis_type} failed: {e}")
                analyses[analysis_type] = {'error': str(e)}
                
        all_insights = self._collect_all_insights(analyses)
        ranked_insights = self._rank_insights(all_insights)
        executive_summary = self._generate_executive_summary(ranked_insights)
        roi_projections = self._calculate_roi_projections(ranked_insights)
        action_plan = self._build_action_plan(ranked_insights)
        
        return {
            'report_date': datetime.utcnow(),
            'executive_summary': executive_summary,
            'top_insights': ranked_insights[:10],
            'detailed_analyses': analyses,
            'roi_projections': roi_projections,
            'action_plan': action_plan,
            'subscription_value': self._calculate_subscription_value(ranked_insights)
        }
        
    async def _analyze_inventory_health(
        self, 
        excel_data: Optional[Dict],
        competitor_data: Optional[Dict],
        historical_data: Optional[List[Dict]]
    ) -> Dict[str, Any]:
        """Analyze inventory health and opportunities"""
        insights = []
        metrics = {}
        
        if excel_data and 'sheets_data' in excel_data:
            for sheet_name, sheet_data in excel_data['sheets_data'].items():
                if sheet_data.get('detected_type') == 'inventory':
                    metrics['total_skus'] = sheet_data.get('row_count', 0)
                    
                    if 'patterns' in sheet_data:
                        for col, stats in sheet_data['patterns'].items():
                            if 'qty' in col.lower() or 'quantity' in col.lower():
                                avg_qty = stats.get('mean', 0)
                                if avg_qty < 10:
                                    insights.append({
                                        'type': 'low_stock_risk',
                                        'title': 'Low Average Stock Levels',
                                        'description': f"Average quantity of {avg_qty:.1f} units indicates potential stockout risk",
                                        'impact': 'Could be losing sales due to stockouts',
                                        'recommendation': 'Implement automated reorder points',
                                        'potential_value': '$50K-200K in prevented lost sales'
                                    })
                                    
        if metrics.get('total_skus', 0) > 1000:
            insights.append({
                'type': 'dead_inventory',
                'title': 'Large SKU Count Indicates Dead Inventory',
                'description': f"Managing {metrics['total_skus']} SKUs likely includes 20-30% dead inventory",
                'impact': 'Tied up working capital',
                'recommendation': 'Implement ABC analysis and liquidation strategy',
                'potential_value': '$100K-500K in freed working capital'
            })
            
        return {
            'metrics': metrics,
            'insights': insights,
            'health_score': self._calculate_inventory_health_score(metrics)
        }
        
    async def _analyze_pricing_opportunities(
        self,
        excel_data: Optional[Dict],
        competitor_data: Optional[Dict],
        historical_data: Optional[List[Dict]]
    ) -> Dict[str, Any]:
        """Find pricing optimization opportunities"""
        insights = []
        opportunities = {}
        
        if competitor_data and 'pricing_intelligence' in competitor_data:
            comp_pricing = competitor_data['pricing_intelligence']
            
            if 'price_range' in comp_pricing:
                avg_price = comp_pricing['price_range']['average']
                insights.append({
                    'type': 'competitive_pricing',
                    'title': 'Competitor Pricing Intelligence',
                    'description': f"Competitor average price: ${avg_price:.2f}",
                    'impact': 'Pricing positioning opportunity',
                    'recommendation': 'Adjust pricing strategy based on value proposition',
                    'potential_value': '2-5% margin improvement'
                })
                
            if 'discount_patterns' in comp_pricing:
                avg_discount = comp_pricing['discount_patterns']['average_discount']
                if avg_discount > 0.15:
                    insights.append({
                        'type': 'discount_strategy',
                        'title': 'Competitor Heavy Discounting Detected',
                        'description': f"Competitors discounting {avg_discount:.0%} on average",
                        'impact': 'Price war risk',
                        'recommendation': 'Focus on value-add services rather than price matching',
                        'potential_value': 'Protect margins worth $100K+ annually'
                    })
                    
        if excel_data and 'sheets_data' in excel_data:
            for sheet_name, sheet_data in excel_data['sheets_data'].items():
                if sheet_data.get('detected_type') == 'pricing':
                    if 'patterns' in sheet_data:
                        for col, stats in sheet_data['patterns'].items():
                            if 'margin' in col.lower():
                                avg_margin = stats.get('mean', 0)
                                if avg_margin < 0.2:
                                    insights.append({
                                        'type': 'margin_improvement',
                                        'title': 'Below-Target Margins Detected',
                                        'description': f"Average margin of {avg_margin:.1%} is below industry standard",
                                        'impact': 'Leaving money on the table',
                                        'recommendation': 'Implement value-based pricing strategy',
                                        'potential_value': '3-7% revenue increase'
                                    })
                                    
        return {
            'insights': insights,
            'opportunities': opportunities,
            'pricing_score': self._calculate_pricing_score(insights)
        }
        
    async def _analyze_customer_patterns(
        self,
        excel_data: Optional[Dict],
        competitor_data: Optional[Dict],
        historical_data: Optional[List[Dict]]
    ) -> Dict[str, Any]:
        """Analyze customer patterns and opportunities"""
        insights = []
        patterns = {}
        
        if excel_data and 'metrics' in excel_data:
            if excel_data['metrics'].get('customer_concentration', 0) > 0.3:
                insights.append({
                    'type': 'customer_risk',
                    'title': 'High Customer Concentration Risk',
                    'description': 'Top customers represent over 30% of business',
                    'impact': 'Business vulnerability',
                    'recommendation': 'Diversification strategy needed',
                    'potential_value': 'Reduce business risk by 50%'
                })
                
        if excel_data and 'sheets_data' in excel_data:
            for sheet_name, sheet_data in excel_data['sheets_data'].items():
                if sheet_data.get('detected_type') == 'customer':
                    total_customers = sheet_data.get('row_count', 0)
                    patterns['total_customers'] = total_customers
                    
                    if total_customers < 100:
                        insights.append({
                            'type': 'growth_opportunity',
                            'title': 'Limited Customer Base',
                            'description': f"Only {total_customers} active customers",
                            'impact': 'Growth constraint',
                            'recommendation': 'Customer acquisition campaign',
                            'potential_value': '$500K+ in new revenue potential'
                        })
                        
        return {
            'insights': insights,
            'patterns': patterns,
            'customer_health_score': self._calculate_customer_score(patterns)
        }
        
    async def _analyze_competitive_position(
        self,
        excel_data: Optional[Dict],
        competitor_data: Optional[Dict],
        historical_data: Optional[List[Dict]]
    ) -> Dict[str, Any]:
        """Analyze competitive position"""
        insights = []
        position_metrics = {}
        
        if competitor_data:
            if 'technology_stack' in competitor_data:
                tech = competitor_data['technology_stack']
                if tech.get('ecommerce_platform'):
                    insights.append({
                        'type': 'technology_gap',
                        'title': f"Competitor Using {tech['ecommerce_platform']}",
                        'description': 'Modern e-commerce platform detected',
                        'impact': 'Customer experience disadvantage',
                        'recommendation': 'Modernize digital presence',
                        'potential_value': '10-20% online sales increase'
                    })
                    
            if 'unique_selling_props' in competitor_data:
                usps = competitor_data['unique_selling_props']
                if any('same day' in usp.lower() for usp in usps):
                    insights.append({
                        'type': 'service_gap',
                        'title': 'Competitor Offers Same-Day Delivery',
                        'description': 'Speed of service competitive disadvantage',
                        'impact': 'Losing time-sensitive orders',
                        'recommendation': 'Implement local delivery network',
                        'potential_value': '$200K+ in captured urgent orders'
                    })
                    
        return {
            'insights': insights,
            'position_metrics': position_metrics,
            'competitive_score': self._calculate_competitive_score(insights)
        }
        
    async def _identify_growth_opportunities(
        self,
        excel_data: Optional[Dict],
        competitor_data: Optional[Dict],
        historical_data: Optional[List[Dict]]
    ) -> Dict[str, Any]:
        """Identify growth opportunities"""
        opportunities = []
        
        if excel_data and 'insights' in excel_data:
            opportunities.append({
                'type': 'cross_sell',
                'title': 'Cross-Sell Opportunity Analysis',
                'description': 'Identify complementary products for bundling',
                'implementation': '2-4 weeks',
                'expected_impact': '15-25% increase in average order value',
                'palmer_ai_features': [
                    'Automated bundle recommendations',
                    'Customer purchase pattern analysis',
                    'Dynamic bundle pricing'
                ]
            })
            
        opportunities.append({
            'type': 'digital_transformation',
            'title': 'Digital Self-Service Portal',
            'description': 'Enable customers to self-serve for routine orders',
            'implementation': '4-8 weeks with Palmer AI',
            'expected_impact': '30% reduction in order processing costs',
            'palmer_ai_features': [
                'Customer portal with AI search',
                'Automated quote generation',
                'Real-time inventory visibility'
            ]
        })
        
        if competitor_data:
            opportunities.append({
                'type': 'market_expansion',
                'title': 'Geographic Expansion Opportunity',
                'description': 'Competitor analysis reveals underserved markets',
                'implementation': '3-6 months',
                'expected_impact': '$1M+ in new market revenue',
                'palmer_ai_features': [
                    'Market demand analysis',
                    'Competitive landscape mapping',
                    'ROI projections by territory'
                ]
            })
            
        return {
            'opportunities': opportunities,
            'total_opportunity_value': self._calculate_total_opportunity(opportunities)
        }
        
    def _rank_insights(self, insights: List[Dict]) -> List[InsightScore]:
        """Rank insights by business impact"""
        scored_insights = []
        
        for insight in insights:
            impact_score = self._calculate_impact_score(insight)
            urgency = self._determine_urgency(insight)
            confidence = self._calculate_confidence(insight)
            
            scored_insights.append(InsightScore(
                insight=insight,
                impact_score=impact_score,
                confidence=confidence,
                urgency=urgency
            ))
            
        scored_insights.sort(key=lambda x: x.impact_score, reverse=True)
        return scored_insights
        
    def _calculate_impact_score(self, insight: Dict) -> float:
        """Calculate business impact score 0-100"""
        score = 50
        
        if 'potential_value' in insight:
            value_str = insight['potential_value'].lower()
            if '$1m' in value_str or 'million' in value_str:
                score += 40
            elif '$500k' in value_str:
                score += 35
            elif '$200k' in value_str:
                score += 30
            elif '$100k' in value_str:
                score += 25
            elif '$50k' in value_str:
                score += 20
            elif '%' in value_str:
                import re
                percentages = re.findall(r'(\d+)%', value_str)
                if percentages:
                    max_pct = max(int(p) for p in percentages)
                    score += min(max_pct * 2, 40)
                    
        high_impact_types = ['customer_risk', 'dead_inventory', 'margin_improvement']
        if insight.get('type') in high_impact_types:
            score += 10
            
        return min(score, 100)
        
    def _determine_urgency(self, insight: Dict) -> str:
        """Determine urgency of insight"""
        urgent_keywords = ['risk', 'losing', 'immediate', 'critical']
        description = insight.get('description', '').lower()
        
        if any(keyword in description for keyword in urgent_keywords):
            return 'immediate'
        elif 'opportunity' in insight.get('type', ''):
            return 'short_term'
        else:
            return 'long_term'
            
    def _calculate_confidence(self, insight: Dict) -> float:
        """Calculate confidence in insight"""
        confidence = 0.85
        
        if 'based on' in insight.get('description', '').lower():
            confidence += 0.1
            
        return min(confidence, 0.95)
        
    def _generate_executive_summary(self, ranked_insights: List[InsightScore]) -> Dict[str, Any]:
        """Generate executive summary"""
        immediate_actions = [i for i in ranked_insights if i.urgency == 'immediate']
        total_opportunity = sum(self._extract_dollar_value(i.insight) for i in ranked_insights[:10])
        
        return {
            'key_findings': len(ranked_insights),
            'immediate_actions_required': len(immediate_actions),
            'total_opportunity_identified': f"${total_opportunity/1000:.0f}K+",
            'top_three_priorities': [
                {
                    'priority': i+1,
                    'insight': insight.insight['title'],
                    'impact': insight.insight.get('potential_value', 'High impact'),
                    'urgency': insight.urgency
                }
                for i, insight in enumerate(ranked_insights[:3])
            ],
            'executive_recommendation': self._generate_recommendation(ranked_insights)
        }
        
    def _extract_dollar_value(self, insight: Dict) -> float:
        """Extract dollar value from insight text"""
        import re
        
        value_text = insight.get('potential_value', '')
        dollar_pattern = r'\$(\d+)([KMk])?'
        match = re.search(dollar_pattern, value_text)
        
        if match:
            value = float(match.group(1))
            multiplier = match.group(2)
            
            if multiplier and multiplier.upper() == 'K':
                value *= 1000
            elif multiplier and multiplier.upper() == 'M':
                value *= 1000000
                
            return value
            
        return 50000
        
    def _generate_recommendation(self, ranked_insights: List[InsightScore]) -> str:
        """Generate executive recommendation"""
        if not ranked_insights:
            return "Continue monitoring operations."
            
        top_insight = ranked_insights[0]
        
        if top_insight.urgency == 'immediate':
            return f"Immediate action required: {top_insight.insight['title']}. " \
                   f"Potential impact: {top_insight.insight.get('potential_value', 'Significant')}."
        else:
            return f"Focus on {top_insight.insight['title']} for maximum business impact. " \
                   f"Palmer AI can help implement solutions within 2-4 weeks."
                   
    def _calculate_roi_projections(self, ranked_insights: List[InsightScore]) -> Dict[str, Any]:
        """Calculate ROI projections"""
        year1_value = 0
        year2_value = 0
        year3_value = 0
        
        for insight in ranked_insights[:10]:
            value = self._extract_dollar_value(insight.insight)
            
            if insight.urgency == 'immediate':
                year1_value += value * 0.7
                year2_value += value * 0.2
                year3_value += value * 0.1
            elif insight.urgency == 'short_term':
                year1_value += value * 0.3
                year2_value += value * 0.5
                year3_value += value * 0.2
            else:
                year1_value += value * 0.1
                year2_value += value * 0.4
                year3_value += value * 0.5
                
        annual_cost = 497 * 12
        
        return {
            'three_year_projection': {
                'year_1': {
                    'value': f"${year1_value:,.0f}",
                    'cost': f"${annual_cost:,.0f}",
                    'net_benefit': f"${year1_value - annual_cost:,.0f}",
                    'roi': f"{((year1_value - annual_cost) / annual_cost * 100):.0f}%"
                },
                'year_2': {
                    'value': f"${year2_value:,.0f}",
                    'cost': f"${annual_cost:,.0f}",
                    'net_benefit': f"${year2_value - annual_cost:,.0f}",
                    'roi': f"{((year2_value - annual_cost) / annual_cost * 100):.0f}%"
                },
                'year_3': {
                    'value': f"${year3_value:,.0f}",
                    'cost': f"${annual_cost:,.0f}",
                    'net_benefit': f"${year3_value - annual_cost:,.0f}",
                    'roi': f"{((year3_value - annual_cost) / annual_cost * 100):.0f}%"
                }
            },
            'total_three_year_value': f"${year1_value + year2_value + year3_value:,.0f}",
            'total_three_year_cost': f"${annual_cost * 3:,.0f}",
            'total_roi': f"{(((year1_value + year2_value + year3_value) - (annual_cost * 3)) / (annual_cost * 3) * 100):.0f}%",
            'payback_period': 'Less than 2 months'
        }
        
    def _build_action_plan(self, ranked_insights: List[InsightScore]) -> List[Dict]:
        """Build prioritized action plan"""
        action_plan = []
        
        immediate = [i for i in ranked_insights if i.urgency == 'immediate'][:3]
        short_term = [i for i in ranked_insights if i.urgency == 'short_term'][:3]
        long_term = [i for i in ranked_insights if i.urgency == 'long_term'][:2]
        
        phase = 1
        
        for insight in immediate:
            action_plan.append({
                'phase': phase,
                'timeline': '0-30 days',
                'action': insight.insight['title'],
                'description': insight.insight.get('recommendation', ''),
                'expected_outcome': insight.insight.get('potential_value', ''),
                'palmer_ai_support': 'Full implementation support with Palmer AI platform'
            })
        phase += 1
        
        for insight in short_term:
            action_plan.append({
                'phase': phase,
                'timeline': '30-60 days',
                'action': insight.insight['title'],
                'description': insight.insight.get('recommendation', ''),
                'expected_outcome': insight.insight.get('potential_value', ''),
                'palmer_ai_support': 'Automated workflows and intelligence'
            })
        phase += 1
        
        for insight in long_term:
            action_plan.append({
                'phase': phase,
                'timeline': '60-90 days',
                'action': insight.insight['title'],
                'description': insight.insight.get('recommendation', ''),
                'expected_outcome': insight.insight.get('potential_value', ''),
                'palmer_ai_support': 'Strategic planning and optimization'
            })
            
        return action_plan
        
    def _calculate_subscription_value(self, ranked_insights: List[InsightScore]) -> Dict[str, Any]:
        """Calculate the value of Palmer AI subscription"""
        total_opportunities = sum(self._extract_dollar_value(i.insight) for i in ranked_insights[:10])
        monthly_value = total_opportunities / 12
        
        if monthly_value > 50000:
            recommended_tier = 'enterprise'
            monthly_cost = 497
        elif monthly_value > 20000:
            recommended_tier = 'professional'
            monthly_cost = 297
        else:
            recommended_tier = 'basic'
            monthly_cost = 97
            
        return {
            'recommended_tier': recommended_tier,
            'monthly_cost': f"${monthly_cost}",
            'monthly_value': f"${monthly_value:,.0f}",
            'value_to_cost_ratio': f"{monthly_value / monthly_cost:.0f}:1",
            'annual_roi': f"{((monthly_value * 12 - monthly_cost * 12) / (monthly_cost * 12) * 100):,.0f}%"
        }
        
    def _collect_all_insights(self, analyses: Dict) -> List[Dict]:
        """Collect all insights from analyses"""
        all_insights = []
        
        for analysis_type, analysis_data in analyses.items():
            if 'insights' in analysis_data:
                all_insights.extend(analysis_data['insights'])
                
        return all_insights
        
    def _calculate_inventory_health_score(self, metrics: Dict) -> float:
        """Calculate inventory health score"""
        score = 50
        
        if metrics.get('total_skus', 0) > 5000:
            score -= 20
        elif metrics.get('total_skus', 0) > 2000:
            score -= 10
            
        return max(score, 0)
        
    def _calculate_pricing_score(self, insights: List[Dict]) -> float:
        """Calculate pricing optimization score"""
        base_score = 70
        
        for insight in insights:
            if 'margin' in insight.get('type', ''):
                base_score -= 15
            elif 'discount' in insight.get('type', ''):
                base_score -= 10
                
        return max(base_score, 0)
        
    def _calculate_customer_score(self, patterns: Dict) -> float:
        """Calculate customer health score"""
        score = 60
        
        if patterns.get('total_customers', 0) < 50:
            score -= 30
        elif patterns.get('total_customers', 0) < 100:
            score -= 15
            
        return max(score, 0)
        
    def _calculate_competitive_score(self, insights: List[Dict]) -> float:
        """Calculate competitive position score"""
        score = 50
        
        for insight in insights:
            if 'gap' in insight.get('type', ''):
                score -= 10
                
        return max(score, 0)
        
    def _calculate_total_opportunity(self, opportunities: List[Dict]) -> str:
        """Calculate total opportunity value"""
        total = 0
        
        for opp in opportunities:
            impact = opp.get('expected_impact', '')
            if '$1M' in impact:
                total += 1000000
            elif '$500K' in impact:
                total += 500000
            elif '$200K' in impact:
                total += 200000
            elif '$100K' in impact:
                total += 100000
            elif '$50K' in impact:
                total += 50000
                
        if total > 1000000:
            return f"${total/1000000:.1f}M+"
        else:
            return f"${total/1000:.0f}K+"

analysis_agent = DistributorAnalysisAgent()
