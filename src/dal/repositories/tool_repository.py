"""Tool repository for data access."""

from datetime import datetime
from typing import List, Optional, Dict, Any
from src.storage.database import Database
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


class ToolRepository:
    """Repository for tool usage data access."""
    
    def __init__(self, db: Database):
        """
        Initialize tool repository.
        
        Args:
            db: Database instance
        """
        self.db = db
    
    def get_tool_decisions(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Get all tool decisions.
        
        Args:
            limit: Optional limit on number of results
        """
        query = "SELECT * FROM tool_decisions ORDER BY timestamp DESC"
        if limit:
            query += f" LIMIT {limit}"
        
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            return [dict(row) for row in cursor.fetchall()]
    
    def get_tool_results(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Get all tool results.
        
        Args:
            limit: Optional limit on number of results
        """
        query = "SELECT * FROM tool_results ORDER BY timestamp DESC"
        if limit:
            query += f" LIMIT {limit}"
        
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            return [dict(row) for row in cursor.fetchall()]
    
    def get_tool_usage_statistics(self) -> List[Dict[str, Any]]:
        """Get tool usage statistics grouped by tool name."""
        query = """
            SELECT 
                tr.tool_name,
                COUNT(*) as total_uses,
                SUM(CASE WHEN tr.success = 1 THEN 1 ELSE 0 END) as successful_uses,
                SUM(CASE WHEN tr.success = 0 THEN 1 ELSE 0 END) as failed_uses,
                CAST(SUM(CASE WHEN tr.success = 1 THEN 1 ELSE 0 END) AS FLOAT) / COUNT(*) * 100 as success_rate,
                AVG(tr.duration_ms) as avg_duration_ms,
                MIN(tr.duration_ms) as min_duration_ms,
                MAX(tr.duration_ms) as max_duration_ms,
                AVG(tr.result_size_bytes) as avg_result_size_bytes
            FROM tool_results tr
            GROUP BY tr.tool_name
            ORDER BY total_uses DESC
        """
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            return [dict(row) for row in cursor.fetchall()]
    
    def get_tool_decision_statistics(self) -> List[Dict[str, Any]]:
        """Get tool decision statistics grouped by tool name."""
        query = """
            SELECT 
                tool_name,
                COUNT(*) as total_decisions,
                SUM(CASE WHEN decision = 'accept' THEN 1 ELSE 0 END) as accepted,
                SUM(CASE WHEN decision = 'reject' THEN 1 ELSE 0 END) as rejected,
                CAST(SUM(CASE WHEN decision = 'accept' THEN 1 ELSE 0 END) AS FLOAT) / COUNT(*) * 100 as acceptance_rate
            FROM tool_decisions
            GROUP BY tool_name
            ORDER BY total_decisions DESC
        """
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            return [dict(row) for row in cursor.fetchall()]
    
    def get_tool_usage_by_user(self, user_id: str) -> List[Dict[str, Any]]:
        """Get tool usage statistics for a specific user."""
        query = """
            SELECT 
                tr.tool_name,
                COUNT(*) as total_uses,
                SUM(CASE WHEN tr.success = 1 THEN 1 ELSE 0 END) as successful_uses,
                AVG(tr.duration_ms) as avg_duration_ms
            FROM tool_results tr
            WHERE tr.user_id = ?
            GROUP BY tr.tool_name
            ORDER BY total_uses DESC
        """
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (user_id,))
            return [dict(row) for row in cursor.fetchall()]
