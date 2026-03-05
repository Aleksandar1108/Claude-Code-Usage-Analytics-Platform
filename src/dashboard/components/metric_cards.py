"""Enhanced metric card components."""

import streamlit as st
from typing import Optional, Dict, Any
from src.dashboard.config import METRIC_COLORS


def metric_card(
    value: Any,
    label: str,
    icon: Optional[str] = None,
    delta: Optional[str] = None,
    delta_color: str = "normal",
    help_text: Optional[str] = None
):
    """
    Create an enhanced metric card with icon and styling.
    
    Args:
        value: Metric value to display
        label: Metric label
        icon: Optional emoji or icon
        delta: Optional delta/change indicator
        delta_color: Color for delta ("normal", "inverse", "off")
        help_text: Optional help text
    """
    # Create metric with icon in label
    display_label = f"{icon} {label}" if icon else label
    st.metric(
        label=display_label,
        value=value,
        delta=delta,
        delta_color=delta_color,
        help=help_text
    )


def metric_card_grid(metrics: list, columns: int = 4):
    """
    Create a grid of metric cards.
    
    Args:
        metrics: List of metric dictionaries with keys: value, label, icon, delta, help_text
        columns: Number of columns in the grid
    """
    cols = st.columns(columns)
    
    for idx, metric in enumerate(metrics):
        with cols[idx % columns]:
            metric_card(
                value=metric.get("value", ""),
                label=metric.get("label", ""),
                icon=metric.get("icon"),
                delta=metric.get("delta"),
                delta_color=metric.get("delta_color", "normal"),
                help_text=metric.get("help_text")
            )


def kpi_card(
    title: str,
    value: Any,
    subtitle: Optional[str] = None,
    trend: Optional[str] = None,
    color: str = "primary"
):
    """
    Create a KPI card with enhanced styling.
    
    Args:
        title: Card title
        value: Main value
        subtitle: Optional subtitle
        trend: Optional trend indicator
        color: Color theme (primary, success, warning, danger, info)
    """
    color_map = {
        "primary": "#2563eb",
        "success": "#10b981",
        "warning": "#f59e0b",
        "danger": "#ef4444",
        "info": "#06b6d4",
    }
    
    bg_color = color_map.get(color, color_map["primary"])
    
    card_html = f"""
    <div style='
        background: linear-gradient(135deg, {bg_color}12 0%, {bg_color}05 100%);
        border: 1px solid {bg_color}25;
        border-radius: 0.75rem;
        padding: 1.75rem;
        margin-bottom: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        transition: all 0.2s ease;
    '>
        <div style='color: #64748b; font-size: 0.8125rem; font-weight: 600; margin-bottom: 0.75rem; text-transform: uppercase; letter-spacing: 0.05em;'>{title}</div>
        <div style='color: #1e293b; font-size: 2.5rem; font-weight: 700; margin-bottom: 0.5rem; letter-spacing: -0.02em; line-height: 1.2;'>{value}</div>
    """
    
    if subtitle:
        card_html += f"<div style='color: #94a3b8; font-size: 0.875rem; margin-top: 0.25rem;'>{subtitle}</div>"
    
    if trend:
        trend_color = "#10b981" if trend.startswith("+") else "#ef4444"
        card_html += f"<div style='color: {trend_color}; font-size: 0.875rem; font-weight: 600; margin-top: 0.75rem; padding-top: 0.75rem; border-top: 1px solid {bg_color}20;'>{trend}</div>"
    
    card_html += "</div>"
    
    st.markdown(card_html, unsafe_allow_html=True)
