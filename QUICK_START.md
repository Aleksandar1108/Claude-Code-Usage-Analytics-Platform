# Quick Start Guide

## Running the Dashboard

### Prerequisites
1. Python 3.9+ installed
2. Dependencies installed: `pip install -r requirements.txt`
3. Database initialized: `python scripts/setup_database.py`
4. Data ingested: `python scripts/ingest_data.py --telemetry <path> --employees <path>`

### Start the Dashboard

```bash
# From project root directory
streamlit run src/dashboard/main.py
```

The dashboard will automatically open in your browser at `http://localhost:8501`

### Dashboard Navigation

1. **Overview**: Start here for high-level metrics
2. **Token Usage Analytics**: Detailed token consumption analysis
3. **Cost Analytics**: Cost breakdown and optimization insights
4. **Usage Patterns**: Peak times and tool usage patterns
5. **Session Analytics**: Session-level metrics and user activity
6. **Daily Trends**: Time-series analysis and trends

### Using Filters

- **Date Range Filter**: Use the sidebar to select a date range
  - Check "Filter by date range" to enable
  - Select start and end dates
  - All charts will update automatically

### Interactive Features

- **Hover**: Hover over charts for detailed information
- **Zoom**: Click and drag to zoom in on charts
- **Pan**: Click and drag to pan across charts
- **Export**: Use Plotly's built-in export options (camera icon)

## Complete Setup Example

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Initialize database
python scripts/setup_database.py

# 3. Generate sample data (if needed)
cd ../claude_code_telemetry
python generate_fake_data.py --num-users 10 --num-sessions 50 --days 7

# 4. Ingest data
cd ../ProjekatPraksa
python scripts/ingest_data.py \
    --telemetry "../claude_code_telemetry/output/telemetry_logs.jsonl" \
    --employees "../claude_code_telemetry/output/employees.csv"

# 5. Start dashboard
streamlit run src/dashboard/main.py
```

## Troubleshooting

### Dashboard shows "No data available"
- Ensure data has been ingested
- Check database exists: `data/database/analytics.db`
- Verify database has data: Run `scripts/test_analytics.py`

### Charts not rendering
- Check Plotly is installed: `pip install plotly`
- Check browser console for errors
- Try refreshing the page

### Slow performance
- Use date range filters to reduce data
- Check database indexes are created
- Consider reducing data volume for testing

### Port already in use
- Streamlit uses port 8501 by default
- Change port: `streamlit run src/dashboard/main.py --server.port 8502`
