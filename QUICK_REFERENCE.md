# Quick Reference Guide

## Entity Relationship Summary

```
┌──────────────┐
│ Organizations│
│  (org_id)    │
└──────┬───────┘
       │
       │ 1:N
       │
┌──────▼───────┐      ┌──────────────┐
│    Users     │◄─────┤  Employees   │
│  (user_id)   │ 1:1  │   (email)    │
└──────┬───────┘      └──────────────┘
       │
       │ 1:N
       │
┌──────▼───────┐
│   Sessions   │
│(session_id)  │
└──────┬───────┘
       │
       │ 1:N
       │
┌──────▼─────────────────────────────────────┐
│              Events                        │
│  ┌─────────────────────────────────────┐  │
│  │ • api_request                        │  │
│  │ • tool_decision                      │  │
│  │ • tool_result                        │  │
│  │ • user_prompt                        │  │
│  │ • api_error                          │  │
│  └─────────────────────────────────────┘  │
└───────────────────────────────────────────┘
```

## Event Type Quick Reference

### `claude_code.api_request`
**Purpose**: Track API calls to Claude models  
**Key Fields**: `model`, `input_tokens`, `output_tokens`, `cache_read_tokens`, `cache_creation_tokens`, `cost_usd`, `duration_ms`

### `claude_code.tool_decision`
**Purpose**: Track tool usage decisions  
**Key Fields**: `tool_name`, `decision` (accept/reject), `source` (config/user_temporary/user_permanent/user_reject)

### `claude_code.tool_result`
**Purpose**: Track tool execution results  
**Key Fields**: `tool_name`, `success`, `duration_ms`, `tool_result_size_bytes`

### `claude_code.user_prompt`
**Purpose**: Track user prompts  
**Key Fields**: `prompt` (redacted), `prompt_length`

### `claude_code.api_error`
**Purpose**: Track API errors  
**Key Fields**: `model`, `error`, `status_code`, `attempt`, `duration_ms`

## Common Attributes (All Events)

- `event.timestamp`: ISO 8601 timestamp
- `organization.id`: Organization UUID
- `session.id`: Session UUID
- `terminal.type`: Terminal type
- `user.account_uuid`: User account UUID
- `user.email`: User email
- `user.id`: User ID (hash)

## Database Tables

| Table | Purpose | Key Columns |
|-------|---------|-------------|
| `users` | User identity | user_id, email, account_uuid, org_id |
| `employees` | HR metadata | email, full_name, practice, level, location |
| `organizations` | Organization info | org_id |
| `sessions` | Session metadata | session_id, user_id, start_time, end_time |
| `events` | Unified event log | event_id, event_type, session_id, timestamp, event_data |
| `api_requests` | API call details | event_id, model, tokens, cost_usd, duration_ms |
| `tool_decisions` | Tool decisions | event_id, tool_name, decision, source |
| `tool_results` | Tool results | event_id, tool_name, success, duration_ms |
| `user_prompts` | User prompts | event_id, prompt_length |
| `api_errors` | API errors | event_id, model, error, status_code |

## Key Analytics Queries

### Token Consumption by Practice
```sql
SELECT 
    e.practice,
    SUM(ar.input_tokens) as total_input_tokens,
    SUM(ar.output_tokens) as total_output_tokens,
    SUM(ar.cost_usd) as total_cost
FROM api_requests ar
JOIN users u ON ar.user_id = u.user_id
JOIN employees e ON u.email = e.email
GROUP BY e.practice;
```

### Peak Usage Times
```sql
SELECT 
    strftime('%H', timestamp) as hour,
    COUNT(*) as event_count
FROM events
GROUP BY hour
ORDER BY event_count DESC;
```

### Tool Success Rates
```sql
SELECT 
    tool_name,
    COUNT(*) as total_uses,
    SUM(CASE WHEN success = 1 THEN 1 ELSE 0 END) as successful_uses,
    AVG(duration_ms) as avg_duration_ms
FROM tool_results
GROUP BY tool_name;
```

### Cost by Model
```sql
SELECT 
    model,
    COUNT(*) as request_count,
    SUM(cost_usd) as total_cost,
    AVG(cost_usd) as avg_cost_per_request
FROM api_requests
GROUP BY model
ORDER BY total_cost DESC;
```

## Project Structure Quick View

```
claude-code-analytics/
├── src/
│   ├── ingestion/      # Data parsing and validation
│   ├── storage/         # Database schema and connection
│   ├── dal/             # Data access layer (repositories)
│   ├── analytics/       # Analytics service functions
│   ├── utils/           # Utilities and configuration
│   └── dashboard/       # Streamlit dashboard
├── scripts/             # Utility scripts
├── tests/               # Test suite
├── data/                # Data files and database
└── docs/                # Documentation
```

## Implementation Checklist

- [ ] Set up project structure
- [ ] Create database schema
- [ ] Implement JSONL parser
- [ ] Implement CSV parser
- [ ] Build data ingestion pipeline
- [ ] Create repository layer
- [ ] Implement analytics functions
- [ ] Build Streamlit dashboard
- [ ] Add visualizations
- [ ] Write tests
- [ ] Complete documentation
- [ ] Create LLM usage log
- [ ] Prepare insights presentation

## Key Metrics to Track

1. **Usage Metrics**
   - Total tokens (input/output/cache)
   - Total cost
   - Session count and duration
   - Event counts

2. **Cost Metrics**
   - Cost by model
   - Cost by practice/level
   - Cost trends over time
   - Cost per session/user

3. **Pattern Metrics**
   - Peak usage times
   - Tool usage frequency
   - Tool success rates
   - Model preferences

4. **Behavioral Metrics**
   - Sessions per user
   - Average session duration
   - User engagement patterns
   - Error rates

## Technology Stack

- **Python 3.9+**
- **SQLite** - Database
- **Streamlit** - Dashboard
- **pandas** - Data processing
- **plotly** - Interactive charts
- **pytest** - Testing

## File Naming Conventions

- **Modules**: `snake_case.py`
- **Classes**: `PascalCase`
- **Functions**: `snake_case()`
- **Constants**: `UPPER_SNAKE_CASE`
- **Database tables**: `snake_case`
- **Database columns**: `snake_case`

## Common Patterns

### Repository Pattern
```python
class UserRepository:
    def __init__(self, db: Database):
        self.db = db
    
    def get_by_id(self, user_id: str) -> User:
        # Implementation
        pass
    
    def create(self, user: User) -> User:
        # Implementation
        pass
```

### Analytics Function Pattern
```python
def calculate_token_usage_by_practice(
    db: Database, 
    start_date: datetime, 
    end_date: datetime
) -> pd.DataFrame:
    # Query and return DataFrame
    pass
```
