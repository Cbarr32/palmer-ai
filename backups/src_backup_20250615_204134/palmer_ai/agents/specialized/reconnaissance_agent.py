"""Reconnaissance Agent for comprehensive site analysis"""
import asyncio
from typing import Dict, Any, List, Optional
from datetime import datetime
import httpx
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin

from ..base.agent import BaseAgent, AgentConfig, AnalysisResult, ConfidenceLevel, AgentMessage
from ...utils.logger import get_logger

logger = get_logger(__name__)

class ReconnaissanceAgent(BaseAgent):
    """Agent specialized in website reconnaissance and initial analysis"""
    
    def __init__(self, config: AgentConfig):
        super().__init__(config)
        self.http_client = httpx.AsyncClient(
            timeout=30.0,
            follow_redirects=True,
            headers={"User-Agent": "Palmer AI Reconnaissance Agent"}
        )
        
    async def analyze(self, input_data: Dict[str, Any]) -> AnalysisResult:
        """Perform comprehensive reconnaissance on target website"""
        start_time = datetime.utcnow()
        
        try:
            url = input_data.get("url")
            if not url:
                return AnalysisResult(
                    success=False,
                    errors=["URL is required for reconnaissance"],
                    confidence=ConfidenceLevel.LOW
                )
                
            # Validate URL
            errors = await self.validate_input(input_data)
            if errors:
                return AnalysisResult(
                    success=False,
                    errors=errors,
                    confidence=ConfidenceLevel.LOW
                )
                
            # Perform reconnaissance phases
            logger.info(f"Starting reconnaissance for {url}")
            
            # Phase 1: Basic site mapping
            site_structure = await self._map_site_structure(url)
            
            # Phase 2: Technology detection
            tech_stack = await self._detect_technologies(url, site_structure)
            
            # Phase 3: Content analysis
            content_analysis = await self._analyze_content(site_structure)
            
            # Phase 4: Performance indicators
            performance_metrics = await self._assess_performance(url)
            
            # Apply UWAS reasoning
            uwas_results = await self.process_with_uwas(
                "comprehensive site reconnaissance",
                {
                    "site_structure": site_structure,
                    "tech_stack": tech_stack,
                    "content": content_analysis,
                    "performance": performance_metrics
                },
                techniques=["chain_of_thought", "expert_persona"]
            )
            
            # Calculate confidence
            evidence_trail = [
                {"type": "site_structure", "quality_score": 0.9, "weight": 1.0},
                {"type": "tech_detection", "quality_score": 0.85, "weight": 0.8},
                {"type": "content_analysis", "quality_score": 0.88, "weight": 0.9},
                {"type": "performance", "quality_score": 0.82, "weight": 0.7}
            ]
            
            confidence = await self.calculate_confidence(evidence_trail)
            
            # Record performance
            elapsed_time = (datetime.utcnow() - start_time).total_seconds()
            self.record_performance("reconnaissance_duration", elapsed_time)
            self.record_performance("pages_analyzed", len(site_structure.get("pages", [])))
            
            return AnalysisResult(
                success=True,
                data={
                    "url": url,
                    "site_structure": site_structure,
                    "technology_stack": tech_stack,
                    "content_analysis": content_analysis,
                    "performance_metrics": performance_metrics,
                    "uwas_insights": uwas_results
                },
                confidence=confidence,
                evidence_trail=evidence_trail,
                reasoning_path=uwas_results.get("reasoning_history", []),
                metadata={
                    "analysis_duration": elapsed_time,
                    "timestamp": datetime.utcnow().isoformat()
                }
            )
            
        except Exception as e:
            logger.error(f"Reconnaissance failed: {str(e)}")
            return AnalysisResult(
                success=False,
                errors=[f"Reconnaissance error: {str(e)}"],
                confidence=ConfidenceLevel.LOW
            )
            
    async def collaborate(self, message: AgentMessage) -> Optional[AgentMessage]:
        """Handle collaboration requests from other agents"""
        if message.message_type == "request_site_data":
            # Provide cached site data if available
            site_data = await self._get_cached_site_data(message.content.get("url"))
            return AgentMessage(
                sender=self.config.agent_id,
                recipient=message.sender,
                message_type="site_data_response",
                content={"site_data": site_data}
            )
        elif message.message_type == "request_tech_stack":
            # Provide technology stack information
            tech_info = await self._get_tech_stack_info(message.content.get("url"))
            return AgentMessage(
                sender=self.config.agent_id,
                recipient=message.sender,
                message_type="tech_stack_response",
                content={"tech_stack": tech_info}
            )
        return None
        
    async def _map_site_structure(self, url: str) -> Dict[str, Any]:
        """Map the structure of the website"""
        structure = {
            "homepage": url,
            "pages": [],
            "navigation": {},
            "sitemap": None,
            "robots_txt": None
        }
        
        try:
            # Fetch homepage
            response = await self.http_client.get(url)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract navigation structure
            nav_elements = soup.find_all(['nav', 'header'])
            for nav in nav_elements:
                links = nav.find_all('a', href=True)
                for link in links:
                    href = urljoin(url, link['href'])
                    if urlparse(href).netloc == urlparse(url).netloc:
                        structure["pages"].append({
                            "url": href,
                            "text": link.get_text(strip=True),
                            "type": "navigation"
                        })
                        
            # Check for sitemap
            sitemap_url = urljoin(url, '/sitemap.xml')
            try:
                sitemap_response = await self.http_client.get(sitemap_url)
                if sitemap_response.status_code == 200:
                    structure["sitemap"] = sitemap_url
            except:
                pass
                
            # Check robots.txt
            robots_url = urljoin(url, '/robots.txt')
            try:
                robots_response = await self.http_client.get(robots_url)
                if robots_response.status_code == 200:
                    structure["robots_txt"] = robots_url
            except:
                pass
                
        except Exception as e:
            logger.error(f"Error mapping site structure: {str(e)}")
            
        return structure
        
    async def _detect_technologies(self, url: str, site_structure: Dict[str, Any]) -> Dict[str, Any]:
        """Detect technologies used by the website"""
        tech_stack = {
            "frontend": [],
            "backend": [],
            "cms": None,
            "analytics": [],
            "frameworks": [],
            "libraries": []
        }
        
        try:
            response = await self.http_client.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')
            headers = response.headers
            
            # Check headers for technology indicators
            if 'x-powered-by' in headers:
                tech_stack["backend"].append(headers['x-powered-by'])
                
            # Check for common frameworks
            if soup.find_all(attrs={"data-react-root": True}):
                tech_stack["frameworks"].append("React")
            if soup.find_all(attrs={"ng-app": True}):
                tech_stack["frameworks"].append("Angular")
            if soup.find_all(attrs={"data-v-": True}):
                tech_stack["frameworks"].append("Vue.js")
                
            # Check for analytics
            scripts = soup.find_all('script', src=True)
            for script in scripts:
                src = script['src']
                if 'google-analytics.com' in src or 'googletagmanager.com' in src:
                    tech_stack["analytics"].append("Google Analytics")
                elif 'segment.com' in src:
                    tech_stack["analytics"].append("Segment")
                    
        except Exception as e:
            logger.error(f"Error detecting technologies: {str(e)}")
            
        return tech_stack
        
    async def _analyze_content(self, site_structure: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze content structure and quality"""
        return {
            "page_count": len(site_structure.get("pages", [])),
            "has_sitemap": site_structure.get("sitemap") is not None,
            "has_robots_txt": site_structure.get("robots_txt") is not None,
            "content_types": ["navigation", "informational", "transactional"],
            "structure_quality": "good" if len(site_structure.get("pages", [])) > 5 else "basic"
        }
        
    async def _assess_performance(self, url: str) -> Dict[str, Any]:
        """Assess basic performance metrics"""
        metrics = {
            "response_time": None,
            "page_size": None,
            "resource_count": 0
        }
        
        try:
            start_time = datetime.utcnow()
            response = await self.http_client.get(url)
            elapsed = (datetime.utcnow() - start_time).total_seconds()
            
            metrics["response_time"] = elapsed
            metrics["page_size"] = len(response.content)
            
            soup = BeautifulSoup(response.content, 'html.parser')
            metrics["resource_count"] = len(soup.find_all(['img', 'script', 'link']))
            
        except Exception as e:
            logger.error(f"Error assessing performance: {str(e)}")
            
        return metrics
        
    async def _get_cached_site_data(self, url: str) -> Optional[Dict[str, Any]]:
        """Retrieve cached site data if available"""
        # Implementation would check cache
        return None
        
    async def _get_tech_stack_info(self, url: str) -> Optional[Dict[str, Any]]:
        """Retrieve technology stack information"""
        # Implementation would return cached or fresh tech stack data
        return None
        
    async def __aenter__(self):
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.http_client.aclose()
