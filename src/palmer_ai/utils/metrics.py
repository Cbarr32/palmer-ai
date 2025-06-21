"""Comprehensive Metrics Collection for Palmer AI"""
import time
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from collections import defaultdict, deque
import json
import threading

class MetricsCollector:
    """Thread-safe metrics collector for Palmer AI"""
    
    def __init__(self):
        self._lock = threading.Lock()
        self._counters = defaultdict(int)
        self._gauges = defaultdict(float)
        self._histograms = defaultdict(lambda: deque(maxlen=1000))
        self._timers = {}
        self.start_time = time.time()
        
    def increment_counter(self, name: str, value: int = 1, tags: Optional[Dict[str, str]] = None):
        """Increment a counter metric"""
        with self._lock:
            key = self._format_metric_key(name, tags)
            self._counters[key] += value
            
    def set_gauge(self, name: str, value: float, tags: Optional[Dict[str, str]] = None):
        """Set a gauge metric"""
        with self._lock:
            key = self._format_metric_key(name, tags)
            self._gauges[key] = value
            
    def record_histogram(self, name: str, value: float, tags: Optional[Dict[str, str]] = None):
        """Record a value in histogram"""
        with self._lock:
            key = self._format_metric_key(name, tags)
            self._histograms[key].append({
                'value': value,
                'timestamp': time.time()
            })
            
    def record_analysis_duration(self, duration: float):
        """Record agent analysis duration"""
        self.record_histogram("palmer_ai_analysis_duration_seconds", duration)
        
    def record_api_request(self, endpoint: str, method: str, status_code: int, duration: float):
        """Record API request metrics"""
        tags = {"endpoint": endpoint, "method": method, "status": str(status_code)}
        self.increment_counter("palmer_ai_api_requests_total", tags=tags)
        self.record_histogram("palmer_ai_api_request_duration_seconds", duration, tags=tags)
        
    def _format_metric_key(self, name: str, tags: Optional[Dict[str, str]] = None) -> str:
        """Format metric key with tags"""
        if not tags:
            return name
        tag_string = ",".join(f"{k}={v}" for k, v in sorted(tags.items()))
        return f"{name}[{tag_string}]"
        
    def get_prometheus_metrics(self) -> str:
        """Export metrics in Prometheus format"""
        with self._lock:
            lines = []
            
            # Export counters
            for key, value in self._counters.items():
                clean_key = key.split('[')[0]
                lines.append(f"# TYPE {clean_key} counter")
                lines.append(f"{key} {value}")
                
            # Export gauges
            for key, value in self._gauges.items():
                clean_key = key.split('[')[0]
                lines.append(f"# TYPE {clean_key} gauge")
                lines.append(f"{key} {value}")
                
            # Export histogram summaries
            for key, values in self._histograms.items():
                if values:
                    clean_key = key.split('[')[0]
                    recent_values = [v['value'] for v in values if time.time() - v['timestamp'] < 300]
                    if recent_values:
                        lines.append(f"# TYPE {clean_key}_avg gauge")
                        lines.append(f"{key}_avg {sum(recent_values) / len(recent_values)}")
                        lines.append(f"# TYPE {clean_key}_count gauge")
                        lines.append(f"{key}_count {len(recent_values)}")
                        
            # System uptime
            uptime = time.time() - self.start_time
            lines.append(f"# TYPE palmer_ai_uptime_seconds gauge")
            lines.append(f"palmer_ai_uptime_seconds {uptime}")
            
            return "\n".join(lines)
            
    def get_summary(self) -> Dict[str, Any]:
        """Get metrics summary"""
        with self._lock:
            return {
                "counters": dict(self._counters),
                "gauges": dict(self._gauges),
                "histograms": {
                    key: {
                        "count": len(values),
                        "latest": values[-1] if values else None,
                        "avg_5min": self._calculate_avg_5min(values)
                    }
                    for key, values in self._histograms.items()
                },
                "uptime_seconds": time.time() - self.start_time
            }
            
    def _calculate_avg_5min(self, values: deque) -> Optional[float]:
        """Calculate average for last 5 minutes"""
        cutoff_time = time.time() - 300  # 5 minutes
        recent_values = [v['value'] for v in values if v['timestamp'] > cutoff_time]
        return sum(recent_values) / len(recent_values) if recent_values else None

# Global metrics instance
metrics_collector = MetricsCollector()
