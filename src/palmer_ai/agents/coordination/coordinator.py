"""Multi-Agent Coordinator for orchestrating collaborative analysis"""
import asyncio
from typing import Dict, Any, List, Optional, Set
from datetime import datetime
from enum import Enum

from ..base.agent import (
    BaseAgent, AgentConfig, AgentRole, AnalysisResult, 
    ConfidenceLevel, AgentMessage
)
from ..specialized.reconnaissance_agent import ReconnaissanceAgent
from ..specialized.competitive_intelligence_agent import CompetitiveIntelligenceAgent
from ...utils.logger import get_logger

logger = get_logger(__name__)

class CoordinationStrategy(str, Enum):
    PARALLEL = "parallel"
    SEQUENTIAL = "sequential"
    ADAPTIVE = "adaptive"
    
class AgentCoordinator:
    """Orchestrates multiple agents for comprehensive analysis"""
    
    def __init__(self):
        self.agents: Dict[AgentRole, BaseAgent] = {}
        self.active_analyses: Dict[str, Dict[str, Any]] = {}
        self.message_queue: asyncio.Queue = asyncio.Queue()
        self.logger = get_logger(__name__)
        self._initialize_agents()
        
    def _initialize_agents(self):
        """Initialize all specialized agents"""
        # Reconnaissance Agent
        recon_config = AgentConfig(
            agent_id="recon_001",
            name="Strategic Reconnaissance Specialist",
            role=AgentRole.RECONNAISSANCE,
            description="Comprehensive website analysis and mapping",
            capabilities=[],
            uwas_techniques=["chain_of_thought", "expert_persona"]
        )
        self.agents[AgentRole.RECONNAISSANCE] = ReconnaissanceAgent(recon_config)
        
        # Competitive Intelligence Agent
        competitive_config = AgentConfig(
            agent_id="competitive_001",
            name="Market Intelligence Analyst",
            role=AgentRole.COMPETITIVE_INTELLIGENCE,
            description="Competitive landscape and market positioning analysis",
            capabilities=[],
            uwas_techniques=["comparative_framework", "tree_of_thought", "outcome_focused"]
        )
        self.agents[AgentRole.COMPETITIVE_INTELLIGENCE] = CompetitiveIntelligenceAgent(competitive_config)
        
        # Additional agents would be initialized here
        
    async def coordinate_analysis(self, 
                                 target_url: str,
                                 analysis_type: str = "comprehensive",
                                 strategy: CoordinationStrategy = CoordinationStrategy.ADAPTIVE,
                                 options: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Coordinate multi-agent analysis"""
        analysis_id = f"analysis_{datetime.utcnow().timestamp()}"
        start_time = datetime.utcnow()
        
        self.logger.info(f"Starting coordinated analysis {analysis_id} for {target_url}")
        
        # Initialize analysis tracking
        self.active_analyses[analysis_id] = {
            "target_url": target_url,
            "analysis_type": analysis_type,
            "strategy": strategy,
            "start_time": start_time,
            "agent_results": {},
            "status": "in_progress"
        }
        
        try:
            # Determine which agents to deploy
            agents_to_deploy = self._select_agents(analysis_type, options)
            
            # Execute analysis based on strategy
            if strategy == CoordinationStrategy.PARALLEL:
                results = await self._parallel_execution(
                    analysis_id, target_url, agents_to_deploy, options
                )
            elif strategy == CoordinationStrategy.SEQUENTIAL:
                results = await self._sequential_execution(
                    analysis_id, target_url, agents_to_deploy, options
                )
            else:  # ADAPTIVE
                results = await self._adaptive_execution(
                    analysis_id, target_url, agents_to_deploy, options
                )
                
            # Synthesize results
            synthesis = await self._synthesize_results(results)
            
            # Calculate overall confidence
            overall_confidence = self._calculate_overall_confidence(results)
            
            # Update analysis record
            self.active_analyses[analysis_id].update({
                "status": "completed",
                "end_time": datetime.utcnow(),
                "duration": (datetime.utcnow() - start_time).total_seconds(),
                "results": synthesis,
                "confidence": overall_confidence
            })
            
            return {
                "analysis_id": analysis_id,
                "target_url": target_url,
                "analysis_type": analysis_type,
                "execution_strategy": strategy,
                "agent_results": results,
                "synthesis": synthesis,
                "confidence": overall_confidence,
                "metadata": {
                    "duration": (datetime.utcnow() - start_time).total_seconds(),
                    "agents_deployed": len(agents_to_deploy),
                    "timestamp": datetime.utcnow().isoformat()
                }
            }
            
        except Exception as e:
            self.logger.error(f"Coordinated analysis failed: {str(e)}")
            self.active_analyses[analysis_id]["status"] = "failed"
            self.active_analyses[analysis_id]["error"] = str(e)
            raise
            
    def _select_agents(self, 
                      analysis_type: str, 
                      options: Optional[Dict[str, Any]]) -> List[AgentRole]:
        """Select which agents to deploy based on analysis type"""
        if analysis_type == "comprehensive":
            return [
                AgentRole.RECONNAISSANCE,
                AgentRole.COMPETITIVE_INTELLIGENCE,
                # Add other agents as they're implemented
            ]
        elif analysis_type == "competitive":
            return [AgentRole.COMPETITIVE_INTELLIGENCE]
        elif analysis_type == "technical":
            return [AgentRole.RECONNAISSANCE]
        else:
            # Default to reconnaissance
            return [AgentRole.RECONNAISSANCE]
            
    async def _parallel_execution(self,
                                 analysis_id: str,
                                 target_url: str,
                                 agents: List[AgentRole],
                                 options: Optional[Dict[str, Any]]) -> Dict[AgentRole, AnalysisResult]:
        """Execute agents in parallel"""
        tasks = []
        
        for agent_role in agents:
            if agent_role in self.agents:
                agent = self.agents[agent_role]
                task = asyncio.create_task(
                    agent.analyze({
                        "url": target_url,
                        "analysis_id": analysis_id,
                        **(options or {})
                    })
                )
                tasks.append((agent_role, task))
                
        # Wait for all agents to complete
        results = {}
        for agent_role, task in tasks:
            try:
                result = await task
                results[agent_role] = result
                self.active_analyses[analysis_id]["agent_results"][agent_role.value] = result
            except Exception as e:
                self.logger.error(f"Agent {agent_role} failed: {str(e)}")
                results[agent_role] = AnalysisResult(
                    success=False,
                    errors=[str(e)],
                    confidence=ConfidenceLevel.LOW
                )
                
        return results
        
    async def _sequential_execution(self,
                                   analysis_id: str,
                                   target_url: str,
                                   agents: List[AgentRole],
                                   options: Optional[Dict[str, Any]]) -> Dict[AgentRole, AnalysisResult]:
        """Execute agents sequentially, passing results forward"""
        results = {}
        accumulated_data = {"url": target_url, "analysis_id": analysis_id}
        
        for agent_role in agents:
            if agent_role in self.agents:
                agent = self.agents[agent_role]
                
                # Add previous results to input
                if results:
                    accumulated_data["previous_results"] = {
                        role.value: result.data 
                        for role, result in results.items() 
                        if result.success
                    }
                    
                try:
                    result = await agent.analyze({
                        **accumulated_data,
                        **(options or {})
                    })
                    results[agent_role] = result
                    
                    # Accumulate successful results
                    if result.success and result.data:
                        accumulated_data.update(result.data)
                        
                except Exception as e:
                    self.logger.error(f"Sequential execution failed at {agent_role}: {str(e)}")
                    results[agent_role] = AnalysisResult(
                        success=False,
                        errors=[str(e)],
                        confidence=ConfidenceLevel.LOW
                    )
                    # Continue with remaining agents despite failure
                    
        return results
        
    async def _adaptive_execution(self,
                                 analysis_id: str,
                                 target_url: str,
                                 agents: List[AgentRole],
                                 options: Optional[Dict[str, Any]]) -> Dict[AgentRole, AnalysisResult]:
        """Adaptively execute agents based on intermediate results"""
        results = {}
        
        # Always start with reconnaissance
        if AgentRole.RECONNAISSANCE in agents:
            recon_result = await self.agents[AgentRole.RECONNAISSANCE].analyze({
                "url": target_url,
                "analysis_id": analysis_id,
                **(options or {})
            })
            results[AgentRole.RECONNAISSANCE] = recon_result
            
            # Adapt strategy based on reconnaissance
            if recon_result.success:
                # Parallel execute remaining agents with reconnaissance data
                remaining_agents = [a for a in agents if a != AgentRole.RECONNAISSANCE]
                
                tasks = []
                for agent_role in remaining_agents:
                    if agent_role in self.agents:
                        agent = self.agents[agent_role]
                        task = asyncio.create_task(
                            agent.analyze({
                                "url": target_url,
                                "analysis_id": analysis_id,
                                "recon_data": recon_result.data,
                                **(options or {})
                            })
                        )
                        tasks.append((agent_role, task))
                        
                # Gather remaining results
                for agent_role, task in tasks:
                    try:
                        result = await task
                        results[agent_role] = result
                    except Exception as e:
                        self.logger.error(f"Adaptive execution failed for {agent_role}: {str(e)}")
                        results[agent_role] = AnalysisResult(
                            success=False,
                            errors=[str(e)],
                            confidence=ConfidenceLevel.LOW
                        )
                        
        return results
        
    async def _synthesize_results(self, 
                                 results: Dict[AgentRole, AnalysisResult]) -> Dict[str, Any]:
        """Synthesize findings from multiple agents"""
        synthesis = {
            "key_findings": [],
            "strategic_recommendations": [],
            "risk_factors": [],
            "opportunities": [],
            "consensus_points": [],
            "divergent_findings": []
        }
        
        # Extract key findings from each agent
        for agent_role, result in results.items():
            if result.success and result.data:
                # Extract role-specific insights
                if agent_role == AgentRole.RECONNAISSANCE:
                    synthesis["key_findings"].append({
                        "source": "reconnaissance",
                        "finding": "Site structure and technology assessment completed",
                        "details": result.data.get("site_structure", {})
                    })
                elif agent_role == AgentRole.COMPETITIVE_INTELLIGENCE:
                    opportunities = result.data.get("strategic_opportunities", [])
                    synthesis["opportunities"].extend(opportunities)
                    synthesis["key_findings"].append({
                        "source": "competitive_intelligence",
                        "finding": "Competitive landscape mapped",
                        "details": result.data.get("market_position", {})
                    })
                    
        # Identify consensus and divergence
        # This would be more sophisticated with more agents
        
        return synthesis
        
    def _calculate_overall_confidence(self, 
                                    results: Dict[AgentRole, AnalysisResult]) -> ConfidenceLevel:
        """Calculate overall confidence from agent results"""
        confidence_scores = {
            ConfidenceLevel.HIGH: 0.9,
            ConfidenceLevel.MEDIUM: 0.6,
            ConfidenceLevel.LOW: 0.3
        }
        
        total_score = 0
        valid_results = 0
        
        for result in results.values():
            if result.success:
                total_score += confidence_scores.get(result.confidence, 0.5)
                valid_results += 1
                
        if valid_results == 0:
            return ConfidenceLevel.LOW
            
        avg_score = total_score / valid_results
        
        if avg_score >= 0.8:
            return ConfidenceLevel.HIGH
        elif avg_score >= 0.5:
            return ConfidenceLevel.MEDIUM
        else:
            return ConfidenceLevel.LOW
            
    async def get_agent_performance(self) -> Dict[str, Dict[str, Any]]:
        """Get performance metrics for all agents"""
        performance = {}
        
        for role, agent in self.agents.items():
            performance[role.value] = await agent.get_performance_summary()
            
        return performance
        
    async def shutdown(self):
        """Gracefully shutdown coordinator and agents"""
        self.logger.info("Shutting down agent coordinator")
        
        # Close HTTP clients in agents
        for agent in self.agents.values():
            if hasattr(agent, '__aexit__'):
                await agent.__aexit__(None, None, None)
