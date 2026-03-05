"""Reusable chart components using Plotly."""

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from typing import Optional, List, Dict, Any
from src.dashboard.config import COLOR_PALETTE


def create_bar_chart(
    df: pd.DataFrame,
    x: str,
    y: str,
    title: str,
    x_label: Optional[str] = None,
    y_label: Optional[str] = None,
    color: Optional[str] = None,
    orientation: str = "v",
    top_n: Optional[int] = None,
) -> go.Figure:
    """
    Create a bar chart.
    
    Args:
        df: DataFrame with data
        x: Column name for x-axis
        y: Column name for y-axis
        title: Chart title
        x_label: Optional x-axis label
        y_label: Optional y-axis label
        color: Optional column name for color grouping
        orientation: 'v' for vertical, 'h' for horizontal
        top_n: Optional limit to top N items
    
    Returns:
        Plotly figure
    """
    if df.empty:
        fig = go.Figure()
        fig.add_annotation(
            text="No data available",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False
        )
        return fig
    
    df_plot = df.copy()
    
    if top_n:
        df_plot = df_plot.nlargest(top_n, y)
    
    if orientation == "h":
        fig = px.bar(
            df_plot,
            x=y,
            y=x,
            orientation='h',
            title=title,
            color=color,
            color_discrete_sequence=COLOR_PALETTE,
        )
    else:
        fig = px.bar(
            df_plot,
            x=x,
            y=y,
            title=title,
            color=color,
            color_discrete_sequence=COLOR_PALETTE,
        )
    
    fig.update_layout(
        xaxis_title=x_label or x,
        yaxis_title=y_label or y,
        template="plotly_white",
        hovermode='closest',
        font=dict(family="Inter, system-ui, sans-serif", size=12),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=20, r=20, t=50, b=20),
        title=dict(
            font=dict(size=18, color='#1e293b'),
            x=0.5,
            xanchor='center'
        ),
        xaxis=dict(
            gridcolor='rgba(0,0,0,0.05)',
            linecolor='rgba(0,0,0,0.1)',
            title_font=dict(size=13, color='#475569'),
            tickfont=dict(size=11, color='#64748b')
        ),
        yaxis=dict(
            gridcolor='rgba(0,0,0,0.05)',
            linecolor='rgba(0,0,0,0.1)',
            title_font=dict(size=13, color='#475569'),
            tickfont=dict(size=11, color='#64748b')
        ),
        hoverlabel=dict(
            bgcolor='rgba(255,255,255,0.95)',
            bordercolor='rgba(0,0,0,0.1)',
            font_size=12
        ),
    )
    
    return fig


def create_line_chart(
    df: pd.DataFrame,
    x: str,
    y: str,
    title: str,
    x_label: Optional[str] = None,
    y_label: Optional[str] = None,
    color: Optional[str] = None,
) -> go.Figure:
    """
    Create a line chart.
    
    Args:
        df: DataFrame with data
        x: Column name for x-axis
        y: Column name for y-axis
        title: Chart title
        x_label: Optional x-axis label
        y_label: Optional y-axis label
        color: Optional column name for color grouping
    
    Returns:
        Plotly figure
    """
    if df.empty:
        fig = go.Figure()
        fig.add_annotation(
            text="No data available",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False
        )
        return fig
    
    df_plot = df.copy()
    df_plot = df_plot.sort_values(x)
    
    fig = px.line(
        df_plot,
        x=x,
        y=y,
        title=title,
        color=color,
        color_discrete_sequence=COLOR_PALETTE,
        markers=True,
    )
    
    fig.update_layout(
        xaxis_title=x_label or x,
        yaxis_title=y_label or y,
        template="plotly_white",
        hovermode='x unified',
        font=dict(family="Inter, system-ui, sans-serif", size=12),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=20, r=20, t=50, b=20),
        title=dict(
            font=dict(size=18, color='#1e293b'),
            x=0.5,
            xanchor='center'
        ),
        xaxis=dict(
            gridcolor='rgba(0,0,0,0.05)',
            linecolor='rgba(0,0,0,0.1)',
            title_font=dict(size=13, color='#475569'),
            tickfont=dict(size=11, color='#64748b')
        ),
        yaxis=dict(
            gridcolor='rgba(0,0,0,0.05)',
            linecolor='rgba(0,0,0,0.1)',
            title_font=dict(size=13, color='#475569'),
            tickfont=dict(size=11, color='#64748b')
        ),
        hoverlabel=dict(
            bgcolor='rgba(255,255,255,0.95)',
            bordercolor='rgba(0,0,0,0.1)',
            font_size=12
        ),
    )
    
    # Update line styling
    fig.update_traces(
        line=dict(width=3),
        marker=dict(size=6)
    )
    
    return fig


def create_pie_chart(
    df: pd.DataFrame,
    names: str,
    values: str,
    title: str,
) -> go.Figure:
    """
    Create a pie chart.
    
    Args:
        df: DataFrame with data
        names: Column name for pie slice labels
        values: Column name for pie slice values
        title: Chart title
    
    Returns:
        Plotly figure
    """
    if df.empty:
        fig = go.Figure()
        fig.add_annotation(
            text="No data available",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False
        )
        return fig
    
    fig = px.pie(
        df,
        names=names,
        values=values,
        title=title,
        color_discrete_sequence=COLOR_PALETTE,
    )
    
    fig.update_traces(
        textposition='inside',
        textinfo='percent+label',
        textfont=dict(size=12, color='white'),
        marker=dict(line=dict(color='white', width=2))
    )
    
    fig.update_layout(
        template="plotly_white",
        font=dict(family="Inter, system-ui, sans-serif", size=12),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=20, r=20, t=50, b=20),
        title=dict(
            font=dict(size=18, color='#1e293b'),
            x=0.5,
            xanchor='center'
        ),
        hoverlabel=dict(
            bgcolor='rgba(255,255,255,0.95)',
            bordercolor='rgba(0,0,0,0.1)',
            font_size=12
        ),
    )
    
    return fig


def create_area_chart(
    df: pd.DataFrame,
    x: str,
    y: str,
    title: str,
    x_label: Optional[str] = None,
    y_label: Optional[str] = None,
) -> go.Figure:
    """
    Create an area chart.
    
    Args:
        df: DataFrame with data
        x: Column name for x-axis
        y: Column name for y-axis
        title: Chart title
        x_label: Optional x-axis label
        y_label: Optional y-axis label
    
    Returns:
        Plotly figure
    """
    if df.empty:
        fig = go.Figure()
        fig.add_annotation(
            text="No data available",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False
        )
        return fig
    
    df_plot = df.copy()
    df_plot = df_plot.sort_values(x)
    
    fig = px.area(
        df_plot,
        x=x,
        y=y,
        title=title,
        color_discrete_sequence=COLOR_PALETTE,
    )
    
    fig.update_layout(
        xaxis_title=x_label or x,
        yaxis_title=y_label or y,
        template="plotly_white",
        hovermode='x unified',
        font=dict(family="Inter, system-ui, sans-serif", size=12),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=20, r=20, t=50, b=20),
        title=dict(
            font=dict(size=18, color='#1e293b'),
            x=0.5,
            xanchor='center'
        ),
        xaxis=dict(
            gridcolor='rgba(0,0,0,0.05)',
            linecolor='rgba(0,0,0,0.1)',
            title_font=dict(size=13, color='#475569'),
            tickfont=dict(size=11, color='#64748b')
        ),
        yaxis=dict(
            gridcolor='rgba(0,0,0,0.05)',
            linecolor='rgba(0,0,0,0.1)',
            title_font=dict(size=13, color='#475569'),
            tickfont=dict(size=11, color='#64748b')
        ),
        hoverlabel=dict(
            bgcolor='rgba(255,255,255,0.95)',
            bordercolor='rgba(0,0,0,0.1)',
            font_size=12
        ),
    )
    
    # Update area styling
    fig.update_traces(
        fillcolor='rgba(37, 99, 235, 0.2)',
        line=dict(width=2)
    )
    
    return fig


def create_metric_card(value: Any, label: str, delta: Optional[str] = None) -> str:
    """
    Create HTML for a metric card (for use with st.metric or st.markdown).
    
    Args:
        value: Metric value
        label: Metric label
        delta: Optional delta/change indicator
    
    Returns:
        HTML string
    """
    delta_html = f"<div style='color: green; font-size: 0.8em;'>{delta}</div>" if delta else ""
    
    return f"""
    <div style='padding: 1rem; background-color: #f0f2f6; border-radius: 0.5rem; margin: 0.5rem 0;'>
        <div style='font-size: 2rem; font-weight: bold;'>{value}</div>
        <div style='color: #666; margin-top: 0.5rem;'>{label}</div>
        {delta_html}
    </div>
    """
