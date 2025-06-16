"""Working Intelligence Engine - Fixed ChromaDB Configuration"""

import os
import json
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import chromadb
from chromadb.config import Settings
import hashlib
import re
from collections import defaultdict
import asyncio
from concurrent.futures import ThreadPoolExecutor
import aiohttp
from bs4 import BeautifulSoup
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WorkingIntelligenceEngine:
    """Production-ready intelligence engine with fixed ChromaDB"""
    
    def __init__(self):
        logger.info("Initializing Working Intelligence Engine...")
        
        # Initialize ChromaDB with new API
        self.chroma_client = chromadb.PersistentClient(
            path="./chroma_db"
        )
        
        # Create or get collections
        try:
            self.companies_collection = self.chroma_client.get_collection("companies")
            logger.info("Using existing companies collection")
        except:
            self.companies_collection = self.chroma_client.create_collection(
                name="companies",
                metadata={"hnsw:space": "cosine"}
            )
            logger.info("Created new companies collection")
            
        try:
            self.products_collection = self.chroma_client.get_collection("products")
            logger.info("Using existing products collection")
        except:
            self.products_collection = self.chroma_client.create_collection(
                name="products",
                metadata={"hnsw:space": "cosine"}
            )
            logger.info("Created new products collection")
        
        # Initialize other components
        self.tfidf_vectorizer = TfidfVectorizer(max_features=1000)
        self.executor = ThreadPoolExecutor(max_workers=5)
        self.cache = {}
        self.session = None
        
        logger.info("✅ Working Intelligence Engine initialized successfully")
    
    async def analyze_company(self, url: str) -> Dict[str, Any]:
        """Analyze company from URL"""
        try:
            logger.info(f"Analyzing company: {url}")
            
            # Check cache first
            cache_key = hashlib.md5(url.encode()).hexdigest()
            if cache_key in self.cache:
                logger.info("Returning cached result")
                return self.cache[cache_key]
            
            # Extract company data
            company_data = await self._extract_company_data(url)
            
            # Generate insights
            insights = self._generate_insights(company_data)
            
            # Store in ChromaDB
            self._store_company_data(url, company_data, insights)
            
            result = {
                "url": url,
                "company_data": company_data,
                "insights": insights,
                "timestamp": datetime.now().isoformat()
            }
            
            # Cache result
            self.cache[cache_key] = result
            
            return result
            
        except Exception as e:
            logger.error(f"Error analyzing company: {str(e)}")
            raise
    
    async def _extract_company_data(self, url: str) -> Dict[str, Any]:
        """Extract data from company website"""
        if not self.session:
            self.session = aiohttp.ClientSession()
        
        try:
            # Normalize URL
            if not url.startswith(('http://', 'https://')):
                url = f'https://{url}'
            
            async with self.session.get(url, timeout=10) as response:
                html = await response.text()
                soup = BeautifulSoup(html, 'html.parser')
                
                # Extract basic info
                title = soup.find('title')
                title_text = title.text.strip() if title else "Unknown Company"
                
                # Extract meta description
                meta_desc = soup.find('meta', attrs={'name': 'description'})
                description = meta_desc.get('content', '') if meta_desc else ''
                
                # Extract text content
                text_content = ' '.join([p.text for p in soup.find_all('p')])[:1000]
                
                return {
                    "title": title_text,
                    "description": description,
                    "content_preview": text_content,
                    "url": str(response.url)
                }
                
        except Exception as e:
            logger.error(f"Error extracting company data: {str(e)}")
            return {
                "title": "Unknown Company",
                "description": f"Unable to analyze {url}",
                "content_preview": "",
                "url": url,
                "error": str(e)
            }
    
    def _generate_insights(self, company_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate AI insights from company data"""
        
        # Basic insights based on content
        content = f"{company_data.get('title', '')} {company_data.get('description', '')} {company_data.get('content_preview', '')}"
        
        # Industry detection
        industries = {
            "HVAC": ["heating", "cooling", "air conditioning", "ventilation", "hvac"],
            "Electrical": ["electrical", "wiring", "voltage", "power", "circuit"],
            "Industrial": ["industrial", "machinery", "equipment", "manufacturing"],
            "Construction": ["construction", "building", "contractor", "project"]
        }
        
        detected_industries = []
        content_lower = content.lower()
        
        for industry, keywords in industries.items():
            if any(keyword in content_lower for keyword in keywords):
                detected_industries.append(industry)
        
        # Generate insights
        insights = {
            "detected_industries": detected_industries or ["General Business"],
            "company_size": "Medium" if len(content) > 500 else "Small",
            "digital_maturity": "High" if company_data.get('description') else "Low",
            "potential_value": "$10K-50K" if detected_industries else "$5K-25K",
            "recommended_products": self._get_product_recommendations(detected_industries),
            "quick_wins": [
                "Product description optimization",
                "Competitive intelligence setup",
                "Digital catalog enhancement"
            ]
        }
        
        return insights
    
    def _get_product_recommendations(self, industries: List[str]) -> List[str]:
        """Get product recommendations based on industry"""
        recommendations = {
            "HVAC": ["Smart Thermostat Analytics", "Equipment Lifecycle Tracking", "Energy Efficiency Calculator"],
            "Electrical": ["Circuit Load Calculator", "Wire Gauge Optimizer", "Code Compliance Checker"],
            "Industrial": ["Inventory Optimization", "Maintenance Predictor", "Supply Chain Analyzer"],
            "Construction": ["Project Timeline Optimizer", "Material Calculator", "Bid Analyzer"]
        }
        
        products = []
        for industry in industries:
            products.extend(recommendations.get(industry, []))
        
        return products[:5] if products else ["General Business Intelligence", "Competitor Analysis", "Market Insights"]
    
    def _store_company_data(self, url: str, company_data: Dict[str, Any], insights: Dict[str, Any]):
        """Store in ChromaDB"""
        try:
            doc_id = hashlib.md5(url.encode()).hexdigest()
            
            # Prepare document
            document = json.dumps({
                **company_data,
                "insights": insights,
                "timestamp": datetime.now().isoformat()
            })
            
            # Store in ChromaDB
            self.companies_collection.upsert(
                ids=[doc_id],
                documents=[document],
                metadatas=[{
                    "url": url,
                    "title": company_data.get("title", "Unknown"),
                    "industries": ",".join(insights.get("detected_industries", [])),
                    "timestamp": datetime.now().isoformat()
                }]
            )
            
            logger.info(f"Stored company data for {url}")
            
        except Exception as e:
            logger.error(f"Error storing company data: {str(e)}")
    
    def search_companies(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Search stored companies"""
        try:
            results = self.companies_collection.query(
                query_texts=[query],
                n_results=limit
            )
            
            companies = []
            for i, doc in enumerate(results['documents'][0]):
                try:
                    data = json.loads(doc)
                    companies.append(data)
                except:
                    pass
            
            return companies
            
        except Exception as e:
            logger.error(f"Error searching companies: {str(e)}")
            return []
    
    async def close(self):
        """Cleanup resources"""
        if self.session:
            await self.session.close()
        self.executor.shutdown(wait=True)

# Initialize the engine as a singleton
working_engine = WorkingIntelligenceEngine()
