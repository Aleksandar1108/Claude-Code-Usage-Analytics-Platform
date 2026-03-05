"""Main data ingestion orchestrator."""

import json
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Set
from src.storage.database import Database
from src.ingestion.jsonl_parser import JSONLParser
from src.ingestion.csv_parser import CSVParser
from src.ingestion.data_validator import DataValidator
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


class DataIngestor:
    """Orchestrates data ingestion from telemetry logs and employee CSV."""
    
    def __init__(self, db: Database):
        """
        Initialize data ingestor.
        
        Args:
            db: Database instance
        """
        self.db = db
        self.validator = DataValidator()
        self.jsonl_parser = JSONLParser(self.validator)
        self.csv_parser = CSVParser()
        
        # Track what we've seen to avoid duplicates
        self.seen_users: Set[str] = set()
        self.seen_orgs: Set[str] = set()
        self.seen_sessions: Set[str] = set()
        self.session_info: Dict[str, Dict] = {}  # session_id -> info
    
    def ingest_employees(self, csv_path: Path, batch_size: int = 100):
        """
        Ingest employee data from CSV.
        
        Args:
            csv_path: Path to employees CSV file
            batch_size: Number of records to insert per batch
        """
        logger.info(f"Starting employee data ingestion from {csv_path}")
        
        records = []
        for record in self.csv_parser.parse_file(csv_path):
            records.append((
                record["email"],
                record["full_name"],
                record["practice"],
                record["level"],
                record["location"],
            ))
            
            if len(records) >= batch_size:
                self._insert_employees_batch(records)
                records = []
        
        # Insert remaining records
        if records:
            self._insert_employees_batch(records)
        
        stats = self.csv_parser.get_stats()
        logger.info(f"Employee ingestion complete: {stats['rows_valid']} valid records")
    
    def _insert_employees_batch(self, records: List[tuple]):
        """Insert a batch of employee records."""
        query = """
            INSERT OR REPLACE INTO employees (email, full_name, practice, level, location)
            VALUES (?, ?, ?, ?, ?)
        """
        self.db.executemany(query, records)
    
    def ingest_telemetry(self, jsonl_path: Path, batch_size: int = 1000):
        """
        Ingest telemetry data from JSONL file.
        
        Args:
            jsonl_path: Path to telemetry logs JSONL file
            batch_size: Number of events to process per batch
        """
        logger.info(f"Starting telemetry data ingestion from {jsonl_path}")
        
        events_batch = []
        for event in self.jsonl_parser.parse_file(jsonl_path):
            events_batch.append(event)
            
            if len(events_batch) >= batch_size:
                self._process_events_batch(events_batch)
                events_batch = []
        
        # Process remaining events
        if events_batch:
            self._process_events_batch(events_batch)
        
        # Update session end times
        self._update_session_end_times()
        
        stats = self.jsonl_parser.get_stats()
        logger.info(f"Telemetry ingestion complete: {stats['events_valid']} valid events")
    
    def _process_events_batch(self, events: List[Dict]):
        """Process a batch of events."""
        users_to_insert = []
        orgs_to_insert = []
        sessions_to_insert = []
        events_to_insert = []
        # Track event type for each event
        event_types = []
        
        for event in events:
            try:
                # Extract common attributes
                common = self.validator.extract_common_attributes(event)
                resource = self.validator.extract_resource_info(event)
                
                user_id = common["user_id"]
                email = common["user_email"]
                org_id = common["org_id"]
                session_id = common["session_id"]
                account_uuid = common.get("account_uuid")
                timestamp = self.validator.clean_timestamp(common["timestamp"])
                
                if not timestamp:
                    continue
                
                # Track users
                if user_id not in self.seen_users:
                    users_to_insert.append((
                        user_id,
                        account_uuid or "",
                        email,
                        org_id,
                    ))
                    self.seen_users.add(user_id)
                
                # Track organizations
                if org_id not in self.seen_orgs:
                    orgs_to_insert.append((org_id,))
                    self.seen_orgs.add(org_id)
                
                # Track sessions
                if session_id not in self.seen_sessions:
                    sessions_to_insert.append((
                        session_id,
                        user_id,
                        org_id,
                        timestamp,
                        None,  # end_time (updated later)
                        None,  # duration_seconds
                        common.get("terminal_type"),
                        resource.get("hostname"),
                        resource.get("os_type"),
                        resource.get("os_version"),
                        resource.get("claude_version"),
                    ))
                    self.seen_sessions.add(session_id)
                    self.session_info[session_id] = {
                        "start_time": timestamp,
                        "end_time": timestamp,
                    }
                else:
                    # Update session end time
                    if timestamp > self.session_info[session_id]["end_time"]:
                        self.session_info[session_id]["end_time"] = timestamp
                
                # Prepare event data JSON
                event_data = json.dumps(event)
                
                # Get event type
                body = event.get("body", "")
                event_type = body.replace("claude_code.", "")
                event_types.append(event_type)
                
                # Insert into events table (we'll get the event_id)
                events_to_insert.append((
                    event_type,
                    session_id,
                    user_id,
                    org_id,
                    timestamp,
                    common.get("terminal_type"),
                    event_data,
                ))
            
            except Exception as e:
                logger.error(f"Error processing event: {e}", exc_info=True)
                continue
        
        # Insert in transaction
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            
            # Insert users
            if users_to_insert:
                cursor.executemany(
                    "INSERT OR IGNORE INTO users (user_id, account_uuid, email, org_id) VALUES (?, ?, ?, ?)",
                    users_to_insert
                )
            
            # Insert organizations
            if orgs_to_insert:
                cursor.executemany(
                    "INSERT OR IGNORE INTO organizations (org_id) VALUES (?)",
                    orgs_to_insert
                )
            
            # Insert sessions
            if sessions_to_insert:
                cursor.executemany(
                    """INSERT OR IGNORE INTO sessions 
                       (session_id, user_id, org_id, start_time, end_time, duration_seconds, 
                        terminal_type, hostname, os_type, os_version, claude_version)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                    sessions_to_insert
                )
            
            # Insert events and get event_ids, then insert event-specific data
            for i, event_data in enumerate(events_to_insert):
                cursor.execute(
                    """INSERT INTO events 
                       (event_type, session_id, user_id, org_id, timestamp, terminal_type, event_data)
                       VALUES (?, ?, ?, ?, ?, ?, ?)""",
                    event_data
                )
                event_id = cursor.lastrowid
                event_type = event_types[i]
                
                # Get the original event to extract attributes
                event = json.loads(event_data[6])  # event_data is the JSON string
                attrs = event.get("attributes", {})
                
                # Insert event-specific data based on type
                if event_type == "api_request":
                    cursor.execute(
                        """INSERT INTO api_requests 
                           (event_id, session_id, user_id, timestamp, model, input_tokens, 
                            output_tokens, cache_read_tokens, cache_creation_tokens, cost_usd, duration_ms)
                           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                        (
                            event_id,
                            event_data[1],  # session_id
                            event_data[2],  # user_id
                            event_data[4],  # timestamp
                            attrs.get("model"),
                            self.validator.safe_int(attrs.get("input_tokens")),
                            self.validator.safe_int(attrs.get("output_tokens")),
                            self.validator.safe_int(attrs.get("cache_read_tokens")),
                            self.validator.safe_int(attrs.get("cache_creation_tokens")),
                            self.validator.safe_float(attrs.get("cost_usd")),
                            self.validator.safe_int(attrs.get("duration_ms")),
                        )
                    )
                
                elif event_type == "tool_decision":
                    cursor.execute(
                        """INSERT INTO tool_decisions 
                           (event_id, session_id, user_id, timestamp, tool_name, decision, source)
                           VALUES (?, ?, ?, ?, ?, ?, ?)""",
                        (
                            event_id,
                            event_data[1],
                            event_data[2],
                            event_data[4],
                            attrs.get("tool_name"),
                            attrs.get("decision"),
                            attrs.get("source"),
                        )
                    )
                
                elif event_type == "tool_result":
                    cursor.execute(
                        """INSERT INTO tool_results 
                           (event_id, session_id, user_id, timestamp, tool_name, success, duration_ms, result_size_bytes)
                           VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                        (
                            event_id,
                            event_data[1],
                            event_data[2],
                            event_data[4],
                            attrs.get("tool_name"),
                            1 if self.validator.safe_bool(attrs.get("success")) else 0,
                            self.validator.safe_int(attrs.get("duration_ms")),
                            self.validator.safe_int(attrs.get("tool_result_size_bytes")),
                        )
                    )
                
                elif event_type == "user_prompt":
                    cursor.execute(
                        """INSERT INTO user_prompts 
                           (event_id, session_id, user_id, timestamp, prompt_length)
                           VALUES (?, ?, ?, ?, ?)""",
                        (
                            event_id,
                            event_data[1],
                            event_data[2],
                            event_data[4],
                            self.validator.safe_int(attrs.get("prompt_length")),
                        )
                    )
                
                elif event_type == "api_error":
                    cursor.execute(
                        """INSERT INTO api_errors 
                           (event_id, session_id, user_id, timestamp, model, error_message, status_code, attempt, duration_ms)
                           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                        (
                            event_id,
                            event_data[1],
                            event_data[2],
                            event_data[4],
                            attrs.get("model"),
                            attrs.get("error"),
                            attrs.get("status_code"),
                            self.validator.safe_int(attrs.get("attempt")),
                            self.validator.safe_int(attrs.get("duration_ms")),
                        )
                    )
    
    def _update_session_end_times(self):
        """Update session end times and durations based on events."""
        logger.info("Updating session end times and durations")
        
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            
            for session_id, info in self.session_info.items():
                start_time = info["start_time"]
                end_time = info["end_time"]
                duration = int((end_time - start_time).total_seconds())
                
                cursor.execute(
                    """UPDATE sessions 
                       SET end_time = ?, duration_seconds = ?
                       WHERE session_id = ?""",
                    (end_time, duration, session_id)
                )
        
        logger.info(f"Updated {len(self.session_info)} sessions")
