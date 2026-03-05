# Claude Code Analytics Platform - Architecture Proposal

## 1. Data Structure Analysis

### 1.1 Telemetry Logs (JSONL)
Each log batch contains:
- **Batch metadata**: `messageType`, `logGroup`, `logStream`, `year`, `month`, `day`
- **Log Events**: Array of events with:
  - `id`: Unique event ID
  - `timestamp`: Epoch milliseconds
  - `message`: JSON string containing the event

### 1.2 Event Types
1. **`claude_code.api_request`**: API calls to Claude models
   - Fields: `model`, `input_tokens`, `output_tokens`, `cache_read_tokens`, `cache_creation_tokens`, `cost_usd`, `duration_ms`
   
2. **`claude_code.tool_decision`**: Tool usage decisions
   - Fields: `tool_name`, `decision` (accept/reject), `source` (config/user_temporary/user_permanent/user_reject)
   
3. **`claude_code.tool_result`**: Tool execution results
   - Fields: `tool_name`, `success`, `duration_ms`, `decision_source`, `decision_type`, `tool_result_size_bytes` (optional)
   
4. **`claude_code.user_prompt`**: User prompts to Claude
   - Fields: `prompt` (redacted), `prompt_length`
   
5. **`claude_code.api_error`**: API errors
   - Fields: `model`, `error`, `status_code`, `attempt`, `duration_ms`

### 1.3 Common Attributes (All Events)
- `event.timestamp`: ISO 8601 timestamp
- `organization.id`: Organization UUID
- `session.id`: Session UUID
- `terminal.type`: Terminal type (vscode, pycharm, etc.)
- `user.account_uuid`: User account UUID
- `user.email`: User email
- `user.id`: User ID (hash)

### 1.4 Resource Attributes (Environment Info)
- `host.arch`: Architecture (arm64, x86_64)
- `host.name`: Hostname
- `os.type`: OS type (darwin, linux, windows)
- `os.version`: OS version
- `service.name`: Service name
- `service.version`: Claude Code version
- `user.practice`: Engineering practice
- `user.profile`: User profile
- `user.serial`: Device serial

### 1.5 Employee Metadata (CSV)
- `email`: Employee email (matches telemetry)
- `full_name`: Full name
- `practice`: Engineering practice
- `level`: Seniority level (L1-L10)
- `location`: Country

## 2. Main Entities

### 2.1 Core Entities
1. **Users**: Identified by `user.id` and `user.email`
   - Attributes: account_uuid, org_id, email
   - Linked to: Employees, Sessions, Events

2. **Sessions**: Identified by `session.id`
   - Attributes: user_id, start_time, end_time, duration
   - Linked to: User, Events

3. **Events**: Individual telemetry events
   - Types: api_request, tool_decision, tool_result, user_prompt, api_error
   - Attributes: timestamp, session_id, user_id, event-specific fields

4. **Employees**: Human resource metadata
   - Attributes: email, full_name, practice, level, location
   - Linked to: Users (via email)

5. **Organizations**: Identified by `organization.id`
   - Attributes: org_id
   - Linked to: Users, Events

6. **Tools**: Tool usage patterns
   - Attributes: tool_name, usage_count, success_rate, avg_duration
   - Derived from: tool_decision and tool_result events

7. **Models**: Claude model usage
   - Attributes: model_name, usage_count, total_cost, avg_tokens
   - Derived from: api_request events

## 3. Database Schema Design (SQLite)

### 3.1 Normalized Tables

```sql
-- Users table
CREATE TABLE users (
    user_id TEXT PRIMARY KEY,
    account_uuid TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    org_id TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Employees table (HR metadata)
CREATE TABLE employees (
    email TEXT PRIMARY KEY,
    full_name TEXT NOT NULL,
    practice TEXT NOT NULL,
    level TEXT NOT NULL,
    location TEXT NOT NULL,
    FOREIGN KEY (email) REFERENCES users(email)
);

-- Organizations table
CREATE TABLE organizations (
    org_id TEXT PRIMARY KEY,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Sessions table
CREATE TABLE sessions (
    session_id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    org_id TEXT NOT NULL,
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP,
    duration_seconds INTEGER,
    terminal_type TEXT,
    hostname TEXT,
    os_type TEXT,
    os_version TEXT,
    claude_version TEXT,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (org_id) REFERENCES organizations(org_id)
);

-- Events table (unified event storage)
CREATE TABLE events (
    event_id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_type TEXT NOT NULL,
    session_id TEXT NOT NULL,
    user_id TEXT NOT NULL,
    org_id TEXT NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    -- Common fields
    terminal_type TEXT,
    -- Event-specific JSON blob for flexibility
    event_data JSON NOT NULL,
    FOREIGN KEY (session_id) REFERENCES sessions(session_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (org_id) REFERENCES organizations(org_id)
);

-- API Requests (denormalized for fast analytics)
CREATE TABLE api_requests (
    event_id INTEGER PRIMARY KEY,
    session_id TEXT NOT NULL,
    user_id TEXT NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    model TEXT NOT NULL,
    input_tokens INTEGER,
    output_tokens INTEGER,
    cache_read_tokens INTEGER,
    cache_creation_tokens INTEGER,
    cost_usd REAL,
    duration_ms INTEGER,
    FOREIGN KEY (session_id) REFERENCES sessions(session_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- Tool Decisions
CREATE TABLE tool_decisions (
    event_id INTEGER PRIMARY KEY,
    session_id TEXT NOT NULL,
    user_id TEXT NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    tool_name TEXT NOT NULL,
    decision TEXT NOT NULL,  -- accept/reject
    source TEXT NOT NULL,     -- config/user_temporary/user_permanent/user_reject
    FOREIGN KEY (session_id) REFERENCES sessions(session_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- Tool Results
CREATE TABLE tool_results (
    event_id INTEGER PRIMARY KEY,
    session_id TEXT NOT NULL,
    user_id TEXT NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    tool_name TEXT NOT NULL,
    success BOOLEAN NOT NULL,
    duration_ms INTEGER,
    result_size_bytes INTEGER,
    FOREIGN KEY (session_id) REFERENCES sessions(session_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- User Prompts
CREATE TABLE user_prompts (
    event_id INTEGER PRIMARY KEY,
    session_id TEXT NOT NULL,
    user_id TEXT NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    prompt_length INTEGER,
    FOREIGN KEY (session_id) REFERENCES sessions(session_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- API Errors
CREATE TABLE api_errors (
    event_id INTEGER PRIMARY KEY,
    session_id TEXT NOT NULL,
    user_id TEXT NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    model TEXT,
    error_message TEXT,
    status_code TEXT,
    attempt INTEGER,
    duration_ms INTEGER,
    FOREIGN KEY (session_id) REFERENCES sessions(session_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- Indexes for performance
CREATE INDEX idx_events_session_id ON events(session_id);
CREATE INDEX idx_events_user_id ON events(user_id);
CREATE INDEX idx_events_timestamp ON events(timestamp);
CREATE INDEX idx_events_type ON events(event_type);
CREATE INDEX idx_api_requests_timestamp ON api_requests(timestamp);
CREATE INDEX idx_api_requests_model ON api_requests(model);
CREATE INDEX idx_sessions_user_id ON sessions(user_id);
CREATE INDEX idx_sessions_start_time ON sessions(start_time);
```

## 4. System Architecture

### 4.1 Layer Structure

```
┌─────────────────────────────────────────────────────────┐
│                   Streamlit Dashboard                    │
│              (Presentation/Visualization Layer)          │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│              Analytics Service Layer                     │
│  - Usage Analytics                                       │
│  - Trend Analysis                                        │
│  - Statistical Insights                                  │
│  - Aggregations                                          │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│              Data Access Layer (DAL)                     │
│  - Repository Pattern                                    │
│  - Query Builders                                        │
│  - Data Transformations                                  │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│              Data Ingestion Layer                        │
│  - JSONL Parser                                          │
│  - CSV Parser                                            │
│  - Data Validation                                       │
│  - Data Cleaning                                         │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│              Storage Layer (SQLite)                      │
│  - Database Schema                                       │
│  - Connection Management                                 │
│  - Transaction Handling                                  │
└─────────────────────────────────────────────────────────┘
```

### 4.2 Component Responsibilities

#### **Data Ingestion Layer**
- Parse JSONL telemetry logs
- Parse CSV employee metadata
- Validate data integrity
- Handle malformed records gracefully
- Extract and normalize event data
- Create/update database records

#### **Storage Layer**
- SQLite database management
- Schema initialization
- Connection pooling
- Transaction management
- Data integrity constraints

#### **Data Access Layer (DAL)**
- Repository pattern for each entity
- Abstract database operations
- Query builders for complex analytics
- Data transformation utilities
- Caching strategies (optional)

#### **Analytics Service Layer**
- Token consumption analysis
- Cost analysis by user/practice/model
- Usage pattern detection
- Peak usage time analysis
- Tool usage statistics
- Session analytics
- Trend calculations
- Statistical aggregations

#### **Dashboard Layer (Streamlit)**
- Interactive visualizations
- Filtering and drill-down capabilities
- Real-time data refresh
- Export capabilities
- Multi-page navigation
- Responsive design

## 5. Key Analytics & Insights

### 5.1 Usage Metrics
- Total tokens consumed (input/output/cache)
- Total cost by model, user, practice, time period
- Average session duration
- Sessions per user
- Events per session

### 5.2 Pattern Analysis
- Peak usage times (hourly/daily patterns)
- Most used tools
- Tool success rates
- Model preferences by practice/level
- API error rates and types
- User engagement patterns

### 5.3 Behavioral Insights
- Token consumption by user role (practice/level)
- Cost efficiency by model
- Tool adoption rates
- Session frequency trends
- Geographic usage patterns
- Terminal/OS preferences

### 5.4 Trend Analysis
- Daily/weekly/monthly trends
- Growth patterns
- Seasonal variations
- Model migration patterns
- Tool usage evolution

## 6. Technology Stack

- **Language**: Python 3.9+
- **Database**: SQLite (for portability and simplicity)
- **Dashboard**: Streamlit
- **Data Processing**: pandas, numpy
- **Visualization**: plotly, matplotlib
- **Data Validation**: pydantic (optional)
- **Testing**: pytest
- **Logging**: Python logging module

## 7. Error Handling Strategy

- **Data Validation**: Validate all input data before insertion
- **Graceful Degradation**: Handle missing fields with defaults
- **Transaction Rollback**: Use transactions for batch operations
- **Logging**: Comprehensive logging for debugging
- **User Feedback**: Clear error messages in dashboard

## 8. Performance Considerations

- **Batch Inserts**: Use executemany for bulk inserts
- **Indexes**: Strategic indexes on frequently queried columns
- **Query Optimization**: Use EXPLAIN QUERY PLAN for slow queries
- **Caching**: Cache frequently accessed aggregations
- **Pagination**: Implement pagination for large result sets
- **Connection Pooling**: Reuse database connections

## 9. Future Enhancements (Optional)

- **Real-time Processing**: Kafka/Redis for streaming
- **ML Components**: Anomaly detection, usage forecasting
- **API Endpoints**: FastAPI for programmatic access
- **Advanced Analytics**: Statistical tests, correlation analysis
- **Export Features**: PDF reports, CSV exports
- **Authentication**: User authentication for dashboard
- **Multi-tenant Support**: Organization-level isolation
