"""Cost analytics for API usage costs."""

import pandas as pd
from datetime import datetime
from typing import Dict, List, Optional, Any
from src.storage.database import Database
from src.dal.repositories.api_request_repository import APIRequestRepository
from src.dal.repositories.user_repository import UserRepository
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


class CostAnalytics:
    """Analytics for cost analysis."""
    
    def __init__(self, db: Database):
        """
        Initialize cost analytics.
        
        Args:
            db: Database instance
        """
        self.db = db
        self.api_repo = APIRequestRepository(db)
        self.user_repo = UserRepository(db)
    
    def get_cost_summary(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> Dict[str, Any]:
        """
        Get overall cost summary.
        
        Args:
            start_date: Optional start date filter
            end_date: Optional end date filter
        
        Returns:
            Dictionary with cost metrics
        """
        if start_date and end_date:
            requests = self.api_repo.get_by_date_range(start_date, end_date)
        else:
            requests = self.api_repo.get_all()
        
        if not requests:
            return {
                "total_cost_usd": 0.0,
                "avg_cost_per_request": 0.0,
                "request_count": 0,
            }
        
        df = pd.DataFrame(requests)
        
        return {
            "total_cost_usd": float(df["cost_usd"].sum() or 0),
            "avg_cost_per_request": float(df["cost_usd"].mean() or 0),
            "min_cost_per_request": float(df["cost_usd"].min() or 0),
            "max_cost_per_request": float(df["cost_usd"].max() or 0),
            "median_cost_per_request": float(df["cost_usd"].median() or 0),
            "request_count": len(requests),
        }
    
    def get_cost_by_model(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> pd.DataFrame:
        """
        Get cost breakdown by model.
        
        Args:
            start_date: Optional start date filter
            end_date: Optional end date filter
        
        Returns:
            DataFrame with cost by model
        """
        if start_date and end_date:
            requests = self.api_repo.get_by_date_range(start_date, end_date)
        else:
            requests = self.api_repo.get_all()
        
        if not requests:
            return pd.DataFrame()
        
        df = pd.DataFrame(requests)
        
        result = df.groupby("model").agg({
            "cost_usd": ["sum", "mean", "count"],
            "input_tokens": "sum",
            "output_tokens": "sum",
        }).reset_index()
        
        result.columns = [
            "model",
            "total_cost_usd",
            "avg_cost_per_request",
            "request_count",
            "total_input_tokens",
            "total_output_tokens",
        ]
        
        result = result.sort_values("total_cost_usd", ascending=False)
        return result
    
    def get_cost_by_practice(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> pd.DataFrame:
        """
        Get cost breakdown by engineering practice.
        
        Args:
            start_date: Optional start date filter
            end_date: Optional end date filter
        
        Returns:
            DataFrame with cost by practice
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
            "cost_usd": ["sum", "mean", "count"],
            "user_id": "nunique",
        }).reset_index()
        
        result.columns = [
            "practice",
            "total_cost_usd",
            "avg_cost_per_request",
            "request_count",
            "unique_users",
        ]
        
        result = result.sort_values("total_cost_usd", ascending=False)
        return result
    
    def get_cost_by_level(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> pd.DataFrame:
        """
        Get cost breakdown by seniority level.
        
        Args:
            start_date: Optional start date filter
            end_date: Optional end date filter
        
        Returns:
            DataFrame with cost by level
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
            "cost_usd": ["sum", "mean", "count"],
            "user_id": "nunique",
        }).reset_index()
        
        result.columns = [
            "level",
            "total_cost_usd",
            "avg_cost_per_request",
            "request_count",
            "unique_users",
        ]
        
        # Sort by level (L1, L2, ..., L10)
        level_order = [f"L{i}" for i in range(1, 11)]
        result["level_order"] = result["level"].str.extract(r'L(\d+)').astype(int)
        result = result.sort_values("level_order")
        result = result.drop(columns=["level_order"])
        
        return result
    
    def get_cost_by_user(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        limit: int = 20
    ) -> pd.DataFrame:
        """
        Get cost breakdown by user (top users).
        
        Args:
            start_date: Optional start date filter
            end_date: Optional end date filter
            limit: Number of top users to return
        
        Returns:
            DataFrame with cost by user
        """
        if start_date and end_date:
            requests = self.api_repo.get_by_date_range(start_date, end_date)
        else:
            requests = self.api_repo.get_all()
        
        if not requests:
            return pd.DataFrame()
        
        df = pd.DataFrame(requests)
        
        # Get user information
        users = self.user_repo.get_with_employee_info()
        user_info_map = {
            u["user_id"]: {
                "email": u.get("email"),
                "full_name": u.get("full_name"),
                "practice": u.get("practice"),
                "level": u.get("level"),
            }
            for u in users
        }
        
        result = df.groupby("user_id").agg({
            "cost_usd": ["sum", "mean", "count"],
        }).reset_index()
        
        result.columns = ["user_id", "total_cost_usd", "avg_cost_per_request", "request_count"]
        
        # Add user info
        result["email"] = result["user_id"].map(lambda x: user_info_map.get(x, {}).get("email", ""))
        result["full_name"] = result["user_id"].map(lambda x: user_info_map.get(x, {}).get("full_name", ""))
        result["practice"] = result["user_id"].map(lambda x: user_info_map.get(x, {}).get("practice", ""))
        result["level"] = result["user_id"].map(lambda x: user_info_map.get(x, {}).get("level", ""))
        
        result = result.sort_values("total_cost_usd", ascending=False).head(limit)
        return result
    
    def get_daily_cost_trend(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> pd.DataFrame:
        """
        Get daily cost trend.
        
        Args:
            start_date: Optional start date filter
            end_date: Optional end date filter
        
        Returns:
            DataFrame with daily cost
        """
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
        
        result = df.groupby("date").agg({
            "cost_usd": "sum",
            "user_id": "nunique",
            "model": "nunique",
        }).reset_index()
        
        result.columns = ["date", "total_cost_usd", "unique_users", "unique_models"]
        result = result.sort_values("date")
        
        return result
