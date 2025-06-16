"""
Palmer AI Dynamic Pricing Engine
Optimize margins while staying competitive
"""
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import numpy as np
from dataclasses import dataclass

from src.palmer_ai.core.logger import get_logger

logger = get_logger(__name__)

@dataclass
class PricingRecommendation:
    """Pricing recommendation with confidence"""
    sku: str
    current_price: float
    recommended_price: float
    confidence: float
    expected_impact: str
    reasoning: List[str]
    

class DynamicPricingEngine:
    """
    AI-powered pricing optimization
    This feature alone is worth the $497/month
    """
    
    def __init__(self):
        self.pricing_strategies = {
            'competitive': self._competitive_pricing,
            'value_based': self._value_based_pricing,
            'dynamic': self._dynamic_pricing,
            'bundle': self._bundle_pricing
        }
        
        # Industry margins by category
        self.target_margins = {
            'commodity': 0.15,  # 15% for commodity items
            'standard': 0.25,   # 25% for standard items
            'premium': 0.35,    # 35% for premium items
            'specialty': 0.45   # 45% for specialty items
        }
        
    async def optimize_pricing(
        self,
        products: List[Dict],
        competitor_data: Optional[Dict] = None,
        historical_data: Optional[List[Dict]] = None,
        strategy: str = 'dynamic'
    ) -> Dict[str, Any]:
        """Main pricing optimization entry point"""
        logger.info(f"Optimizing pricing for {len(products)} products using {strategy} strategy")
        
        # Analyze current pricing
        current_analysis = self._analyze_current_pricing(products)
        
        # Get pricing recommendations
        recommendations = await self.pricing_strategies[strategy](
            products, competitor_data, historical_data
        )
        
        # Calculate expected impact
        impact_analysis = self._calculate_pricing_impact(
            products, recommendations
        )
        
        # Generate pricing report
        report = {
            'optimization_date': datetime.utcnow(),
            'products_analyzed': len(products),
            'strategy_used': strategy,
            'current_state': current_analysis,
            'recommendations': recommendations[:100],  # Top 100
            'expected_impact': impact_analysis,
            'implementation_guide': self._generate_implementation_guide(recommendations)
        }
        
        return report
        
    def _analyze_current_pricing(self, products: List[Dict]) -> Dict[str, Any]:
        """Analyze current pricing state"""
        prices = []
        margins = []
        
        for product in products:
            if 'price' in product and product['price']:
                prices.append(product['price'])
                
            if 'margin' in product and product['margin']:
                margins.append(product['margin'])
                
        analysis = {
            'total_products': len(products),
            'products_with_pricing': len(prices)
        }
        
        if prices:
            analysis['price_statistics'] = {
                'min': min(prices),
                'max': max(prices),
                'average': np.mean(prices),
                'median': np.median(prices),
                'std_dev': np.std(prices)
            }
            
        if margins:
            analysis['margin_statistics'] = {
                'average': np.mean(margins),
                'below_target': sum(1 for m in margins if m < 0.2),
                'healthy': sum(1 for m in margins if 0.2 <= m <= 0.4),
                'high': sum(1 for m in margins if m > 0.4)
            }
            
        return analysis
        
    async def _competitive_pricing(
        self,
        products: List[Dict],
        competitor_data: Optional[Dict],
        historical_data: Optional[List[Dict]]
    ) -> List[PricingRecommendation]:
        """Competitive pricing strategy"""
        recommendations = []
        
        if not competitor_data:
            logger.warning("No competitor data available for competitive pricing")
            return recommendations
            
        comp_prices = competitor_data.get('pricing_intelligence', {}).get('price_range', {})
        
        for product in products[:100]:  # Process top 100
            if 'sku' not in product or 'price' not in product:
                continue
                
            current_price = product['price']
            
            # Find competitive position
            if comp_prices:
                avg_comp_price = comp_prices.get('average', current_price)
                
                # Determine pricing position
                if current_price > avg_comp_price * 1.1:
                    # We're priced too high
                    recommended_price = avg_comp_price * 1.05  # 5% premium
                    reasoning = ["Priced above market average", "Moderate premium maintains value perception"]
                elif current_price < avg_comp_price * 0.9:
                    # We're priced too low
                    recommended_price = avg_comp_price * 0.95  # 5% discount
                    reasoning = ["Priced below market average", "Opportunity to increase margins"]
                else:
                    # We're competitively priced
                    recommended_price = current_price
                    reasoning = ["Already competitively positioned"]
                    
                if abs(recommended_price - current_price) > 0.01:
                    recommendations.append(PricingRecommendation(
                        sku=product['sku'],
                        current_price=current_price,
                        recommended_price=round(recommended_price, 2),
                        confidence=0.75,
                        expected_impact=self._estimate_price_impact(
                            current_price, recommended_price
                        ),
                        reasoning=reasoning
                    ))
                    
        return recommendations
        
    async def _value_based_pricing(
        self,
        products: List[Dict],
        competitor_data: Optional[Dict],
        historical_data: Optional[List[Dict]]
    ) -> List[PricingRecommendation]:
        """Value-based pricing strategy"""
        recommendations = []
        
        for product in products[:100]:
            if 'sku' not in product or 'price' not in product:
                continue
                
            current_price = product['price']
            product_category = self._categorize_product(product)
            target_margin = self.target_margins[product_category]
            
            # Calculate value-based price
            cost = product.get('cost', current_price * 0.7)  # Assume 30% margin if no cost
            recommended_price = cost / (1 - target_margin)
            
            reasoning = [
                f"Product categorized as: {product_category}",
                f"Target margin: {target_margin:.0%}",
                "Price set to achieve target margin"
            ]
            
            # Add value factors
            if product.get('brand_strength', 0) > 0.7:
                recommended_price *= 1.1  # 10% premium for strong brands
                reasoning.append("Premium brand adjustment applied")
                
            if product.get('availability', '') == 'exclusive':
                recommended_price *= 1.15  # 15% premium for exclusive items
                reasoning.append("Exclusive product premium applied")
                
            if abs(recommended_price - current_price) > 0.01:
                recommendations.append(PricingRecommendation(
                    sku=product['sku'],
                    current_price=current_price,
                    recommended_price=round(recommended_price, 2),
                    confidence=0.85,
                    expected_impact=self._estimate_price_impact(
                        current_price, recommended_price
                    ),
                    reasoning=reasoning
                ))
                
        return recommendations
        
    async def _dynamic_pricing(
        self,
        products: List[Dict],
        competitor_data: Optional[Dict],
        historical_data: Optional[List[Dict]]
    ) -> List[PricingRecommendation]:
        """Dynamic pricing based on multiple factors"""
        recommendations = []
        
        # Get both competitive and value-based recommendations
        competitive_recs = await self._competitive_pricing(products, competitor_data, historical_data)
        value_recs = await self._value_based_pricing(products, competitor_data, historical_data)
        
        # Merge recommendations intelligently
        rec_map = {}
        
        # Index competitive recommendations
        for rec in competitive_recs:
            rec_map[rec.sku] = rec
            
        # Blend with value recommendations
        for rec in value_recs:
            if rec.sku in rec_map:
                # Average the two approaches
                comp_rec = rec_map[rec.sku]
                blended_price = (comp_rec.recommended_price + rec.recommended_price) / 2
                
                rec_map[rec.sku] = PricingRecommendation(
                    sku=rec.sku,
                    current_price=rec.current_price,
                    recommended_price=round(blended_price, 2),
                    confidence=(comp_rec.confidence + rec.confidence) / 2,
                    expected_impact=self._estimate_price_impact(
                        rec.current_price, blended_price
                    ),
                    reasoning=["Blended competitive and value-based pricing"] + 
                             comp_rec.reasoning[:1] + rec.reasoning[:1]
                )
            else:
                rec_map[rec.sku] = rec
                
        # Add demand-based adjustments
        for sku, rec in rec_map.items():
            product = next((p for p in products if p.get('sku') == sku), None)
            if product:
                # High demand adjustment
                if product.get('demand_score', 0) > 0.8:
                    rec.recommended_price *= 1.05
                    rec.reasoning.append("High demand premium applied")
                    
                # Low inventory adjustment
                if product.get('inventory_level', 100) < 10:
                    rec.recommended_price *= 1.08
                    rec.reasoning.append("Low inventory scarcity pricing")
                    
        return list(rec_map.values())
        
    async def _bundle_pricing(
        self,
        products: List[Dict],
        competitor_data: Optional[Dict],
        historical_data: Optional[List[Dict]]
    ) -> List[PricingRecommendation]:
        """Bundle pricing recommendations"""
        recommendations = []
        
        # Identify potential bundles
        bundles = self._identify_bundles(products)
        
        for bundle in bundles:
            bundle_products = bundle['products']
            individual_total = sum(p.get('price', 0) for p in bundle_products)
            
            # Calculate bundle discount
            if bundle['type'] == 'complementary':
                discount = 0.10  # 10% off complementary bundles
            elif bundle['type'] == 'volume':
                discount = 0.15  # 15% off volume bundles
            else:
                discount = 0.08  # 8% off general bundles
                
            bundle_price = individual_total * (1 - discount)
            
            # Create bundle recommendation
            recommendations.append(PricingRecommendation(
                sku=f"BUNDLE_{bundle['id']}",
                current_price=individual_total,
                recommended_price=round(bundle_price, 2),
                confidence=0.80,
                expected_impact=f"Increase average order value by {discount*100:.0f}%",
                reasoning=[
                    f"Bundle type: {bundle['type']}",
                    f"Contains {len(bundle_products)} products",
                    f"Bundle discount: {discount:.0%}",
                    "Encourages larger purchases"
                ]
            ))
            
        return recommendations
        
    def _categorize_product(self, product: Dict) -> str:
        """Categorize product for pricing strategy"""
        # Simple categorization logic
        name = product.get('name', '').lower()
        price = product.get('price', 0)
        
        if any(term in name for term in ['basic', 'standard', 'generic']):
            return 'commodity'
        elif any(term in name for term in ['premium', 'pro', 'professional']):
            return 'premium'
        elif any(term in name for term in ['special', 'custom', 'exclusive']):
            return 'specialty'
        elif price > 1000:
            return 'premium'
        else:
            return 'standard'
            
    def _estimate_price_impact(self, current: float, recommended: float) -> str:
        """Estimate impact of price change"""
        change_pct = (recommended - current) / current
        
        if change_pct > 0.10:
            return f"+{change_pct:.0%} revenue potential with elasticity management"
        elif change_pct > 0.05:
            return f"+{change_pct:.0%} margin improvement expected"
        elif change_pct < -0.10:
            return f"{change_pct:.0%} price reduction to gain market share"
        elif change_pct < -0.05:
            return f"{change_pct:.0%} competitive adjustment"
        else:
            return "Minor optimization for market alignment"
            
    def _identify_bundles(self, products: List[Dict]) -> List[Dict]:
        """Identify potential product bundles"""
        bundles = []
        
        # Simple bundling logic - in reality this would be much more sophisticated
        # Group by category or complementary products
        
        # Example: Find products often bought together
        bundle_id = 1
        for i, product1 in enumerate(products[:20]):
            for product2 in products[i+1:i+5]:
                if self._are_complementary(product1, product2):
                    bundles.append({
                        'id': bundle_id,
                        'type': 'complementary',
                        'products': [product1, product2]
                    })
                    bundle_id += 1
                    
        return bundles[:10]  # Return top 10 bundles
        
    def _are_complementary(self, product1: Dict, product2: Dict) -> bool:
        """Check if two products are complementary"""
        # Simple logic - in reality would use purchase history
        name1 = product1.get('name', '').lower()
        name2 = product2.get('name', '').lower()
        
        complementary_pairs = [
            ('drill', 'bit'),
            ('saw', 'blade'),
            ('paint', 'brush'),
            ('hammer', 'nail')
        ]
        
        for pair in complementary_pairs:
            if (pair[0] in name1 and pair[1] in name2) or \
               (pair[1] in name1 and pair[0] in name2):
                return True
                
        return False
        
    def _calculate_pricing_impact(
        self,
        products: List[Dict],
        recommendations: List[PricingRecommendation]
    ) -> Dict[str, Any]:
        """Calculate overall impact of pricing changes"""
        
        total_current_value = 0
        total_recommended_value = 0
        
        rec_map = {r.sku: r for r in recommendations}
        
        for product in products:
            sku = product.get('sku')
            if sku in rec_map:
                current = rec_map[sku].current_price
                recommended = rec_map[sku].recommended_price
                volume = product.get('monthly_volume', 100)  # Default 100 units
                
                total_current_value += current * volume
                total_recommended_value += recommended * volume
                
        revenue_impact = total_recommended_value - total_current_value
        revenue_impact_pct = (revenue_impact / total_current_value * 100) if total_current_value > 0 else 0
        
        return {
            'total_products_optimized': len(recommendations),
            'average_price_change': np.mean([
                (r.recommended_price - r.current_price) / r.current_price * 100
                for r in recommendations
            ]),
            'expected_monthly_impact': f"${revenue_impact:,.0f}",
            'expected_annual_impact': f"${revenue_impact * 12:,.0f}",
            'revenue_change_percentage': f"{revenue_impact_pct:+.1f}%",
            'implementation_complexity': self._assess_implementation_complexity(recommendations)
        }
        
    def _assess_implementation_complexity(self, recommendations: List[PricingRecommendation]) -> str:
        """Assess how complex the pricing changes will be to implement"""
        
        avg_change = np.mean([
            abs(r.recommended_price - r.current_price) / r.current_price
            for r in recommendations
        ])
        
        if avg_change < 0.05:
            return "Low - Minor adjustments only"
        elif avg_change < 0.15:
            return "Medium - Moderate price changes requiring communication"
        else:
            return "High - Significant changes requiring phased rollout"
            
    def _generate_implementation_guide(self, recommendations: List[PricingRecommendation]) -> Dict[str, Any]:
        """Generate step-by-step implementation guide"""
        
        # Group recommendations by impact
        high_impact = [r for r in recommendations if abs(r.recommended_price - r.current_price) / r.current_price > 0.10]
        medium_impact = [r for r in recommendations if 0.05 < abs(r.recommended_price - r.current_price) / r.current_price <= 0.10]
        low_impact = [r for r in recommendations if abs(r.recommended_price - r.current_price) / r.current_price <= 0.05]
        
        return {
            'phase_1': {
                'timeline': 'Week 1',
                'actions': [
                    f"Implement {len(low_impact)} low-impact price adjustments (≤5% change)",
                    "Monitor customer response",
                    "Adjust inventory levels"
                ],
                'products_affected': len(low_impact)
            },
            'phase_2': {
                'timeline': 'Week 2-3',
                'actions': [
                    f"Roll out {len(medium_impact)} medium-impact changes (5-10% change)",
                    "Communicate value proposition to sales team",
                    "Update marketing materials"
                ],
                'products_affected': len(medium_impact)
            },
            'phase_3': {
                'timeline': 'Week 4+',
                'actions': [
                    f"Implement {len(high_impact)} high-impact changes (>10% change)",
                    "Provide customer communication templates",
                    "Monitor competitive response"
                ],
                'products_affected': len(high_impact)
            },
            'success_metrics': [
                "Revenue impact vs. projection",
                "Customer retention rate",
                "Competitive win rate",
                "Margin improvement"
            ]
        }

# Create singleton
pricing_engine = DynamicPricingEngine()
