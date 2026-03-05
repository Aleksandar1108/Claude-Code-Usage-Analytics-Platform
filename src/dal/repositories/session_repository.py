"""Session repository for data access."""

from datetime import datetime
from typing import List, Optional, Dict, Any
from src.storage.database import Database
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


class SessionRepository:
    """Repository for session data access."""
    
    def __init__(self, db: Database):
        """
        Initialize session repository.
        
        Args:
            db: Database instance
        """
        self.db = db
    
    def get_all(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Get all sessions.
        
        Args:
            limit: Optional limit on number of results
        """
        query = "SELECT * FROM sessions ORDER BY start_time DESC"
        if limit:
            query += f" LIMIT {limit}"
        
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            return [dict(row) for row in cursor.fetchall()]
    
    def get_by_id(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get session by ID."""
        query = "SELECT * FROM sessions WHERE session_id = ?"
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (session_id,))
            row = cursor.fetchone()
            return dict(row) if row else None
    
    def get_by_user_id(self, user_id: str) -> List[Dict[str, Any]]:
        """Get all sessions for a user."""
        query = "SELECT * FROM sessions WHERE user_id = ? ORDER BY start_time DESC"
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (user_id,))
            return [dict(row) for row in cursor.fetchall()]
    
    def get_by_date_range(
        self, 
        start_date: datetime, 
        end_date: datetime
    ) -> List[Dict[str, Any]]:
        """Get sessions within date range."""
        query = """
            SELECT * FROM sessions 
            WHERE start_time >= ? AND start_time <= ?
            ORDER BY start_time DESC
        """
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (start_date, end_date))
            return [dict(row) for row in cursor.fetchall()]
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get session statistics."""
        query = """
            SELECT 
                COUNT(*) as total_sessions,
                COUNT(DISTINCT user_id) as unique_users,
                AVG(duration_seconds) as avg_duration,
                MIN(duration_seconds) as min_duration,
                MAX(duration_seconds) as max_duration,
                SUM(duration_seconds) as total_duration
            FROM sessions
            WHERE duration_seconds IS NOT NULL
        """
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            row = cursor.fetchone()
            return dict(row) if row else {}
    
    def count(self) -> int:
        """Get total session count."""
        query = "SELECT COUNT(*) as count FROM sessions"
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            return cursor.fetchone()["count"]
