"""Configuration management for the analytics platform."""

import os
from pathlib import Path
from typing import Optional


class Config:
    """Application configuration."""
    
    # Project root directory
    PROJECT_ROOT = Path(__file__).parent.parent.parent
    
    # Data directories
    DATA_DIR = PROJECT_ROOT / "data"
    RAW_DATA_DIR = DATA_DIR / "raw"
    PROCESSED_DATA_DIR = DATA_DIR / "processed"
    DATABASE_DIR = DATA_DIR / "database"
    
    # Database configuration
    DATABASE_PATH = DATABASE_DIR / "analytics.db"
    
    # Input file paths (can be overridden)
    TELEMETRY_LOGS_PATH: Optional[Path] = None
    EMPLOYEES_CSV_PATH: Optional[Path] = None
    
    # Logging configuration
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE = PROJECT_ROOT / "logs" / "analytics.log"
    
    @classmethod
    def setup_directories(cls):
        """Create necessary directories if they don't exist."""
        cls.DATA_DIR.mkdir(exist_ok=True)
        cls.RAW_DATA_DIR.mkdir(exist_ok=True)
        cls.PROCESSED_DATA_DIR.mkdir(exist_ok=True)
        cls.DATABASE_DIR.mkdir(exist_ok=True)
        (cls.PROJECT_ROOT / "logs").mkdir(exist_ok=True)
    
    @classmethod
    def set_input_paths(cls, telemetry_path: Optional[str] = None, employees_path: Optional[str] = None):
        """Set input file paths."""
        if telemetry_path:
            cls.TELEMETRY_LOGS_PATH = Path(telemetry_path)
        if employees_path:
            cls.EMPLOYEES_CSV_PATH = Path(employees_path)
