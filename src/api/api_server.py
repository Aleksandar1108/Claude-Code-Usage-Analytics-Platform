"""FastAPI server for analytics API."""

from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import JSONResponse
from datetime import datetime, date
from typing import Optional, Dict, Any, List
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.storage.database import Database
from src.analytics.usage_analytics import UsageAnalytics
from src.analytics.cost_analytics import CostAnalytics
from src.analytics.pattern_analytics import PatternAnalytics
from src.utils.logger import setup_logger

logger = setup_logger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Claude Code Analytics API",
    description="REST API for programmatic access to Claude Code telemetry analytics",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Initialize database and analytics
db = Database()
usage_analytics = UsageAnalytics(db)
cost_analytics = CostAnalytics(db)
pattern_analytics = PatternAnalytics(db)


def convert_dataframe_to_dict(df) -> List[Dict[str, Any]]:
    """Convert pandas DataFrame to list of dictionaries."""
    import pandas as pd
    if df.empty:
        return []
    # Replace NaN and NA with None for JSON serialization
    return df.replace({float('nan'): None, pd.NA: None}).to_dict('records')


@app.get("/")
async def root():
    """
    Root endpoint - API information.
    
    Returns:
        API description and available endpoints
    """
    return {
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


@app.get("/api/tokens")
async def get_tokens(
    start_date: Optional[date] = Query(None, description="Start date filter (YYYY-MM-DD)"),
    end_date: Optional[date] = Query(None, description="End date filter (YYYY-MM-DD)"),
    by_practice: bool = Query(False, description="Include breakdown by practice")
):
    """
    Get token consumption summary.
    
    Args:
        start_date: Optional start date filter
        end_date: Optional end date filter
        by_practice: Include breakdown by practice
    
    Returns:
        Token consumption metrics
    """
    try:
        # Convert date to datetime
        start_datetime = datetime.combine(start_date, datetime.min.time()) if start_date else None
        end_datetime = datetime.combine(end_date, datetime.max.time()) if end_date else None
        
        # Validate date range
        if start_date and end_date and start_date > end_date:
            raise HTTPException(status_code=400, detail="Start date must be before end date")
        
        # Get summary
        summary = usage_analytics.get_token_consumption_summary(start_datetime, end_datetime)
        
        response = {
            "summary": summary,
            "filters": {
                "start_date": start_date.isoformat() if start_date else None,
                "end_date": end_date.isoformat() if end_date else None
            }
        }
        
        # Add practice breakdown if requested
        if by_practice:
            practice_df = usage_analytics.get_token_consumption_by_practice(start_datetime, end_datetime)
            response["by_practice"] = convert_dataframe_to_dict(practice_df)
        
        return response
    
    except Exception as e:
        logger.error(f"Error in get_tokens: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@app.get("/api/cost")
async def get_cost(
    start_date: Optional[date] = Query(None, description="Start date filter (YYYY-MM-DD)"),
    end_date: Optional[date] = Query(None, description="End date filter (YYYY-MM-DD)"),
    by_model: bool = Query(False, description="Include breakdown by model"),
    by_practice: bool = Query(False, description="Include breakdown by practice")
):
    """
    Get cost analytics summary.
    
    Args:
        start_date: Optional start date filter
        end_date: Optional end date filter
        by_model: Include breakdown by model
        by_practice: Include breakdown by practice
    
    Returns:
        Cost analytics metrics
    """
    try:
        # Convert date to datetime
        start_datetime = datetime.combine(start_date, datetime.min.time()) if start_date else None
        end_datetime = datetime.combine(end_date, datetime.max.time()) if end_date else None
        
        # Validate date range
        if start_date and end_date and start_date > end_date:
            raise HTTPException(status_code=400, detail="Start date must be before end date")
        
        # Get summary
        summary = cost_analytics.get_cost_summary(start_datetime, end_datetime)
        
        response = {
            "summary": summary,
            "filters": {
                "start_date": start_date.isoformat() if start_date else None,
                "end_date": end_date.isoformat() if end_date else None
            }
        }
        
        # Add model breakdown if requested
        if by_model:
            model_df = cost_analytics.get_cost_by_model(start_datetime, end_datetime)
            response["by_model"] = convert_dataframe_to_dict(model_df)
        
        # Add practice breakdown if requested
        if by_practice:
            practice_df = cost_analytics.get_cost_by_practice(start_datetime, end_datetime)
            response["by_practice"] = convert_dataframe_to_dict(practice_df)
        
        return response
    
    except Exception as e:
        logger.error(f"Error in get_cost: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@app.get("/api/sessions")
async def get_sessions(
    start_date: Optional[date] = Query(None, description="Start date filter (YYYY-MM-DD)"),
    end_date: Optional[date] = Query(None, description="End date filter (YYYY-MM-DD)")
):
    """
    Get session metrics.
    
    Args:
        start_date: Optional start date filter
        end_date: Optional end date filter
    
    Returns:
        Session analytics metrics
    """
    try:
        # Convert date to datetime
        start_datetime = datetime.combine(start_date, datetime.min.time()) if start_date else None
        end_datetime = datetime.combine(end_date, datetime.max.time()) if end_date else None
        
        # Validate date range
        if start_date and end_date and start_date > end_date:
            raise HTTPException(status_code=400, detail="Start date must be before end date")
        
        # Get session metrics
        metrics = usage_analytics.get_session_metrics(start_datetime, end_datetime)
        
        return {
            "metrics": metrics,
            "filters": {
                "start_date": start_date.isoformat() if start_date else None,
                "end_date": end_date.isoformat() if end_date else None
            }
        }
    
    except Exception as e:
        logger.error(f"Error in get_sessions: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@app.get("/api/users")
async def get_users():
    """
    Get employee activity analytics.
    
    Returns:
        User activity summary
    """
    try:
        # Get user activity summary
        user_activity = usage_analytics.get_user_activity_summary()
        
        # Convert DataFrame to list of dicts
        users_data = convert_dataframe_to_dict(user_activity)
        
        return {
            "users": users_data,
            "total_users": len(users_data)
        }
    
    except Exception as e:
        logger.error(f"Error in get_users: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@app.get("/api/usage-patterns")
async def get_usage_patterns(
    start_date: Optional[date] = Query(None, description="Start date filter (YYYY-MM-DD)"),
    end_date: Optional[date] = Query(None, description="End date filter (YYYY-MM-DD)"),
    include_tools: bool = Query(True, description="Include tool usage statistics"),
    include_models: bool = Query(False, description="Include model usage patterns")
):
    """
    Get usage patterns including peak hours and tool usage.
    
    Args:
        start_date: Optional start date filter
        end_date: Optional end date filter
        include_tools: Include tool usage statistics
        include_models: Include model usage patterns
    
    Returns:
        Usage patterns including peak hours and tool statistics
    """
    try:
        # Convert date to datetime
        start_datetime = datetime.combine(start_date, datetime.min.time()) if start_date else None
        end_datetime = datetime.combine(end_date, datetime.max.time()) if end_date else None
        
        # Validate date range
        if start_date and end_date and start_date > end_date:
            raise HTTPException(status_code=400, detail="Start date must be before end date")
        
        # Get peak usage hours
        peak_hours_df = pattern_analytics.get_peak_usage_hours(start_datetime, end_datetime)
        peak_hours = convert_dataframe_to_dict(peak_hours_df)
        
        response = {
            "peak_usage_hours": peak_hours,
            "filters": {
                "start_date": start_date.isoformat() if start_date else None,
                "end_date": end_date.isoformat() if end_date else None
            }
        }
        
        # Add tool usage if requested
        if include_tools:
            tool_patterns_df = pattern_analytics.get_tool_usage_patterns()
            response["tool_usage"] = convert_dataframe_to_dict(tool_patterns_df)
        
        # Add model usage if requested
        if include_models:
            model_patterns_df = pattern_analytics.get_model_usage_patterns(start_datetime, end_datetime)
            response["model_usage"] = convert_dataframe_to_dict(model_patterns_df)
        
        return response
    
    except Exception as e:
        logger.error(f"Error in get_usage_patterns: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
