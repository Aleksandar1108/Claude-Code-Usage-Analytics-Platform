"""Initialize the database schema."""

import argparse
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.storage.database import Database
from src.utils.config import Config
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


def main():
    parser = argparse.ArgumentParser(description="Initialize database schema")
    parser.add_argument(
        "--drop-existing",
        action="store_true",
        help="Drop existing tables before creating (WARNING: This will delete all data!)"
    )
    parser.add_argument(
        "--db-path",
        type=str,
        help="Path to database file (default: data/database/analytics.db)"
    )
    args = parser.parse_args()
    
    # Setup directories
    Config.setup_directories()
    
    # Initialize database
    db_path = Path(args.db_path) if args.db_path else None
    db = Database(db_path)
    
    if args.drop_existing:
        response = input("WARNING: This will delete all existing data. Continue? (yes/no): ")
        if response.lower() != "yes":
            logger.info("Aborted.")
            return
    
    logger.info("Initializing database schema...")
    db.initialize(drop_existing=args.drop_existing)
    logger.info("Database schema initialized successfully!")


if __name__ == "__main__":
    main()
