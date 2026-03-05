"""Dashboard configuration."""

# Page configuration
PAGE_TITLE = "Claude Code Analytics Platform"
PAGE_ICON = "📊"
LAYOUT = "wide"
INITIAL_SIDEBAR_STATE = "expanded"

# Professional color palette
COLOR_PALETTE = [
    "#2563eb",  # Modern blue
    "#f59e0b",  # Amber
    "#10b981",  # Emerald
    "#ef4444",  # Red
    "#8b5cf6",  # Purple
    "#06b6d4",  # Cyan
    "#f97316",  # Orange
    "#6366f1",  # Indigo
    "#ec4899",  # Pink
    "#14b8a6",  # Teal
]

# Chart template
CHART_TEMPLATE = "plotly_white"
CHART_FONT = "Inter, system-ui, -apple-system, sans-serif"

# Metric card colors
METRIC_COLORS = {
    "primary": "#2563eb",
    "success": "#10b981",
    "warning": "#f59e0b",
    "danger": "#ef4444",
    "info": "#06b6d4",
}

# Date range defaults
DEFAULT_DAYS_BACK = 30

# Custom CSS
CUSTOM_CSS = """
<style>
    /* Main container */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1400px;
    }
    
    /* Headers */
    h1 {
        color: #1e293b;
        font-weight: 700;
        margin-bottom: 1rem;
        letter-spacing: -0.02em;
    }
    
    h2 {
        color: #1e293b;
        font-weight: 700;
        margin-top: 2.5rem;
        margin-bottom: 1.5rem;
        padding-bottom: 0.75rem;
        border-bottom: 3px solid #e2e8f0;
        font-size: 1.75rem;
        letter-spacing: -0.01em;
    }
    
    h3 {
        color: #334155;
        font-weight: 600;
        margin-top: 2rem;
        margin-bottom: 1rem;
        font-size: 1.25rem;
        letter-spacing: -0.01em;
    }
    
    /* Metric cards - Enhanced styling */
    [data-testid="stMetricValue"] {
        font-size: 2.25rem;
        font-weight: 700;
        color: #1e293b;
        letter-spacing: -0.02em;
        line-height: 1.2;
    }
    
    [data-testid="stMetricLabel"] {
        font-size: 0.875rem;
        color: #64748b;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-top: 0.25rem;
    }
    
    [data-testid="stMetricDelta"] {
        font-size: 0.875rem;
        font-weight: 600;
    }
    
    /* Metric container enhancement */
    div[data-testid="stMetricContainer"] {
        background: linear-gradient(135deg, #f8fafc 0%, #ffffff 100%);
        padding: 1.5rem;
        border-radius: 0.75rem;
        border: 1px solid #e2e8f0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        transition: all 0.2s ease;
    }
    
    div[data-testid="stMetricContainer"]:hover {
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transform: translateY(-2px);
    }
    
    /* Sidebar Navigation */
    .css-1d391kg {
        padding-top: 2rem;
    }
    
    /* Sidebar navigation styling */
    .sidebar-nav-item {
        padding: 0.75rem 1rem;
        margin: 0.25rem 0;
        border-radius: 0.5rem;
        cursor: pointer;
        transition: all 0.2s ease;
        display: flex;
        align-items: center;
        gap: 0.75rem;
        color: #64748b;
        font-weight: 500;
        font-size: 0.9375rem;
    }
    
    .sidebar-nav-item:hover {
        background-color: #f1f5f9;
        color: #1e293b;
    }
    
    .sidebar-nav-item.active {
        background: linear-gradient(135deg, #2563eb 0%, #6366f1 100%);
        color: white;
        font-weight: 600;
        box-shadow: 0 2px 4px rgba(37, 99, 235, 0.2);
    }
    
    .sidebar-nav-item.active:hover {
        background: linear-gradient(135deg, #1d4ed8 0%, #4f46e5 100%);
    }
    
    .sidebar-nav-icon {
        font-size: 1.25rem;
        width: 1.5rem;
        text-align: center;
    }
    
    /* Radio button styling - hide default and style custom */
    .stRadio > div {
        display: flex;
        flex-direction: column;
        gap: 0.25rem;
    }
    
    .stRadio > div > label {
        padding: 0.75rem 1rem;
        margin: 0.25rem 0;
        border-radius: 0.5rem;
        cursor: pointer;
        transition: all 0.2s ease;
        display: flex;
        align-items: center;
        gap: 0.75rem;
        color: #64748b;
        font-weight: 500;
        font-size: 0.9375rem;
        background-color: transparent;
        border: none;
    }
    
    .stRadio > div > label:hover {
        background-color: #f1f5f9;
        color: #1e293b;
    }
    
    .stRadio > div > label > div[data-testid="stMarkdownContainer"] {
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }
    
    /* Selected radio button */
    .stRadio > div > label[data-baseweb="radio"]:has(input:checked),
    .stRadio > div > label:has(input:checked) {
        background: linear-gradient(135deg, #2563eb 0%, #6366f1 100%);
        color: white;
        font-weight: 600;
        box-shadow: 0 2px 4px rgba(37, 99, 235, 0.2);
    }
    
    .stRadio > div > label:has(input:checked):hover {
        background: linear-gradient(135deg, #1d4ed8 0%, #4f46e5 100%);
    }
    
    /* Navigation section grouping */
    .nav-section {
        margin-bottom: 1.5rem;
    }
    
    .nav-section-title {
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        color: #94a3b8;
        padding: 0.5rem 1rem;
        margin-bottom: 0.5rem;
    }
    
    /* Sidebar checkbox styling */
    .stCheckbox > label {
        color: #475569;
        font-weight: 500;
        font-size: 0.9375rem;
    }
    
    /* Sidebar date input styling */
    .stDateInput > label {
        color: #475569;
        font-weight: 500;
        font-size: 0.875rem;
    }
    
    /* Sidebar spacing improvements */
    .sidebar .element-container {
        margin-bottom: 1rem;
    }
    
    /* Sidebar divider */
    .sidebar-divider {
        border-top: 2px solid #e2e8f0;
        margin: 1.5rem 0;
    }
    
    /* Section containers */
    .metric-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 0.75rem;
        color: white;
        margin-bottom: 1rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    /* Info boxes */
    .info-box {
        background-color: #f8fafc;
        border-left: 4px solid #2563eb;
        padding: 1rem 1.25rem;
        border-radius: 0.5rem;
        margin: 1.5rem 0;
        box-shadow: 0 1px 2px rgba(0,0,0,0.05);
    }
    
    /* Divider - Enhanced */
    .section-divider {
        margin: 3rem 0;
        border: none;
        height: 2px;
        background: linear-gradient(to right, transparent, #e2e8f0 50%, transparent);
    }
    
    /* Chart containers */
    .js-plotly-plot {
        border-radius: 0.5rem;
        padding: 0.5rem;
    }
    
    /* Table styling */
    .dataframe {
        border-radius: 0.5rem;
        overflow: hidden;
    }
    
    /* Button styling */
    .stButton > button {
        border-radius: 0.5rem;
        font-weight: 600;
        transition: all 0.2s ease;
    }
    
    /* Selectbox and inputs */
    .stSelectbox > div > div {
        border-radius: 0.5rem;
    }
    
    /* Spacing improvements */
    .element-container {
        margin-bottom: 1.5rem;
    }
    
    /* Better text readability */
    p {
        line-height: 1.6;
        color: #475569;
    }
</style>
"""
