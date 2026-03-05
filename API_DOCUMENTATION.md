# REST API Documentation

## Overview

The Claude Code Analytics Platform provides a REST API built with FastAPI for programmatic access to analytics data. The API returns JSON responses and includes automatic interactive documentation.

## Base URL

```
http://localhost:8000
```

## Running the API Server

### Option 1: Using the Run Script (Recommended)

```bash
python scripts/run_api.py
```

### Option 2: Using Uvicorn Directly

```bash
uvicorn src.api.api_server:app --host 0.0.0.0 --port 8000 --reload
```

### Option 3: Using Python Module

```bash
python -m uvicorn src.api.api_server:app --host 0.0.0.0 --port 8000 --reload
```

## Interactive Documentation

Once the server is running, access the interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Endpoints

### Root Endpoint

#### `GET /`

Returns API information and available endpoints.

**Response:**
```json
{
  "name": "Claude Code Analytics API",
  "version": "1.0.0",
  "description": "REST API for programmatic access to Claude Code telemetry analytics",
  "endpoints": {
    "tokens": "/api/tokens",
    "cost": "/api/cost",
    "sessions": "/api/sessions",
    "users": "/api/users",
    "usage_patterns": "/api/usage-patterns"
  },
  "documentation": {
    "swagger": "/docs",
    "redoc": "/redoc"
  }
}
```

### Token Analytics

#### `GET /api/tokens`

Returns token consumption summary.

**Query Parameters:**
- `start_date` (optional): Start date filter in YYYY-MM-DD format
- `end_date` (optional): End date filter in YYYY-MM-DD format
- `by_practice` (optional, default: false): Include breakdown by practice

**Example Request:**
```bash
curl "http://localhost:8000/api/tokens?start_date=2026-01-01&end_date=2026-01-31&by_practice=true"
```

**Response:**
```json
{
  "summary": {
    "total_input_tokens": 1500000,
    "total_output_tokens": 800000,
    "total_cache_read_tokens": 200000,
    "total_cache_creation_tokens": 100000,
    "total_tokens": 2600000,
    "avg_input_tokens": 1500.0,
    "avg_output_tokens": 800.0,
    "request_count": 1000
  },
  "filters": {
    "start_date": "2026-01-01",
    "end_date": "2026-01-31"
  },
  "by_practice": [
    {
      "practice": "Backend",
      "total_tokens": 1200000,
      "unique_users": 25
    }
  ]
}
```

### Cost Analytics

#### `GET /api/cost`

Returns cost analytics summary.

**Query Parameters:**
- `start_date` (optional): Start date filter in YYYY-MM-DD format
- `end_date` (optional): End date filter in YYYY-MM-DD format
- `by_model` (optional, default: false): Include breakdown by model
- `by_practice` (optional, default: false): Include breakdown by practice

**Example Request:**
```bash
curl "http://localhost:8000/api/cost?start_date=2026-01-01&end_date=2026-01-31&by_model=true"
```

**Response:**
```json
{
  "summary": {
    "total_cost_usd": 1250.50,
    "avg_cost_per_request": 0.0125,
    "min_cost_per_request": 0.001,
    "max_cost_per_request": 0.05,
    "median_cost_per_request": 0.01,
    "request_count": 1000
  },
  "filters": {
    "start_date": "2026-01-01",
    "end_date": "2026-01-31"
  },
  "by_model": [
    {
      "model": "claude-3-opus-20240229",
      "total_cost_usd": 800.00,
      "request_count": 500
    }
  ]
}
```

### Session Analytics

#### `GET /api/sessions`

Returns session metrics.

**Query Parameters:**
- `start_date` (optional): Start date filter in YYYY-MM-DD format
- `end_date` (optional): End date filter in YYYY-MM-DD format

**Example Request:**
```bash
curl "http://localhost:8000/api/sessions?start_date=2026-01-01&end_date=2026-01-31"
```

**Response:**
```json
{
  "metrics": {
    "total_sessions": 500,
    "unique_users": 50,
    "avg_duration_seconds": 3600.0,
    "median_duration_seconds": 3000.0,
    "min_duration_seconds": 60.0,
    "max_duration_seconds": 7200.0,
    "total_duration_seconds": 1800000.0
  },
  "filters": {
    "start_date": "2026-01-01",
    "end_date": "2026-01-31"
  }
}
```

### User Analytics

#### `GET /api/users`

Returns employee activity analytics.

**Example Request:**
```bash
curl http://localhost:8000/api/users
```

**Response:**
```json
{
  "users": [
    {
      "full_name": "John Doe",
      "practice": "Backend",
      "level": "L5",
      "session_count": 25,
      "request_count": 150,
      "total_duration": 90000
    }
  ],
  "total_users": 50
}
```

### Usage Patterns

#### `GET /api/usage-patterns`

Returns peak usage hours and tool usage statistics.

**Query Parameters:**
- `start_date` (optional): Start date filter in YYYY-MM-DD format
- `end_date` (optional): End date filter in YYYY-MM-DD format
- `include_tools` (optional, default: true): Include tool usage statistics
- `include_models` (optional, default: false): Include model usage patterns

**Example Request:**
```bash
curl "http://localhost:8000/api/usage-patterns?include_tools=true&include_models=true"
```

**Response:**
```json
{
  "peak_usage_hours": [
    {
      "hour": 9,
      "event_count": 500
    },
    {
      "hour": 10,
      "event_count": 750
    }
  ],
  "filters": {
    "start_date": null,
    "end_date": null
  },
  "tool_usage": [
    {
      "tool_name": "read_file",
      "total_uses": 1000,
      "successful_uses": 950,
      "failed_uses": 50,
      "success_rate": 95.0,
      "avg_duration_ms": 150.0
    }
  ],
  "model_usage": [
    {
      "model": "claude-3-opus-20240229",
      "request_count": 500
    }
  ]
}
```

## Error Handling

The API returns standard HTTP status codes:

- `200 OK`: Successful request
- `400 Bad Request`: Invalid request parameters (e.g., start_date > end_date)
- `500 Internal Server Error`: Server error

**Error Response Format:**
```json
{
  "detail": "Error message description"
}
```

## Date Format

All date parameters should be in `YYYY-MM-DD` format (ISO 8601 date format).

**Example:**
```
2026-01-15
```

## Response Format

All responses are in JSON format with UTF-8 encoding.

## Rate Limiting

Currently, the API does not implement rate limiting. For production use, consider adding rate limiting middleware.

## Authentication

Currently, the API does not require authentication. For production use, consider adding authentication middleware (e.g., API keys, OAuth2).

## Examples

### Python Example

```python
import requests

# Get token consumption
response = requests.get(
    "http://localhost:8000/api/tokens",
    params={
        "start_date": "2026-01-01",
        "end_date": "2026-01-31",
        "by_practice": True
    }
)
data = response.json()
print(data)
```

### JavaScript Example

```javascript
// Get cost analytics
fetch('http://localhost:8000/api/cost?start_date=2026-01-01&end_date=2026-01-31&by_model=true')
  .then(response => response.json())
  .then(data => console.log(data));
```

### cURL Examples

```bash
# Get all tokens
curl http://localhost:8000/api/tokens

# Get cost with filters
curl "http://localhost:8000/api/cost?start_date=2026-01-01&end_date=2026-01-31"

# Get usage patterns
curl "http://localhost:8000/api/usage-patterns?include_tools=true"
```

## Notes

- The API uses the same database and analytics modules as the Streamlit dashboard
- Date filters are optional - if not provided, all data is returned
- All numeric values in responses are properly formatted (integers for counts, floats for averages)
- NaN values in DataFrames are converted to `null` in JSON responses
