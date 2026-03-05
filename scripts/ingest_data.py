"""Data ingestion script for telemetry logs and employee data."""

import argparse
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.storage.database import Database
from src.ingestion.ingestor import DataIngestor
from src.utils.config import Config
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


def main():
    parser = argparse.ArgumentParser(description="Ingest telemetry and employee data")
    parser.add_argument(
        "--telemetry",
        type=str,
        required=True,
        help="Path to telemetry_logs.jsonl file"
    )
    parser.add_argument(
        "--employees",
        type=str,
        required=True,
        help="Path to employees.csv file"
    )
    parser.add_argument(
        "--db-path",
        type=str,
        help="Path to database file (default: data/database/analytics.db)"
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=1000,
        help="Batch size for processing events (default: 1000)"
    )
    parser.add_argument(
        "--skip-employees",
        action="store_true",
        help="Skip employee data ingestion"
    )
    parser.add_argument(
        "--skip-telemetry",
        action="store_true",
        help="Skip telemetry data ingestion"
    )
    args = parser.parse_args()
    
    # Setup directories
    Config.setup_directories()
    
    # Initialize database
    db_path = Path(args.db_path) if args.db_path else None
    db = Database(db_path)
    
    # Ensure database is initialized
    logger.info("Ensuring database schema exists...")
    db.initialize(drop_existing=False)
    
    # Create ingestor
    ingestor = DataIngestor(db)
    
    # Ingest employees
    if not args.skip_employees:
        employees_path = Path(args.employees)
        if not employees_path.exists():
            logger.error(f"Employees file not found: {employees_path}")
            return
        
        logger.info("Ingesting employee data...")
        ingestor.ingest_employees(employees_path, batch_size=100)
        logger.info("Employee data ingestion complete!")
    
    # Ingest telemetry
    if not args.skip_telemetry:
        telemetry_path = Path(args.telemetry)
        if not telemetry_path.exists():
            logger.error(f"Telemetry file not found: {telemetry_path}")
            return
        
        logger.info("Ingesting telemetry data...")
        ingestor.ingest_telemetry(telemetry_path, batch_size=args.batch_size)
        logger.info("Telemetry data ingestion complete!")
    
    logger.info("Data ingestion completed successfully!")


if __name__ == "__main__":
    main()
