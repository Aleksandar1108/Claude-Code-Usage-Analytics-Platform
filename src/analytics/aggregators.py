"""Aggregator utilities for common data operations."""

import pandas as pd
import numpy as np
from datetime import datetime
from typing import Dict, List, Optional, Any, Callable
from src.storage.database import Database
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


class Aggregators:
    """Utility class for common aggregation operations."""
    
    @staticmethod
    def group_by_time_period(
        df: pd.DataFrame,
        date_column: str,
        period: str = "day"
    ) -> pd.DataFrame:
        """
        Group DataFrame by time period.
        
        Args:
            df: Input DataFrame
            date_column: Name of date column
            period: Time period ('day', 'week', 'month', 'hour')
        
        Returns:
            Grouped DataFrame
        """
        if df.empty or date_column not in df.columns:
            return pd.DataFrame()
        
        df = df.copy()
        df[date_column] = pd.to_datetime(df[date_column])
        
        if period == "hour":
            df["period"] = df[date_column].dt.floor("H")
        elif period == "day":
            df["period"] = df[date_column].dt.date
        elif period == "week":
            df["period"] = df[date_column].dt.to_period("W").dt.start_time
        elif period == "month":
            df["period"] = df[date_column].dt.to_period("M").dt.start_time
        else:
            return df
        
        return df.groupby("period")
    
    @staticmethod
    def calculate_percentages(df: pd.DataFrame, column: str) -> pd.DataFrame:
        """
        Calculate percentages for a column.
        
        Args:
            df: Input DataFrame
            column: Column name to calculate percentages for
        
        Returns:
            DataFrame with percentage column added
        """
        if df.empty or column not in df.columns:
            return df
        
        df = df.copy()
        total = df[column].sum()
        
        if total > 0:
            df[f"{column}_pct"] = (df[column] / total) * 100
        else:
            df[f"{column}_pct"] = 0.0
        
        return df
    
    @staticmethod
    def top_n(df: pd.DataFrame, column: str, n: int = 10) -> pd.DataFrame:
        """
        Get top N rows by column value.
        
        Args:
            df: Input DataFrame
            column: Column to sort by
            n: Number of top rows to return
        
        Returns:
            Top N rows DataFrame
        """
        if df.empty or column not in df.columns:
            return df
        
        return df.nlargest(n, column)
    
    @staticmethod
    def calculate_statistics(df: pd.DataFrame, column: str) -> Dict[str, float]:
        """
        Calculate basic statistics for a column.
        
        Args:
            df: Input DataFrame
            column: Column name
        
        Returns:
            Dictionary with statistics
        """
        if df.empty or column not in df.columns:
            return {
                "count": 0,
                "mean": 0.0,
                "median": 0.0,
                "std": 0.0,
                "min": 0.0,
                "max": 0.0,
            }
        
        return {
            "count": int(df[column].count()),
            "mean": float(df[column].mean() or 0),
            "median": float(df[column].median() or 0),
            "std": float(df[column].std() or 0),
            "min": float(df[column].min() or 0),
            "max": float(df[column].max() or 0),
        }
    
    @staticmethod
    def fill_date_gaps(
        df: pd.DataFrame,
        date_column: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> pd.DataFrame:
        """
        Fill gaps in date series with zero values.
        
        Args:
            df: Input DataFrame
            date_column: Name of date column
            start_date: Start date (if None, uses min date from df)
            end_date: End date (if None, uses max date from df)
        
        Returns:
            DataFrame with filled date gaps
        """
        if df.empty or date_column not in df.columns:
            return df
        
        df = df.copy()
        df[date_column] = pd.to_datetime(df[date_column])
        
        if start_date is None:
            start_date = df[date_column].min()
        if end_date is None:
            end_date = df[date_column].max()
        
        # Create complete date range
        date_range = pd.date_range(start=start_date, end=end_date, freq="D")
        date_df = pd.DataFrame({date_column: date_range})
        
        # Merge with original data
        result = date_df.merge(df, on=date_column, how="left")
        
        # Fill numeric columns with 0
        numeric_columns = result.select_dtypes(include=[np.number]).columns
        result[numeric_columns] = result[numeric_columns].fillna(0)
        
        return result
