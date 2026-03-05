"""Data validation and cleaning utilities."""

import json
from datetime import datetime
from typing import Any, Dict, Optional, Tuple
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


class DataValidator:
    """Validates and cleans telemetry data."""
    
    @staticmethod
    def validate_event(event: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
        """
        Validate an event structure.
        
        Args:
            event: Event dictionary
        
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not isinstance(event, dict):
            return False, "Event is not a dictionary"
        
        # Check required top-level fields
        required_fields = ["body", "attributes"]
        for field in required_fields:
            if field not in event:
                return False, f"Missing required field: {field}"
        
        # Check required attributes
        attrs = event.get("attributes", {})
        required_attrs = ["event.timestamp", "session.id", "user.id", "user.email", "organization.id"]
        for attr in required_attrs:
            if attr not in attrs:
                return False, f"Missing required attribute: {attr}"
        
        # Validate event type
        body = event.get("body", "")
        if not body.startswith("claude_code."):
            return False, f"Invalid event body: {body}"
        
        return True, None
    
    @staticmethod
    def clean_timestamp(timestamp_str: str) -> Optional[datetime]:
        """
        Parse and clean timestamp string.
        
        Args:
            timestamp_str: ISO 8601 timestamp string
        
        Returns:
            Parsed datetime object or None if invalid
        """
        try:
            # Handle format: 2026-01-15T10:30:45.123Z
            if timestamp_str.endswith('Z'):
                timestamp_str = timestamp_str[:-1] + '+00:00'
            
            # Try parsing with microseconds
            try:
                return datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
            except ValueError:
                # Try without microseconds
                return datetime.strptime(timestamp_str.replace('Z', ''), '%Y-%m-%dT%H:%M:%S')
        except (ValueError, AttributeError) as e:
            logger.warning(f"Invalid timestamp format: {timestamp_str} - {e}")
            return None
    
    @staticmethod
    def safe_int(value: Any, default: int = 0) -> int:
        """Safely convert value to integer."""
        if value is None:
            return default
        try:
            return int(float(str(value)))
        except (ValueError, TypeError):
            return default
    
    @staticmethod
    def safe_float(value: Any, default: float = 0.0) -> float:
        """Safely convert value to float."""
        if value is None:
            return default
        try:
            return float(str(value))
        except (ValueError, TypeError):
            return default
    
    @staticmethod
    def safe_bool(value: Any, default: bool = False) -> bool:
        """Safely convert value to boolean."""
        if value is None:
            return default
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            return value.lower() in ('true', '1', 'yes', 'on')
        return bool(value)
    
    @staticmethod
    def clean_string(value: Any, max_length: Optional[int] = None) -> Optional[str]:
        """Clean and validate string value."""
        if value is None:
            return None
        s = str(value).strip()
        if not s:
            return None
        if max_length and len(s) > max_length:
            return s[:max_length]
        return s
    
    @staticmethod
    def extract_common_attributes(event: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract common attributes from an event.
        
        Args:
            event: Event dictionary
        
        Returns:
            Dictionary of common attributes
        """
        attrs = event.get("attributes", {})
        return {
            "timestamp": attrs.get("event.timestamp"),
            "session_id": attrs.get("session.id"),
            "user_id": attrs.get("user.id"),
            "user_email": attrs.get("user.email"),
            "org_id": attrs.get("organization.id"),
            "terminal_type": attrs.get("terminal.type"),
            "account_uuid": attrs.get("user.account_uuid"),
        }
    
    @staticmethod
    def extract_resource_info(event: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract resource information from an event.
        
        Args:
            event: Event dictionary
        
        Returns:
            Dictionary of resource attributes
        """
        resource = event.get("resource", {})
        return {
            "hostname": resource.get("host.name"),
            "os_type": resource.get("os.type"),
            "os_version": resource.get("os.version"),
            "claude_version": resource.get("service.version"),
        }
