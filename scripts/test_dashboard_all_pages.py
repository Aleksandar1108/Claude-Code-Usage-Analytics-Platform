"""Test script to verify all dashboard pages work correctly."""

import sys
from pathlib import Path
from datetime import datetime, timedelta

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.storage.database import Database
from src.analytics.usage_analytics import UsageAnalytics
from src.analytics.cost_analytics import CostAnalytics
from src.analytics.pattern_analytics import PatternAnalytics
from src.analytics.trend_analytics import TrendAnalytics
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


def test_all_dashboard_pages():
    """Test all dashboard page functionality."""
    print("=" * 60)
    print("Testing All Dashboard Pages")
    print("=" * 60)
    
    # Initialize database and analytics
    db = Database()
    usage = UsageAnalytics(db)
    cost = CostAnalytics(db)
    pattern = PatternAnalytics(db)
    trend = TrendAnalytics(db)
    
    # Test date range
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)
    
    tests_passed = 0
    tests_failed = 0
    
    # Test 1: Token Usage Analytics
    print("\n1. Testing Token Usage Analytics...")
    try:
        token_summary = usage.get_token_consumption_summary(start_date, end_date)
        tokens_by_practice = usage.get_token_consumption_by_practice(start_date, end_date)
        tokens_by_level = usage.get_token_consumption_by_level(start_date, end_date)
        print("   [OK] Token usage analytics working")
        tests_passed += 1
    except Exception as e:
        print(f"   [ERROR] {e}")
        tests_failed += 1
    
    # Test 2: Cost Analytics
    print("\n2. Testing Cost Analytics...")
    try:
        cost_summary = cost.get_cost_summary(start_date, end_date)
        cost_by_model = cost.get_cost_by_model(start_date, end_date)
        cost_by_practice = cost.get_cost_by_practice(start_date, end_date)
        daily_cost = cost.get_daily_cost_trend(start_date, end_date)
        print("   [OK] Cost analytics working")
        tests_passed += 1
    except Exception as e:
        print(f"   [ERROR] {e}")
        import traceback
        traceback.print_exc()
        tests_failed += 1
    
    # Test 3: Usage Patterns
    print("\n3. Testing Usage Patterns...")
    try:
        peak_hours = pattern.get_peak_usage_hours(start_date, end_date)
        tool_patterns = pattern.get_tool_usage_patterns()
        model_patterns = pattern.get_model_usage_patterns(start_date, end_date)
        weekday_pattern = pattern.get_weekday_pattern(start_date, end_date)
        print("   [OK] Usage patterns working")
        tests_passed += 1
    except Exception as e:
        print(f"   [ERROR] {e}")
        import traceback
        traceback.print_exc()
        tests_failed += 1
    
    # Test 4: Session Analytics
    print("\n4. Testing Session Analytics...")
    try:
        session_metrics = usage.get_session_metrics(start_date, end_date)
        user_activity = usage.get_user_activity_summary()
        print("   [OK] Session analytics working")
        tests_passed += 1
    except Exception as e:
        print(f"   [ERROR] {e}")
        tests_failed += 1
    
    # Test 5: Daily Trends (all metrics)
    print("\n5. Testing Daily Trends...")
    try:
        for metric in ["events", "sessions", "cost", "tokens"]:
            daily = trend.get_daily_trends(metric, start_date, end_date)
            weekly = trend.get_weekly_trends(metric, start_date, end_date)
            monthly = trend.get_monthly_trends(metric, start_date, end_date)
            summary = trend.get_trend_summary(metric, start_date, end_date)
        print("   [OK] Daily trends working for all metrics")
        tests_passed += 1
    except Exception as e:
        print(f"   [ERROR] {e}")
        import traceback
        traceback.print_exc()
        tests_failed += 1
    
    # Summary
    print("\n" + "=" * 60)
    print(f"Tests Passed: {tests_passed}")
    print(f"Tests Failed: {tests_failed}")
    if tests_failed == 0:
        print("All dashboard pages working correctly! [OK]")
    else:
        print("Some tests failed. Please check errors above.")
    print("=" * 60)
    
    return tests_failed == 0


if __name__ == "__main__":
    success = test_all_dashboard_pages()
    sys.exit(0 if success else 1)
