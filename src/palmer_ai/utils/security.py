"""Security utilities for Palmer AI"""
import hashlib
import hmac
import secrets
import re
from typing import Dict, Any, List, Optional, Union
from urllib.parse import urlparse
import bleach
from datetime import datetime, timedelta

from ..config import settings
from .logger import get_logger

logger = get_logger(__name__)

class SecurityValidator:
    """Comprehensive security validation for Palmer AI"""
    
    def __init__(self):
        self.allowed_domains = [
            'localhost',
            '127.0.0.1',
            'palmer-apps.com'
        ]
        self.max_file_size = 50 * 1024 * 1024  # 50MB
        self.allowed_file_types = ['.xlsx', '.xls', '.csv', '.txt']
        
    def validate_url(self, url: str) -> bool:
        """Validate URL for safety"""
        try:
            parsed = urlparse(url)
            
            # Check scheme
            if parsed.scheme not in ['http', 'https']:
                return False
                
            # Check domain
            if parsed.netloc not in self.allowed_domains and not settings.debug:
                # In production, only allow whitelisted domains
                return False
                
            # Check for suspicious patterns
            suspicious_patterns = [
                'javascript:', 'data:', 'file:', 'ftp:',
                '../', '..\\', '%2e%2e', '%2f', '%5c'
            ]
            
            for pattern in suspicious_patterns:
                if pattern in url.lower():
                    return False
                    
            return True
        except Exception:
            return False
            
    def validate_file_upload(self, filename: str, content: bytes) -> Dict[str, Any]:
        """Validate uploaded file"""
        errors = []
        
        # Check file size
        if len(content) > self.max_file_size:
            errors.append(f"File too large: {len(content)} bytes (max: {self.max_file_size})")
            
        # Check file extension
        if not any(filename.lower().endswith(ext) for ext in self.allowed_file_types):
            errors.append(f"Invalid file type. Allowed: {', '.join(self.allowed_file_types)}")
            
        # Check for malicious content patterns
        content_str = content[:1024].decode('utf-8', errors='ignore').lower()
        malicious_patterns = [
            '<script', 'javascript:', 'vbscript:', 'onload=', 'onerror=',
            'data:text/html', '<?php', '<%', 'exec(', 'eval('
        ]
        
        for pattern in malicious_patterns:
            if pattern in content_str:
                errors.append(f"Potentially malicious content detected")
                break
                
        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "file_size": len(content),
            "file_type": filename.split('.')[-1].lower() if '.' in filename else 'unknown'
        }
        
    def sanitize_input(self, data: Any) -> Any:
        """Sanitize user input"""
        if isinstance(data, str):
            # Remove potentially harmful characters
            sanitized = bleach.clean(data, strip=True)
            # Limit length
            return sanitized[:10000]
        elif isinstance(data, dict):
            return {key: self.sanitize_input(value) for key, value in data.items()}
        elif isinstance(data, list):
            return [self.sanitize_input(item) for item in data]
        else:
            return data
            
    def validate_api_request(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate API request data"""
        errors = []
        
        # Check for required fields
        if 'distributor_id' in request_data:
            distributor_id = request_data['distributor_id']
            if not re.match(r'^[a-zA-Z0-9_-]{1,50}$', distributor_id):
                errors.append("Invalid distributor_id format")
                
        # Check message length
        if 'message' in request_data:
            message = request_data['message']
            if len(message) > 10000:
                errors.append("Message too long (max: 10000 characters)")
                
        # Sanitize all inputs
        sanitized_data = self.sanitize_input(request_data)
        
        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "sanitized_data": sanitized_data
        }
        
    def generate_api_key(self) -> str:
        """Generate secure API key"""
        return secrets.token_urlsafe(32)
        
    def verify_api_key(self, api_key: str, stored_hash: str) -> bool:
        """Verify API key against stored hash"""
        return hmac.compare_digest(
            hashlib.sha256(api_key.encode()).hexdigest(),
            stored_hash
        )

# Global security validator
security_validator = SecurityValidator()
