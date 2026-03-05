"""Usage analytics for token consumption and session metrics."""

import pandas as pd
from datetime import datetime
from typing import Dict, List, Optional, Any
from src.storage.database import Database
from src.dal.repositories.api_request_repository import APIRequestRepository
from src.dal.repositories.session_repository import SessionRepository
from src.dal.repositories.user_repository import UserRepository
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


class UsageAnalytics:
    """Analytics for usage metrics."""
    
    def __init__(self, db: Database):
        """
        Initialize usage analytics.
        
        Args:
            db: Database instance
        """
        self.db = db
        self.api_repo = APIRequestRepository(db)
        self.session_repo = SessionRepository(db)
        self.user_repo = UserRepository(db)
    
    def get_token_consumption_summary(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> Dict[str, Any]:
        """
        Get overall token consumption summary.
        
        Args:
            start_date: Optional start date filter
            end_date: Optional end date filter
        
        Returns:
            Dictionary with token consumption metrics
        """
        if start_date and end_date:
            requests = self.api_repo.get_by_date_range(start_date, end_date)
        else:
            requests = self.api_repo.get_all()
        
        if not requests:
            return {
                "total_input_tokens": 0,
                "total_output_tokens": 0,
                "total_cache_read_tokens": 0,
                "total_cache_creation_tokens": 0,
                "total_tokens": 0,
                "avg_input_tokens": 0,
                "avg_output_tokens": 0,
            }
        
        df = pd.DataFrame(requests)
        
        total_input = int(df["input_tokens"].sum() or 0)
        total_output = int(df["output_tokens"].sum() or 0)
        total_cache_read = int(df["cache_read_tokens"].sum() or 0)
        total_cache_create = int(df["cache_creation_tokens"].sum() or 0)
        total_tokens = total_input + total_output + total_cache_read + total_cache_create
        
        return {
            "total_input_tokens": total_input,
            "total_output_tokens": total_output,
            "total_cache_read_tokens": total_cache_read,
            "total_cache_creation_tokens": total_cache_create,
            "total_tokens": total_tokens,
            "avg_input_tokens": float(df["input_tokens"].mean() or 0),
            "avg_output_tokens": float(df["output_tokens"].mean() or 0),
            "request_count": len(requests),
        }
    
    def get_token_consumption_by_practice(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> pd.DataFrame:
        """
        Get token consumption grouped by engineering practice.
        
        Args:
            start_date: Optional start date filter
            end_date: Optional end date filter
        
        Returns:
            DataFrame with token consumption by practice
        """
        if start_date and end_date:
            requests = self.api_repo.get_by_date_range(start_date, end_date)
        else:
            requests = self.api_repo.get_all()
        
        if not requests:
            return pd.DataFrame()
        
        df = pd.DataFrame(requests)
        
        # Get user practice information
        users = self.user_repo.get_with_employee_info()
        user_practice_map = {u["user_id"]: u.get("practice") for u in users if u.get("practice")}
        
        df["practice"] = df["user_id"].map(user_practice_map)
        df = df[df["practice"].notna()]
        
        result = df.groupby("practice").agg({
            "input_tokens": "sum",
            "output_tokens": "sum",
            "cache_read_tokens": "sum",
            "cache_creation_tokens": "sum",
            "user_id": "nunique",
        }).reset_index()
        
        result["total_tokens"] = (
            result["input_tokens"] + 
            result["output_tokens"] + 
            result["cache_read_tokens"] + 
            result["cache_creation_tokens"]
        )
        result = result.rename(columns={"user_id": "unique_users"})
        result = result.sort_values("total_tokens", ascending=False)
        
        return result
    
    def get_token_consumption_by_level(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> pd.DataFrame:
        """
        Get token consumption grouped by seniority level.
        
        Args:
            start_date: Optional start date filter
            end_date: Optional end date filter
        
        Returns:
            DataFrame with token consumption by level
        """
        if start_date and end_date:
            requests = self.api_repo.get_by_date_range(start_date, end_date)
        else:
            requests = self.api_repo.get_all()
        
        if not requests:
            return pd.DataFrame()
        
        df = pd.DataFrame(requests)
        
        # Get user level information
        users = self.user_repo.get_with_employee_info()
        user_level_map = {u["user_id"]: u.get("level") for u in users if u.get("level")}
        
        df["level"] = df["user_id"].map(user_level_map)
        df = df[df["level"].notna()]
        
        result = df.groupby("level").agg({
            "input_tokens": "sum",
            "output_tokens": "sum",
            "cache_read_tokens": "sum",
            "cache_creation_tokens": "sum",
            "user_id": "nunique",
        }).reset_index()
        
        result["total_tokens"] = (
            result["input_tokens"] + 
            result["output_tokens"] + 
            result["cache_read_tokens"] + 
            result["cache_creation_tokens"]
        )
        result = result.rename(columns={"user_id": "unique_users"})
        
        # Sort by level (L1, L2, ..., L10)
        level_order = [f"L{i}" for i in range(1, 11)]
        result["level_order"] = result["level"].str.extract(r'L(\d+)').astype(int)
        result = result.sort_values("level_order")
        result = result.drop(columns=["level_order"])
        
        return result
    
    def get_session_metrics(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> Dict[str, Any]:
        """
        Get session metrics.
        
        Args:
            start_date: Optional start date filter
            end_date: Optional end date filter
        
        Returns:
            Dictionary with session metrics
        """
        if start_date and end_date:
            sessions = self.session_repo.get_by_date_range(start_date, end_date)
        else:
            sessions = self.session_repo.get_all()
        
        if not sessions:
            return {
                "total_sessions": 0,
                "unique_users": 0,
                "avg_duration_seconds": 0,
                "total_duration_seconds": 0,
            }
        
        df = pd.DataFrame(sessions)
        df = df[df["duration_seconds"].notna()]
        
        return {
            "total_sessions": len(sessions),
            "unique_users": int(df["user_id"].nunique()) if not df.empty else 0,
            "avg_duration_seconds": float(df["duration_seconds"].mean() or 0),
            "min_duration_seconds": float(df["duration_seconds"].min() or 0),
            "max_duration_seconds": float(df["duration_seconds"].max() or 0),
            "total_duration_seconds": float(df["duration_seconds"].sum() or 0),
            "median_duration_seconds": float(df["duration_seconds"].median() or 0),
        }
    
    def get_user_activity_summary(self) -> pd.DataFrame:
        """
        Get user activity summary.
        
        Returns:
            DataFrame with user activity metrics
        """
        users = self.user_repo.get_with_employee_info()
        if not users:
            return pd.DataFrame()
        
        df = pd.DataFrame(users)
        
        # Get session counts per user
        all_sessions = self.session_repo.get_all()
        session_df = pd.DataFrame(all_sessions)
        
        if not session_df.empty:
            session_counts = session_df.groupby("user_id").size().reset_index(name="session_count")
            session_durations = session_df.groupby("user_id")["duration_seconds"].sum().reset_index(name="total_duration")
            
            df = df.merge(session_counts, on="user_id", how="left")
            df = df.merge(session_durations, on="user_id", how="left")
            df["session_count"] = df["session_count"].fillna(0).astype(int)
            df["total_duration"] = df["total_duration"].fillna(0).astype(float)
        else:
            df["session_count"] = 0
            df["total_duration"] = 0.0
        
        # Get API request counts per user
        all_requests = self.api_repo.get_all()
        request_df = pd.DataFrame(all_requests)
        
        if not request_df.empty:
            request_counts = request_df.groupby("user_id").size().reset_index(name="request_count")
            request_tokens = request_df.groupby("user_id").agg({
                "input_tokens": "sum",
                "output_tokens": "sum",
            }).reset_index()
            
            df = df.merge(request_counts, on="user_id", how="left")
            df = df.merge(request_tokens, on="user_id", how="left")
            df["request_count"] = df["request_count"].fillna(0).astype(int)
            df["input_tokens"] = df["input_tokens"].fillna(0).astype(int)
            df["output_tokens"] = df["output_tokens"].fillna(0).astype(int)
        else:
            df["request_count"] = 0
            df["input_tokens"] = 0
            df["output_tokens"] = 0
        
        return df
