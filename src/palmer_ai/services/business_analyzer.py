"""Business Analysis Service for Palmer AI"""
import re
from typing import Dict, Any, List
from urllib.parse import urlparse
import asyncio

class BusinessAnalyzer:
    """Advanced business analysis algorithms"""
    
    def __init__(self):
        self.industry_keywords = {
            "technology": ["software", "ai", "tech", "app", "digital", "saas"],
            "healthcare": ["health", "medical", "hospital", "clinic", "care"],
            "finance": ["bank", "financial", "investment", "insurance", "fintech"],
            "retail": ["store", "shop", "retail", "ecommerce", "marketplace"],
            "education": ["school", "university", "education", "learning", "training"]
        }
    
    def calculate_mpb_score(self, company_data: Dict[str, Any]) -> float:
        """Calculate MPB (Most Personal Best) score"""
        score = 50.0  # Base score
        
        # Website quality indicator
        if company_data.get("website"):
            if self._is_professional_website(company_data["website"]):
                score += 15
            else:
                score += 5
        
        # Industry stability
        industry = self._detect_industry(company_data)
        industry_multipliers = {
            "technology": 1.2,
            "healthcare": 1.1,
            "finance": 1.0,
            "retail": 0.9,
            "education": 1.15
        }
        score *= industry_multipliers.get(industry, 1.0)
        
        # Company description quality
        description = company_data.get("description", "")
        if len(description) > 100:
            score += 10
        elif len(description) > 50:
            score += 5
        
        # Vision/mission keywords
        vision_keywords = ["mission", "vision", "purpose", "impact", "future", "innovation"]
        description_lower = description.lower()
        vision_score = sum(1 for keyword in vision_keywords if keyword in description_lower)
        score += min(vision_score * 3, 15)  # Max 15 points for vision
        
        # Cap score at 100
        return min(score, 100.0)
    
    def _detect_industry(self, company_data: Dict[str, Any]) -> str:
        """Detect company industry from available data"""
        text_to_analyze = " ".join([
            company_data.get("name", ""),
            company_data.get("description", ""),
            company_data.get("website", "")
        ]).lower()
        
        industry_scores = {}
        for industry, keywords in self.industry_keywords.items():
            score = sum(1 for keyword in keywords if keyword in text_to_analyze)
            if score > 0:
                industry_scores[industry] = score
        
        if industry_scores:
            return max(industry_scores.items(), key=lambda x: x[1])[0]
        return "general"
    
    def _is_professional_website(self, url: str) -> bool:
        """Basic check if website appears professional"""
        try:
            parsed = urlparse(url)
            domain = parsed.netloc.lower()
            
            # Professional indicators
            professional_tlds = [".com", ".org", ".net", ".io", ".co"]
            has_professional_tld = any(domain.endswith(tld) for tld in professional_tlds)
            
            # Avoid free hosting indicators
            free_hosting = ["blogspot", "wix", "squarespace", "wordpress.com"]
            has_free_hosting = any(host in domain for host in free_hosting)
            
            return has_professional_tld and not has_free_hosting
        except:
            return False
    
    def generate_journey_stage(self, mpb_score: float) -> str:
        """Generate journey stage based on MPB score"""
        if mpb_score >= 90:
            return "🌟 Luminous Leader"
        elif mpb_score >= 80:
            return "🚀 Soaring High"
        elif mpb_score >= 70:
            return "🌿 Growing Stronger"
        elif mpb_score >= 60:
            return "🌱 Building Foundation"
        elif mpb_score >= 50:
            return "⛅ Finding Direction"
        else:
            return "🌧️ Weathering Storms"
    
    def generate_encouragement(self, mpb_score: float, company_name: str) -> str:
        """Generate personalized encouragement"""
        if mpb_score >= 80:
            return f"{company_name} is demonstrating exceptional leadership and vision!"
        elif mpb_score >= 70:
            return f"{company_name} shows remarkable potential and steady growth!"
        elif mpb_score >= 60:
            return f"{company_name} is building something meaningful with solid foundations!"
        else:
            return f"Every great journey starts with a single step. {company_name} has incredible potential!"
