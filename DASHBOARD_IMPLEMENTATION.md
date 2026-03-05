# Streamlit Dashboard Implementation

## Overview

The Streamlit dashboard provides an interactive analytics platform for Claude Code telemetry data. It includes comprehensive visualizations, filtering capabilities, and multiple analytical views.

## Dashboard Structure

### Main Application
- **File**: `src/dashboard/main.py`
- **Entry Point**: Run with `streamlit run src/dashboard/main.py`
- **Layout**: Wide layout for better chart visibility
- **Navigation**: Sidebar-based page navigation

### Components

#### 1. Chart Components (`src/dashboard/components/charts.py`)
Reusable Plotly chart functions:
- `create_bar_chart()`: Vertical and horizontal bar charts
- `create_line_chart()`: Line charts with markers
- `create_pie_chart()`: Pie charts with percentages
- `create_area_chart()`: Area charts for trends
- `create_metric_card()`: HTML metric cards

#### 2. Filter Components (`src/dashboard/components/filters.py`)
Interactive filtering:
- `date_range_filter()`: Date range selection in sidebar
- `practice_filter()`: Filter by engineering practice
- `refresh_button()`: Manual data refresh

#### 3. Configuration (`src/dashboard/config.py`)
Dashboard settings:
- Page title and icon
- Color palette for charts
- Default date range settings

## Dashboard Pages

### 1. Overview Dashboard
**Purpose**: High-level summary with key metrics

**Features**:
- Key metrics cards (Total Tokens, Total Cost, Total Sessions, Daily Avg Events)
- Cost by Model chart
- Token Consumption by Practice chart
- Peak Usage Hours chart
- Daily Activity Trend chart

### 2. Token Usage Analytics
**Purpose**: Detailed token consumption analysis

**Sections**:
- **Total Token Consumption**
  - Total tokens metric
  - Input tokens metric
  - Output tokens metric
  - Cache tokens metric

- **Token Consumption by Practice**
  - Bar chart showing tokens per practice
  - Pie chart showing distribution
  - Data table with details

- **Token Consumption by Model**
  - Bar chart showing tokens per model
  - Data table with input/output breakdown

### 3. Cost Analytics
**Purpose**: Cost analysis and optimization insights

**Sections**:
- **Total Cost Summary**
  - Total cost metric
  - Average cost per request
  - Min/Max cost per request

- **Cost by Model**
  - Bar chart showing cost per model
  - Pie chart showing cost distribution
  - Data table with detailed metrics

- **Cost by Practice**
  - Bar chart showing cost per practice
  - Data table with cost breakdown

### 4. Usage Patterns
**Purpose**: Identify usage patterns and behaviors

**Sections**:
- **Peak Usage Hours**
  - Bar chart showing events by hour
  - Peak hour indicator

- **Tool Usage Statistics**
  - Tool usage count chart
  - Tool success rate chart
  - Data table with tool metrics

- **Model Usage Patterns**
  - API requests by model chart

### 5. Session Analytics
**Purpose**: Session-level insights

**Sections**:
- **Session Metrics**
  - Total sessions
  - Unique users
  - Average/Median duration
  - Min/Max duration
  - Total duration

- **User Activity Summary**
  - Top 10 users by session count
  - Top 10 users by API requests
  - Data table with user activity

### 6. Daily Trends
**Purpose**: Time-series analysis and trends

**Sections**:
- **Trend Summary**
  - Total metric
  - Average daily metric
  - 7-day growth rate
  - Trend direction indicator

- **Daily Trends Chart**
  - Line chart for daily trends
  - Area chart for cumulative view
  - Data table

- **Weekly and Monthly Trends**
  - Weekly aggregation chart
  - Monthly aggregation chart

## Features

### ✅ Interactive Visualizations
- All charts use Plotly for interactivity
- Hover tooltips with detailed information
- Zoom and pan capabilities
- Export options (via Plotly)

### ✅ Date Range Filtering
- Sidebar date range selector
- Applies to all analytics queries
- Default: Last 30 days
- Optional: Disable filter for all-time data

### ✅ Responsive Design
- Wide layout for better chart visibility
- Multi-column layouts for metrics
- Responsive charts that adapt to container width

### ✅ Data Tables
- Detailed data tables for drill-down
- Formatted numbers (commas, currency, percentages)
- Sortable columns
- Full-width display

### ✅ Real-time Data
- Direct database queries
- No caching (always fresh data)
- Fast query execution with indexes

## Chart Types Used

1. **Bar Charts**: For comparisons (cost by model, tokens by practice, etc.)
2. **Line Charts**: For trends over time (daily trends)
3. **Pie Charts**: For distributions (cost distribution, token distribution)
4. **Area Charts**: For cumulative trends
5. **Horizontal Bar Charts**: For rankings (top users, top tools)

## Color Palette

Consistent color scheme across all charts:
- Blue, Orange, Green, Red, Purple, Brown, Pink, Gray, Olive, Cyan
- Ensures visual consistency
- Accessible color combinations

## Alignment with Assignment Requirements

### ✅ Data Processing
- Efficient data retrieval from SQLite
- Proper data aggregation
- Date range filtering

### ✅ Analytics & Insights
- Token consumption trends by user role (practice/level)
- Peak usage times
- Common code generation behaviors (tool usage)
- Cost analysis by model, user, practice

### ✅ Visualization
- Interactive dashboard using Streamlit
- Clear presentation for different stakeholders
- Multiple chart types for different insights

### ✅ Technical Implementation
- Error handling (empty data checks)
- Data validation (handles missing data gracefully)
- Clean architectural design (component-based)

## Usage

### Starting the Dashboard

```bash
# From project root
streamlit run src/dashboard/main.py
```

The dashboard will open in your default browser at `http://localhost:8501`

### Navigation

- Use the sidebar to navigate between pages
- Use date range filter to adjust time period
- Click on charts for interactive exploration
- View data tables for detailed information

### Best Practices

1. **Start with Overview**: Get high-level insights first
2. **Use Date Filters**: Narrow down to specific time periods
3. **Drill Down**: Use data tables for detailed analysis
4. **Compare Metrics**: Use multiple pages to understand relationships

## Performance Considerations

- Database queries are optimized with indexes
- Charts render efficiently with Plotly
- Data tables use Streamlit's built-in formatting
- No data caching (always fresh, but may be slower with large datasets)

## Future Enhancements

Potential improvements:
- Data export functionality (CSV, PDF)
- User authentication
- Saved dashboard configurations
- Real-time updates (if streaming data)
- Advanced filtering (by user, practice, level)
- Custom date range presets (Last 7 days, Last month, etc.)
- Comparison mode (compare two time periods)

## Testing

To test the dashboard:
1. Ensure database is populated with data
2. Run `streamlit run src/dashboard/main.py`
3. Navigate through all pages
4. Test date range filtering
5. Verify all charts render correctly
6. Check data tables display properly

## Troubleshooting

**Issue**: Dashboard shows "No data available"
- **Solution**: Ensure data has been ingested using `scripts/ingest_data.py`

**Issue**: Charts not rendering
- **Solution**: Check that Plotly is installed: `pip install plotly`

**Issue**: Database connection errors
- **Solution**: Verify database exists at `data/database/analytics.db`

**Issue**: Slow loading
- **Solution**: Check database indexes are created, consider date filtering
