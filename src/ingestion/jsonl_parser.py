"""JSONL telemetry log parser."""

import json
from pathlib import Path
from typing import Dict, Iterator, List, Any
from src.utils.logger import setup_logger
from src.ingestion.data_validator import DataValidator

logger = setup_logger(__name__)


class JSONLParser:
    """Parser for JSONL telemetry log files."""
    
    def __init__(self, validator: DataValidator = None):
        """
        Initialize JSONL parser.
        
        Args:
            validator: DataValidator instance for validation
        """
        self.validator = validator or DataValidator()
        self.stats = {
            "batches_processed": 0,
            "events_parsed": 0,
            "events_valid": 0,
            "events_invalid": 0,
            "errors": [],
        }
    
    def parse_file(self, file_path: Path) -> Iterator[Dict[str, Any]]:
        """
        Parse JSONL file and yield events.
        
        Args:
            file_path: Path to JSONL file
        
        Yields:
            Parsed event dictionaries
        """
        if not file_path.exists():
            raise FileNotFoundError(f"Telemetry log file not found: {file_path}")
        
        logger.info(f"Parsing telemetry log file: {file_path}")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue
                
                try:
                    # Parse batch
                    batch = json.loads(line)
                    self.stats["batches_processed"] += 1
                    
                    # Extract log events from batch
                    log_events = batch.get("logEvents", [])
                    
                    for log_event in log_events:
                        self.stats["events_parsed"] += 1
                        
                        # Parse event message
                        message_str = log_event.get("message", "")
                        if not message_str:
                            self.stats["events_invalid"] += 1
                            continue
                        
                        try:
                            event = json.loads(message_str)
                        except json.JSONDecodeError as e:
                            error_msg = f"Line {line_num}: Invalid JSON in message: {e}"
                            logger.warning(error_msg)
                            self.stats["events_invalid"] += 1
                            self.stats["errors"].append(error_msg)
                            continue
                        
                        # Validate event
                        is_valid, error_msg = self.validator.validate_event(event)
                        if not is_valid:
                            logger.warning(f"Line {line_num}: Invalid event: {error_msg}")
                            self.stats["events_invalid"] += 1
                            self.stats["errors"].append(f"Line {line_num}: {error_msg}")
                            continue
                        
                        # Add metadata from batch
                        event["_batch_metadata"] = {
                            "log_group": batch.get("logGroup"),
                            "log_stream": batch.get("logStream"),
                            "year": batch.get("year"),
                            "month": batch.get("month"),
                            "day": batch.get("day"),
                        }
                        
                        # Add log event metadata
                        event["_log_event_metadata"] = {
                            "id": log_event.get("id"),
                            "timestamp_ms": log_event.get("timestamp"),
                        }
                        
                        self.stats["events_valid"] += 1
                        yield event
                
                except json.JSONDecodeError as e:
                    error_msg = f"Line {line_num}: Invalid JSON: {e}"
                    logger.warning(error_msg)
                    self.stats["errors"].append(error_msg)
                    continue
                except Exception as e:
                    error_msg = f"Line {line_num}: Unexpected error: {e}"
                    logger.error(error_msg, exc_info=True)
                    self.stats["errors"].append(error_msg)
                    continue
        
        logger.info(f"Parsing complete. Valid: {self.stats['events_valid']}, Invalid: {self.stats['events_invalid']}")
    
    def get_stats(self) -> Dict[str, Any]:
        """Get parsing statistics."""
        return self.stats.copy()
