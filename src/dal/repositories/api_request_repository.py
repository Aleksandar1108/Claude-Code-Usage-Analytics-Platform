"""API request repository for data access."""

from datetime import datetime
from typing import List, Optional, Dict, Any
from src.storage.database import Database
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


class APIRequestRepository:
    """Repository for API request data access."""
    
    def __init__(self, db: Database):
        """
        Initialize API request repository.
        
        Args:
            db: Database instance
        """
        self.db = db
    
    def get_all(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Get all API requests.
        
        Args:
            limit: Optional limit on number of results
        """
        query = "SELECT * FROM api_requests ORDER BY timestamp DESC"
        if limit:
            query += f" LIMIT {limit}"
        
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            return [dict(row) for row in cursor.fetchall()]
    
    def get_by_date_range(
        self, 
        start_date: datetime, 
        end_date: datetime
    ) -> List[Dict[str, Any]]:
        """Get API requests within date range."""
        query = """
            SELECT * FROM api_requests 
            WHERE timestamp >= ? AND timestamp <= ?
            ORDER BY timestamp DESC
        """
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (start_date, end_date))
            return [dict(row) for row in cursor.fetchall()]
    
    def get_by_user_id(self, user_id: str) -> List[Dict[str, Any]]:
        """Get all API requests for a user."""
        query = "SELECT * FROM api_requests WHERE user_id = ? ORDER BY timestamp DESC"
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (user_id,))
            return [dict(row) for row in cursor.fetchall()]
    
    def get_by_model(self, model: str) -> List[Dict[str, Any]]:
        """Get all API requests for a specific model."""
        query = "SELECT * FROM api_requests WHERE model = ? ORDER BY timestamp DESC"
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (model,))
            return [dict(row) for row in cursor.fetchall()]
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get API request statistics."""
        query = """
            SELECT 
                COUNT(*) as total_requests,
                COUNT(DISTINCT user_id) as unique_users,
                COUNT(DISTINCT model) as unique_models,
                SUM(input_tokens) as total_input_tokens,
                SUM(output_tokens) as total_output_tokens,
                SUM(cache_read_tokens) as total_cache_read_tokens,
                SUM(cache_creation_tokens) as total_cache_creation_tokens,
                SUM(cost_usd) as total_cost,
                AVG(cost_usd) as avg_cost,
                AVG(duration_ms) as avg_duration_ms
            FROM api_requests
        """
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            row = cursor.fetchone()
            return dict(row) if row else {}
    
    def get_by_model_statistics(self) -> List[Dict[str, Any]]:
        """Get statistics grouped by model."""
        query = """
            SELECT 
                model,
                COUNT(*) as request_count,
                COUNT(DISTINCT user_id) as unique_users,
                SUM(input_tokens) as total_input_tokens,
                SUM(output_tokens) as total_output_tokens,
                SUM(cost_usd) as total_cost,
                AVG(cost_usd) as avg_cost_per_request,
                AVG(duration_ms) as avg_duration_ms
            FROM api_requests
            GROUP BY model
            ORDER BY total_cost DESC
        """
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            return [dict(row) for row in cursor.fetchall()]
    
    def count(self) -> int:
        """Get total API request count."""
        query = "SELECT COUNT(*) as count FROM api_requests"
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            return cursor.fetchone()["count"]
