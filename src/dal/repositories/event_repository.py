"""Event repository for data access."""

from datetime import datetime
from typing import List, Optional, Dict, Any
from src.storage.database import Database
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


class EventRepository:
    """Repository for event data access."""
    
    def __init__(self, db: Database):
        """
        Initialize event repository.
        
        Args:
            db: Database instance
        """
        self.db = db
    
    def get_by_type(
        self, 
        event_type: str, 
        limit: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Get events by type.
        
        Args:
            event_type: Event type (api_request, tool_decision, etc.)
            limit: Optional limit on number of results
        """
        query = "SELECT * FROM events WHERE event_type = ? ORDER BY timestamp DESC"
        if limit:
            query += f" LIMIT {limit}"
        
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (event_type,))
            return [dict(row) for row in cursor.fetchall()]
    
    def get_by_date_range(
        self, 
        start_date: datetime, 
        end_date: datetime,
        event_type: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Get events within date range.
        
        Args:
            start_date: Start date
            end_date: End date
            event_type: Optional event type filter
        """
        if event_type:
            query = """
                SELECT * FROM events 
                WHERE timestamp >= ? AND timestamp <= ? AND event_type = ?
                ORDER BY timestamp DESC
            """
            params = (start_date, end_date, event_type)
        else:
            query = """
                SELECT * FROM events 
                WHERE timestamp >= ? AND timestamp <= ?
                ORDER BY timestamp DESC
            """
            params = (start_date, end_date)
        
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]
    
    def get_event_counts_by_type(self) -> List[Dict[str, Any]]:
        """Get event counts grouped by type."""
        query = """
            SELECT 
                event_type,
                COUNT(*) as count
            FROM events
            GROUP BY event_type
            ORDER BY count DESC
        """
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            return [dict(row) for row in cursor.fetchall()]
    
    def get_hourly_distribution(
        self, 
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> List[Dict[str, Any]]:
        """
        Get event distribution by hour of day.
        
        Args:
            start_date: Optional start date filter
            end_date: Optional end date filter
        """
        if start_date and end_date:
            query = """
                SELECT 
                    CAST(strftime('%H', timestamp) AS INTEGER) as hour,
                    COUNT(*) as event_count
                FROM events
                WHERE timestamp >= ? AND timestamp <= ?
                GROUP BY hour
                ORDER BY hour
            """
            params = (start_date, end_date)
        else:
            query = """
                SELECT 
                    CAST(strftime('%H', timestamp) AS INTEGER) as hour,
                    COUNT(*) as event_count
                FROM events
                GROUP BY hour
                ORDER BY hour
            """
            params = ()
        
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]
    
    def get_daily_distribution(
        self, 
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> List[Dict[str, Any]]:
        """
        Get event distribution by day.
        
        Args:
            start_date: Optional start date filter
            end_date: Optional end date filter
        """
        if start_date and end_date:
            query = """
                SELECT 
                    DATE(timestamp) as date,
                    COUNT(*) as event_count
                FROM events
                WHERE timestamp >= ? AND timestamp <= ?
                GROUP BY date
                ORDER BY date
            """
            params = (start_date, end_date)
        else:
            query = """
                SELECT 
                    DATE(timestamp) as date,
                    COUNT(*) as event_count
                FROM events
                GROUP BY date
                ORDER BY date
            """
            params = ()
        
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]
