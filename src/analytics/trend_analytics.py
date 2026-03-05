"""Trend analytics for time-series analysis."""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from src.storage.database import Database
from src.dal.repositories.api_request_repository import APIRequestRepository
from src.dal.repositories.session_repository import SessionRepository
from src.dal.repositories.event_repository import EventRepository
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


class TrendAnalytics:
    """Analytics for trend analysis."""
    
    def __init__(self, db: Database):
        """
        Initialize trend analytics.
        
        Args:
            db: Database instance
        """
        self.db = db
        self.api_repo = APIRequestRepository(db)
        self.session_repo = SessionRepository(db)
        self.event_repo = EventRepository(db)
    
    def get_daily_trends(
        self,
        metric: str = "events",
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> pd.DataFrame:
        """
        Get daily trends for specified metric.
        
        Args:
            metric: Metric to track ('events', 'sessions', 'cost', 'tokens')
            start_date: Optional start date filter
            end_date: Optional end date filter
        
        Returns:
            DataFrame with daily trends
        """
        if metric == "events":
            if start_date and end_date:
                events = self.event_repo.get_by_date_range(start_date, end_date)
            else:
                daily_data = self.event_repo.get_daily_distribution()
                if daily_data:
                    df = pd.DataFrame(daily_data)
                    df["date"] = pd.to_datetime(df["date"])
                    # Normalize column name to 'count' for consistency
                    if "event_count" in df.columns:
                        df = df.rename(columns={"event_count": "count"})
                    elif "count" not in df.columns and len(df.columns) > 1:
                        # If no count column, rename the last numeric column to 'count'
                        df = df.rename(columns={df.columns[-1]: "count"})
                    return df
                return pd.DataFrame()
            
            if not events:
                return pd.DataFrame()
            
            df = pd.DataFrame(events)
            # Handle ISO8601 timestamp parsing safely
            df["date"] = pd.to_datetime(df["timestamp"], format='ISO8601', errors='coerce').dt.date
            df = df[df["date"].notna()]  # Remove rows with invalid dates
            result = df.groupby("date").size().reset_index(name="count")
            result["date"] = pd.to_datetime(result["date"])
            return result
        
        elif metric == "sessions":
            if start_date and end_date:
                sessions = self.session_repo.get_by_date_range(start_date, end_date)
            else:
                sessions = self.session_repo.get_all()
            
            if not sessions:
                return pd.DataFrame()
            
            df = pd.DataFrame(sessions)
            # Handle ISO8601 timestamp parsing safely
            df["date"] = pd.to_datetime(df["start_time"], format='ISO8601', errors='coerce').dt.date
            df = df[df["date"].notna()]  # Remove rows with invalid dates
            result = df.groupby("date").size().reset_index(name="count")
            result["date"] = pd.to_datetime(result["date"])
            return result
        
        elif metric == "cost":
            if start_date and end_date:
                requests = self.api_repo.get_by_date_range(start_date, end_date)
            else:
                requests = self.api_repo.get_all()
            
            if not requests:
                return pd.DataFrame()
            
            df = pd.DataFrame(requests)
            # Handle ISO8601 timestamp parsing safely
            df["date"] = pd.to_datetime(df["timestamp"], format='ISO8601', errors='coerce').dt.date
            df = df[df["date"].notna()]  # Remove rows with invalid dates
            result = df.groupby("date")["cost_usd"].sum().reset_index(name="count")
            result["date"] = pd.to_datetime(result["date"])
            return result
        
        elif metric == "tokens":
            if start_date and end_date:
                requests = self.api_repo.get_by_date_range(start_date, end_date)
            else:
                requests = self.api_repo.get_all()
            
            if not requests:
                return pd.DataFrame()
            
            df = pd.DataFrame(requests)
            # Handle ISO8601 timestamp parsing safely
            df["date"] = pd.to_datetime(df["timestamp"], format='ISO8601', errors='coerce').dt.date
            df = df[df["date"].notna()]  # Remove rows with invalid dates
            df["total_tokens"] = (
                df["input_tokens"] + 
                df["output_tokens"] + 
                df["cache_read_tokens"] + 
                df["cache_creation_tokens"]
            )
            result = df.groupby("date")["total_tokens"].sum().reset_index(name="count")
            result["date"] = pd.to_datetime(result["date"])
            return result
        
        return pd.DataFrame()
    
    def get_weekly_trends(
        self,
        metric: str = "events",
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> pd.DataFrame:
        """
        Get weekly trends for specified metric.
        
        Args:
            metric: Metric to track ('events', 'sessions', 'cost', 'tokens')
            start_date: Optional start date filter
            end_date: Optional end date filter
        
        Returns:
            DataFrame with weekly trends
        """
        daily_df = self.get_daily_trends(metric, start_date, end_date)
        
        if daily_df.empty:
            return pd.DataFrame()
        
        # Get the count column (it might be named 'count' or 'event_count' depending on source)
        count_col = 'count' if 'count' in daily_df.columns else daily_df.columns[-1]
        
        daily_df["week"] = daily_df["date"].dt.to_period("W").dt.start_time
        result = daily_df.groupby("week")[count_col].sum().reset_index()
        result = result.rename(columns={"week": "date", count_col: "count"})
        
        return result
    
    def get_monthly_trends(
        self,
        metric: str = "events",
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> pd.DataFrame:
        """
        Get monthly trends for specified metric.
        
        Args:
            metric: Metric to track ('events', 'sessions', 'cost', 'tokens')
            start_date: Optional start date filter
            end_date: Optional end date filter
        
        Returns:
            DataFrame with monthly trends
        """
        daily_df = self.get_daily_trends(metric, start_date, end_date)
        
        if daily_df.empty:
            return pd.DataFrame()
        
        # Get the count column (it might be named 'count' or 'event_count' depending on source)
        count_col = 'count' if 'count' in daily_df.columns else daily_df.columns[-1]
        
        daily_df["month"] = daily_df["date"].dt.to_period("M").dt.start_time
        result = daily_df.groupby("month")[count_col].sum().reset_index()
        result = result.rename(columns={"month": "date", count_col: "count"})
        
        return result
    
    def calculate_growth_rate(self, df: pd.DataFrame, period: int = 7) -> float:
        """
        Calculate growth rate over specified period.
        
        Args:
            df: DataFrame with date and count columns
            period: Number of days to compare
        
        Returns:
            Growth rate as percentage
        """
        if df.empty or len(df) < period:
            return 0.0
        
        # Get the count column
        count_col = 'count' if 'count' in df.columns else df.columns[-1]
        
        df = df.sort_values("date")
        recent = df.tail(period)[count_col].sum()
        previous = df.iloc[-(period*2):-period][count_col].sum() if len(df) >= period*2 else df.head(period)[count_col].sum()
        
        if previous == 0:
            return 100.0 if recent > 0 else 0.0
        
        return ((recent - previous) / previous) * 100
    
    def get_trend_summary(
        self,
        metric: str = "events",
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> Dict[str, Any]:
        """
        Get trend summary with growth rates.
        
        Args:
            metric: Metric to track
            start_date: Optional start date filter
            end_date: Optional end date filter
        
        Returns:
            Dictionary with trend summary
        """
        daily_df = self.get_daily_trends(metric, start_date, end_date)
        
        if daily_df.empty:
            return {
                "total": 0,
                "avg_daily": 0,
                "growth_rate_7d": 0,
                "growth_rate_30d": 0,
                "trend": "stable",
            }
        
        # Get the count column (it might be named 'count' or 'event_count' depending on source)
        count_col = 'count' if 'count' in daily_df.columns else daily_df.columns[-1]
        
        total = float(daily_df[count_col].sum())
        avg_daily = float(daily_df[count_col].mean())
        growth_7d = self.calculate_growth_rate(daily_df, 7)
        growth_30d = self.calculate_growth_rate(daily_df, 30)
        
        # Determine trend
        if growth_7d > 5:
            trend = "increasing"
        elif growth_7d < -5:
            trend = "decreasing"
        else:
            trend = "stable"
        
        return {
            "total": total,
            "avg_daily": avg_daily,
            "growth_rate_7d": growth_7d,
            "growth_rate_30d": growth_30d,
            "trend": trend,
            "min_daily": float(daily_df[count_col].min()),
            "max_daily": float(daily_df[count_col].max()),
        }
