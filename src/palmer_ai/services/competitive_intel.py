"""Real Competitive Intelligence Service - Not a Demo"""
import asyncio
from typing import Dict, List, Any, Optional
from datetime import datetime
import httpx
from bs4 import BeautifulSoup
import hashlib
import json
from urllib.parse import urlparse

from palmer_ai.core.config import settings
from palmer_ai.utils.logger import get_logger

logger = get_logger(__name__)

class CompetitiveIntelService:
    """This is what actually competes with Klue"""
    
    def __init__(self):
        self.http_client = httpx.AsyncClient(timeout=30.0)
        self._monitored_competitors: Dict[str, Dict] = {}
        
    async def add_competitor(self, user_id: str, competitor_url: str) -> Dict[str, Any]:
        """Add a competitor to monitor"""
        domain = urlparse(competitor_url).netloc
        
        competitor_id = hashlib.md5(f"{user_id}:{domain}".encode()).hexdigest()
        
        # Initial scan
        intel = await self.analyze_competitor(competitor_url)
        
        # Store for monitoring
        self._monitored_competitors[competitor_id] = {
            "user_id": user_id,
            "url": competitor_url,
            "domain": domain,
            "added": datetime.utcnow(),
            "last_scan": datetime.utcnow(),
            "intel": intel
        }
        
        return {
            "competitor_id": competitor_id,
            "domain": domain,
            "initial_intel": intel
        }
    
    async def analyze_competitor(self, url: str) -> Dict[str, Any]:
        """Deep competitive analysis - this is our secret sauce"""
        logger.info(f"Analyzing competitor: {url}")
        
        try:
            # Fetch competitor page
            response = await self.http_client.get(url, follow_redirects=True)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract intelligence
            intel = {
                "basic_info": await self._extract_basic_info(soup, url),
                "messaging": await self._extract_messaging(soup),
                "features": await self._extract_features(soup),
                "pricing": await self._extract_pricing(soup, url),
                "social_proof": await self._extract_social_proof(soup),
                "technology": await self._detect_technology(soup, response),
                "changes": [],  # Will populate from monitoring
                "insights": await self._generate_insights(soup, url)
            }
            
            return intel
            
        except Exception as e:
            logger.error(f"Analysis failed for {url}: {str(e)}")
            raise
    
    async def _extract_basic_info(self, soup: BeautifulSoup, url: str) -> Dict:
        """Extract basic company information"""
        return {
            "title": soup.find('title').text if soup.find('title') else "",
            "meta_description": soup.find('meta', {'name': 'description'})['content'] 
                if soup.find('meta', {'name': 'description'}) else "",
            "h1_text": soup.find('h1').text.strip() if soup.find('h1') else "",
            "domain": urlparse(url).netloc
        }
    
    async def _extract_messaging(self, soup: BeautifulSoup) -> Dict:
        """Extract key messaging and positioning"""
        messaging = {
            "headlines": [],
            "value_props": [],
            "ctas": []
        }
        
        # Headlines (h1, h2, h3)
        for tag in ['h1', 'h2', 'h3']:
            for heading in soup.find_all(tag)[:5]:  # Top 5 of each
                text = heading.text.strip()
                if text and len(text) > 5:
                    messaging["headlines"].append({
                        "tag": tag,
                        "text": text
                    })
        
        # CTAs (buttons and prominent links)
        for button in soup.find_all(['button', 'a'], class_=lambda x: x and ('btn' in x or 'button' in x)):
            text = button.text.strip()
            if text and len(text) > 2:
                messaging["ctas"].append(text)
        
        # Value props (often in lists near hero)
        for ul in soup.find_all('ul')[:3]:  # First 3 lists
            items = []
            for li in ul.find_all('li')[:5]:
                text = li.text.strip()
                if text and 10 < len(text) < 200:
                    items.append(text)
            if items:
                messaging["value_props"].extend(items)
        
        return messaging
    
    async def _extract_features(self, soup: BeautifulSoup) -> List[str]:
        """Extract product features"""
        features = []
        
        # Look for feature sections
        feature_keywords = ['feature', 'capability', 'benefit', 'solution']
        
        for keyword in feature_keywords:
            # Find sections with these keywords
            for element in soup.find_all(class_=lambda x: x and keyword in x.lower()):
                text = element.text.strip()
                if text and 10 < len(text) < 200:
                    features.append(text)
        
        # Deduplicate
        return list(set(features))[:20]  # Top 20 features
    
    async def _extract_pricing(self, soup: BeautifulSoup, url: str) -> Dict:
        """Extract pricing information"""
        pricing = {
            "currency": "$",
            "plans": [],
            "model": "unknown"
        }
        
        # Look for pricing
        price_indicators = ['$', '€', '£', 'price', 'pricing', 'cost', 'plan']
        
        for indicator in price_indicators:
            for element in soup.find_all(text=lambda text: text and indicator in text.lower()):
                parent = element.parent
                if parent:
                    text = parent.text.strip()
                    # Extract prices with regex
                    import re
                    prices = re.findall(r'[\$€£]\s*\d+(?:,\d{3})*(?:\.\d{2})?', text)
                    if prices:
                        for price in prices:
                            pricing["plans"].append({
                                "price": price,
                                "context": text[:100]
                            })
        
        # Detect pricing model
        if 'per month' in str(soup).lower() or '/mo' in str(soup).lower():
            pricing["model"] = "subscription"
        elif 'one time' in str(soup).lower() or 'perpetual' in str(soup).lower():
            pricing["model"] = "one-time"
        
        return pricing
    
    async def _extract_social_proof(self, soup: BeautifulSoup) -> Dict:
        """Extract social proof elements"""
        social_proof = {
            "testimonials": [],
            "client_logos": [],
            "stats": []
        }
        
        # Testimonials (often in blockquotes or specific classes)
        for quote in soup.find_all(['blockquote', 'div'], class_=lambda x: x and 'testimonial' in str(x).lower())[:5]:
            text = quote.text.strip()
            if text and len(text) > 20:
                social_proof["testimonials"].append(text[:300])
        
        # Stats (numbers with context)
        import re
        stat_pattern = r'(\d+(?:,\d{3})*(?:\+)?)\s*([A-Za-z\s]+)'
        for match in re.finditer(stat_pattern, str(soup)):
            number, context = match.groups()
            if len(context) < 50:  # Reasonable length
                social_proof["stats"].append(f"{number} {context.strip()}")
        
        return social_proof
    
    async def _detect_technology(self, soup: BeautifulSoup, response: httpx.Response) -> Dict:
        """Detect technology stack"""
        tech = {
            "frontend": [],
            "analytics": [],
            "marketing": [],
            "infrastructure": []
        }
        
        # Check for common technologies
        html_content = str(soup)
        headers = response.headers
        
        # Frontend frameworks
        if 'react' in html_content.lower():
            tech["frontend"].append("React")
        if 'vue' in html_content.lower():
            tech["frontend"].append("Vue.js")
        if 'angular' in html_content.lower():
            tech["frontend"].append("Angular")
        
        # Analytics
        if 'google-analytics' in html_content or 'ga(' in html_content:
            tech["analytics"].append("Google Analytics")
        if 'segment' in html_content.lower():
            tech["analytics"].append("Segment")
        
        # Marketing tools
        if 'hubspot' in html_content.lower():
            tech["marketing"].append("HubSpot")
        if 'marketo' in html_content.lower():
            tech["marketing"].append("Marketo")
        
        # Infrastructure (from headers)
        if 'cloudflare' in str(headers).lower():
            tech["infrastructure"].append("Cloudflare")
        if 'x-powered-by' in headers:
            tech["infrastructure"].append(headers['x-powered-by'])
        
        return tech
    
    async def _generate_insights(self, soup: BeautifulSoup, url: str) -> List[Dict]:
        """Generate actionable insights using AI"""
        insights = []
        
        # This is where we'd use Claude/GPT to analyze
        # For now, rule-based insights
        
        # Messaging analysis
        h1_text = soup.find('h1').text.strip() if soup.find('h1') else ""
        if h1_text:
            insights.append({
                "type": "messaging",
                "title": "Primary Value Proposition",
                "insight": f"Competitor leads with: '{h1_text[:100]}'",
                "recommendation": "Consider how your messaging differentiates"
            })
        
        # CTA analysis
        ctas = [btn.text.strip() for btn in soup.find_all(['button', 'a'], class_=lambda x: x and 'btn' in str(x))[:5]]
        if ctas:
            primary_cta = ctas[0] if ctas else "Unknown"
            insights.append({
                "type": "conversion",
                "title": "Primary Call-to-Action",
                "insight": f"Main CTA is '{primary_cta}'",
                "recommendation": "Test if a different CTA would convert better"
            })
        
        # Pricing visibility
        has_pricing = '$' in str(soup) or 'pricing' in str(soup).lower()
        insights.append({
            "type": "pricing",
            "title": "Pricing Transparency",
            "insight": "Pricing is visible on homepage" if has_pricing else "Pricing is hidden",
            "recommendation": "Transparent pricing builds trust" if not has_pricing else "Consider testing hidden pricing for enterprise"
        })
        
        return insights
    
    async def monitor_changes(self, competitor_id: str) -> Dict[str, Any]:
        """Monitor competitor for changes"""
        if competitor_id not in self._monitored_competitors:
            raise ValueError(f"Competitor {competitor_id} not found")
        
        competitor = self._monitored_competitors[competitor_id]
        old_intel = competitor["intel"]
        
        # Re-analyze
        new_intel = await self.analyze_competitor(competitor["url"])
        
        # Detect changes
        changes = await self._detect_changes(old_intel, new_intel)
        
        # Update stored intel
        competitor["intel"] = new_intel
        competitor["last_scan"] = datetime.utcnow()
        
        if changes:
            # Add to change history
            new_intel["changes"].append({
                "detected": datetime.utcnow().isoformat(),
                "changes": changes
            })
        
        return {
            "competitor_id": competitor_id,
            "domain": competitor["domain"],
            "changes_detected": len(changes) > 0,
            "changes": changes,
            "intel": new_intel
        }
    
    async def _detect_changes(self, old_intel: Dict, new_intel: Dict) -> List[Dict]:
        """Detect what changed between scans"""
        changes = []
        
        # Check messaging changes
        old_headlines = {h["text"] for h in old_intel["messaging"]["headlines"]}
        new_headlines = {h["text"] for h in new_intel["messaging"]["headlines"]}
        
        added_headlines = new_headlines - old_headlines
        removed_headlines = old_headlines - new_headlines
        
        if added_headlines:
            changes.append({
                "type": "messaging",
                "change": "added",
                "details": f"New headlines: {list(added_headlines)[:3]}"
            })
        
        if removed_headlines:
            changes.append({
                "type": "messaging",
                "change": "removed",
                "details": f"Removed headlines: {list(removed_headlines)[:3]}"
            })
        
        # Check pricing changes
        old_prices = {p["price"] for p in old_intel["pricing"]["plans"]}
        new_prices = {p["price"] for p in new_intel["pricing"]["plans"]}
        
        if old_prices != new_prices:
            changes.append({
                "type": "pricing",
                "change": "modified",
                "details": f"Pricing changed from {old_prices} to {new_prices}"
            })
        
        # Check feature changes
        old_features = set(old_intel["features"])
        new_features = set(new_intel["features"])
        
        added_features = new_features - old_features
        if added_features:
            changes.append({
                "type": "features",
                "change": "added",
                "details": f"New features: {list(added_features)[:5]}"
            })
        
        return changes
    
    async def get_competitor_report(self, competitor_id: str) -> Dict[str, Any]:
        """Generate comprehensive competitor report"""
        if competitor_id not in self._monitored_competitors:
            raise ValueError(f"Competitor {competitor_id} not found")
        
        competitor = self._monitored_competitors[competitor_id]
        intel = competitor["intel"]
        
        # Generate report
        report = {
            "competitor": {
                "domain": competitor["domain"],
                "url": competitor["url"],
                "monitoring_since": competitor["added"].isoformat(),
                "last_updated": competitor["last_scan"].isoformat()
            },
            "executive_summary": self._generate_executive_summary(intel),
            "detailed_analysis": intel,
            "recommendations": await self._generate_recommendations(intel),
            "change_history": intel.get("changes", [])
        }
        
        return report
    
    def _generate_executive_summary(self, intel: Dict) -> str:
        """Generate executive summary of competitor"""
        domain = intel["basic_info"]["domain"]
        headline = intel["basic_info"]["h1_text"]
        features_count = len(intel["features"])
        has_pricing = len(intel["pricing"]["plans"]) > 0
        
        summary = f"{domain} positions itself as '{headline}'. "
        summary += f"They highlight {features_count} key features. "
        summary += f"Pricing is {'transparent' if has_pricing else 'not publicly available'}. "
        
        if intel["insights"]:
            key_insight = intel["insights"][0]["insight"]
            summary += f"Key insight: {key_insight}"
        
        return summary
    
    async def _generate_recommendations(self, intel: Dict) -> List[Dict]:
        """Generate strategic recommendations"""
        recommendations = []
        
        # Messaging recommendations
        if intel["messaging"]["headlines"]:
            recommendations.append({
                "area": "Messaging",
                "priority": "high",
                "recommendation": "Differentiate from competitor's positioning",
                "specific_actions": [
                    "Identify unique value props not mentioned by competitor",
                    "Test alternative messaging angles",
                    "A/B test against competitor's primary CTA"
                ]
            })
        
        # Pricing recommendations
        if intel["pricing"]["plans"]:
            recommendations.append({
                "area": "Pricing",
                "priority": "medium",
                "recommendation": "Optimize pricing strategy",
                "specific_actions": [
                    "Consider pricing relative to competitor",
                    "Test value-based pricing if competitor uses cost-plus",
                    "Add pricing tier competitor doesn't offer"
                ]
            })
        
        # Feature recommendations
        if intel["features"]:
            recommendations.append({
                "area": "Product",
                "priority": "high",
                "recommendation": "Feature differentiation",
                "specific_actions": [
                    "Identify feature gaps competitor doesn't address",
                    "Emphasize unique features in marketing",
                    "Build features competitor charges extra for"
                ]
            })
        
        return recommendations

# Global service instance
competitive_intel_service = CompetitiveIntelService()
