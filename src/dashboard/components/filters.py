"""Filter components for the dashboard."""

import streamlit as st
from datetime import datetime, timedelta
from typing import Optional, Tuple
from src.dashboard.config import DEFAULT_DAYS_BACK


def date_range_filter() -> Tuple[Optional[datetime], Optional[datetime]]:
    """
    Create a date range filter in the sidebar.
    
    Returns:
        Tuple of (start_date, end_date) or (None, None) if not set
    """
    st.sidebar.markdown("""
    <div style='padding: 1.5rem 0 1rem 0; border-top: 2px solid #e2e8f0; margin-top: 1.5rem;'>
        <h3 style='color: #1e293b; margin: 0 0 1rem 0; font-size: 1rem; font-weight: 600;'>
            📅 Date Range Filter
        </h3>
    </div>
    """, unsafe_allow_html=True)
    
    use_filter = st.sidebar.checkbox("Filter by date range", value=False, key="use_date_filter")
    
    if not use_filter:
        return None, None
    
    # Get date range
    col1, col2 = st.sidebar.columns(2)
    
    with col1:
        start_date = st.date_input(
            "Start Date",
            value=datetime.now().date() - timedelta(days=DEFAULT_DAYS_BACK),
            key="start_date"
        )
    
    with col2:
        end_date = st.date_input(
            "End Date",
            value=datetime.now().date(),
            key="end_date"
        )
    
    # Validate date range
    if start_date > end_date:
        st.sidebar.error("Start date must be before end date")
        return None, None
    
    # Convert to datetime
    start_datetime = datetime.combine(start_date, datetime.min.time())
    end_datetime = datetime.combine(end_date, datetime.max.time())
    
    return start_datetime, end_datetime


def practice_filter(practices: list) -> Optional[str]:
    """
    Create a practice filter in the sidebar.
    
    Args:
        practices: List of available practices
    
    Returns:
        Selected practice or None
    """
    if not practices:
        return None
    
    st.sidebar.header("👥 Filter by Practice")
    selected = st.sidebar.selectbox(
        "Select Practice",
        options=["All"] + practices,
        key="practice_filter"
    )
    
    return None if selected == "All" else selected


def refresh_button() -> bool:
    """
    Create a refresh button in the sidebar.
    
    Returns:
        True if button was clicked
    """
    st.sidebar.header("🔄 Actions")
    return st.sidebar.button("Refresh Data", key="refresh_button")
