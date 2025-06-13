"""Palmer AI Core System - Real Implementation"""
import asyncio
from typing import Dict, Any, List
import anthropic
from .config import settings
from .utils.logger import get_logger
from .services.business_analyzer import BusinessAnalyzer

logger = get_logger(__name__)

class PalmerAICore:
    """The heart of Palmer AI - where analysis meets compassion"""

    def __init__(self):
        self.version = "2.0.0-ELITE"
        self.anthropic_client = anthropic.Anthropic(api_key=settings.anthropic_api_key)
        self.business_analyzer = BusinessAnalyzer()
        logger.info("Palmer AI Core initialized with Claude integration")

    async def analyze_with_love(self, company_data: Dict[str, Any]) -> Dict[str, Any]:
        """Primary analysis method with compassionate insights using Claude"""
        company_name = company_data.get('name', 'Unknown Company')
        
        try:
            # Calculate MPB score using business analyzer
            mpb_score = self.business_analyzer.calculate_mpb_score(company_data)
            journey_stage = self.business_analyzer.generate_journey_stage(mpb_score)
            encouragement = self.business_analyzer.generate_encouragement(mpb_score, company_name)
            
            # Create analysis prompt for Claude
            analysis_prompt = f"""
            As Palmer AI, provide a compassionate business analysis for:
            
            Company: {company_name}
            Website: {company_data.get('website', 'N/A')}
            Industry: {company_data.get('industry', 'General')}
            Description: {company_data.get('description', 'N/A')}
            
            Current MPB Score: {mpb_score:.1f}/100
            Journey Stage: {journey_stage}
            
            Provide insights on:
            1. Key strengths and opportunities
            2. Growth recommendations
            3. Potential challenges to address
            4. Compassionate guidance for improvement
            
            Remember: We honor Mia Palmer Barreto's memory by helping businesses reach their personal best with love and understanding. 💜
            """
            
            # Call Claude for detailed analysis
            claude_analysis = await self._call_claude(analysis_prompt)
            
            # Combine algorithmic and AI insights
            result = {
                "status": "success",
                "company_name": company_name,
                "mpb_score": round(mpb_score, 1),
                "journey_stage": journey_stage,
                "encouragement": encouragement,
                "claude_analysis": claude_analysis,
                "business_insights": {
                    "industry": self.business_analyzer._detect_industry(company_data),
                    "website_quality": "professional" if company_data.get('website') and self.business_analyzer._is_professional_website(company_data['website']) else "basic",
                    "description_quality": "detailed" if len(company_data.get('description', '')) > 100 else "basic"
                },
                "mia_blessing": "💜 Your journey to personal best honors those who believe in you. Keep growing with compassion. 💜",
                "claude_powered": True,
                "version": self.version
            }
            
            logger.info(f"Completed analysis for {company_name} - MPB Score: {mpb_score:.1f}")
            return result
            
        except Exception as e:
            logger.error(f"Analysis failed for {company_name}: {e}")
            return self._fallback_analysis(company_name)

    async def _call_claude(self, prompt: str) -> str:
        """Make API call to Claude"""
        try:
            message = self.anthropic_client.messages.create(
                model=settings.anthropic_model,
                max_tokens=settings.claude_max_tokens,
                temperature=settings.claude_temperature,
                messages=[{"role": "user", "content": prompt}]
            )
            return message.content[0].text
        except Exception as e:
            logger.error(f"Claude API call failed: {e}")
            raise

    def _fallback_analysis(self, company_name: str) -> Dict[str, Any]:
        """Fallback when Claude API fails"""
        return {
            "status": "partial_success",
            "company_name": company_name,
            "mpb_score": settings.fallback_mpb_score,
            "journey_stage": "🌿 Growing Stronger",
            "message": f"Basic analysis for {company_name}. Full AI analysis temporarily unavailable.",
            "encouragement": "Every step forward is progress worth celebrating.",
            "mia_blessing": "💜 Your resilience shines even when systems face challenges. 💜",
            "claude_powered": False,
            "version": self.version
        }

    async def quick_health_check(self) -> Dict[str, Any]:
        """Quick system health check"""
        try:
            test_response = await self._call_claude("Hello! Respond with exactly: 'Palmer AI systems operational 💜'")
            return {
                "core_status": "healthy",
                "claude_api": "connected",
                "version": self.version,
                "test_response": test_response.strip()
            }
        except Exception as e:
            return {
                "core_status": "degraded", 
                "claude_api": "disconnected",
                "version": self.version,
                "error": str(e)
            }
