"""Main Streamlit dashboard application."""

import streamlit as st
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.storage.database import Database
from src.analytics.usage_analytics import UsageAnalytics
from src.analytics.cost_analytics import CostAnalytics
from src.analytics.pattern_analytics import PatternAnalytics
from src.analytics.trend_analytics import TrendAnalytics
from src.dashboard.config import PAGE_TITLE, PAGE_ICON, LAYOUT, CUSTOM_CSS
from src.utils.logger import setup_logger

logger = setup_logger(__name__)

# Page configuration
st.set_page_config(
    page_title=PAGE_TITLE,
    page_icon=PAGE_ICON,
    layout=LAYOUT,
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': "Claude Code Analytics Platform - GenAI Internship Project"
    }
)

# Apply custom CSS
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# Initialize session state
if 'db' not in st.session_state:
    st.session_state.db = Database()
    st.session_state.usage_analytics = UsageAnalytics(st.session_state.db)
    st.session_state.cost_analytics = CostAnalytics(st.session_state.db)
    st.session_state.pattern_analytics = PatternAnalytics(st.session_state.db)
    st.session_state.trend_analytics = TrendAnalytics(st.session_state.db)


def main():
    """Main dashboard application."""
    
    # Enhanced header with gradient styling
    st.markdown("""
    <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                padding: 2rem 1rem;
                border-radius: 0.75rem;
                margin-bottom: 2rem;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);'>
        <h1 style='color: white; margin: 0; font-size: 2.5rem; font-weight: 700;'>
            📊 Claude Code Analytics Platform
        </h1>
        <p style='color: rgba(255,255,255,0.9); margin: 0.5rem 0 0 0; font-size: 1.1rem;'>
            Comprehensive analytics for AI-assisted software engineering
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Enhanced sidebar navigation with icons
    st.sidebar.markdown("""
    <div style='padding: 1.5rem 0 1rem 0; border-bottom: 2px solid #e2e8f0; margin-bottom: 1.5rem;'>
        <h2 style='color: #1e293b; margin: 0; font-size: 1.5rem; font-weight: 700; letter-spacing: -0.01em;'>
            Navigation
        </h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Navigation pages with icons
    navigation_pages = {
        "Overview": "📈",
        "Token Usage Analytics": "🔢",
        "Cost Analytics": "💰",
        "Usage Patterns": "📊",
        "Session Analytics": "🕐",
        "Daily Trends": "📅"
    }
    
    # Create navigation options with icons
    nav_options = [f"{icon} {name}" for name, icon in navigation_pages.items()]
    
    # Main Analytics section
    st.sidebar.markdown("""
    <div style='font-size: 0.75rem; font-weight: 600; text-transform: uppercase; 
         letter-spacing: 0.1em; color: #94a3b8; padding: 0.5rem 1rem; margin-bottom: 0.75rem;'>
        Main Analytics
    </div>
    """, unsafe_allow_html=True)
    
    page_selection = st.sidebar.radio(
        "Select Page",
        nav_options,
        label_visibility="collapsed",
        key="main_nav"
    )
    
    # Extract page name (remove icon)
    page = page_selection.split(" ", 1)[1] if " " in page_selection else page_selection
    
    # Date range filter (available on all pages)
    from src.dashboard.components.filters import date_range_filter
    start_date, end_date = date_range_filter()
    
    # Route to appropriate page
    if page == "Overview":
        show_overview(start_date, end_date)
    elif page == "Token Usage Analytics":
        show_token_analytics(start_date, end_date)
    elif page == "Cost Analytics":
        show_cost_analytics(start_date, end_date)
    elif page == "Usage Patterns":
        show_usage_patterns(start_date, end_date)
    elif page == "Session Analytics":
        show_session_analytics(start_date, end_date)
    elif page == "Daily Trends":
        show_daily_trends(start_date, end_date)


def show_overview(start_date, end_date):
    """Show overview dashboard."""
    st.markdown("""
    <div style='margin-bottom: 2rem;'>
        <h2 style='color: #1e293b; font-size: 2rem; font-weight: 700; margin-bottom: 0.5rem;'>
            📈 Overview Dashboard
        </h2>
        <p style='color: #64748b; font-size: 1rem; margin: 0;'>
            High-level insights and key performance indicators
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Get analytics instances
    usage = st.session_state.usage_analytics
    cost = st.session_state.cost_analytics
    pattern = st.session_state.pattern_analytics
    trend = st.session_state.trend_analytics
    
    # Enhanced key metrics with icons
    from src.dashboard.components.metric_cards import metric_card
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        token_summary = usage.get_token_consumption_summary(start_date, end_date)
        metric_card(
            value=f"{token_summary.get('total_tokens', 0):,}",
            label="Total Tokens",
            icon="🔢",
            help_text="Total tokens consumed across all API requests"
        )
    
    with col2:
        cost_summary = cost.get_cost_summary(start_date, end_date)
        metric_card(
            value=f"${cost_summary.get('total_cost_usd', 0):,.2f}",
            label="Total Cost",
            icon="💰",
            help_text="Total cost in USD for all API requests"
        )
    
    with col3:
        session_metrics = usage.get_session_metrics(start_date, end_date)
        metric_card(
            value=f"{session_metrics.get('total_sessions', 0):,}",
            label="Total Sessions",
            icon="🕐",
            help_text="Total number of coding sessions"
        )
    
    with col4:
        trend_summary = trend.get_trend_summary("events", start_date, end_date)
        metric_card(
            value=f"{trend_summary.get('avg_daily', 0):.0f}",
            label="Daily Avg Events",
            icon="📊",
            help_text="Average number of events per day"
        )
    
    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
    
    # Charts row 1 - Cost and Tokens
    st.markdown("### 💰 Cost & Token Analytics")
    col1, col2 = st.columns(2)
    
    with col1:
        cost_by_model = cost.get_cost_by_model(start_date, end_date)
        if not cost_by_model.empty:
            from src.dashboard.components.charts import create_bar_chart
            fig = create_bar_chart(
                cost_by_model,
                x="model",
                y="total_cost_usd",
                title="Cost by Model",
                x_label="Model",
                y_label="Cost (USD)",
                top_n=10
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No cost data available for the selected date range.")
    
    with col2:
        tokens_by_practice = usage.get_token_consumption_by_practice(start_date, end_date)
        if not tokens_by_practice.empty:
            from src.dashboard.components.charts import create_bar_chart
            fig = create_bar_chart(
                tokens_by_practice,
                x="practice",
                y="total_tokens",
                title="Token Consumption by Practice",
                x_label="Practice",
                y_label="Total Tokens",
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No token data available for the selected date range.")
    
    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
    
    # Charts row 2 - Usage Patterns
    st.markdown("### 📊 Usage Patterns & Trends")
    col1, col2 = st.columns(2)
    
    with col1:
        peak_hours = pattern.get_peak_usage_hours(start_date, end_date)
        if not peak_hours.empty:
            from src.dashboard.components.charts import create_bar_chart
            fig = create_bar_chart(
                peak_hours,
                x="hour",
                y="event_count",
                title="Peak Usage Hours",
                x_label="Hour (24-hour format)",
                y_label="Event Count",
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Find and display peak hour
            max_hour = peak_hours.loc[peak_hours['event_count'].idxmax()]
            st.success(f"📌 **Peak hour:** {int(max_hour['hour'])}:00 with {max_hour['event_count']:,} events")
        else:
            st.info("No usage pattern data available.")
    
    with col2:
        daily_trends = trend.get_daily_trends("events", start_date, end_date)
        if not daily_trends.empty:
            from src.dashboard.components.charts import create_line_chart
            count_col = 'count' if 'count' in daily_trends.columns else daily_trends.columns[-1]
            fig = create_line_chart(
                daily_trends,
                x="date",
                y=count_col,
                title="Daily Activity Trend",
                x_label="Date",
                y_label="Event Count",
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No trend data available for the selected date range.")


def show_token_analytics(start_date, end_date):
    """Show token usage analytics page."""
    st.markdown("""
    <div style='margin-bottom: 2rem;'>
        <h2 style='color: #1e293b; font-size: 2rem; font-weight: 700; margin-bottom: 0.5rem;'>
            🔢 Token Usage Analytics
        </h2>
        <p style='color: #64748b; font-size: 1rem; margin: 0;'>
            Detailed analysis of token consumption across models, practices, and users
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    usage = st.session_state.usage_analytics
    
    # Total token summary with enhanced cards
    st.markdown("### 📊 Total Token Consumption")
    token_summary = usage.get_token_consumption_summary(start_date, end_date)
    
    from src.dashboard.components.metric_cards import metric_card
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        metric_card(
            value=f"{token_summary.get('total_tokens', 0):,}",
            label="Total Tokens",
            icon="🔢"
        )
    
    with col2:
        metric_card(
            value=f"{token_summary.get('total_input_tokens', 0):,}",
            label="Input Tokens",
            icon="⬇️"
        )
    
    with col3:
        metric_card(
            value=f"{token_summary.get('total_output_tokens', 0):,}",
            label="Output Tokens",
            icon="⬆️"
        )
    
    with col4:
        cache_tokens = token_summary.get('total_cache_read_tokens', 0) + token_summary.get('total_cache_creation_tokens', 0)
        metric_card(
            value=f"{cache_tokens:,}",
            label="Cache Tokens",
            icon="💾"
        )
    
    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
    
    # Tokens by practice
    st.markdown("### 🏢 Token Consumption by Practice")
    tokens_by_practice = usage.get_token_consumption_by_practice(start_date, end_date)
    
    if not tokens_by_practice.empty:
        col1, col2 = st.columns(2)
        
        with col1:
            from src.dashboard.components.charts import create_bar_chart
            fig = create_bar_chart(
                tokens_by_practice,
                x="practice",
                y="total_tokens",
                title="Total Tokens by Practice",
                y_label="Total Tokens",
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            from src.dashboard.components.charts import create_pie_chart
            fig = create_pie_chart(
                tokens_by_practice,
                names="practice",
                values="total_tokens",
                title="Token Distribution by Practice"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Show table
        st.dataframe(
            tokens_by_practice[["practice", "total_tokens", "unique_users"]].style.format({
                "total_tokens": "{:,.0f}",
                "unique_users": "{:,.0f}"
            }),
            use_container_width=True
        )
    
    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
    
    # Tokens by model
    st.markdown("### 🤖 Token Consumption by Model")
    cost_analytics = st.session_state.cost_analytics
    cost_by_model = cost_analytics.get_cost_by_model(start_date, end_date)
    
    if not cost_by_model.empty and "total_input_tokens" in cost_by_model.columns:
        # Calculate total tokens per model
        cost_by_model["total_tokens"] = (
            cost_by_model["total_input_tokens"] + 
            cost_by_model["total_output_tokens"]
        )
        
        from src.dashboard.components.charts import create_bar_chart
        fig = create_bar_chart(
            cost_by_model,
            x="model",
            y="total_tokens",
            title="Total Tokens by Model",
            y_label="Total Tokens",
            top_n=10
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Show table
        display_cols = ["model", "total_tokens", "total_input_tokens", "total_output_tokens"]
        available_cols = [col for col in display_cols if col in cost_by_model.columns]
        st.dataframe(
            cost_by_model[available_cols].style.format({
                col: "{:,.0f}" for col in available_cols if col != "model"
            }),
            use_container_width=True
        )


def show_cost_analytics(start_date, end_date):
    """Show cost analytics page."""
    st.markdown("""
    <div style='margin-bottom: 2rem;'>
        <h2 style='color: #1e293b; font-size: 2rem; font-weight: 700; margin-bottom: 0.5rem;'>
            💰 Cost Analytics
        </h2>
        <p style='color: #64748b; font-size: 1rem; margin: 0;'>
            Comprehensive cost analysis by model, practice, and time period
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    cost = st.session_state.cost_analytics
    
    # Total cost summary with enhanced cards
    st.markdown("### 💵 Total Cost Summary")
    cost_summary = cost.get_cost_summary(start_date, end_date)
    
    from src.dashboard.components.metric_cards import metric_card
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        metric_card(
            value=f"${cost_summary.get('total_cost_usd', 0):,.2f}",
            label="Total Cost",
            icon="💰"
        )
    
    with col2:
        metric_card(
            value=f"${cost_summary.get('avg_cost_per_request', 0):.4f}",
            label="Avg Cost/Request",
            icon="📊"
        )
    
    with col3:
        metric_card(
            value=f"${cost_summary.get('min_cost_per_request', 0):.4f}",
            label="Min Cost/Request",
            icon="⬇️"
        )
    
    with col4:
        metric_card(
            value=f"${cost_summary.get('max_cost_per_request', 0):.4f}",
            label="Max Cost/Request",
            icon="⬆️"
        )
    
    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
    
    # Cost by model
    st.markdown("### 💵 Cost by Model")
    cost_by_model = cost.get_cost_by_model(start_date, end_date)
    
    if not cost_by_model.empty:
        col1, col2 = st.columns(2)
        
        with col1:
            from src.dashboard.components.charts import create_bar_chart
            fig = create_bar_chart(
                cost_by_model,
                x="model",
                y="total_cost_usd",
                title="Total Cost by Model",
                y_label="Cost (USD)",
                top_n=10
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            from src.dashboard.components.charts import create_pie_chart
            fig = create_pie_chart(
                cost_by_model,
                names="model",
                values="total_cost_usd",
                title="Cost Distribution by Model"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Show table
        st.dataframe(
            cost_by_model[["model", "total_cost_usd", "avg_cost_per_request", "request_count"]].style.format({
                "total_cost_usd": "${:,.2f}",
                "avg_cost_per_request": "${:,.4f}",
                "request_count": "{:,.0f}"
            }),
            use_container_width=True
        )
    
    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
    
    # Cost by practice
    st.markdown("### 🏢 Cost by Practice")
    cost_by_practice = cost.get_cost_by_practice(start_date, end_date)
    
    if not cost_by_practice.empty:
        from src.dashboard.components.charts import create_bar_chart
        fig = create_bar_chart(
            cost_by_practice,
            x="practice",
            y="total_cost_usd",
            title="Total Cost by Practice",
            y_label="Cost (USD)",
        )
        st.plotly_chart(fig, use_container_width=True)
        
        st.dataframe(
            cost_by_practice[["practice", "total_cost_usd", "avg_cost_per_request", "unique_users"]].style.format({
                "total_cost_usd": "${:,.2f}",
                "avg_cost_per_request": "${:,.4f}",
                "unique_users": "{:,.0f}"
            }),
            use_container_width=True
        )


def show_usage_patterns(start_date, end_date):
    """Show usage patterns page."""
    st.markdown("""
    <div style='margin-bottom: 2rem;'>
        <h2 style='color: #1e293b; font-size: 2rem; font-weight: 700; margin-bottom: 0.5rem;'>
            📊 Usage Patterns
        </h2>
        <p style='color: #64748b; font-size: 1rem; margin: 0;'>
            Analyze usage patterns, peak hours, and tool utilization
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    pattern = st.session_state.pattern_analytics
    
    # Peak usage hours
    st.markdown("### ⏰ Peak Usage Hours")
    peak_hours = pattern.get_peak_usage_hours(start_date, end_date)
    
    if not peak_hours.empty:
        from src.dashboard.components.charts import create_bar_chart
        fig = create_bar_chart(
            peak_hours,
            x="hour",
            y="event_count",
            title="Events by Hour of Day",
            x_label="Hour (24-hour format)",
            y_label="Event Count",
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Find peak hour
        max_hour = peak_hours.loc[peak_hours['event_count'].idxmax()]
        st.info(f"📌 Peak usage hour: {int(max_hour['hour'])}:00 with {max_hour['event_count']} events")
    
    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
    
    # Tool usage statistics
    st.markdown("### 🛠️ Tool Usage Statistics")
    tool_patterns = pattern.get_tool_usage_patterns()
    
    if not tool_patterns.empty:
        col1, col2 = st.columns(2)
        
        with col1:
            from src.dashboard.components.charts import create_bar_chart
            fig = create_bar_chart(
                tool_patterns,
                x="tool_name",
                y="total_uses",
                title="Tool Usage Count",
                y_label="Total Uses",
                orientation="h",
                top_n=15
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            from src.dashboard.components.charts import create_bar_chart
            fig = create_bar_chart(
                tool_patterns,
                x="tool_name",
                y="success_rate",
                title="Tool Success Rate (%)",
                y_label="Success Rate (%)",
                orientation="h",
                top_n=15
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Show table
        display_cols = ["tool_name", "total_uses", "successful_uses", "failed_uses", "success_rate", "avg_duration_ms"]
        available_cols = [col for col in display_cols if col in tool_patterns.columns]
        st.dataframe(
            tool_patterns[available_cols].style.format({
                "total_uses": "{:,.0f}",
                "successful_uses": "{:,.0f}",
                "failed_uses": "{:,.0f}",
                "success_rate": "{:.1f}%",
                "avg_duration_ms": "{:,.0f}"
            }),
            use_container_width=True
        )
    
    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
    
    # Model usage patterns
    st.markdown("### 🤖 Model Usage Patterns")
    model_patterns = pattern.get_model_usage_patterns(start_date, end_date)
    
    if not model_patterns.empty:
        from src.dashboard.components.charts import create_bar_chart
        fig = create_bar_chart(
            model_patterns,
            x="model",
            y="request_count",
            title="API Requests by Model",
            y_label="Request Count",
        )
        st.plotly_chart(fig, use_container_width=True)


def show_session_analytics(start_date, end_date):
    """Show session analytics page."""
    st.markdown("""
    <div style='margin-bottom: 2rem;'>
        <h2 style='color: #1e293b; font-size: 2rem; font-weight: 700; margin-bottom: 0.5rem;'>
            🕐 Session Analytics
        </h2>
        <p style='color: #64748b; font-size: 1rem; margin: 0;'>
            Track session metrics, durations, and user activity
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    usage = st.session_state.usage_analytics
    
    # Session metrics
    st.markdown("### 📈 Session Metrics")
    session_metrics = usage.get_session_metrics(start_date, end_date)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Total Sessions",
            f"{session_metrics.get('total_sessions', 0):,}"
        )
    
    with col2:
        st.metric(
            "Unique Users",
            f"{session_metrics.get('unique_users', 0):,}"
        )
    
    with col3:
        avg_duration = session_metrics.get('avg_duration_seconds', 0)
        st.metric(
            "Avg Duration",
            f"{avg_duration:.0f} sec" if avg_duration < 60 else f"{avg_duration/60:.1f} min"
        )
    
    with col4:
        median_duration = session_metrics.get('median_duration_seconds', 0)
        st.metric(
            "Median Duration",
            f"{median_duration:.0f} sec" if median_duration < 60 else f"{median_duration/60:.1f} min"
        )
    
    # Additional metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "Min Duration",
            f"{session_metrics.get('min_duration_seconds', 0):.0f} sec"
        )
    
    with col2:
        st.metric(
            "Max Duration",
            f"{session_metrics.get('max_duration_seconds', 0):.0f} sec"
        )
    
    with col3:
        total_duration = session_metrics.get('total_duration_seconds', 0)
        st.metric(
            "Total Duration",
            f"{total_duration/3600:.1f} hours"
        )
    
    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
    
    # User activity summary
    st.markdown("### 👥 User Activity Summary")
    user_activity = usage.get_user_activity_summary()
    
    if not user_activity.empty:
        # Filter by date if needed (this would require additional filtering logic)
        col1, col2 = st.columns(2)
        
        with col1:
            from src.dashboard.components.charts import create_bar_chart
            fig = create_bar_chart(
                user_activity.nlargest(10, "session_count"),
                x="full_name",
                y="session_count",
                title="Top 10 Users by Session Count",
                y_label="Session Count",
                orientation="h"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            from src.dashboard.components.charts import create_bar_chart
            fig = create_bar_chart(
                user_activity.nlargest(10, "request_count"),
                x="full_name",
                y="request_count",
                title="Top 10 Users by API Requests",
                y_label="Request Count",
                orientation="h"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Show table
        display_cols = ["full_name", "practice", "level", "session_count", "request_count", "total_duration"]
        available_cols = [col for col in display_cols if col in user_activity.columns]
        st.dataframe(
            user_activity[available_cols].style.format({
                "session_count": "{:,.0f}",
                "request_count": "{:,.0f}",
                "total_duration": "{:,.0f}"
            }),
            use_container_width=True
        )


def show_daily_trends(start_date, end_date):
    """Show daily trends page."""
    st.markdown("""
    <div style='margin-bottom: 2rem;'>
        <h2 style='color: #1e293b; font-size: 2rem; font-weight: 700; margin-bottom: 0.5rem;'>
            📈 Daily Trends
        </h2>
        <p style='color: #64748b; font-size: 1rem; margin: 0;'>
            Analyze trends over time with daily, weekly, and monthly views
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    trend = st.session_state.trend_analytics
    
    # Metric selector
    st.markdown("#### Select Metric to Analyze")
    metric = st.selectbox(
        "Select Metric",
        ["events", "sessions", "cost", "tokens"],
        key="trend_metric",
        label_visibility="collapsed"
    )
    
    # Get trend summary
    trend_summary = trend.get_trend_summary(metric, start_date, end_date)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Total",
            f"{trend_summary.get('total', 0):,.0f}"
        )
    
    with col2:
        st.metric(
            "Avg Daily",
            f"{trend_summary.get('avg_daily', 0):.1f}"
        )
    
    with col3:
        growth_7d = trend_summary.get('growth_rate_7d', 0)
        st.metric(
            "7-Day Growth",
            f"{growth_7d:.1f}%"
        )
    
    with col4:
        trend_direction = trend_summary.get('trend', 'stable')
        trend_icon = "📈" if trend_direction == "increasing" else "📉" if trend_direction == "decreasing" else "➡️"
        st.metric(
            "Trend",
            f"{trend_icon} {trend_direction.title()}"
        )
    
    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
    
    # Daily trends chart
    st.markdown(f"### 📊 Daily {metric.title()} Trends")
    daily_trends = trend.get_daily_trends(metric, start_date, end_date)
    
    if not daily_trends.empty:
        from src.dashboard.components.charts import create_line_chart, create_area_chart
        
        col1, col2 = st.columns(2)
        
        with col1:
            count_col = 'count' if 'count' in daily_trends.columns else daily_trends.columns[-1]
            fig = create_line_chart(
                daily_trends,
                x="date",
                y=count_col,
                title=f"Daily {metric.title()}",
                x_label="Date",
                y_label=metric.title(),
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = create_area_chart(
                daily_trends,
                x="date",
                y=count_col,
                title=f"Daily {metric.title()} (Area)",
                x_label="Date",
                y_label=metric.title(),
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Show table
        st.dataframe(
            daily_trends.style.format({
                count_col: "{:,.0f}"
            }),
            use_container_width=True
        )
    
    st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)
    
    # Weekly and monthly trends
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📅 Weekly Trends")
        weekly_trends = trend.get_weekly_trends(metric, start_date, end_date)
        
        if not weekly_trends.empty:
            from src.dashboard.components.charts import create_bar_chart
            count_col = 'count' if 'count' in weekly_trends.columns else weekly_trends.columns[-1]
            fig = create_bar_chart(
                weekly_trends,
                x="date",
                y=count_col,
                title=f"Weekly {metric.title()}",
                x_label="Week",
                y_label=metric.title(),
            )
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### 📆 Monthly Trends")
        monthly_trends = trend.get_monthly_trends(metric, start_date, end_date)
        
        if not monthly_trends.empty:
            from src.dashboard.components.charts import create_bar_chart
            count_col = 'count' if 'count' in monthly_trends.columns else monthly_trends.columns[-1]
            fig = create_bar_chart(
                monthly_trends,
                x="date",
                y=count_col,
                title=f"Monthly {metric.title()}",
                x_label="Month",
                y_label=metric.title(),
            )
            st.plotly_chart(fig, use_container_width=True)


if __name__ == "__main__":
    main()
