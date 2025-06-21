"""Product Reconnaissance Agent for B2B manufacturer site analysis"""
import asyncio
from typing import Dict, Any, List, Optional
from datetime import datetime
import httpx
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import re

from ..base.agent import BaseAgent, AgentConfig, AnalysisResult, ConfidenceLevel, AgentMessage
from ...utils.logger import get_logger

logger = get_logger(__name__)

class ProductReconnaissanceAgent(BaseAgent):
    """Specialized agent for discovering and mapping manufacturer product catalogs"""
    
    def __init__(self, config: AgentConfig):
        super().__init__(config)
        self.http_client = httpx.AsyncClient(
            timeout=30.0,
            follow_redirects=True,
            headers={"User-Agent": "Palmer AI B2B Product Intelligence Bot"}
        )
        
    async def analyze(self, input_data: Dict[str, Any]) -> AnalysisResult:
        """Analyze manufacturer website for product discovery opportunities"""
        start_time = datetime.utcnow()
        
        try:
            manufacturer_url = input_data.get("manufacturer_url")
            if not manufacturer_url:
                return AnalysisResult(
                    success=False,
                    errors=["Manufacturer URL is required"],
                    confidence=ConfidenceLevel.LOW
                )
            
            logger.info(f"Starting product reconnaissance for {manufacturer_url}")
            
            # Phase 1: Site structure analysis
            site_structure = await self._analyze_site_structure(manufacturer_url)
            
            # Phase 2: Product catalog discovery
            product_catalog = await self._discover_product_catalog(site_structure)
            
            # Phase 3: Content pattern analysis
            content_patterns = await self._analyze_content_patterns(product_catalog)
            
            # Phase 4: Extraction strategy generation
            extraction_strategy = await self._generate_extraction_strategy(
                site_structure, product_catalog, content_patterns
            )
            
            # Calculate confidence
            evidence_trail = [
                {"type": "site_structure", "quality_score": 0.9, "weight": 1.0},
                {"type": "catalog_discovery", "quality_score": 0.85, "weight": 1.2},
                {"type": "content_patterns", "quality_score": 0.88, "weight": 0.9},
                {"type": "extraction_strategy", "quality_score": 0.82, "weight": 1.1}
            ]
            
            confidence = await self.calculate_confidence(evidence_trail)
            
            # Record performance
            elapsed_time = (datetime.utcnow() - start_time).total_seconds()
            self.record_performance("reconnaissance_duration", elapsed_time)
            self.record_performance("products_discovered", len(product_catalog.get("product_urls", [])))
            
            return AnalysisResult(
                success=True,
                data={
                    "manufacturer_url": manufacturer_url,
                    "site_structure": site_structure,
                    "product_catalog": product_catalog,
                    "content_patterns": content_patterns,
                    "extraction_strategy": extraction_strategy,
                    "estimated_product_count": len(product_catalog.get("product_urls", [])),
                    "complexity_score": self._calculate_complexity_score(content_patterns)
                },
                confidence=confidence,
                evidence_trail=evidence_trail,
                metadata={
                    "analysis_duration": elapsed_time,
                    "timestamp": datetime.utcnow().isoformat()
                }
            )
            
        except Exception as e:
            logger.error(f"Product reconnaissance failed: {str(e)}")
            return AnalysisResult(
                success=False,
                errors=[f"Reconnaissance error: {str(e)}"],
                confidence=ConfidenceLevel.LOW
            )
    
    async def _analyze_site_structure(self, manufacturer_url: str) -> Dict[str, Any]:
        """Analyze the structure of the manufacturer website"""
        structure = {
            "base_url": manufacturer_url,
            "navigation_links": [],
            "product_sections": [],
            "technology_stack": {}
        }
        
        try:
            response = await self.http_client.get(manufacturer_url)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract navigation structure
            nav_elements = soup.find_all(['nav', 'header'])
            for nav in nav_elements:
                links = nav.find_all('a', href=True)
                for link in links:
                    href = urljoin(manufacturer_url, link['href'])
                    text = link.get_text(strip=True).lower()
                    
                    # Identify product-related navigation
                    if self._is_product_related(text):
                        structure["navigation_links"].append({
                            "url": href,
                            "text": text,
                            "type": "product_navigation"
                        })
            
        except Exception as e:
            logger.error(f"Error analyzing site structure: {str(e)}")
            
        return structure
    
    async def _discover_product_catalog(self, site_structure: Dict[str, Any]) -> Dict[str, Any]:
        """Discover product catalog URLs and structure"""
        catalog = {
            "product_urls": [],
            "category_urls": [],
            "catalog_structure": {}
        }
        
        # Check common product catalog paths
        common_paths = ['/products', '/catalog', '/shop', '/store']
        base_url = site_structure["base_url"]
        
        for path in common_paths:
            try:
                catalog_url = urljoin(base_url, path)
                response = await self.http_client.get(catalog_url)
                
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    
                    # Find product links
                    product_links = await self._extract_product_links(soup, catalog_url)
                    catalog["product_urls"].extend(product_links)
                    
            except Exception as e:
                logger.debug(f"Could not access {catalog_url}: {str(e)}")
                continue
        
        # Remove duplicates
        catalog["product_urls"] = list(set(catalog["product_urls"]))
        
        return catalog
    
    async def _analyze_content_patterns(self, product_catalog: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze content patterns across product pages"""
        patterns = {
            "common_selectors": {},
            "content_structure": {},
            "data_formats": {}
        }
        
        # Sample a few product pages for pattern analysis
        sample_urls = product_catalog["product_urls"][:3]
        
        for url in sample_urls:
            try:
                response = await self.http_client.get(url)
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Basic pattern analysis
                if soup.find('h1'):
                    patterns["common_selectors"]["title"] = "h1"
                if soup.find(class_="price"):
                    patterns["common_selectors"]["price"] = ".price"
                
            except Exception as e:
                logger.debug(f"Could not analyze {url}: {str(e)}")
                continue
        
        return patterns
    
    async def _generate_extraction_strategy(self, 
                                          site_structure: Dict[str, Any],
                                          product_catalog: Dict[str, Any],
                                          content_patterns: Dict[str, Any]) -> Dict[str, Any]:
        """Generate optimized extraction strategy"""
        strategy = {
            "approach": "intelligent_scraping",
            "batch_size": 10,
            "rate_limit": 2.0,
            "extraction_rules": {},
            "quality_checks": []
        }
        
        # Generate extraction rules based on patterns
        if content_patterns.get("common_selectors"):
            strategy["extraction_rules"] = {
                "title": content_patterns["common_selectors"].get("title", "h1"),
                "price": content_patterns["common_selectors"].get("price", ".price"),
                "description": content_patterns["common_selectors"].get("description", ".description"),
                "images": content_patterns["common_selectors"].get("images", "img")
            }
        
        return strategy
    
    def _is_product_related(self, text: str) -> bool:
        """Check if navigation text is product-related"""
        product_keywords = ['product', 'catalog', 'shop', 'store', 'parts', 'inventory']
        return any(keyword in text.lower() for keyword in product_keywords)
    
    async def _extract_product_links(self, soup: BeautifulSoup, base_url: str) -> List[str]:
        """Extract product page URLs from catalog page"""
        product_links = []
        
        # Common product link patterns
        link_selectors = ['a[href*="/product"]', 'a[href*="/item"]', '.product-link']
        
        for selector in link_selectors:
            links = soup.select(selector)
            for link in links:
                href = link.get('href')
                if href:
                    full_url = urljoin(base_url, href)
                    product_links.append(full_url)
        
        return product_links
    
    def _calculate_complexity_score(self, content_patterns: Dict[str, Any]) -> float:
        """Calculate extraction complexity score (0-1)"""
        if not content_patterns:
            return 0.8  # High complexity if no patterns detected
        return 0.5  # Medium complexity as default
    
    async def collaborate(self, message: AgentMessage) -> Optional[AgentMessage]:
        """Handle collaboration with other agents"""
        return None
    
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.http_client.aclose()
