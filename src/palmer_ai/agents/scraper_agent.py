"""
Palmer AI Competitor Intelligence Agent
Automated market and competitor analysis
"""
import asyncio
import httpx
from bs4 import BeautifulSoup
from typing import Dict, List, Any, Optional
import re
from urllib.parse import urljoin, urlparse
from datetime import datetime
import json

from src.palmer_ai.core.logger import get_logger
from src.palmer_ai.core.cache import SemanticCache

logger = get_logger(__name__)

class CompetitorIntelligenceAgent:
    """
    Scrape competitor sites for pricing, inventory, and market intelligence
    This replaces $5K/month market research services
    """
    
    def __init__(self):
        self.session = httpx.AsyncClient(
            timeout=30.0,
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
        )
        self.cache = SemanticCache()
        
    async def analyze_competitor(self, url: str) -> Dict[str, Any]:
        """Full competitor analysis from their website"""
        logger.info(f"Starting competitor analysis: {url}")
        
        try:
            cached = await self.cache.get_similar(url)
            if cached:
                logger.info("Returning cached competitor analysis")
                return cached
                
            main_page = await self._fetch_page(url)
            company_info = await self._extract_company_info(main_page, url)
            product_urls = await self._find_product_pages(main_page, url)
            logger.info(f"Found {len(product_urls)} product pages")
            
            products = []
            for product_url in product_urls[:20]:
                try:
                    product_data = await self._analyze_product_page(product_url)
                    if product_data:
                        products.append(product_data)
                except Exception as e:
                    logger.error(f"Failed to analyze product {product_url}: {e}")
                    
            pricing_intel = self._analyze_pricing_patterns(products)
            usps = self._extract_usps(main_page)
            tech_stack = self._identify_technologies(main_page)
            
            analysis = {
                'url': url,
                'analyzed_at': datetime.utcnow(),
                'company_info': company_info,
                'products_analyzed': len(products),
                'product_samples': products[:5],
                'pricing_intelligence': pricing_intel,
                'unique_selling_props': usps,
                'technology_stack': tech_stack,
                'competitive_insights': self._generate_competitive_insights(
                    company_info, products, pricing_intel
                )
            }
            
            await self.cache.store(url, analysis)
            return analysis
            
        except Exception as e:
            logger.error(f"Competitor analysis failed: {str(e)}")
            raise
            
    async def _fetch_page(self, url: str) -> BeautifulSoup:
        """Fetch and parse a web page"""
        response = await self.session.get(url)
        response.raise_for_status()
        return BeautifulSoup(response.text, 'html.parser')
        
    async def _extract_company_info(self, soup: BeautifulSoup, base_url: str) -> Dict:
        """Extract company information"""
        info = {
            'name': self._get_company_name(soup),
            'tagline': self._get_tagline(soup),
            'contact': self._extract_contact_info(soup),
            'social_media': self._find_social_links(soup),
            'certifications': self._find_certifications(soup)
        }
        
        about_link = soup.find('a', href=re.compile(r'about|company', re.I))
        if about_link:
            try:
                about_url = urljoin(base_url, about_link['href'])
                about_page = await self._fetch_page(about_url)
                info['about_content'] = self._extract_about_content(about_page)
            except:
                pass
                
        return info
        
    def _get_company_name(self, soup: BeautifulSoup) -> str:
        """Extract company name"""
        title = soup.find('title')
        if title:
            name = title.text.split('|')[0].split('-')[0].strip()
            if len(name) < 50:
                return name
                
        logo = soup.find('img', class_=re.compile('logo', re.I))
        if logo and logo.get('alt'):
            return logo['alt']
            
        h1 = soup.find('h1')
        if h1 and len(h1.text.strip()) < 50:
            return h1.text.strip()
            
        return "Unknown Company"
        
    async def _find_product_pages(self, soup: BeautifulSoup, base_url: str) -> List[str]:
        """Find product page URLs"""
        product_urls = set()
        
        product_patterns = [
            r'/product[s]?/', r'/item[s]?/', r'/p/', r'/shop/',
            r'/catalog/', r'/equipment/', r'/tools/', r'/supplies/'
        ]
        
        for link in soup.find_all('a', href=True):
            href = link['href']
            for pattern in product_patterns:
                if re.search(pattern, href, re.I):
                    full_url = urljoin(base_url, href)
                    product_urls.add(full_url)
                    
        product_containers = soup.find_all(
            class_=re.compile(r'product|item|listing|grid', re.I)
        )
        for container in product_containers[:5]:
            links = container.find_all('a', href=True)
            for link in links:
                full_url = urljoin(base_url, link['href'])
                product_urls.add(full_url)
                
        return list(product_urls)
        
    async def _analyze_product_page(self, url: str) -> Optional[Dict]:
        """Analyze individual product page"""
        try:
            soup = await self._fetch_page(url)
            
            product = {
                'url': url,
                'name': self._extract_product_name(soup),
                'price': self._extract_price(soup),
                'sku': self._extract_sku(soup),
                'description': self._extract_description(soup),
                'specifications': self._extract_specifications(soup),
                'availability': self._check_availability(soup),
                'images': self._extract_images(soup, url)
            }
            
            if product['name'] or product['price']:
                return product
                
        except Exception as e:
            logger.error(f"Failed to analyze product page {url}: {e}")
            
        return None
        
    def _extract_product_name(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract product name"""
        selectors = [
            'h1', '[itemprop="name"]', '.product-name',
            '.product-title', '#product-name'
        ]
        
        for selector in selectors:
            element = soup.select_one(selector)
            if element:
                return element.text.strip()
                
        return None
        
    def _extract_price(self, soup: BeautifulSoup) -> Optional[Dict]:
        """Extract pricing information"""
        price_data = {}
        price_pattern = re.compile(r'\$?\s*(\d+(?:,\d{3})*(?:\.\d{2})?)')
        
        price_selectors = [
            '[itemprop="price"]', '.price', '.product-price',
            '.cost', '[class*="price"]'
        ]
        
        for selector in price_selectors:
            elements = soup.select(selector)
            for element in elements:
                text = element.text.strip()
                match = price_pattern.search(text)
                if match:
                    price_str = match.group(1).replace(',', '')
                    try:
                        price = float(price_str)
                        if price > 0:
                            if 'list' in text.lower() or 'msrp' in text.lower():
                                price_data['list_price'] = price
                            elif 'sale' in text.lower() or 'special' in text.lower():
                                price_data['sale_price'] = price
                            else:
                                price_data['current_price'] = price
                    except:
                        pass
                        
        return price_data if price_data else None
        
    def _extract_specifications(self, soup: BeautifulSoup) -> Dict:
        """Extract product specifications"""
        specs = {}
        
        spec_tables = soup.find_all('table', class_=re.compile(r'spec|detail|attribute', re.I))
        for table in spec_tables:
            rows = table.find_all('tr')
            for row in rows:
                cells = row.find_all(['td', 'th'])
                if len(cells) >= 2:
                    key = cells[0].text.strip()
                    value = cells[1].text.strip()
                    if key and value:
                        specs[key] = value
                        
        dl_elements = soup.find_all('dl')
        for dl in dl_elements:
            dts = dl.find_all('dt')
            dds = dl.find_all('dd')
            for dt, dd in zip(dts, dds):
                key = dt.text.strip()
                value = dd.text.strip()
                if key and value:
                    specs[key] = value
                    
        return specs
        
    def _analyze_pricing_patterns(self, products: List[Dict]) -> Dict:
        """Analyze pricing patterns across products"""
        prices = []
        list_prices = []
        discounts = []
        
        for product in products:
            if product.get('price'):
                if 'current_price' in product['price']:
                    prices.append(product['price']['current_price'])
                if 'list_price' in product['price']:
                    list_prices.append(product['price']['list_price'])
                if 'list_price' in product['price'] and 'current_price' in product['price']:
                    discount = (product['price']['list_price'] - product['price']['current_price']) / product['price']['list_price']
                    discounts.append(discount)
                    
        analysis = {}
        
        if prices:
            analysis['price_range'] = {
                'min': min(prices),
                'max': max(prices),
                'average': sum(prices) / len(prices),
                'median': sorted(prices)[len(prices) // 2]
            }
            
        if discounts:
            analysis['discount_patterns'] = {
                'average_discount': sum(discounts) / len(discounts),
                'max_discount': max(discounts),
                'products_on_sale': len(discounts)
            }
            
        return analysis
        
    def _extract_usps(self, soup: BeautifulSoup) -> List[str]:
        """Extract unique selling propositions"""
        usps = []
        
        value_keywords = [
            'free shipping', 'same day', 'next day', 'warranty',
            'guarantee', 'certified', 'authorized', 'exclusive',
            'lowest price', 'price match', 'expert', 'support',
            '24/7', 'in stock', 'fast delivery'
        ]
        
        text_content = soup.get_text().lower()
        
        for keyword in value_keywords:
            if keyword in text_content:
                sentences = [s.strip() for s in text_content.split('.') if keyword in s.lower()]
                for sentence in sentences[:2]:
                    if len(sentence) < 200:
                        usps.append(sentence.capitalize())
                        
        trust_elements = soup.find_all(class_=re.compile(r'badge|trust|certif|award', re.I))
        for element in trust_elements[:5]:
            text = element.text.strip()
            if text and len(text) < 100:
                usps.append(text)
                
        return list(set(usps))[:10]
        
    def _identify_technologies(self, soup: BeautifulSoup) -> Dict:
        """Identify technologies and platforms used"""
        tech = {
            'ecommerce_platform': None,
            'analytics': [],
            'payment_providers': [],
            'other_technologies': []
        }
        
        html_content = str(soup)
        
        if 'shopify' in html_content.lower():
            tech['ecommerce_platform'] = 'Shopify'
        elif 'woocommerce' in html_content.lower():
            tech['ecommerce_platform'] = 'WooCommerce'
        elif 'magento' in html_content.lower():
            tech['ecommerce_platform'] = 'Magento'
        elif 'bigcommerce' in html_content.lower():
            tech['ecommerce_platform'] = 'BigCommerce'
            
        if 'google-analytics' in html_content or 'gtag' in html_content:
            tech['analytics'].append('Google Analytics')
        if 'facebook.com/tr' in html_content:
            tech['analytics'].append('Facebook Pixel')
            
        if 'stripe' in html_content.lower():
            tech['payment_providers'].append('Stripe')
        if 'paypal' in html_content.lower():
            tech['payment_providers'].append('PayPal')
            
        return tech
        
    def _generate_competitive_insights(
        self, 
        company_info: Dict, 
        products: List[Dict], 
        pricing: Dict
    ) -> List[Dict]:
        """Generate actionable competitive insights"""
        insights = []
        
        if pricing.get('discount_patterns'):
            avg_discount = pricing['discount_patterns']['average_discount']
            if avg_discount > 0.2:
                insights.append({
                    'type': 'pricing_strategy',
                    'finding': 'Heavy discounting strategy',
                    'detail': f"Average discount of {avg_discount:.0%} across products",
                    'opportunity': 'Compete on value and service rather than price'
                })
                
        if len(products) > 0:
            insights.append({
                'type': 'product_range',
                'finding': f"Analyzed {len(products)} products",
                'detail': 'Product categories and depth identified',
                'opportunity': 'Identify gaps in their product lineup'
            })
            
        if company_info.get('technology_stack'):
            insights.append({
                'type': 'technology',
                'finding': f"Using {company_info['technology_stack'].get('ecommerce_platform', 'Unknown')} platform",
                'detail': 'Technology stack analyzed',
                'opportunity': 'Leverage superior technology for competitive advantage'
            })
            
        return insights
        
    def _extract_contact_info(self, soup: BeautifulSoup) -> Dict:
        """Extract contact information"""
        contact = {}
        
        phone_pattern = re.compile(r'(\+?1[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}')
        phones = phone_pattern.findall(soup.get_text())
        if phones:
            contact['phone'] = phones[0]
            
        email_pattern = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}')
        emails = email_pattern.findall(soup.get_text())
        if emails:
            contact['email'] = emails[0]
            
        return contact
        
    def _find_social_links(self, soup: BeautifulSoup) -> Dict:
        """Find social media links"""
        social = {}
        
        social_patterns = {
            'facebook': r'facebook\.com/[\w\-\.]+',
            'twitter': r'twitter\.com/[\w\-\.]+',
            'linkedin': r'linkedin\.com/company/[\w\-\.]+',
            'instagram': r'instagram\.com/[\w\-\.]+',
            'youtube': r'youtube\.com/[\w\-\.]+'
        }
        
        for link in soup.find_all('a', href=True):
            href = link['href']
            for platform, pattern in social_patterns.items():
                if re.search(pattern, href, re.I):
                    social[platform] = href
                    
        return social
        
    def _find_certifications(self, soup: BeautifulSoup) -> List[str]:
        """Find certifications and accreditations"""
        certs = []
        
        cert_keywords = [
            'certified', 'authorized', 'accredited', 'iso', 
            'dealer', 'partner', 'member', 'association'
        ]
        
        for keyword in cert_keywords:
            elements = soup.find_all(text=re.compile(keyword, re.I))
            for element in elements[:3]:
                text = element.strip()
                if 20 < len(text) < 100:
                    certs.append(text)
                    
        return list(set(certs))[:5]
        
    def _extract_about_content(self, soup: BeautifulSoup) -> str:
        """Extract about page content"""
        content_selectors = [
            'main', '[role="main"]', '.content',
            '.about-content', 'article'
        ]
        
        for selector in content_selectors:
            element = soup.select_one(selector)
            if element:
                text = element.get_text(separator=' ', strip=True)
                if len(text) > 100:
                    return text[:1000]
                    
        return ""
        
    def _extract_description(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract product description"""
        desc_selectors = [
            '[itemprop="description"]', '.product-description',
            '.description', '#description'
        ]
        
        for selector in desc_selectors:
            element = soup.select_one(selector)
            if element:
                return element.get_text(separator=' ', strip=True)[:500]
                
        return None
        
    def _extract_sku(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract SKU/part number"""
        sku_patterns = [
            r'sku[:\s]+([A-Z0-9\-]+)',
            r'part[:\s]+([A-Z0-9\-]+)',
            r'item[:\s]+([A-Z0-9\-]+)',
            r'model[:\s]+([A-Z0-9\-]+)'
        ]
        
        text = soup.get_text()
        for pattern in sku_patterns:
            match = re.search(pattern, text, re.I)
            if match:
                return match.group(1)
                
        return None
        
    def _check_availability(self, soup: BeautifulSoup) -> str:
        """Check product availability"""
        text_lower = soup.get_text().lower()
        
        if 'in stock' in text_lower:
            return 'in_stock'
        elif 'out of stock' in text_lower:
            return 'out_of_stock'
        elif 'backorder' in text_lower:
            return 'backorder'
        elif 'discontinued' in text_lower:
            return 'discontinued'
        else:
            return 'unknown'
            
    def _extract_images(self, soup: BeautifulSoup, base_url: str) -> List[str]:
        """Extract product images"""
        images = []
        
        img_selectors = [
            '.product-image', '[itemprop="image"]',
            '.gallery img', '[class*="product"] img'
        ]
        
        for selector in img_selectors:
            elements = soup.select(selector)
            for element in elements[:5]:
                src = element.get('src') or element.get('data-src')
                if src:
                    full_url = urljoin(base_url, src)
                    images.append(full_url)
                    
        return images
        
    def _get_tagline(self, soup: BeautifulSoup) -> str:
        """Extract company tagline"""
        tagline_selectors = [
            '.tagline', '.slogan', '[class*="tagline"]',
            'h2', '.hero-subtitle'
        ]
        
        for selector in tagline_selectors:
            element = soup.select_one(selector)
            if element:
                text = element.text.strip()
                if 10 < len(text) < 150:
                    return text
                    
        return ""

scraper_agent = CompetitorIntelligenceAgent()
