# Claude Code Analytics Platform

An end-to-end analytics platform that processes telemetry data from Claude Code sessions and produces insights about developer behavior and AI usage.

## Overview

This platform ingests, processes, and analyzes telemetry data from Claude Code usage, providing actionable insights through an interactive dashboard. It demonstrates proficiency in data processing, analytics, visualization, and clean architectural design.

## Features

- **Data Ingestion**: Parse and validate JSONL telemetry logs and CSV employee metadata
- **SQL Storage**: Efficient SQLite database with normalized and denormalized tables
- **Analytics Layer**: Comprehensive analytics for usage patterns, costs, and trends
- **Interactive Dashboard**: Streamlit-based dashboard for data exploration and visualization
- **Clean Architecture**: Modular, testable, and maintainable codebase

## Project Structure

```
claude-code-analytics/
├── src/                    # Source code
│   ├── ingestion/          # Data parsing and validation
│   ├── storage/            # Database schema and connection
│   ├── dal/                # Data access layer
│   ├── analytics/          # Analytics service functions
│   ├── utils/              # Utilities and configuration
│   └── dashboard/          # Streamlit dashboard
├── scripts/                # Utility scripts
├── tests/                  # Test suite
├── data/                   # Data files and database
└── docs/                   # Documentation
```

## Setup

### Prerequisites

- Python 3.9 or higher
- pip (Python package manager)

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd claude-code-analytics
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Initialize the database:
```bash
python scripts/setup_database.py
```

## Usage

### Data Ingestion

To ingest telemetry data and employee metadata:

```bash
python scripts/ingest_data.py \
    --telemetry path/to/telemetry_logs.jsonl \
    --employees path/to/employees.csv
```

Options:
- `--telemetry`: Path to telemetry_logs.jsonl file (required)
- `--employees`: Path to employees.csv file (required)
- `--db-path`: Custom database path (optional)
- `--batch-size`: Batch size for processing events (default: 1000)
- `--skip-employees`: Skip employee data ingestion
- `--skip-telemetry`: Skip telemetry data ingestion

### Running the Dashboard

```bash
streamlit run src/dashboard/main.py
```

## Data Format

### Telemetry Logs (JSONL)

Each line contains a batch of log events in CloudWatch format:
- Batch metadata: `logGroup`, `logStream`, `year`, `month`, `day`
- Log events: Array of events with `id`, `timestamp`, and `message` (JSON)

### Employee Metadata (CSV)

CSV file with columns:
- `email`: Employee email (matches telemetry data)
- `full_name`: Full name
- `practice`: Engineering practice
- `level`: Seniority level (L1-L10)
- `location`: Country

## Architecture

The platform follows a clean, layered architecture:

1. **Data Ingestion Layer**: Parses and validates input data
2. **Storage Layer**: SQLite database with normalized schema
3. **Data Access Layer**: Repository pattern for data access
4. **Analytics Service Layer**: Business logic for analytics
5. **Dashboard Layer**: Streamlit UI for visualization

See [ARCHITECTURE.md](ARCHITECTURE.md) for detailed architecture documentation.

## Database Schema

The database includes:
- **Core tables**: users, employees, organizations, sessions
- **Event tables**: events (unified), api_requests, tool_decisions, tool_results, user_prompts, api_errors
- **Indexes**: Strategic indexes for query performance

See [ARCHITECTURE.md](ARCHITECTURE.md) for complete schema details.

## Development

### Running Tests

```bash
pytest tests/
```

### Code Structure

- Follows Python best practices
- Type hints where appropriate
- Comprehensive logging
- Error handling and validation

## Documentation

- [ARCHITECTURE.md](ARCHITECTURE.md) - Architecture documentation
- [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) - Project structure details
- [ANALYSIS_SUMMARY.md](ANALYSIS_SUMMARY.md) - Data analysis summary
- [QUICK_REFERENCE.md](QUICK_REFERENCE.md) - Quick reference guide

## License

This project is part of a technical assignment for a GenAI internship program.

## Acknowledgments

Built as part of a technical assignment demonstrating proficiency in:
- Data processing and ETL pipelines
- Database design and optimization
- Analytics and insights generation
- Interactive dashboard development
- Clean architecture and software engineering practices
