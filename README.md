# Claude Code Analytics Platform

An end-to-end analytics platform that processes telemetry data from Claude Code sessions and produces insights about developer behavior and AI usage. Built with Python, SQLite, Streamlit, and FastAPI.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Setup Instructions](#setup-instructions)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [API Documentation](#api-documentation)
- [Dashboard Guide](#dashboard-guide)
- [Development](#development)

## 🎯 Overview

This platform ingests, processes, and analyzes telemetry data from Claude Code usage, providing actionable insights through an interactive dashboard and REST API. It demonstrates proficiency in:

- Data processing and ETL pipelines
- Database design and optimization
- Analytics and insights generation
- Interactive dashboard development
- REST API development
- Clean architecture and software engineering practices

## ✨ Features

- **Data Ingestion**: Parse and validate JSONL telemetry logs and CSV employee metadata
- **SQL Storage**: Efficient SQLite database with normalized and denormalized tables
- **Analytics Layer**: Comprehensive analytics for usage patterns, costs, and trends
- **Interactive Dashboard**: Streamlit-based dashboard for data exploration and visualization
- **REST API**: FastAPI-based API for programmatic access to analytics data
- **Clean Architecture**: Modular, testable, and maintainable codebase

## 🏗️ Architecture

The platform follows a clean, layered architecture that separates concerns and enables scalability:

```
┌─────────────────────────────────────────────────────────┐
│              Streamlit Dashboard (UI Layer)              │
│              FastAPI REST API (API Layer)                │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│           Analytics Service Layer                        │
│  • Usage Analytics (tokens, sessions, users)             │
│  • Cost Analytics (by model, practice, time)            │
│  • Pattern Analytics (peak hours, tool usage)            │
│  • Trend Analytics (daily, weekly, monthly trends)       │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│           Data Access Layer (DAL)                        │
│  • Repository Pattern                                    │
│  • Query Builders                                        │
│  • Data Transformations                                  │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│           Data Ingestion Layer                           │
│  • JSONL Parser (telemetry logs)                         │
│  • CSV Parser (employee metadata)                        │
│  • Data Validation & Cleaning                            │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│           Storage Layer (SQLite)                         │
│  • Database Schema (normalized & denormalized)           │
│  • Connection Management                                 │
│  • Transaction Handling                                  │
└─────────────────────────────────────────────────────────┘
```

### Architecture Components

#### 1. **Data Ingestion Layer**
- Parses JSONL telemetry logs and CSV employee metadata
- Validates data integrity and handles malformed records
- Extracts and normalizes event data
- Batch inserts for efficient database operations

#### 2. **Storage Layer**
- SQLite database with normalized schema
- Strategic indexes for query performance
- Connection pooling and transaction management
- Data integrity constraints

#### 3. **Data Access Layer (DAL)**
- Repository pattern for each entity type
- Abstracts database operations
- Query builders for complex analytics
- Data transformation utilities

#### 4. **Analytics Service Layer**
- Token consumption analysis
- Cost analysis by user/practice/model
- Usage pattern detection (peak hours, tool preferences)
- Session analytics and user behavior
- Trend calculations (daily, weekly, monthly)
- Statistical aggregations

#### 5. **Presentation Layer**
- **Streamlit Dashboard**: Interactive visualizations with filtering
- **FastAPI REST API**: Programmatic access to analytics data

### Database Schema

The database includes:

- **Core Tables**: `users`, `employees`, `organizations`, `sessions`
- **Event Tables**: `events` (unified), `api_requests`, `tool_decisions`, `tool_results`, `user_prompts`, `api_errors`
- **Indexes**: Strategic indexes on frequently queried columns for performance



## 🚀 Setup Instructions

### Prerequisites

- **Python 3.9 or higher**
- **pip** (Python package manager)
- **Git** (for cloning the repository)

### Step 1: Clone the Repository

```bash
git clone https://github.com/Aleksandar1108/Claude-Code-Usage-Analytics-Platform.git
cd Claude-Code-Usage-Analytics-Platform
```

### Step 2: Create Virtual Environment (Recommended)

```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

This will install all required packages including:
- `streamlit` - Dashboard framework
- `fastapi` - REST API framework
- `uvicorn` - ASGI server
- `pandas` - Data manipulation
- `plotly` - Interactive visualizations
- `sqlite3` - Database (built-in with Python)

### Step 4: Initialize the Database

```bash
python scripts/setup_database.py
```

This creates the SQLite database schema in `data/database/analytics.db`.

### Step 5: Ingest Data

```bash
python scripts/ingest_data.py --generate-if-missing
```

This script will:
- Generate sample data if `output/telemetry_logs.jsonl` and `output/employees.csv` don't exist
- Parse and validate telemetry logs
- Load employee metadata
- Insert all data into the database

**Options:**
- `--telemetry`: Path to telemetry_logs.jsonl file (default: `output/telemetry_logs.jsonl`)
- `--employees`: Path to employees.csv file (default: `output/employees.csv`)
- `--db-path`: Custom database path (optional)
- `--batch-size`: Batch size for processing events (default: 1000)
- `--generate-if-missing`: Automatically generate data if input files are missing

## 📖 Usage

### Running the Platform

The platform consists of two main components that can run simultaneously:

#### 1. Start the REST API Server

**First, start the API server:**

```bash
python scripts/run_api.py
```

The API will be available at:
- **Base URL**: `http://localhost:8000`
- **Swagger UI**: `http://localhost:8000/docs` (Interactive API documentation)
- **ReDoc**: `http://localhost:8000/redoc` (Alternative documentation)

**Alternative ways to run the API:**

```bash
# Using uvicorn directly
uvicorn src.api.api_server:app --host 0.0.0.0 --port 8000 --reload

# Using Python module
python -m uvicorn src.api.api_server:app --host 0.0.0.0 --port 8000 --reload
```

#### 2. Start the Streamlit Dashboard

**In a separate terminal, start the dashboard:**

```bash
python -m streamlit run src/dashboard/main.py
```

The dashboard will automatically open in your browser at `http://localhost:8501`

**Note**: Keep both the API server and dashboard running. The dashboard can work independently, but the API provides programmatic access to the analytics data.

### Quick Start Summary

```bash
# Terminal 1: Start API Server
python scripts/run_api.py

# Terminal 2: Start Dashboard
python -m streamlit run src/dashboard/main.py
```

## 📊 Dashboard Guide

The Streamlit dashboard provides an interactive interface for exploring analytics data:

### Dashboard Pages

1. **📈 Overview**
   - Key metrics and summary visualizations
   - High-level insights and KPIs
   - Quick access to important data

2. **🔢 Token Usage Analytics**
   - Total tokens consumed (input/output/cache)
   - Token consumption by engineering practice
   - Token consumption by model
   - Token trends over time

3. **💰 Cost Analytics**
   - Total cost across all models
   - Cost breakdown by model
   - Cost by engineering practice
   - Cost efficiency metrics

4. **📊 Usage Patterns**
   - Peak usage hours (hourly patterns)
   - Tool usage statistics
   - Model preferences
   - API error rates

5. **👥 Session Analytics**
   - Number of sessions
   - Average session duration
   - User activity metrics
   - Session frequency trends

6. **📅 Daily Trends**
   - Activity over time
   - Weekly aggregations
   - Monthly aggregations
   - Growth patterns

### Dashboard Features

- **Interactive Date Range Filtering**: Filter data by custom date ranges
- **Practice Filtering**: Filter by engineering practice
- **Real-time Visualizations**: Plotly charts with hover information
- **Responsive Layout**: Works on different screen sizes
- **Multiple Chart Types**: Bar charts, line charts, pie charts, area charts
- **Detailed Data Tables**: Drill-down analysis with raw data

## 🔌 API Documentation

### Available Endpoints

#### Root Endpoint
```
GET /
```
Returns API information and available endpoints.

#### Token Analytics
```
GET /api/tokens
```
Returns token consumption summary.

**Query Parameters:**
- `start_date` (optional): Start date in YYYY-MM-DD format
- `end_date` (optional): End date in YYYY-MM-DD format
- `by_practice` (optional): Group by engineering practice (boolean)
- `by_model` (optional): Group by model (boolean)

**Example:**
```bash
curl http://localhost:8000/api/tokens?by_model=true
```

#### Cost Analytics
```
GET /api/cost
```
Returns cost analytics summary.

**Query Parameters:**
- `start_date` (optional): Start date in YYYY-MM-DD format
- `end_date` (optional): End date in YYYY-MM-DD format
- `by_model` (optional): Group by model (boolean)
- `by_practice` (optional): Group by engineering practice (boolean)

**Example:**
```bash
curl "http://localhost:8000/api/cost?start_date=2026-01-01&end_date=2026-01-31&by_model=true"
```

#### Session Metrics
```
GET /api/sessions
```
Returns session metrics and statistics.

**Query Parameters:**
- `start_date` (optional): Start date in YYYY-MM-DD format
- `end_date` (optional): End date in YYYY-MM-DD format

**Example:**
```bash
curl "http://localhost:8000/api/sessions?start_date=2026-01-01&end_date=2026-01-31"
```

#### User Analytics
```
GET /api/users
```
Returns employee activity analytics.

**Example:**
```bash
curl http://localhost:8000/api/users
```

#### Usage Patterns
```
GET /api/usage-patterns
```
Returns peak usage hours and tool usage statistics.

**Query Parameters:**
- `start_date` (optional): Start date in YYYY-MM-DD format
- `end_date` (optional): End date in YYYY-MM-DD format
- `include_tools` (optional): Include tool usage statistics (boolean)
- `include_models` (optional): Include model usage patterns (boolean)

**Example:**
```bash
curl "http://localhost:8000/api/usage-patterns?include_tools=true&include_models=true"
```

### API Documentation

- **Swagger UI**: Visit `http://localhost:8000/docs` for interactive API documentation
- **ReDoc**: Visit `http://localhost:8000/redoc` for alternative documentation

All responses are in JSON format. See the Swagger documentation for detailed request/response schemas.

## 📁 Project Structure

```
claude-code-analytics/
├── src/                    # Source code
│   ├── ingestion/          # Data parsing and validation
│   ├── storage/            # Database schema and connection
│   ├── dal/                # Data access layer (repositories)
│   ├── analytics/          # Analytics service functions
│   ├── utils/              # Utilities and configuration
│   ├── dashboard/          # Streamlit dashboard
│   └── api/                # REST API server (FastAPI)
├── scripts/                # Utility scripts
│   ├── setup_database.py   # Initialize database schema
│   ├── ingest_data.py      # Data ingestion script
│   └── run_api.py          # API server launcher
├── data/                   # Data files and database
│   ├── database/           # SQLite database location
│   └── output/             # Generated data files
├── tests/                  # Test suite
├── docs/                   # Documentation
├── requirements.txt        # Python dependencies
├── README.md               # This file
├── ARCHITECTURE.md         # Detailed architecture documentation
└── PROJECT_STRUCTURE.md    # Project structure details
```



## 🛠️ Development

### Running Tests

```bash
pytest tests/
```

### Code Structure

- Follows Python best practices
- Type hints where appropriate
- Comprehensive logging
- Error handling and validation
- Modular, testable design

### Data Format

#### Telemetry Logs (JSONL)

Each line contains a batch of log events in CloudWatch format:
- Batch metadata: `logGroup`, `logStream`, `year`, `month`, `day`
- Log events: Array of events with `id`, `timestamp`, and `message` (JSON)

#### Employee Metadata (CSV)

CSV file with columns:
- `email`: Employee email (matches telemetry data)
- `full_name`: Full name
- `practice`: Engineering practice
- `level`: Seniority level (L1-L10)
- `location`: Country


## 🐛 Troubleshooting

### Database Issues

If you encounter database errors:
1. Ensure the database is initialized: `python scripts/setup_database.py`
2. Check that data has been ingested: `python scripts/ingest_data.py`
3. Verify database file exists: `data/database/analytics.db`

### Import Errors

If you encounter import errors:
1. Ensure you're in the project root directory
2. Activate your virtual environment
3. Verify all dependencies are installed: `pip install -r requirements.txt`

### Port Already in Use

If port 8000 (API) or 8501 (Dashboard) is already in use:
- **API**: Change port in `scripts/run_api.py` or use `--port` flag with uvicorn
- **Dashboard**: Streamlit will automatically use the next available port

## 📝 License

This project is part of a technical assignment for a GenAI internship program.

## 🙏 Acknowledgments

Built as part of a technical assignment demonstrating proficiency in:
- Data processing and ETL pipelines
- Database design and optimization
- Analytics and insights generation
- Interactive dashboard development
- REST API development
- Clean architecture and software engineering practices

---

**For questions or issues, please refer to the documentation files or check the code comments.**
