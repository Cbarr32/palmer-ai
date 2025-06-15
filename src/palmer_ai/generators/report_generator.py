"""
Palmer AI Report Generator
Professional reports that sell the value
"""
from typing import Dict, List, Any
from datetime import datetime
import json
from pathlib import Path

from src.palmer_ai.core.logger import get_logger

logger = get_logger(__name__)

class IntelligenceReportGenerator:
    """
    Generate professional PDF/HTML reports
    This is what justifies the $497/month price
    """
    
    def __init__(self):
        self.report_templates = {
            'executive': self._generate_executive_report,
            'detailed': self._generate_detailed_report,
            'opportunity': self._generate_opportunity_report,
            'competitive': self._generate_competitive_report
        }
        
    async def generate_report(
        self,
        report_type: str,
        analysis_data: Dict[str, Any],
        company_name: str
    ) -> Dict[str, Any]:
        """Generate professional intelligence report"""
        logger.info(f"Generating {report_type} report for {company_name}")
        
        if report_type not in self.report_templates:
            report_type = 'executive'
            
        report_content = await self.report_templates[report_type](
            analysis_data, company_name
        )
        
        # Save report
        report_path = await self._save_report(report_content, company_name, report_type)
        
        return {
            'report_type': report_type,
            'company_name': company_name,
            'generated_at': datetime.utcnow(),
            'report_path': report_path,
            'content': report_content
        }
        
    async def _generate_executive_report(
        self,
        analysis_data: Dict[str, Any],
        company_name: str
    ) -> Dict[str, Any]:
        """Generate executive summary report"""
        
        executive_summary = analysis_data.get('executive_summary', {})
        roi_projections = analysis_data.get('roi_projections', {})
        top_insights = analysis_data.get('top_insights', [])
        
        report = {
            'title': f'Executive Intelligence Report - {company_name}',
            'date': datetime.utcnow().strftime('%B %d, %Y'),
            'sections': [
                {
                    'title': 'Executive Summary',
                    'content': self._format_executive_summary(executive_summary)
                },
                {
                    'title': 'Top Strategic Priorities',
                    'content': self._format_top_priorities(top_insights[:3])
                },
                {
                    'title': 'Financial Impact Analysis',
                    'content': self._format_roi_projections(roi_projections)
                },
                {
                    'title': 'Immediate Action Items',
                    'content': self._format_action_items(top_insights)
                },
                {
                    'title': 'Palmer AI Value Proposition',
                    'content': self._format_value_proposition(analysis_data)
                }
            ]
        }
        
        return report
        
    async def _generate_detailed_report(
        self,
        analysis_data: Dict[str, Any],
        company_name: str
    ) -> Dict[str, Any]:
        """Generate detailed analysis report"""
        
        report = {
            'title': f'Detailed Business Intelligence Report - {company_name}',
            'date': datetime.utcnow().strftime('%B %d, %Y'),
            'sections': []
        }
        
        # Add all analysis sections
        if 'detailed_analyses' in analysis_data:
            for analysis_type, analysis_content in analysis_data['detailed_analyses'].items():
                section = {
                    'title': self._format_section_title(analysis_type),
                    'content': self._format_detailed_analysis(analysis_content)
                }
                report['sections'].append(section)
                
        # Add insights section
        if 'top_insights' in analysis_data:
            report['sections'].append({
                'title': 'Comprehensive Insights & Recommendations',
                'content': self._format_all_insights(analysis_data['top_insights'])
            })
            
        # Add action plan
        if 'action_plan' in analysis_data:
            report['sections'].append({
                'title': '90-Day Implementation Roadmap',
                'content': self._format_action_plan(analysis_data['action_plan'])
            })
            
        return report
        
    async def _generate_opportunity_report(
        self,
        analysis_data: Dict[str, Any],
        company_name: str
    ) -> Dict[str, Any]:
        """Generate opportunity-focused report"""
        
        opportunities = []
        
        # Extract opportunities from analyses
        if 'detailed_analyses' in analysis_data:
            for analysis in analysis_data['detailed_analyses'].values():
                if 'opportunities' in analysis:
                    opportunities.extend(analysis['opportunities'])
                    
        report = {
            'title': f'Growth Opportunity Analysis - {company_name}',
            'date': datetime.utcnow().strftime('%B %d, %Y'),
            'sections': [
                {
                    'title': 'Executive Opportunity Summary',
                    'content': self._format_opportunity_summary(opportunities)
                },
                {
                    'title': 'Revenue Growth Opportunities',
                    'content': self._format_revenue_opportunities(opportunities)
                },
                {
                    'title': 'Cost Reduction Opportunities',
                    'content': self._format_cost_opportunities(opportunities)
                },
                {
                    'title': 'Competitive Advantage Opportunities',
                    'content': self._format_competitive_opportunities(opportunities)
                },
                {
                    'title': 'Implementation Timeline',
                    'content': self._format_opportunity_timeline(opportunities)
                }
            ]
        }
        
        return report
        
    async def _generate_competitive_report(
        self,
        analysis_data: Dict[str, Any],
        company_name: str
    ) -> Dict[str, Any]:
        """Generate competitive analysis report"""
        
        competitor_data = {}
        
        # Extract competitor data
        if 'detailed_analyses' in analysis_data:
            if 'competitive_position' in analysis_data['detailed_analyses']:
                competitor_data = analysis_data['detailed_analyses']['competitive_position']
                
        report = {
            'title': f'Competitive Intelligence Report - {company_name}',
            'date': datetime.utcnow().strftime('%B %d, %Y'),
            'sections': [
                {
                    'title': 'Competitive Landscape Overview',
                    'content': self._format_competitive_overview(competitor_data)
                },
                {
                    'title': 'Competitor Strengths & Weaknesses',
                    'content': self._format_competitor_analysis(competitor_data)
                },
                {
                    'title': 'Market Positioning Strategy',
                    'content': self._format_positioning_strategy(competitor_data)
                },
                {
                    'title': 'Competitive Response Plan',
                    'content': self._format_response_plan(competitor_data)
                }
            ]
        }
        
        return report
        
    def _format_executive_summary(self, summary: Dict) -> str:
        """Format executive summary section"""
        content = []
        
        if 'key_findings' in summary:
            content.append(f"**Key Findings:** {summary['key_findings']} critical insights identified")
            
        if 'total_opportunity_identified' in summary:
            content.append(f"**Total Opportunity:** {summary['total_opportunity_identified']}")
            
        if 'immediate_actions_required' in summary:
            content.append(f"**Immediate Actions:** {summary['immediate_actions_required']} urgent items")
            
        if 'executive_recommendation' in summary:
            content.append(f"\n**Recommendation:** {summary['executive_recommendation']}")
            
        return '\n'.join(content)
        
    def _format_top_priorities(self, insights: List) -> str:
        """Format top priorities section"""
        content = []
        
        for i, insight_score in enumerate(insights):
            insight = insight_score.insight if hasattr(insight_score, 'insight') else insight_score
            
            priority = f"### Priority {i+1}: {insight.get('title', 'Unknown')}\n"
            priority += f"**Impact:** {insight.get('potential_value', 'High impact')}\n"
            priority += f"**Description:** {insight.get('description', '')}\n"
            priority += f"**Recommended Action:** {insight.get('recommendation', '')}"
            
            content.append(priority)
            
        return '\n\n'.join(content)
        
    def _format_roi_projections(self, roi_data: Dict) -> str:
        """Format ROI projections section"""
        content = []
        
        if 'three_year_projection' in roi_data:
            content.append("### Three-Year Financial Impact\n")
            
            for year, data in roi_data['three_year_projection'].items():
                year_num = year.split('_')[1]
                content.append(f"**Year {year_num}:**")
                content.append(f"- Expected Value: {data['value']}")
                content.append(f"- Palmer AI Cost: {data['cost']}")
                content.append(f"- Net Benefit: {data['net_benefit']}")
                content.append(f"- ROI: {data['roi']}\n")
                
        if 'total_roi' in roi_data:
            content.append(f"**Total 3-Year ROI:** {roi_data['total_roi']}")
            
        if 'payback_period' in roi_data:
            content.append(f"**Payback Period:** {roi_data['payback_period']}")
            
        return '\n'.join(content)
        
    def _format_action_items(self, insights: List) -> str:
        """Format immediate action items"""
        content = []
        
        immediate_actions = [
            i for i in insights 
            if hasattr(i, 'urgency') and i.urgency == 'immediate'
        ][:5]
        
        for i, insight_score in enumerate(immediate_actions):
            insight = insight_score.insight if hasattr(insight_score, 'insight') else insight_score
            
            action = f"{i+1}. **{insight.get('title', 'Action')}**\n"
            action += f"   - {insight.get('recommendation', 'Take action')}\n"
            action += f"   - Expected Impact: {insight.get('potential_value', 'Significant')}"
            
            content.append(action)
            
        return '\n'.join(content)
        
    def _format_value_proposition(self, analysis_data: Dict) -> str:
        """Format Palmer AI value proposition"""
        content = []
        
        content.append("### Why Palmer AI?")
        content.append("- **Replace $30K+ enterprise tools** with intelligent automation")
        content.append("- **Implementation in days, not months** - no IT required")
        content.append("- **Guaranteed ROI** - typically 10x+ return on investment")
        
        if 'subscription_value' in analysis_data:
            sub_value = analysis_data['subscription_value']
            content.append(f"\n**Recommended Plan:** {sub_value.get('recommended_tier', 'Professional').title()} - {sub_value.get('monthly_cost', '$297')}/month")
            content.append(f"**Value Ratio:** {sub_value.get('value_to_cost_ratio', '100:1')}")
            
        return '\n'.join(content)
        
    def _format_section_title(self, analysis_type: str) -> str:
        """Format section title from analysis type"""
        title_map = {
            'inventory_health': 'Inventory Optimization Analysis',
            'pricing_optimization': 'Pricing Strategy Analysis',
            'customer_patterns': 'Customer Intelligence',
            'competitive_position': 'Competitive Positioning',
            'growth_opportunities': 'Growth Opportunity Analysis'
        }
        
        return title_map.get(analysis_type, analysis_type.replace('_', ' ').title())
        
    def _format_detailed_analysis(self, analysis: Dict) -> str:
        """Format detailed analysis section"""
        content = []
        
        if 'metrics' in analysis:
            content.append("### Key Metrics")
            for metric, value in analysis['metrics'].items():
                content.append(f"- **{metric.replace('_', ' ').title()}:** {value}")
            content.append("")
            
        if 'insights' in analysis:
            content.append("### Insights")
            for insight in analysis['insights']:
                content.append(f"**{insight.get('title', 'Insight')}**")
                content.append(f"- {insight.get('description', '')}")
                if 'recommendation' in insight:
                    content.append(f"- *Recommendation:* {insight['recommendation']}")
                content.append("")
                
        return '\n'.join(content)
        
    def _format_all_insights(self, insights: List) -> str:
        """Format all insights comprehensively"""
        content = []
        
        # Group by urgency
        immediate = []
        short_term = []
        long_term = []
        
        for insight_score in insights:
            if hasattr(insight_score, 'urgency'):
                if insight_score.urgency == 'immediate':
                    immediate.append(insight_score)
                elif insight_score.urgency == 'short_term':
                    short_term.append(insight_score)
                else:
                    long_term.append(insight_score)
                    
        if immediate:
            content.append("### Immediate Actions Required")
            for i in immediate:
                content.append(self._format_single_insight(i))
                
        if short_term:
            content.append("\n### Short-Term Opportunities (30-60 days)")
            for i in short_term:
                content.append(self._format_single_insight(i))
                
        if long_term:
            content.append("\n### Long-Term Strategic Initiatives")
            for i in long_term:
                content.append(self._format_single_insight(i))
                
        return '\n'.join(content)
        
    def _format_single_insight(self, insight_score) -> str:
        """Format a single insight"""
        insight = insight_score.insight if hasattr(insight_score, 'insight') else insight_score
        
        content = f"\n**{insight.get('title', 'Insight')}**\n"
        content += f"- *Impact Score:* {getattr(insight_score, 'impact_score', 'High')}/100\n"
        content += f"- *Description:* {insight.get('description', '')}\n"
        content += f"- *Potential Value:* {insight.get('potential_value', 'Significant')}\n"
        content += f"- *Recommended Action:* {insight.get('recommendation', 'Review and implement')}"
        
        return content
        
    def _format_action_plan(self, action_plan: List[Dict]) -> str:
        """Format 90-day action plan"""
        content = []
        
        current_phase = 0
        for action in action_plan:
            if action['phase'] != current_phase:
                current_phase = action['phase']
                content.append(f"\n### Phase {current_phase}: {action['timeline']}")
                
            content.append(f"\n**{action['action']}**")
            content.append(f"- {action['description']}")
            content.append(f"- *Expected Outcome:* {action['expected_outcome']}")
            content.append(f"- *Palmer AI Support:* {action['palmer_ai_support']}")
            
        return '\n'.join(content)
        
    def _format_opportunity_summary(self, opportunities: List[Dict]) -> str:
        """Format opportunity summary"""
        total_value = 0
        
        for opp in opportunities:
            impact = opp.get('expected_impact', '')
            if ' in impact:
                # Extract dollar value
                import re
                match = re.search(r'\$(\d+)([KM])?', impact)
                if match:
                    value = int(match.group(1))
                    if match.group(2) == 'K':
                        value *= 1000
                    elif match.group(2) == 'M':
                        value *= 1000000
                    total_value += value
                    
        content = [
            f"**Total Opportunities Identified:** {len(opportunities)}",
            f"**Combined Potential Value:** ${total_value:,}+",
            f"**Average Implementation Time:** 4-8 weeks",
            f"**Success Rate with Palmer AI:** 85%+"
        ]
        
        return '\n'.join(content)
        
    def _format_revenue_opportunities(self, opportunities: List[Dict]) -> str:
        """Format revenue growth opportunities"""
        revenue_opps = [o for o in opportunities if 'revenue' in str(o).lower()]
        
        content = []
        for opp in revenue_opps:
            content.append(f"**{opp.get('title', 'Opportunity')}**")
            content.append(f"- {opp.get('description', '')}")
            content.append(f"- *Impact:* {opp.get('expected_impact', 'Significant')}")
            content.append(f"- *Timeline:* {opp.get('implementation', '4-6 weeks')}")
            content.append("")
            
        return '\n'.join(content)
        
    def _format_cost_opportunities(self, opportunities: List[Dict]) -> str:
        """Format cost reduction opportunities"""
        cost_opps = [o for o in opportunities if 'cost' in str(o).lower() or 'capital' in str(o).lower()]
        
        content = []
        for opp in cost_opps:
            content.append(f"**{opp.get('title', 'Opportunity')}**")
            content.append(f"- {opp.get('description', '')}")
            content.append(f"- *Savings:* {opp.get('potential_impact', 'Significant')}")
            content.append("")
            
        return '\n'.join(content) if content else "No immediate cost reduction opportunities identified."
        
    def _format_competitive_opportunities(self, opportunities: List[Dict]) -> str:
        """Format competitive advantage opportunities"""
        comp_opps = [o for o in opportunities if 'competitive' in str(o).lower() or 'market' in str(o).lower()]
        
        content = []
        for opp in comp_opps:
            content.append(f"**{opp.get('title', 'Opportunity')}**")
            content.append(f"- {opp.get('description', '')}")
            content.append("")
            
        return '\n'.join(content) if content else "Focus on operational excellence for competitive advantage."
        
    def _format_opportunity_timeline(self, opportunities: List[Dict]) -> str:
        """Format opportunity implementation timeline"""
        content = [
            "### Implementation Roadmap",
            "",
            "**Weeks 1-2:** Initial setup and data integration",
            "**Weeks 3-4:** Quick wins implementation",
            "**Weeks 5-8:** Major system rollout",
            "**Weeks 9-12:** Optimization and scaling",
            "",
            "*Palmer AI provides hands-on support throughout the entire journey.*"
        ]
        
        return '\n'.join(content)
        
    def _format_competitive_overview(self, data: Dict) -> str:
        """Format competitive landscape overview"""
        content = [
            "Palmer AI's analysis reveals critical competitive intelligence:",
            "",
            "- Market is rapidly digitizing",
            "- Competitors investing heavily in technology",
            "- Customer expectations rising for instant service",
            "- Price transparency increasing margin pressure"
        ]
        
        return '\n'.join(content)
        
    def _format_competitor_analysis(self, data: Dict) -> str:
        """Format competitor strengths and weaknesses"""
        if 'insights' in data:
            return self._format_detailed_analysis(data)
        else:
            return "Detailed competitor analysis available with Palmer AI Professional."
            
    def _format_positioning_strategy(self, data: Dict) -> str:
        """Format market positioning strategy"""
        content = [
            "### Recommended Positioning Strategy",
            "",
            "1. **Differentiate on Service** - While competitors compete on price",
            "2. **Leverage Technology** - Offer instant quotes and real-time inventory",
            "3. **Build Relationships** - Use data to personalize every interaction",
            "4. **Create Value** - Bundle products and services intelligently"
        ]
        
        return '\n'.join(content)
        
    def _format_response_plan(self, data: Dict) -> str:
        """Format competitive response plan"""
        content = [
            "### 30-Day Competitive Response Plan",
            "",
            "**Week 1:** Implement Palmer AI core intelligence",
            "**Week 2:** Launch customer portal with AI search",
            "**Week 3:** Roll out dynamic pricing engine",
            "**Week 4:** Activate proactive customer outreach",
            "",
            "*Turn competitive threats into growth opportunities with Palmer AI.*"
        ]
        
        return '\n'.join(content)
        
    async def _save_report(
        self,
        report_content: Dict,
        company_name: str,
        report_type: str
    ) -> str:
        """Save report to file"""
        # Create reports directory
        reports_dir = Path("data/reports")
        reports_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate filename
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        filename = f"{company_name.replace(' ', '_')}_{report_type}_{timestamp}.json"
        filepath = reports_dir / filename
        
        # Save report
        with open(filepath, 'w') as f:
            json.dump(report_content, f, indent=2, default=str)
            
        logger.info(f"Report saved to {filepath}")
        
        return str(filepath)

# Create singleton
report_generator = IntelligenceReportGenerator()
