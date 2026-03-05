"""Database connection and management."""

import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Optional
from src.utils.config import Config
from src.utils.logger import setup_logger
from src.storage.schema import create_schema

logger = setup_logger(__name__)


class Database:
    """Database connection manager."""
    
    def __init__(self, db_path: Optional[Path] = None):
        """
        Initialize database connection.
        
        Args:
            db_path: Path to SQLite database file. If None, uses Config.DATABASE_PATH
        """
        self.db_path = db_path or Config.DATABASE_PATH
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._conn: Optional[sqlite3.Connection] = None
    
    @contextmanager
    def get_connection(self):
        """
        Get database connection as context manager.
        
        Yields:
            SQLite connection object
        """
        conn = sqlite3.connect(str(self.db_path))
        conn.row_factory = sqlite3.Row  # Enable column access by name
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            logger.error(f"Database error: {e}")
            raise
        finally:
            conn.close()
    
    def initialize(self, drop_existing: bool = False):
        """
        Initialize database schema.
        
        Args:
            drop_existing: If True, drop existing tables before creating
        """
        with self.get_connection() as conn:
            if drop_existing:
                from src.storage.schema import drop_schema
                drop_schema(conn)
            create_schema(conn)
            logger.info(f"Database initialized at {self.db_path}")
    
    def execute(self, query: str, params: tuple = ()):
        """
        Execute a single query.
        
        Args:
            query: SQL query string
            params: Query parameters
        
        Returns:
            Query result
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            return cursor.fetchall()
    
    def executemany(self, query: str, params_list: list):
        """
        Execute a query multiple times with different parameters.
        
        Args:
            query: SQL query string
            params_list: List of parameter tuples
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.executemany(query, params_list)
            logger.debug(f"Executed {len(params_list)} insertions")
