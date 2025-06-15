"""Content Extraction Agent powered by Claude Sonnet 4"""
import asyncio
from typing import Dict, Any, List, Optional
from datetime import datetime
import json
import httpx
from bs4 import BeautifulSoup
from anthropic import Anthropic

from ..base.agent import BaseAgent, AgentConfig, AnalysisResult, ConfidenceLevel, AgentMessage
from ...utils.logger import get_logger
from ...config import settings

logger = get_logger(__name__)

class ContentExtractionAgent(BaseAgent):
    """AI-powered product content extraction using Claude Sonnet 4"""
    
    def __init__(self, config: AgentConfig):
        super().__init__(config)
        self.anthropic_client = Anthropic(api_key=settings.anthropic_api_key)
        self.http_client = httpx.AsyncClient(timeout=30.0)
        
    async def analyze(self, input_data: Dict[str, Any]) -> AnalysisResult:
        """Extract and enhance product content using Claude Sonnet 4"""
        start_time = datetime.utcnow()
        
        try:
            product_urls = input_data.get("product_urls", [])
            extraction_strategy = input_data.get("extraction_strategy", {})
            
            if not product_urls:
                return AnalysisResult(
                    success=False,
                    errors=["Product URLs are required for extraction"],
                    confidence=ConfidenceLevel.LOW
                )
            
            logger.info(f"Starting Sonnet 4 content extraction for {len(product_urls)} products")
            
            extracted_products = []
            extraction_errors = []
            
            # Process products in batches with Sonnet 4 efficiency
            batch_size = extraction_strategy.get("batch_size", 8)
            rate_limit = extraction_strategy.get("rate_limit", 1.5)
            
            for i in range(0, len(product_urls), batch_size):
                batch = product_urls[i:i + batch_size]
                
                # Process batch concurrently
                batch_results = await asyncio.gather(
                    *[self._sonnet4_extract_product_content(url, extraction_strategy) 
                      for url in batch],
                    return_exceptions=True
                )
                
                for url, result in zip(batch, batch_results):
                    if isinstance(result, Exception):
                        extraction_errors.append({"url": url, "error": str(result)})
                    else:
                        extracted_products.append(result)
                
                # Rate limiting
                if i + batch_size < len(product_urls):
                    await asyncio.sleep(rate_limit)
            
            # Calculate confidence
            success_rate = len(extracted_products) / len(product_urls) if product_urls else 0
            confidence = ConfidenceLevel.HIGH if success_rate > 0.9 else (
                ConfidenceLevel.MEDIUM if success_rate > 0.7 else ConfidenceLevel.LOW
            )
            
            elapsed_time = (datetime.utcnow() - start_time).total_seconds()
            self.record_performance("sonnet4_extraction_duration", elapsed_time)
            self.record_performance("products_extracted", len(extracted_products))
            
            return AnalysisResult(
                success=True,
                data={
                    "extracted_products": extracted_products,
                    "extraction_errors": extraction_errors,
                    "success_rate": success_rate,
                    "ai_model": "claude-sonnet-4-20250514",
                    "extraction_metadata": {
                        "total_products": len(product_urls),
                        "successful_extractions": len(extracted_products),
                        "failed_extractions": len(extraction_errors)
                    }
                },
                confidence=confidence,
                metadata={
                    "extraction_duration": elapsed_time,
                    "ai_model": "claude-sonnet-4-20250514",
                    "timestamp": datetime.utcnow().isoformat()
                }
            )
            
        except Exception as e:
            logger.error(f"Sonnet 4 content extraction failed: {str(e)}")
            return AnalysisResult(
                success=False,
                errors=[f"Extraction error: {str(e)}"],
                confidence=ConfidenceLevel.LOW
            )
    
    async def _sonnet4_extract_product_content(self, 
                                             product_url: str, 
                                             extraction_strategy: Dict[str, Any]) -> Dict[str, Any]:
        """Extract content from product page using Claude Sonnet 4"""
        
        # Step 1: Get raw content
        raw_content = await self._scrape_product_page(product_url)
        
        # Step 2: Use Sonnet 4 for comprehensive processing
        enhanced_product = await self._sonnet4_comprehensive_processing(raw_content, product_url)
        
        return {
            "source_url": product_url,
            "extraction_timestamp": datetime.utcnow().isoformat(),
            "ai_model": "claude-sonnet-4-20250514",
            "raw_data": enhanced_product.get("structured_data", {}),
            "enhanced_data": enhanced_product.get("enhanced_data", {}),
            "b2b_optimization": enhanced_product.get("b2b_optimization", {}),
            "confidence_score": enhanced_product.get("confidence_score", 0.0)
        }
    
    async def _scrape_product_page(self, product_url: str) -> Dict[str, Any]:
        """Scrape raw content from product page"""
        try:
            response = await self.http_client.get(product_url)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            return {
                "url": product_url,
                "title": soup.title.string if soup.title else "",
                "text_content": soup.get_text()[:8000],
                "html_structure": str(soup)[:12000],
                "images": [{"url": img.get("src"), "alt": img.get("alt", "")} 
                          for img in soup.find_all("img")][:10]
            }
            
        except Exception as e:
            logger.error(f"Error scraping {product_url}: {str(e)}")
            raise
    
    async def _sonnet4_comprehensive_processing(self, 
                                              raw_content: Dict[str, Any],
                                              product_url: str) -> Dict[str, Any]:
        """Use Claude Sonnet 4 for comprehensive product processing"""
        
        prompt = f"""You are an expert B2B product intelligence analyst. Extract and enhance product information for distributors.

PRODUCT SOURCE: {product_url}

RAW CONTENT:
Title: {raw_content.get('title', '')}
Text: {raw_content['text_content']}

Provide comprehensive B2B product intelligence in JSON format:

{{
  "structured_data": {{
    "sku": "product SKU",
    "name": "product name",
    "price": "price with currency",
    "description": "technical description",
    "specifications": {{"key": "value"}},
    "categories": ["category1", "category2"],
    "images": ["image URLs"],
    "manufacturer": "manufacturer name"
  }},
  "enhanced_data": {{
    "enhanced_name": "professional B2B name",
    "distributor_description": "compelling B2B description",
    "key_features": ["top 5 B2B features"],
    "competitive_advantages": ["advantages"],
    "target_customer_types": ["customer types"]
  }},
  "b2b_optimization": {{
    "distributor_selling_points": ["selling points"],
    "cross_sell_opportunities": ["related products"],
    "target_industries": ["industries"],
    "typical_order_quantities": "bulk info"
  }},
  "confidence_score": 0.95
}}

Return only valid JSON."""

        try:
            response = await self.anthropic_client.messages.create(
                model=settings.anthropic_model,
                max_tokens=settings.anthropic_max_tokens,
                temperature=0.1,
                messages=[{"role": "user", "content": prompt}]
            )
            
            content = response.content[0].text
            
            # Extract JSON
            json_start = content.find('{')
            json_end = content.rfind('}') + 1
            
            if json_start != -1 and json_end != -1:
                json_content = content[json_start:json_end]
                return json.loads(json_content)
            else:
                return self._fallback_processing(raw_content)
                
        except Exception as e:
            logger.error(f"Sonnet 4 processing failed: {str(e)}")
            return self._fallback_processing(raw_content)
    
    def _fallback_processing(self, raw_content: Dict[str, Any]) -> Dict[str, Any]:
        """Fallback when Sonnet 4 fails"""
        return {
            "structured_data": {
                "name": raw_content.get("title", ""),
                "description": "Product information extraction in progress"
            },
            "enhanced_data": {
                "enhanced_name": raw_content.get("title", ""),
                "distributor_description": "Enhanced description pending"
            },
            "b2b_optimization": {
                "distributor_selling_points": ["Quality product"]
            },
            "confidence_score": 0.3
        }
    
    async def collaborate(self, message: AgentMessage) -> Optional[AgentMessage]:
        """Handle collaboration with other agents"""
        return None
    
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.http_client.aclose()
