"""Palmer AI Intelligent Cache System"""
import json
import hashlib
import pickle
from pathlib import Path
from datetime import datetime, timedelta
from typing import Any, Optional, Dict

class SemanticCache:
    """High-performance semantic cache for distributor data"""
    
    def __init__(self, cache_dir: str = "cache"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
        self.memory_cache: Dict[str, Any] = {}
        self.ttl = timedelta(hours=24)
        
    def _get_key(self, url: str) -> str:
        """Generate cache key"""
        return hashlib.md5(url.encode()).hexdigest()
        
    async def get_similar(self, url: str, threshold: float = 0.95) -> Optional[Any]:
        """Get cached result if available"""
        key = self._get_key(url)
        
        # Memory cache check
        if key in self.memory_cache:
            entry = self.memory_cache[key]
            if datetime.utcnow() - entry['timestamp'] < self.ttl:
                return entry['data']
                
        # Disk cache check
        cache_file = self.cache_dir / f"{key}.pkl"
        if cache_file.exists():
            try:
                with open(cache_file, 'rb') as f:
                    entry = pickle.load(f)
                if datetime.utcnow() - entry['timestamp'] < self.ttl:
                    self.memory_cache[key] = entry
                    return entry['data']
            except:
                pass
                
        return None
        
    async def store(self, url: str, data: Any) -> None:
        """Store data in cache"""
        key = self._get_key(url)
        entry = {'timestamp': datetime.utcnow(), 'data': data}
        
        # Store in memory
        self.memory_cache[key] = entry
        
        # Store on disk
        try:
            with open(self.cache_dir / f"{key}.pkl", 'wb') as f:
                pickle.dump(entry, f)
        except:
            pass
