"""Test script to verify Daily Trends dashboard works correctly."""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.storage.database import Database
from src.analytics.trend_analytics import TrendAnalytics
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


def test_daily_trends():
    """Test daily trends functionality."""
    print("=" * 60)
    print("Testing Daily Trends Dashboard")
    print("=" * 60)
    
    # Initialize database and analytics
    db = Database()
    trend = TrendAnalytics(db)
    
    # Test all metrics
    metrics = ["events", "sessions", "cost", "tokens"]
    
    for metric in metrics:
        print(f"\nTesting metric: {metric}")
        print("-" * 40)
        
        try:
            # Test daily trends
            daily = trend.get_daily_trends(metric)
            if not daily.empty:
                print(f"  [OK] Daily trends: {len(daily)} days")
                print(f"  [OK] Columns: {daily.columns.tolist()}")
                if 'count' in daily.columns:
                    print(f"  [OK] Total: {daily['count'].sum():,.0f}")
                else:
                    print(f"  [WARN] No 'count' column, last column: {daily.columns[-1]}")
            else:
                print(f"  [WARN] No daily data for {metric}")
            
            # Test weekly trends
            weekly = trend.get_weekly_trends(metric)
            if not weekly.empty:
                print(f"  [OK] Weekly trends: {len(weekly)} weeks")
                print(f"  [OK] Columns: {weekly.columns.tolist()}")
                if 'count' in weekly.columns:
                    print(f"  [OK] Total: {weekly['count'].sum():,.0f}")
                else:
                    print(f"  [ERROR] No 'count' column in weekly trends!")
                    return False
            else:
                print(f"  [WARN] No weekly data for {metric}")
            
            # Test monthly trends
            monthly = trend.get_monthly_trends(metric)
            if not monthly.empty:
                print(f"  [OK] Monthly trends: {len(monthly)} months")
                print(f"  [OK] Columns: {monthly.columns.tolist()}")
                if 'count' in monthly.columns:
                    print(f"  [OK] Total: {monthly['count'].sum():,.0f}")
                else:
                    print(f"  [ERROR] No 'count' column in monthly trends!")
                    return False
            else:
                print(f"  [WARN] No monthly data for {metric}")
            
            # Test trend summary
            summary = trend.get_trend_summary(metric)
            print(f"  [OK] Trend summary: {summary.get('trend', 'unknown')}")
            
        except Exception as e:
            print(f"  [ERROR] Error testing {metric}: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    print("\n" + "=" * 60)
    print("All Daily Trends tests passed successfully! [OK]")
    print("=" * 60)
    return True


if __name__ == "__main__":
    success = test_daily_trends()
    sys.exit(0 if success else 1)
