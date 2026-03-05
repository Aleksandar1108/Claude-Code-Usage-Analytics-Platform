"""User repository for data access."""

from typing import List, Optional, Dict, Any
from src.storage.database import Database
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


class UserRepository:
    """Repository for user data access."""
    
    def __init__(self, db: Database):
        """
        Initialize user repository.
        
        Args:
            db: Database instance
        """
        self.db = db
    
    def get_all(self) -> List[Dict[str, Any]]:
        """Get all users."""
        query = "SELECT * FROM users ORDER BY created_at"
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            return [dict(row) for row in cursor.fetchall()]
    
    def get_by_id(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get user by ID."""
        query = "SELECT * FROM users WHERE user_id = ?"
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (user_id,))
            row = cursor.fetchone()
            return dict(row) if row else None
    
    def get_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """Get user by email."""
        query = "SELECT * FROM users WHERE email = ?"
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (email,))
            row = cursor.fetchone()
            return dict(row) if row else None
    
    def get_with_employee_info(self, user_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get users with employee information.
        
        Args:
            user_id: Optional user ID to filter by
        
        Returns:
            List of users with employee data
        """
        if user_id:
            query = """
                SELECT u.*, e.full_name, e.practice, e.level, e.location
                FROM users u
                LEFT JOIN employees e ON u.email = e.email
                WHERE u.user_id = ?
            """
            params = (user_id,)
        else:
            query = """
                SELECT u.*, e.full_name, e.practice, e.level, e.location
                FROM users u
                LEFT JOIN employees e ON u.email = e.email
                ORDER BY u.created_at
            """
            params = ()
        
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]
    
    def count(self) -> int:
        """Get total user count."""
        query = "SELECT COUNT(*) as count FROM users"
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            return cursor.fetchone()["count"]
