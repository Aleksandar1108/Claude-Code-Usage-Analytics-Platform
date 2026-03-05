"""Pattern analytics for usage patterns and peak times."""

import pandas as pd
from datetime import datetime
from typing import Dict, List, Optional, Any
from src.storage.database import Database
from src.dal.repositories.event_repository import EventRepository
from src.dal.repositories.tool_repository import ToolRepository
from src.dal.repositories.api_request_repository import APIRequestRepository
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


class PatternAnalytics:
    """Analytics for usage patterns."""
    
    def __init__(self, db: Database):
        """
        Initialize pattern analytics.
        
        Args:
            db: Database instance
        """
        self.db = db
        self.event_repo = EventRepository(db)
        self.tool_repo = ToolRepository(db)
        self.api_repo = APIRequestRepository(db)
    
    def get_peak_usage_hours(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> pd.DataFrame:
        """
        Get peak usage hours (hourly distribution).
        
        Args:
            start_date: Optional start date filter
            end_date: Optional end date filter
        
        Returns:
            DataFrame with hourly event distribution
        """
        hourly_data = self.event_repo.get_hourly_distribution(start_date, end_date)
        
        if not hourly_data:
            return pd.DataFrame(columns=["hour", "event_count"])
        
        df = pd.DataFrame(hourly_data)
        df = df.sort_values("hour")
        
        return df
    
    def get_daily_usage_pattern(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> pd.DataFrame:
        """
        Get daily usage pattern.
        
        Args:
            start_date: Optional start date filter
            end_date: Optional end date filter
        
        Returns:
            DataFrame with daily event distribution
        """
        daily_data = self.event_repo.get_daily_distribution(start_date, end_date)
        
        if not daily_data:
            return pd.DataFrame(columns=["date", "event_count"])
        
        df = pd.DataFrame(daily_data)
        df["date"] = pd.to_datetime(df["date"])
        df = df.sort_values("date")
        
        return df
    
    def get_tool_usage_patterns(self) -> pd.DataFrame:
        """
        Get tool usage patterns and statistics.
        
        Returns:
            DataFrame with tool usage statistics
        """
        tool_stats = self.tool_repo.get_tool_usage_statistics()
        
        if not tool_stats:
            return pd.DataFrame()
        
        df = pd.DataFrame(tool_stats)
        return df
    
    def get_tool_decision_patterns(self) -> pd.DataFrame:
        """
        Get tool decision patterns.
        
        Returns:
            DataFrame with tool decision statistics
        """
        decision_stats = self.tool_repo.get_tool_decision_statistics()
        
        if not decision_stats:
            return pd.DataFrame()
        
        df = pd.DataFrame(decision_stats)
        return df
    
    def get_model_usage_patterns(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> pd.DataFrame:
        """
        Get model usage patterns.
        
        Args:
            start_date: Optional start date filter
            end_date: Optional end date filter
        
        Returns:
            DataFrame with model usage statistics
        """
        model_stats = self.api_repo.get_by_model_statistics()
        
        if not model_stats:
            return pd.DataFrame()
        
        df = pd.DataFrame(model_stats)
        
        # Filter by date if provided
        if start_date or end_date:
            all_requests = self.api_repo.get_all()
            request_df = pd.DataFrame(all_requests)
            
            if not request_df.empty:
                # Handle ISO8601 timestamp parsing safely
                request_df["timestamp"] = pd.to_datetime(request_df["timestamp"], format='ISO8601', errors='coerce')
                request_df = request_df[request_df["timestamp"].notna()]  # Remove rows with invalid dates
                
                # Handle timezone-aware comparison
                if start_date and not request_df.empty:
                    # Convert timezone-aware timestamps to timezone-naive for comparison
                    if request_df["timestamp"].dt.tz is not None:
                        request_df["timestamp"] = request_df["timestamp"].dt.tz_localize(None)
                    request_df = request_df[request_df["timestamp"] >= start_date]
                if end_date and not request_df.empty:
                    # Ensure timestamps are timezone-naive for comparison
                    if request_df["timestamp"].dt.tz is not None:
                        request_df["timestamp"] = request_df["timestamp"].dt.tz_localize(None)
                    request_df = request_df[request_df["timestamp"] <= end_date]
                
                # Recalculate stats for filtered data
                filtered_stats = request_df.groupby("model").agg({
                    "cost_usd": ["sum", "mean", "count"],
                    "input_tokens": "sum",
                    "output_tokens": "sum",
                }).reset_index()
                
                filtered_stats.columns = [
                    "model",
                    "total_cost_usd",
                    "avg_cost_per_request",
                    "request_count",
                    "total_input_tokens",
                    "total_output_tokens",
                ]
                
                df = filtered_stats.sort_values("total_cost_usd", ascending=False)
        
        return df
    
    def get_weekday_pattern(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> pd.DataFrame:
        """
        Get usage pattern by day of week.
        
        Args:
            start_date: Optional start date filter
            end_date: Optional end date filter
        
        Returns:
            DataFrame with weekday distribution
        """
        if start_date and end_date:
            events = self.event_repo.get_by_date_range(start_date, end_date)
        else:
            # Get all events (we'll filter by timestamp in pandas)
            events = []
            # We need to get events differently - let's use a direct query
            with self.db.get_connection() as conn:
                cursor = conn.cursor()
                if start_date and end_date:
                    query = """
                        SELECT timestamp FROM events
                        WHERE timestamp >= ? AND timestamp <= ?
                    """
                    cursor.execute(query, (start_date, end_date))
                else:
                    query = "SELECT timestamp FROM events"
                    cursor.execute(query)
                
                events = [{"timestamp": row["timestamp"]} for row in cursor.fetchall()]
        
        if not events:
            return pd.DataFrame()
        
        df = pd.DataFrame(events)
        # Handle ISO8601 timestamp parsing safely
        df["timestamp"] = pd.to_datetime(df["timestamp"], format='ISO8601', errors='coerce')
        df = df[df["timestamp"].notna()]  # Remove rows with invalid dates
        df["weekday"] = df["timestamp"].dt.day_name()
        df["weekday_num"] = df["timestamp"].dt.dayofweek
        
        result = df.groupby(["weekday", "weekday_num"]).size().reset_index(name="event_count")
        result = result.sort_values("weekday_num")
        result = result.drop(columns=["weekday_num"])
        
        return result
    
    def get_event_type_distribution(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> pd.DataFrame:
        """
        Get distribution of event types.
        
        Args:
            start_date: Optional start date filter
            end_date: Optional end date filter
        
        Returns:
            DataFrame with event type distribution
        """
        if start_date and end_date:
            events = self.event_repo.get_by_date_range(start_date, end_date)
        else:
            event_counts = self.event_repo.get_event_counts_by_type()
            return pd.DataFrame(event_counts)
        
        if not events:
            return pd.DataFrame()
        
        df = pd.DataFrame(events)
        result = df.groupby("event_type").size().reset_index(name="count")
        result = result.sort_values("count", ascending=False)
        
        return result
