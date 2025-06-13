"""Basic metrics collection for Palmer AI"""
from typing import Dict, Any
import time

class MetricsCollector:
    """Simple metrics collector"""
    
    def __init__(self):
        self.metrics = {
            "requests_total": 0,
            "analysis_duration": [],
            "active_connections": 0
        }
        self.start_time = time.time()
    
    async def start(self):
        """Start metrics collection"""
        pass
    
    async def stop(self):
        """Stop metrics collection"""
        pass
    
    def record_request(self):
        """Record a request"""
        self.metrics["requests_total"] += 1
    
    def record_analysis_duration(self, duration: float):
        """Record analysis duration"""
        self.metrics["analysis_duration"].append(duration)
        if len(self.metrics["analysis_duration"]) > 100:
            self.metrics["analysis_duration"] = self.metrics["analysis_duration"][-100:]
    
    def get_prometheus_metrics(self) -> str:
        """Get metrics in Prometheus format"""
        uptime = time.time() - self.start_time
        avg_duration = (
            sum(self.metrics["analysis_duration"]) / len(self.metrics["analysis_duration"])
            if self.metrics["analysis_duration"] else 0
        )
        
        return f"""# HELP palmer_ai_requests_total Total requests processed
# TYPE palmer_ai_requests_total counter
palmer_ai_requests_total {self.metrics["requests_total"]}

# HELP palmer_ai_uptime_seconds Uptime in seconds
# TYPE palmer_ai_uptime_seconds gauge
palmer_ai_uptime_seconds {uptime}

# HELP palmer_ai_analysis_duration_avg Average analysis duration
# TYPE palmer_ai_analysis_duration_avg gauge
palmer_ai_analysis_duration_avg {avg_duration}
"""

metrics_collector = MetricsCollector()
