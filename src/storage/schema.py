"""Database schema definitions and initialization."""

import sqlite3
from typing import Optional
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


def create_schema(conn: sqlite3.Connection):
    """
    Create all database tables and indexes.
    
    Args:
        conn: SQLite database connection
    """
    cursor = conn.cursor()
    
    # Enable foreign keys
    cursor.execute("PRAGMA foreign_keys = ON")
    
    # Users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id TEXT PRIMARY KEY,
            account_uuid TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            org_id TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Employees table (HR metadata)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS employees (
            email TEXT PRIMARY KEY,
            full_name TEXT NOT NULL,
            practice TEXT NOT NULL,
            level TEXT NOT NULL,
            location TEXT NOT NULL,
            FOREIGN KEY (email) REFERENCES users(email)
        )
    """)
    
    # Organizations table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS organizations (
            org_id TEXT PRIMARY KEY,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Sessions table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sessions (
            session_id TEXT PRIMARY KEY,
            user_id TEXT NOT NULL,
            org_id TEXT NOT NULL,
            start_time TIMESTAMP NOT NULL,
            end_time TIMESTAMP,
            duration_seconds INTEGER,
            terminal_type TEXT,
            hostname TEXT,
            os_type TEXT,
            os_version TEXT,
            claude_version TEXT,
            FOREIGN KEY (user_id) REFERENCES users(user_id),
            FOREIGN KEY (org_id) REFERENCES organizations(org_id)
        )
    """)
    
    # Events table (unified event storage)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS events (
            event_id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_type TEXT NOT NULL,
            session_id TEXT NOT NULL,
            user_id TEXT NOT NULL,
            org_id TEXT NOT NULL,
            timestamp TIMESTAMP NOT NULL,
            terminal_type TEXT,
            event_data TEXT NOT NULL,
            FOREIGN KEY (session_id) REFERENCES sessions(session_id),
            FOREIGN KEY (user_id) REFERENCES users(user_id),
            FOREIGN KEY (org_id) REFERENCES organizations(org_id)
        )
    """)
    
    # API Requests (denormalized for fast analytics)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS api_requests (
            event_id INTEGER PRIMARY KEY,
            session_id TEXT NOT NULL,
            user_id TEXT NOT NULL,
            timestamp TIMESTAMP NOT NULL,
            model TEXT NOT NULL,
            input_tokens INTEGER,
            output_tokens INTEGER,
            cache_read_tokens INTEGER,
            cache_creation_tokens INTEGER,
            cost_usd REAL,
            duration_ms INTEGER,
            FOREIGN KEY (session_id) REFERENCES sessions(session_id),
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )
    """)
    
    # Tool Decisions
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tool_decisions (
            event_id INTEGER PRIMARY KEY,
            session_id TEXT NOT NULL,
            user_id TEXT NOT NULL,
            timestamp TIMESTAMP NOT NULL,
            tool_name TEXT NOT NULL,
            decision TEXT NOT NULL,
            source TEXT NOT NULL,
            FOREIGN KEY (session_id) REFERENCES sessions(session_id),
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )
    """)
    
    # Tool Results
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tool_results (
            event_id INTEGER PRIMARY KEY,
            session_id TEXT NOT NULL,
            user_id TEXT NOT NULL,
            timestamp TIMESTAMP NOT NULL,
            tool_name TEXT NOT NULL,
            success INTEGER NOT NULL,
            duration_ms INTEGER,
            result_size_bytes INTEGER,
            FOREIGN KEY (session_id) REFERENCES sessions(session_id),
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )
    """)
    
    # User Prompts
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_prompts (
            event_id INTEGER PRIMARY KEY,
            session_id TEXT NOT NULL,
            user_id TEXT NOT NULL,
            timestamp TIMESTAMP NOT NULL,
            prompt_length INTEGER,
            FOREIGN KEY (session_id) REFERENCES sessions(session_id),
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )
    """)
    
    # API Errors
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS api_errors (
            event_id INTEGER PRIMARY KEY,
            session_id TEXT NOT NULL,
            user_id TEXT NOT NULL,
            timestamp TIMESTAMP NOT NULL,
            model TEXT,
            error_message TEXT,
            status_code TEXT,
            attempt INTEGER,
            duration_ms INTEGER,
            FOREIGN KEY (session_id) REFERENCES sessions(session_id),
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )
    """)
    
    # Create indexes for performance
    indexes = [
        "CREATE INDEX IF NOT EXISTS idx_events_session_id ON events(session_id)",
        "CREATE INDEX IF NOT EXISTS idx_events_user_id ON events(user_id)",
        "CREATE INDEX IF NOT EXISTS idx_events_timestamp ON events(timestamp)",
        "CREATE INDEX IF NOT EXISTS idx_events_type ON events(event_type)",
        "CREATE INDEX IF NOT EXISTS idx_api_requests_timestamp ON api_requests(timestamp)",
        "CREATE INDEX IF NOT EXISTS idx_api_requests_model ON api_requests(model)",
        "CREATE INDEX IF NOT EXISTS idx_api_requests_user_id ON api_requests(user_id)",
        "CREATE INDEX IF NOT EXISTS idx_tool_decisions_tool_name ON tool_decisions(tool_name)",
        "CREATE INDEX IF NOT EXISTS idx_tool_results_tool_name ON tool_results(tool_name)",
        "CREATE INDEX IF NOT EXISTS idx_sessions_user_id ON sessions(user_id)",
        "CREATE INDEX IF NOT EXISTS idx_sessions_start_time ON sessions(start_time)",
        "CREATE INDEX IF NOT EXISTS idx_users_email ON users(email)",
        "CREATE INDEX IF NOT EXISTS idx_users_org_id ON users(org_id)",
    ]
    
    for index_sql in indexes:
        cursor.execute(index_sql)
    
    conn.commit()
    logger.info("Database schema created successfully")


def drop_schema(conn: sqlite3.Connection):
    """
    Drop all database tables (use with caution!).
    
    Args:
        conn: SQLite database connection
    """
    cursor = conn.cursor()
    
    tables = [
        "api_errors",
        "user_prompts",
        "tool_results",
        "tool_decisions",
        "api_requests",
        "events",
        "sessions",
        "employees",
        "users",
        "organizations",
    ]
    
    for table in tables:
        cursor.execute(f"DROP TABLE IF EXISTS {table}")
    
    conn.commit()
    logger.warning("All database tables dropped")
