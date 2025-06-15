"""Palmer AI Authentication System"""
from typing import Dict, Optional

async def get_current_user(token: Optional[str] = None) -> Dict[str, Any]:
    """Get current user (development stub)"""
    return {
        "id": "dev_user",
        "email": "dev@palmerai.com",
        "subscription": "professional"
    }
