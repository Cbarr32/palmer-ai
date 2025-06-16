"""Palmer AI Core - Public Demo Version"""

class PalmerAICore:
    """The heart of Palmer AI - Enterprise features hidden"""
    
    def __init__(self):
        self.version = "PUBLIC_DEMO"
        self.proprietary_features_enabled = False
    
    async def analyze_with_love(self, company_data):
        """Public demo analysis"""
        return {
            "status": "demo",
            "message": "Palmer AI Enterprise includes full analysis",
            "company_name": company_data.get("name", "Demo Company"),
            "contact": "sales@palmerai.com"
        }

# Real implementation uses proprietary algorithms

    async def analyze_basic(self, company_data: Dict[str, Any]) -> Dict[str, Any]:
        """Basic analysis for first message - tease value"""
        prompt = f"""Analyze {company_data.get('company_name', 'this company')} briefly.
        Focus on impressive but basic insights. Keep it concise but impactful."""
        
        response = self.anthropic_client.messages.create(
            model=settings.anthropic_model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1000
        )
        
        return {
            "status": "basic_analysis",
            "insights": response.content[0].text,
            "teaser": "Upgrade to see pricing intelligence and competitor analysis..."
        }
    
    async def analyze_enhanced(self, company_data: Dict[str, Any]) -> Dict[str, Any]:
        """Enhanced analysis for second message - show more value"""
        prompt = f"""Analyze {company_data.get('company_name', 'this company')} with medium depth.
        Include pricing indicators, market position, and growth signals."""
        
        response = self.anthropic_client.messages.create(
            model=settings.anthropic_model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=2000
        )
        
        return {
            "status": "enhanced_analysis",
            "insights": response.content[0].text,
            "teaser": "Next analysis includes decision-maker contacts and strategic recommendations..."
        }
    
    async def analyze_complete(self, company_data: Dict[str, Any]) -> Dict[str, Any]:
        """Complete analysis for third message - maximum value before paywall"""
        return await self.analyze_with_love(company_data)
    
    async def analyze_with_hook(self, company_data: Dict[str, Any], session_id: str) -> Dict[str, Any]:
        """Analyze with 3-message conversion hook"""
        # Check rate limit
        if not conversion_hook.check_rate_limit(session_id):
            hook_data = await conversion_hook.track_message(session_id, "analysis_blocked")
            return hook_data
        
        # Track message
        hook_data = await conversion_hook.track_message(session_id, "analysis")
        
        # Perform analysis based on message stage
        if hook_data["message_count"] == 1:
            analysis = await self.analyze_basic(company_data)
        elif hook_data["message_count"] == 2:
            analysis = await self.analyze_enhanced(company_data)
        else:
            analysis = await self.analyze_complete(company_data)
        
        # Combine analysis with hook data
        return {
            "analysis": analysis,
            "conversion_hook": hook_data,
            "timestamp": datetime.utcnow().isoformat()
        }

    async def analyze_basic(self, company_data: Dict[str, Any]) -> Dict[str, Any]:
        """Basic analysis for first message - tease value"""
        prompt = f"""Analyze {company_data.get('company_name', 'this company')} briefly.
        Focus on impressive but basic insights. Keep it concise but impactful."""
        
        response = self.anthropic_client.messages.create(
            model=settings.anthropic_model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1000
        )
        
        return {
            "status": "basic_analysis",
            "insights": response.content[0].text,
            "teaser": "Upgrade to see pricing intelligence and competitor analysis..."
        }
    
    async def analyze_enhanced(self, company_data: Dict[str, Any]) -> Dict[str, Any]:
        """Enhanced analysis for second message - show more value"""
        prompt = f"""Analyze {company_data.get('company_name', 'this company')} with medium depth.
        Include pricing indicators, market position, and growth signals."""
        
        response = self.anthropic_client.messages.create(
            model=settings.anthropic_model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=2000
        )
        
        return {
            "status": "enhanced_analysis",
            "insights": response.content[0].text,
            "teaser": "Next analysis includes decision-maker contacts and strategic recommendations..."
        }
    
    async def analyze_complete(self, company_data: Dict[str, Any]) -> Dict[str, Any]:
        """Complete analysis for third message - maximum value before paywall"""
        return await self.analyze_with_love(company_data)
    
    async def analyze_with_hook(self, company_data: Dict[str, Any], session_id: str) -> Dict[str, Any]:
        """Analyze with 3-message conversion hook"""
        # Check rate limit
        if not conversion_hook.check_rate_limit(session_id):
            hook_data = await conversion_hook.track_message(session_id, "analysis_blocked")
            return hook_data
        
        # Track message
        hook_data = await conversion_hook.track_message(session_id, "analysis")
        
        # Perform analysis based on message stage
        if hook_data["message_count"] == 1:
            analysis = await self.analyze_basic(company_data)
        elif hook_data["message_count"] == 2:
            analysis = await self.analyze_enhanced(company_data)
        else:
            analysis = await self.analyze_complete(company_data)
        
        # Combine analysis with hook data
        return {
            "analysis": analysis,
            "conversion_hook": hook_data,
            "timestamp": datetime.utcnow().isoformat()
        }
