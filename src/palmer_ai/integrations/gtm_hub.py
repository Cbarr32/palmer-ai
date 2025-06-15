"""
Palmer AI GTM Integration Hub
Pushes intelligence to all your sales and marketing tools
"""
from typing import Dict, List, Any, Optional
from datetime import datetime
from enum import Enum
import json
import asyncio

from src.palmer_ai.core.logger import get_logger

logger = get_logger(__name__)

class GTMSystem(Enum):
    """Supported GTM systems"""
    SALESFORCE = "salesforce"
    HUBSPOT = "hubspot"
    DYNAMICS = "dynamics"
    CONFLUENCE = "confluence"
    SLACK = "slack"
    TEAMS = "teams"
    EMAIL = "email"
    

class GTMIntegrationHub:
    """
    Central hub for pushing intelligence to all GTM tools
    One source of truth, many destinations
    """
    
    def __init__(self):
        self.integrations = {
            GTMSystem.SALESFORCE: SalesforceIntegration(),
            GTMSystem.HUBSPOT: HubSpotIntegration(),
            GTMSystem.SLACK: SlackIntegration(),
            GTMSystem.EMAIL: EmailIntegration()
        }
        self.active_integrations = set()
        
    async def broadcast_intelligence(
        self,
        intelligence_type: str,
        data: Dict[str, Any],
        priority: str = "normal"
    ) -> Dict[str, Any]:
        """Broadcast intelligence to all active integrations"""
        logger.info(f"Broadcasting {intelligence_type} to {len(self.active_integrations)} systems")
        
        results = {}
        
        for system in self.active_integrations:
            if system in self.integrations:
                try:
                    result = await self.integrations[system].send(
                        intelligence_type,
                        data,
                        priority
                    )
                    results[system.value] = result
                except Exception as e:
                    logger.error(f"Failed to send to {system.value}: {str(e)}")
                    results[system.value] = {'success': False, 'error': str(e)}
                    
        return {
            'broadcast_id': f"BC-{datetime.utcnow().timestamp()}",
            'intelligence_type': intelligence_type,
            'systems_notified': len([r for r in results.values() if r.get('success')]),
            'results': results
        }
        
    def enable_integration(self, system: GTMSystem, config: Dict[str, Any]):
        """Enable a GTM integration"""
        self.integrations[system].configure(config)
        self.active_integrations.add(system)
        logger.info(f"Enabled integration: {system.value}")
        

class SalesforceIntegration:
    """Salesforce CRM integration"""
    
    def __init__(self):
        self.configured = False
        
    def configure(self, config: Dict[str, Any]):
        """Configure Salesforce connection"""
        # Would store auth tokens, instance URL, etc.
        self.configured = True
        
    async def send(self, intelligence_type: str, data: Dict[str, Any], priority: str) -> Dict[str, Any]:
        """Send intelligence to Salesforce"""
        
        if not self.configured:
            return {'success': False, 'error': 'Not configured'}
            
        # Map intelligence types to Salesforce objects
        if intelligence_type == 'battle_card':
            return await self._update_competitor_record(data)
        elif intelligence_type == 'opportunity':
            return await self._create_opportunity(data)
        elif intelligence_type == 'rfp':
            return await self._update_rfp_tracking(data)
            
        return {'success': True}
        
    async def _update_competitor_record(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Update competitor intelligence in Salesforce"""
        # In production, would use Salesforce API
        return {
            'success': True,
            'object': 'Competitor__c',
            'id': 'COMP-12345',
            'fields_updated': ['Battle_Card__c', 'Last_Intel_Update__c']
        }
        
    async def _create_opportunity(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create opportunity in Salesforce"""
        return {
            'success': True,
            'object': 'Opportunity',
            'id': 'OPP-67890',
            'stage': 'Prospecting'
        }
        

class HubSpotIntegration:
    """HubSpot CRM integration"""
    
    def __init__(self):
        self.configured = False
        
    def configure(self, config: Dict[str, Any]):
        """Configure HubSpot connection"""
        self.configured = True
        
    async def send(self, intelligence_type: str, data: Dict[str, Any], priority: str) -> Dict[str, Any]:
        """Send intelligence to HubSpot"""
        
        if not self.configured:
            return {'success': False, 'error': 'Not configured'}
            
        # Would use HubSpot API
        return {
            'success': True,
            'contact_updated': data.get('company'),
            'properties_set': ['competitive_intel', 'last_analysis']
        }
        

class SlackIntegration:
    """Slack notifications"""
    
    def __init__(self):
        self.configured = False
        self.channels = {
            'high': '#sales-alerts',
            'normal': '#competitive-intel',
            'rfp': '#rfp-team'
        }
        
    def configure(self, config: Dict[str, Any]):
        """Configure Slack webhook"""
        self.webhook_url = config.get('webhook_url')
        self.configured = True
        
    async def send(self, intelligence_type: str, data: Dict[str, Any], priority: str) -> Dict[str, Any]:
        """Send intelligence to Slack"""
        
        if not self.configured:
            return {'success': False, 'error': 'Not configured'}
            
        # Format message based on type
        message = self._format_message(intelligence_type, data, priority)
        
        # Would post to Slack
        return {
            'success': True,
            'channel': self.channels.get(priority, '#general'),
            'message_sent': True
        }
        
    def _format_message(self, intel_type: str, data: Dict[str, Any], priority: str) -> Dict[str, Any]:
        """Format Slack message"""
        
        if intel_type == 'opportunity':
            return {
                'text': f"🎯 New Opportunity Detected: {data.get('company')}",
                'blocks': [
                    {
                        'type': 'section',
                        'text': {
                            'type': 'mrkdwn',
                            'text': f"*Company:* {data.get('company')}\n*Stage:* {data.get('stage')}\n*Probability:* {data.get('probability', 0):.0%}"
                        }
                    }
                ]
            }
        elif intel_type == 'battle_card':
            return {
                'text': f"⚔️ Battle Card Updated: {data.get('competitor')}",
                'blocks': [
                    {
                        'type': 'section',
                        'text': {
                            'type': 'mrkdwn',
                            'text': f"*Competitor:* {data.get('competitor')}\n*New Vulnerabilities:* {len(data.get('vulnerabilities', []))}"
                        }
                    }
                ]
            }
            
        return {'text': f"Intelligence Update: {intel_type}"}
        

class EmailIntegration:
    """Email notifications"""
    
    def __init__(self):
        self.configured = False
        
    def configure(self, config: Dict[str, Any]):
        """Configure email settings"""
        self.configured = True
        
    async def send(self, intelligence_type: str, data: Dict[str, Any], priority: str) -> Dict[str, Any]:
        """Send intelligence via email"""
        
        if not self.configured:
            return {'success': False, 'error': 'Not configured'}
            
        # Would send email
        return {
            'success': True,
            'recipients': ['sales-team@company.com'],
            'subject': f"Palmer AI: {intelligence_type} Alert"
        }
