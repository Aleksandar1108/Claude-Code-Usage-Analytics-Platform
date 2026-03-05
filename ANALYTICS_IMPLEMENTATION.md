# Analytics Layer Implementation

## Overview

The analytics layer provides comprehensive analytics capabilities for the Claude Code telemetry data. It follows a clean architecture with repository pattern for data access and service classes for business logic.

## Architecture

```
Analytics Service Layer
    ├── UsageAnalytics      # Token consumption, session metrics
    ├── CostAnalytics       # Cost analysis by various dimensions
    ├── PatternAnalytics    # Usage patterns, peak times
    ├── TrendAnalytics      # Time-series trends
    └── Aggregators         # Utility functions for aggregations
```

## Data Access Layer (DAL)

### Repository Classes

All repositories follow the same pattern and provide clean interfaces for data access:

1. **UserRepository** (`src/dal/repositories/user_repository.py`)
   - Get all users
   - Get user by ID or email
   - Get users with employee information
   - User count

2. **SessionRepository** (`src/dal/repositories/session_repository.py`)
   - Get all sessions (with optional limit)
   - Get session by ID
   - Get sessions by user ID
   - Get sessions by date range
   - Session statistics
   - Session count

3. **APIRequestRepository** (`src/dal/repositories/api_request_repository.py`)
   - Get all API requests
   - Get requests by date range
   - Get requests by user ID
   - Get requests by model
   - Overall statistics
   - Statistics by model
   - Request count

4. **ToolRepository** (`src/dal/repositories/tool_repository.py`)
   - Get tool decisions
   - Get tool results
   - Tool usage statistics
   - Tool decision statistics
   - Tool usage by user

5. **EventRepository** (`src/dal/repositories/event_repository.py`)
   - Get events by type
   - Get events by date range
   - Event counts by type
   - Hourly distribution
   - Daily distribution

## Analytics Services

### 1. Usage Analytics (`src/analytics/usage_analytics.py`)

Provides metrics for token consumption and session activity.

#### Methods:

- **`get_token_consumption_summary()`**
  - Overall token consumption (input, output, cache)
  - Average tokens per request
  - Total request count

- **`get_token_consumption_by_practice()`**
  - Token consumption grouped by engineering practice
  - Includes unique users per practice

- **`get_token_consumption_by_level()`**
  - Token consumption grouped by seniority level (L1-L10)
  - Sorted by level

- **`get_session_metrics()`**
  - Total sessions
  - Unique users
  - Average, min, max, median session duration
  - Total duration

- **`get_user_activity_summary()`**
  - Comprehensive user activity metrics
  - Session counts and durations
  - API request counts
  - Token consumption per user

### 2. Cost Analytics (`src/analytics/cost_analytics.py`)

Provides cost analysis across various dimensions.

#### Methods:

- **`get_cost_summary()`**
  - Total cost
  - Average, min, max, median cost per request
  - Request count

- **`get_cost_by_model()`**
  - Cost breakdown by Claude model
  - Includes token consumption
  - Sorted by total cost

- **`get_cost_by_practice()`**
  - Cost breakdown by engineering practice
  - Average cost per request
  - Unique users per practice

- **`get_cost_by_level()`**
  - Cost breakdown by seniority level
  - Sorted by level (L1-L10)

- **`get_cost_by_user()`**
  - Top users by cost
  - Includes user information (name, practice, level)
  - Configurable limit

- **`get_daily_cost_trend()`**
  - Daily cost over time
  - Includes unique users and models per day

### 3. Pattern Analytics (`src/analytics/pattern_analytics.py`)

Identifies usage patterns and peak times.

#### Methods:

- **`get_peak_usage_hours()`**
  - Hourly event distribution
  - Identifies peak usage hours

- **`get_daily_usage_pattern()`**
  - Daily event distribution
  - Shows usage trends over time

- **`get_tool_usage_patterns()`**
  - Tool usage statistics
  - Success rates
  - Average durations
  - Result sizes

- **`get_tool_decision_patterns()`**
  - Tool decision statistics
  - Acceptance/rejection rates
  - Decision sources

- **`get_model_usage_patterns()`**
  - Model usage statistics
  - Cost and token consumption by model
  - Can filter by date range

- **`get_weekday_pattern()`**
  - Usage pattern by day of week
  - Shows weekday vs weekend patterns

- **`get_event_type_distribution()`**
  - Distribution of event types
  - Shows relative frequency of each event type

### 4. Trend Analytics (`src/analytics/trend_analytics.py`)

Provides time-series analysis and trend calculations.

#### Methods:

- **`get_daily_trends()`**
  - Daily trends for various metrics
  - Supports: 'events', 'sessions', 'cost', 'tokens'

- **`get_weekly_trends()`**
  - Weekly aggregation of trends
  - Useful for longer-term analysis

- **`get_monthly_trends()`**
  - Monthly aggregation of trends
  - High-level overview

- **`calculate_growth_rate()`**
  - Calculate growth rate over specified period
  - Returns percentage change

- **`get_trend_summary()`**
  - Comprehensive trend summary
  - Includes growth rates (7-day, 30-day)
  - Trend direction (increasing/decreasing/stable)
  - Min/max daily values

### 5. Aggregators (`src/analytics/aggregators.py`)

Utility functions for common aggregation operations.

#### Methods:

- **`group_by_time_period()`**
  - Group DataFrame by time period (hour, day, week, month)

- **`calculate_percentages()`**
  - Calculate percentages for a column
  - Adds percentage column to DataFrame

- **`top_n()`**
  - Get top N rows by column value
  - Useful for rankings

- **`calculate_statistics()`**
  - Calculate basic statistics (mean, median, std, min, max)
  - Returns dictionary with statistics

- **`fill_date_gaps()`**
  - Fill gaps in date series with zero values
  - Ensures continuous time series for visualization

## Usage Example

```python
from src.storage.database import Database
from src.analytics.usage_analytics import UsageAnalytics
from src.analytics.cost_analytics import CostAnalytics
from src.analytics.pattern_analytics import PatternAnalytics
from src.analytics.trend_analytics import TrendAnalytics

# Initialize database
db = Database()

# Initialize analytics
usage_analytics = UsageAnalytics(db)
cost_analytics = CostAnalytics(db)
pattern_analytics = PatternAnalytics(db)
trend_analytics = TrendAnalytics(db)

# Get token consumption summary
token_summary = usage_analytics.get_token_consumption_summary()
print(f"Total tokens: {token_summary['total_tokens']}")

# Get cost by model
cost_by_model = cost_analytics.get_cost_by_model()
print(cost_by_model)

# Get peak usage hours
peak_hours = pattern_analytics.get_peak_usage_hours()
print(peak_hours)

# Get daily trends
daily_trends = trend_analytics.get_daily_trends(metric="cost")
print(daily_trends)
```

## Features

### ✅ Comprehensive Coverage
- All major analytics dimensions covered
- Multiple aggregation levels (daily, weekly, monthly)
- Support for date range filtering

### ✅ Performance Optimized
- Uses pandas for efficient data processing
- Repository pattern for clean data access
- Batch operations where possible

### ✅ Flexible Filtering
- Optional date range filtering on all methods
- Supports filtering by user, practice, level, model
- Configurable limits for top-N queries

### ✅ Rich Metrics
- Token consumption (input, output, cache)
- Cost analysis (total, average, by dimension)
- Usage patterns (hourly, daily, weekly)
- Trend analysis with growth rates

### ✅ Data Quality
- Handles missing data gracefully
- Returns empty DataFrames when no data
- Type-safe conversions
- Comprehensive error handling

## Integration with Dashboard

The analytics layer is designed to be easily consumed by the Streamlit dashboard:

- Returns pandas DataFrames for easy visualization
- Provides dictionaries for metric cards
- Supports date filtering for interactive dashboards
- Clean interfaces for all analytics functions

## Next Steps

The analytics layer is complete and ready for:
1. Integration with Streamlit dashboard
2. Unit testing
3. Performance optimization (if needed)
4. Additional analytics functions (as requirements evolve)
