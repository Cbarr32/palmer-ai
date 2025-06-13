from pydantic import BaseModel, Field
from typing import List, Dict, Any
from enum import Enum

class AgentRole(str, Enum):
    RECONNAISSANCE = "reconnaissance"
    COMPETITIVE_INTELLIGENCE = "competitive_intelligence"

class AgentCapability(BaseModel):
    name: str
    description: str
    required_resources: List[str] = Field(default_factory=list)

# Test the problematic model
try:
    class AgentConfig(BaseModel):
        agent_id: str
        name: str
        role: AgentRole
        description: str
        capabilities: List[AgentCapability]
        model_config: Dict[str, Any] = Field(default_factory=dict)
        max_concurrent_tasks: int = 5
        timeout_seconds: int = 300
        uwas_techniques: List[str] = Field(default_factory=list)
    
    print("AgentConfig model created successfully")
    
    # Test instantiation
    test_config = AgentConfig(
        agent_id="test",
        name="Test Agent",
        role=AgentRole.RECONNAISSANCE,
        description="Test",
        capabilities=[]
    )
    print("AgentConfig instantiated successfully")
    
except Exception as e:
    print(f"Error: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
