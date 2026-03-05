"""Data ingestion script for telemetry logs and employee data."""

import argparse
import sys
import subprocess
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
    
    # Default paths in project output directory
    default_telemetry = project_root / "output" / "telemetry_logs.jsonl"
    default_employees = project_root / "output" / "employees.csv"
    
    parser.add_argument(
        "--telemetry",
        type=str,
        default=str(default_telemetry),
        help=f"Path to telemetry_logs.jsonl file (default: {default_telemetry})"
    )
    parser.add_argument(
        "--employees",
        type=str,
        default=str(default_employees),
        help=f"Path to employees.csv file (default: {default_employees})"
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
    parser.add_argument(
        "--generate-if-missing",
        action="store_true",
        help="Generate sample data if input files are missing"
    )
    parser.add_argument(
        "--data-gen-dir",
        type=str,
        help="Directory containing generate_fake_data.py (default: ../claude_code_telemetry)"
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
    
    # Check if files exist, generate if missing and flag is set
    employees_path = Path(args.employees)
    telemetry_path = Path(args.telemetry)
    
    if args.generate_if_missing:
        # Determine data generation directory
        data_gen_dir = Path(args.data_gen_dir) if args.data_gen_dir else project_root.parent / "claude_code_telemetry"
        generate_script = data_gen_dir / "generate_fake_data.py"
        
        if not employees_path.exists() or not telemetry_path.exists():
            if generate_script.exists():
                logger.info("Input files missing. Generating sample data...")
                try:
                    # Run data generation
                    result = subprocess.run(
                        [sys.executable, str(generate_script), "--num-users", "30", "--num-sessions", "500", "--days", "30"],
                        cwd=str(data_gen_dir),
                        capture_output=True,
                        text=True
                    )
                    if result.returncode == 0:
                        logger.info("Sample data generated successfully")
                        # Update paths to generated files
                        employees_path = data_gen_dir / "output" / "employees.csv"
                        telemetry_path = data_gen_dir / "output" / "telemetry_logs.jsonl"
                    else:
                        logger.error(f"Data generation failed: {result.stderr}")
                        return
                except Exception as e:
                    logger.error(f"Error generating data: {e}")
                    return
            else:
                logger.warning(f"Data generation script not found at {generate_script}")
                logger.warning("Please generate data manually or provide correct file paths")
    
    # Ingest employees
    if not args.skip_employees:
        if not employees_path.exists():
            logger.error(f"Employees file not found: {employees_path}")
            logger.error("Use --generate-if-missing to auto-generate sample data")
            return
        
        logger.info("Ingesting employee data...")
        ingestor.ingest_employees(employees_path, batch_size=100)
        logger.info("Employee data ingestion complete!")
    
    # Ingest telemetry
    if not args.skip_telemetry:
        if not telemetry_path.exists():
            logger.error(f"Telemetry file not found: {telemetry_path}")
            logger.error("Use --generate-if-missing to auto-generate sample data")
            return
        
        logger.info("Ingesting telemetry data...")
        ingestor.ingest_telemetry(telemetry_path, batch_size=args.batch_size)
        logger.info("Telemetry data ingestion complete!")
    
    logger.info("Data ingestion completed successfully!")


if __name__ == "__main__":
    main()
