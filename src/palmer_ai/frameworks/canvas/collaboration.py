"""Canvas Collaboration Framework for Palmer AI"""
from typing import Dict, Any, Optional
from datetime import datetime
from enum import Enum
from pydantic import BaseModel

class ElementType(str, Enum):
    INSIGHT = "insight"
    RECOMMENDATION = "recommendation"
    ANALYSIS = "analysis"
    COMMENT = "comment"

class CanvasUpdate(BaseModel):
    """Canvas collaboration update model"""
    element_id: str
    element_type: ElementType
    content: Dict[str, Any]
    metadata: Dict[str, Any] = {}
    timestamp: datetime = datetime.utcnow()
    user_id: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "element_id": self.element_id,
            "element_type": self.element_type.value,
            "content": self.content,
            "metadata": self.metadata,
            "timestamp": self.timestamp.isoformat(),
            "user_id": self.user_id
        }
