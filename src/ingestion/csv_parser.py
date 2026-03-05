"""CSV employee metadata parser."""

import csv
from pathlib import Path
from typing import Dict, Iterator, List, Optional
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


class CSVParser:
    """Parser for CSV employee metadata files."""
    
    def __init__(self):
        self.stats = {
            "rows_processed": 0,
            "rows_valid": 0,
            "rows_invalid": 0,
            "errors": [],
        }
    
    def parse_file(self, file_path: Path) -> Iterator[Dict[str, str]]:
        """
        Parse CSV file and yield employee records.
        
        Args:
            file_path: Path to CSV file
        
        Yields:
            Employee record dictionaries
        """
        if not file_path.exists():
            raise FileNotFoundError(f"Employee CSV file not found: {file_path}")
        
        logger.info(f"Parsing employee CSV file: {file_path}")
        
        required_columns = ["email", "full_name", "practice", "level", "location"]
        
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            
            # Validate header
            if not reader.fieldnames:
                raise ValueError("CSV file is empty or has no header")
            
            missing_columns = set(required_columns) - set(reader.fieldnames)
            if missing_columns:
                raise ValueError(f"Missing required columns: {missing_columns}")
            
            for row_num, row in enumerate(reader, 2):  # Start at 2 (header is row 1)
                self.stats["rows_processed"] += 1
                
                # Validate required fields
                is_valid = True
                for col in required_columns:
                    if not row.get(col) or not row[col].strip():
                        error_msg = f"Row {row_num}: Missing or empty {col}"
                        logger.warning(error_msg)
                        self.stats["rows_invalid"] += 1
                        self.stats["errors"].append(error_msg)
                        is_valid = False
                        break
                
                if not is_valid:
                    continue
                
                # Clean and yield record
                record = {
                    "email": row["email"].strip().lower(),
                    "full_name": row["full_name"].strip(),
                    "practice": row["practice"].strip(),
                    "level": row["level"].strip(),
                    "location": row["location"].strip(),
                }
                
                self.stats["rows_valid"] += 1
                yield record
        
        logger.info(f"CSV parsing complete. Valid: {self.stats['rows_valid']}, Invalid: {self.stats['rows_invalid']}")
    
    def get_stats(self) -> Dict[str, any]:
        """Get parsing statistics."""
        return self.stats.copy()
