"""Test script to verify analytics functions work correctly."""

import sys
from pathlib import Path

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


def test_analytics():
    """Test all analytics functions."""
    print("=" * 60)
    print("Testing Analytics Functions")
    print("=" * 60)
    
    # Initialize database and analytics
    db = Database()
    usage_analytics = UsageAnalytics(db)
    cost_analytics = CostAnalytics(db)
    pattern_analytics = PatternAnalytics(db)
    trend_analytics = TrendAnalytics(db)
    
    # Test 1: Token Consumption Summary
    print("\n1. Testing Token Consumption Summary...")
    try:
        token_summary = usage_analytics.get_token_consumption_summary()
        print(f"   [OK] Total tokens: {token_summary.get('total_tokens', 0):,}")
        print(f"   [OK] Input tokens: {token_summary.get('total_input_tokens', 0):,}")
        print(f"   [OK] Output tokens: {token_summary.get('total_output_tokens', 0):,}")
        print(f"   [OK] Request count: {token_summary.get('request_count', 0)}")
    except Exception as e:
        print(f"   [ERROR] Error: {e}")
        return False
    
    # Test 2: Token Consumption by Practice
    print("\n2. Testing Token Consumption by Practice...")
    try:
        tokens_by_practice = usage_analytics.get_token_consumption_by_practice()
        if not tokens_by_practice.empty:
            print(f"   [OK] Found {len(tokens_by_practice)} practices")
            print(f"   [OK] Top practice: {tokens_by_practice.iloc[0]['practice']}")
            print(f"   [OK] Total tokens for top practice: {tokens_by_practice.iloc[0]['total_tokens']:,.0f}")
        else:
            print("   [WARN] No data found")
    except Exception as e:
        print(f"   [ERROR] Error: {e}")
        return False
    
    # Test 3: Session Metrics
    print("\n3. Testing Session Metrics...")
    try:
        session_metrics = usage_analytics.get_session_metrics()
        print(f"   [OK] Total sessions: {session_metrics.get('total_sessions', 0)}")
        print(f"   [OK] Unique users: {session_metrics.get('unique_users', 0)}")
        print(f"   [OK] Avg duration: {session_metrics.get('avg_duration_seconds', 0):.2f} seconds")
    except Exception as e:
        print(f"   [ERROR] Error: {e}")
        return False
    
    # Test 4: Cost Summary
    print("\n4. Testing Cost Summary...")
    try:
        cost_summary = cost_analytics.get_cost_summary()
        print(f"   [OK] Total cost: ${cost_summary.get('total_cost_usd', 0):.2f}")
        print(f"   [OK] Avg cost per request: ${cost_summary.get('avg_cost_per_request', 0):.4f}")
        print(f"   [OK] Request count: {cost_summary.get('request_count', 0)}")
    except Exception as e:
        print(f"   [ERROR] Error: {e}")
        return False
    
    # Test 5: Cost by Model
    print("\n5. Testing Cost by Model...")
    try:
        cost_by_model = cost_analytics.get_cost_by_model()
        if not cost_by_model.empty:
            print(f"   [OK] Found {len(cost_by_model)} models")
            print(f"   [OK] Top model: {cost_by_model.iloc[0]['model']}")
            print(f"   [OK] Cost for top model: ${cost_by_model.iloc[0]['total_cost_usd']:.2f}")
        else:
            print("   [WARN] No data found")
    except Exception as e:
        print(f"   [ERROR] Error: {e}")
        return False
    
    # Test 6: Peak Usage Hours
    print("\n6. Testing Peak Usage Hours...")
    try:
        peak_hours = pattern_analytics.get_peak_usage_hours()
        if not peak_hours.empty:
            print(f"   [OK] Found data for {len(peak_hours)} hours")
            max_hour = peak_hours.loc[peak_hours['event_count'].idxmax()]
            print(f"   [OK] Peak hour: {int(max_hour['hour'])}:00 with {max_hour['event_count']} events")
        else:
            print("   [WARN] No data found")
    except Exception as e:
        print(f"   [ERROR] Error: {e}")
        return False
    
    # Test 7: Tool Usage Patterns
    print("\n7. Testing Tool Usage Patterns...")
    try:
        tool_patterns = pattern_analytics.get_tool_usage_patterns()
        if not tool_patterns.empty:
            print(f"   [OK] Found {len(tool_patterns)} tools")
            top_tool = tool_patterns.iloc[0]
            print(f"   [OK] Top tool: {top_tool['tool_name']} ({top_tool['total_uses']} uses)")
            print(f"   [OK] Success rate: {top_tool.get('success_rate', 0):.1f}%")
        else:
            print("   [WARN] No data found")
    except Exception as e:
        print(f"   [ERROR] Error: {e}")
        return False
    
    # Test 8: Daily Trends
    print("\n8. Testing Daily Trends...")
    try:
        daily_trends = trend_analytics.get_daily_trends(metric="events")
        if not daily_trends.empty:
            print(f"   [OK] Found {len(daily_trends)} days of data")
            count_col = 'count' if 'count' in daily_trends.columns else daily_trends.columns[-1]
            print(f"   [OK] Total events: {daily_trends[count_col].sum():,.0f}")
            print(f"   [OK] Avg events per day: {daily_trends[count_col].mean():.1f}")
        else:
            print("   [WARN] No data found")
    except Exception as e:
        print(f"   [ERROR] Error: {e}")
        return False
    
    # Test 9: Trend Summary
    print("\n9. Testing Trend Summary...")
    try:
        trend_summary = trend_analytics.get_trend_summary(metric="events")
        print(f"   [OK] Total: {trend_summary.get('total', 0):,.0f}")
        print(f"   [OK] Avg daily: {trend_summary.get('avg_daily', 0):.1f}")
        print(f"   [OK] Trend: {trend_summary.get('trend', 'unknown')}")
        print(f"   [OK] 7-day growth rate: {trend_summary.get('growth_rate_7d', 0):.1f}%")
    except Exception as e:
        print(f"   [ERROR] Error: {e}")
        return False
    
    # Test 10: User Activity Summary
    print("\n10. Testing User Activity Summary...")
    try:
        user_activity = usage_analytics.get_user_activity_summary()
        if not user_activity.empty:
            print(f"   [OK] Found {len(user_activity)} users")
            print(f"   [OK] Total sessions: {user_activity['session_count'].sum()}")
            print(f"   [OK] Avg sessions per user: {user_activity['session_count'].mean():.1f}")
        else:
            print("   [WARN] No data found")
    except Exception as e:
        print(f"   [ERROR] Error: {e}")
        return False
    
    print("\n" + "=" * 60)
    print("All tests passed successfully! [OK]")
    print("=" * 60)
    return True


if __name__ == "__main__":
    success = test_analytics()
    sys.exit(0 if success else 1)
