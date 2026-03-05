# Project Structure

## Recommended Folder Structure

```
claude-code-analytics/
│
├── README.md                          # Project overview, setup instructions, usage
├── ARCHITECTURE.md                     # Architecture documentation (this file)
├── requirements.txt                    # Python dependencies
├── .gitignore                         # Git ignore rules
├── .env.example                        # Example environment variables (if needed)
│
├── data/                               # Data directory (gitignored)
│   ├── raw/                            # Raw input data
│   │   ├── telemetry_logs.jsonl       # Input telemetry logs
│   │   └── employees.csv               # Employee metadata
│   ├── processed/                      # Processed/intermediate data (optional)
│   └── database/                       # SQLite database location
│       └── analytics.db                # SQLite database file
│
├── src/                                # Source code
│   ├── __init__.py
│   │
│   ├── ingestion/                      # Data ingestion module
│   │   ├── __init__.py
│   │   ├── jsonl_parser.py             # JSONL log parser
│   │   ├── csv_parser.py               # CSV employee parser
│   │   ├── data_validator.py           # Data validation logic
│   │   └── ingestor.py                 # Main ingestion orchestrator
│   │
│   ├── storage/                        # Database layer
│   │   ├── __init__.py
│   │   ├── database.py                 # Database connection and setup
│   │   ├── schema.py                   # Schema definitions and migrations
│   │   └── models.py                   # SQLAlchemy models (if using ORM) or raw SQL
│   │
│   ├── dal/                            # Data Access Layer
│   │   ├── __init__.py
│   │   ├── repositories/               # Repository pattern implementations
│   │   │   ├── __init__.py
│   │   │   ├── user_repository.py
│   │   │   ├── session_repository.py
│   │   │   ├── event_repository.py
│   │   │   ├── api_request_repository.py
│   │   │   ├── tool_repository.py
│   │   │   └── employee_repository.py
│   │   └── query_builder.py            # Complex query builders
│   │
│   ├── analytics/                      # Analytics service layer
│   │   ├── __init__.py
│   │   ├── usage_analytics.py          # Usage metrics and statistics
│   │   ├── cost_analytics.py           # Cost analysis
│   │   ├── pattern_analytics.py        # Pattern detection
│   │   ├── trend_analytics.py          # Trend analysis
│   │   └── aggregators.py              # Data aggregation utilities
│   │
│   ├── utils/                          # Utility functions
│   │   ├── __init__.py
│   │   ├── logger.py                   # Logging configuration
│   │   ├── config.py                   # Configuration management
│   │   └── helpers.py                  # General helper functions
│   │
│   └── dashboard/                     # Streamlit dashboard
│       ├── __init__.py
│       ├── main.py                     # Main Streamlit app entry point
│       ├── pages/                      # Multi-page dashboard
│       │   ├── __init__.py
│       │   ├── overview.py             # Overview/dashboard home
│       │   ├── usage_metrics.py        # Usage metrics page
│       │   ├── cost_analysis.py        # Cost analysis page
│       │   ├── tool_analytics.py       # Tool usage page
│       │   ├── user_insights.py        # User behavior page
│       │   └── trends.py               # Trend analysis page
│       ├── components/                 # Reusable dashboard components
│       │   ├── __init__.py
│       │   ├── charts.py               # Chart components
│       │   ├── filters.py              # Filter components
│       │   └── metrics_cards.py        # Metric display cards
│       └── config.py                   # Dashboard configuration
│
├── scripts/                            # Utility scripts
│   ├── setup_database.py               # Initialize database schema
│   ├── ingest_data.py                  # Data ingestion script
│   └── generate_sample_data.py         # Generate test data (if needed)
│
├── tests/                              # Test suite
│   ├── __init__.py
│   ├── conftest.py                     # Pytest configuration
│   ├── test_ingestion/
│   │   ├── __init__.py
│   │   ├── test_jsonl_parser.py
│   │   └── test_data_validator.py
│   ├── test_storage/
│   │   ├── __init__.py
│   │   └── test_database.py
│   ├── test_analytics/
│   │   ├── __init__.py
│   │   └── test_usage_analytics.py
│   └── test_dashboard/
│       ├── __init__.py
│       └── test_components.py
│
├── docs/                               # Additional documentation
│   ├── API.md                          # API documentation (if applicable)
│   ├── LLM_USAGE_LOG.md                # LLM usage log (required by assignment)
│   └── INSIGHTS_PRESENTATION.md        # Insights summary (for presentation)
│
└── notebooks/                          # Jupyter notebooks (optional)
    ├── data_exploration.ipynb          # Initial data exploration
    └── analysis_experiments.ipynb      # Analysis experiments
```

## File Descriptions

### Root Level
- **README.md**: Main project documentation with setup, usage, and architecture overview
- **ARCHITECTURE.md**: Detailed architecture documentation
- **requirements.txt**: Python package dependencies
- **.gitignore**: Excludes data files, database, __pycache__, etc.

### Data Directory
- **raw/**: Input data files (should be gitignored or use git-lfs)
- **processed/**: Intermediate processed data (optional)
- **database/**: SQLite database file location

### Source Code (`src/`)

#### `ingestion/`
- **jsonl_parser.py**: Parses JSONL telemetry logs, extracts events
- **csv_parser.py**: Parses employee CSV metadata
- **data_validator.py**: Validates data integrity, handles missing fields
- **ingestor.py**: Orchestrates the ingestion process

#### `storage/`
- **database.py**: Database connection management, connection pooling
- **schema.py**: Schema definitions, table creation, migrations
- **models.py**: Data models (if using ORM) or SQL query definitions

#### `dal/` (Data Access Layer)
- **repositories/**: Repository pattern for each entity type
  - Abstracts database operations
  - Provides clean interface for data access
- **query_builder.py**: Builds complex SQL queries for analytics

#### `analytics/`
- **usage_analytics.py**: Token usage, session metrics, user activity
- **cost_analytics.py**: Cost calculations, cost by model/user/practice
- **pattern_analytics.py**: Usage patterns, peak times, tool preferences
- **trend_analytics.py**: Time-series trends, growth patterns
- **aggregators.py**: Reusable aggregation functions

#### `utils/`
- **logger.py**: Centralized logging configuration
- **config.py**: Configuration management (paths, database location, etc.)
- **helpers.py**: General utility functions

#### `dashboard/`
- **main.py**: Streamlit app entry point, navigation setup
- **pages/**: Individual dashboard pages
- **components/**: Reusable UI components (charts, filters, cards)

### Scripts
- **setup_database.py**: Initialize database schema
- **ingest_data.py**: CLI script to ingest data from files
- **generate_sample_data.py**: Generate test data (optional)

### Tests
- Organized by module with corresponding test files
- **conftest.py**: Shared pytest fixtures (database connections, test data)

### Documentation
- **LLM_USAGE_LOG.md**: Required by assignment - documents AI tool usage
- **INSIGHTS_PRESENTATION.md**: Summary of key insights for presentation

## Key Design Principles

1. **Separation of Concerns**: Each layer has a clear responsibility
2. **Modularity**: Components are loosely coupled and reusable
3. **Testability**: Clear interfaces enable easy testing
4. **Scalability**: Structure supports future enhancements
5. **Maintainability**: Clear organization and documentation

## Import Structure Example

```python
# Example import pattern
from src.ingestion.jsonl_parser import JSONLParser
from src.storage.database import Database
from src.dal.repositories.user_repository import UserRepository
from src.analytics.usage_analytics import UsageAnalytics
```

## Configuration Management

Use a centralized config file (`src/utils/config.py`) for:
- Database path
- Data file paths
- Logging configuration
- Feature flags
- Environment-specific settings

## Database Location

SQLite database should be in `data/database/analytics.db` to:
- Keep data separate from code
- Enable easy backup
- Support .gitignore for database files
