import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import config as cfg
import numpy as np

# Page configuration
st.set_page_config(
    page_title="Mental Health & Digital Usage Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS - Modern Clean Design
st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global Styles */
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Main Background */
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 2rem 1rem;
    }
    
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
        padding-top: 2rem;
    }
    
    [data-testid="stSidebar"] * {
        color: white !important;
    }
    
    [data-testid="stSidebar"] .css-1d391kg {
        background-color: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        padding: 10px;
    }
    
    /* Title Styling */
    h1 {
        color: #2d3748;
        font-weight: 700;
        font-size: 2.5rem !important;
        margin-bottom: 1rem;
    }
    
    h3 {
        color: #4a5568;
        font-weight: 600;
        font-size: 1.3rem !important;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
    }
    
    /* Metric Cards - Beautiful Colored Cards */
    [data-testid="stMetric"] {
        background: white;
        padding: 1.5rem;
        border-radius: 20px;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.08);
        border: none;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    [data-testid="stMetric"]:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.12);
    }
    
    [data-testid="stMetricLabel"] {
        font-size: 0.9rem;
        font-weight: 500;
        color: #718096;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    [data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: 700;
        color: #2d3748;
    }
    
    /* Chart Container */
    .stPlotlyChart {
        background: white;
        border-radius: 20px;
        padding: 1.5rem;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.08);
        border: none;
        margin-bottom: 1.5rem;
    }
    
    /* Filter Section */
    .stSelectbox {
        background: white;
        border-radius: 15px;
        padding: 0.5rem;
    }
    
    .stSelectbox label {
        color: #2d3748 !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
    }
    
    .stSelectbox > div > div {
        background: white !important;
        border: 2px solid #e2e8f0 !important;
        border-radius: 10px !important;
        color: #2d3748 !important;
    }
    
    .stSelectbox [data-baseweb="select"] {
        background: white !important;
    }
    
    .stSelectbox [data-baseweb="select"] > div {
        background: white !important;
        color: #2d3748 !important;
        font-weight: 500 !important;
    }
    
    /* Radio Button Styling */
    [data-testid="stSidebar"] .stRadio > label {
        background-color: rgba(255, 255, 255, 0.1);
        padding: 12px 20px;
        border-radius: 10px;
        margin-bottom: 8px;
        display: block;
        transition: all 0.3s ease;
    }
    
    [data-testid="stSidebar"] .stRadio > label:hover {
        background-color: rgba(255, 255, 255, 0.2);
        transform: translateX(5px);
    }
    
    /* Divider */
    hr {
        margin: 2rem 0;
        border: none;
        height: 1px;
        background: linear-gradient(to right, transparent, #cbd5e0, transparent);
    }
    
    /* Button Styling */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 15px;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
    }
    
    .stDownloadButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(102, 126, 234, 0.6);
    }
    
    /* Info Box */
    .stAlert {
        background: white;
        border-radius: 15px;
        border-left: 4px solid #667eea;
        padding: 1rem;
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.05);
    }
    
    /* Dataframe Styling */
    .stDataFrame {
        border-radius: 15px;
        overflow: hidden;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.08);
    }
    
    /* Remove default padding */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    </style>
    """, unsafe_allow_html=True)

@st.cache_data(ttl=600)
def load_data():
    """Load data from database (prefer Postgres) with caching"""
    data = cfg.load_data(table_name="mental_health_data", prefer_postgres=True)
    if data:
        return pd.DataFrame(data)
    else:
        st.error("Could not connect to database/Supabase.")
        return None

def categorize_device_hours(hours):
    """Categorize device usage hours"""
    if hours <= 2:
        return "0-2 hours"
    elif hours <= 5:
        return "3-5 hours"
    elif hours <= 8:
        return "6-8 hours"
    else:
        return ">8 hours"

def categorize_sleep(hours):
    """Categorize sleep duration"""
    if hours < 6:
        return "<6 hours"
    elif hours <= 7:
        return "6-7 hours"
    elif hours <= 8:
        return "7-8 hours"
    else:
        return ">8 hours"

def categorize_unlocks(unlocks):
    """Categorize phone unlocks"""
    if unlocks <= 20:
        return "0-20"
    elif unlocks <= 50:
        return "21-50"
    elif unlocks <= 80:
        return "51-80"
    else:
        return ">80"

# ========== VISUALIZATION FUNCTIONS ==========

def plot_device_usage_vs_stress(df):
    """1. Device Usage vs Stress Level - Line Chart"""
    df['device_category'] = df['device_hours_per_day'].apply(categorize_device_hours)
    
    # Calculate average stress per category
    category_order = ["0-2 hours", "3-5 hours", "6-8 hours", ">8 hours"]
    grouped = df.groupby('device_category')['stress_level'].mean().reindex(category_order)
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=grouped.index,
        y=grouped.values,
        mode='lines+markers',
        name='Avg Stress Level',
        line=dict(color='#667eea', width=4, shape='spline'),
        marker=dict(size=12, color='#667eea', line=dict(color='white', width=2)),
        fill='tozeroy',
        fillcolor='rgba(102, 126, 234, 0.1)'
    ))
    
    fig.update_layout(
        title={'text': '<b>Device Usage vs Stress Level</b>', 'font': {'size': 20, 'color': '#1a202c', 'family': 'Inter'}},
        xaxis=dict(
            title={'text': '<b>Daily Device Usage</b>', 'font': {'size': 14, 'color': '#2d3748'}},
            showgrid=True,
            gridcolor='#cbd5e0',
            gridwidth=1,
            linecolor='#2d3748',
            linewidth=2,
            tickfont=dict(size=13, color='#1a202c'),
            showline=True
        ),
        yaxis=dict(
            title={'text': '<b>Average Stress Level</b>', 'font': {'size': 14, 'color': '#2d3748'}},
            showgrid=True,
            gridcolor='#cbd5e0',
            gridwidth=1,
            linecolor='#2d3748',
            linewidth=2,
            tickfont=dict(size=13, color='#1a202c'),
            showline=True
        ),
        template='plotly_white',
        height=450,
        plot_bgcolor='#ffffff',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Inter', color='#2d3748', size=12),
        hovermode='x unified',
        hoverlabel=dict(
            bgcolor='white',
            font_size=14,
            font_family='Inter',
            font_color='#1a202c'
        ),
        margin=dict(l=70, r=30, t=90, b=70)
    )
    return fig

def plot_sleep_vs_anxiety(df):
    """2. Sleep Duration vs Anxiety Score - Column Bar Chart"""
    df['sleep_category'] = df['sleep_duration'].apply(categorize_sleep)
    
    category_order = ["<6 hours", "6-7 hours", "7-8 hours", ">8 hours"]
    grouped = df.groupby('sleep_category')['anxiety_score'].mean().reindex(category_order)
    
    colors = ['#ff6b9d', '#ffa500', '#6bcb77', '#4d96ff']
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=grouped.index,
        y=grouped.values,
        marker=dict(color=colors, line=dict(color='white', width=2)),
        text=grouped.values.round(2),
        textposition='outside',
        textfont=dict(size=12, color='#2d3748', family='Inter')
    ))
    
    fig.update_layout(
        title={'text': '<b>Sleep Duration vs Anxiety Score</b>', 'font': {'size': 20, 'color': '#1a202c', 'family': 'Inter'}},
        xaxis=dict(
            title={'text': '<b>Sleep Duration</b>', 'font': {'size': 14, 'color': '#2d3748'}},
            showgrid=False,
            linecolor='#2d3748',
            linewidth=2,
            tickfont=dict(size=13, color='#1a202c'),
            showline=True
        ),
        yaxis=dict(
            title={'text': '<b>Average Anxiety Score</b>', 'font': {'size': 14, 'color': '#2d3748'}},
            showgrid=True,
            gridcolor='#cbd5e0',
            gridwidth=1,
            linecolor='#2d3748',
            linewidth=2,
            tickfont=dict(size=13, color='#1a202c'),
            showline=True
        ),
        template='plotly_white',
        height=450,
        plot_bgcolor='#ffffff',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Inter', color='#2d3748', size=12),
        hovermode='x unified',
        hoverlabel=dict(
            bgcolor='white',
            font_size=14,
            font_family='Inter',
            font_color='#1a202c'
        ),
        margin=dict(l=70, r=30, t=90, b=70)
    )
    return fig

def plot_device_type_vs_productivity(df):
    """3. Device Type vs Productivity Score - Horizontal Bar Chart"""
    grouped = df.groupby('device_type')['productivity_score'].mean().sort_values()
    
    colors = ['#c780fa', '#ff6b9d', '#ffa500', '#6bcb77']
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=grouped.index,
        x=grouped.values,
        orientation='h',
        marker=dict(color=colors[:len(grouped)], line=dict(color='white', width=2)),
        text=grouped.values.round(2),
        textposition='outside',
        textfont=dict(size=12, color='#2d3748', family='Inter')
    ))
    
    fig.update_layout(
        title={'text': '<b>Device Type vs Productivity Score</b>', 'font': {'size': 20, 'color': '#1a202c', 'family': 'Inter'}},
        xaxis=dict(
            title={'text': '<b>Average Productivity Score</b>', 'font': {'size': 14, 'color': '#2d3748'}},
            showgrid=True,
            gridcolor='#cbd5e0',
            gridwidth=1,
            linecolor='#2d3748',
            linewidth=2,
            tickfont=dict(size=13, color='#1a202c'),
            showline=True
        ),
        yaxis=dict(
            title={'text': '<b>Device Type</b>', 'font': {'size': 14, 'color': '#2d3748'}},
            showgrid=False,
            linecolor='#2d3748',
            linewidth=2,
            tickfont=dict(size=13, color='#1a202c'),
            showline=True
        ),
        template='plotly_white',
        height=450,
        plot_bgcolor='#ffffff',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Inter', color='#2d3748', size=12),
        hovermode='y unified',
        hoverlabel=dict(
            bgcolor='white',
            font_size=14,
            font_family='Inter',
            font_color='#1a202c'
        ),
        margin=dict(l=120, r=30, t=90, b=70)
    )
    return fig

def plot_region_vs_happiness(df):
    """4. Region vs Happiness Score - Pie Chart"""
    grouped = df.groupby('region')['happiness_score'].mean()
    
    fig = go.Figure()
    fig.add_trace(go.Pie(
        labels=grouped.index,
        values=grouped.values,
        hole=0.4,
        marker=dict(colors=['#667eea', '#764ba2', '#ff6b9d', '#ffa500', '#6bcb77', '#4d96ff'], 
                   line=dict(color='white', width=3)),
        textinfo='label+percent',
        textposition='outside',
        textfont=dict(size=13, family='Inter', color='#2d3748')
    ))
    
    fig.update_layout(
        title={'text': '<b>Region vs Happiness Score Distribution</b>', 'font': {'size': 20, 'color': '#1a202c', 'family': 'Inter'}},
        template='plotly_white',
        height=450,
        plot_bgcolor='#ffffff',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Inter', color='#2d3748', size=13),
        showlegend=True,
        legend=dict(
            orientation='v',
            yanchor='middle',
            y=0.5,
            xanchor='left',
            x=1.05,
            font=dict(size=13, color='#1a202c')
        ),
        hoverlabel=dict(
            bgcolor='white',
            font_size=14,
            font_family='Inter',
            font_color='#1a202c'
        ),
        margin=dict(l=30, r=150, t=90, b=30)
    )
    return fig

def plot_education_vs_dependence(df):
    """5. Education Level vs Digital Dependence Score - Radar Chart"""
    education_order = ['High School', 'Bachelor', 'Master', 'PhD']
    grouped = df.groupby('education_level')['digital_dependence_score'].mean().reindex(education_order)
    
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=grouped.values,
        theta=grouped.index,
        fill='toself',
        name='Digital Dependence',
        line=dict(color='#764ba2', width=3),
        fillcolor='rgba(118, 75, 162, 0.3)',
        marker=dict(size=8, color='#764ba2')
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True, 
                range=[0, grouped.max() * 1.2], 
                gridcolor='#cbd5e0',
                gridwidth=1,
                linecolor='#2d3748',
                linewidth=2,
                tickfont=dict(size=12, color='#1a202c')
            ),
            angularaxis=dict(
                gridcolor='#cbd5e0',
                gridwidth=1,
                linecolor='#2d3748',
                linewidth=2,
                tickfont=dict(size=13, color='#1a202c')
            ),
            bgcolor='#ffffff'
        ),
        title={'text': '<b>Education Level vs Digital Dependence Score</b>', 'font': {'size': 20, 'color': '#1a202c', 'family': 'Inter'}},
        template='plotly_white',
        height=500,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Inter', color='#2d3748', size=12),
        showlegend=True,
        hoverlabel=dict(
            bgcolor='white',
            font_size=14,
            font_family='Inter',
            font_color='#1a202c'
        ),
        margin=dict(l=80, r=80, t=110, b=80)
    )
    return fig

def plot_gender_vs_stress(df):
    """6. Gender vs Stress Level - Clustered Bar Chart"""
    grouped = df.groupby('gender')['stress_level'].agg(['mean', 'std']).reset_index()
    
    colors_map = {'Male': '#4d96ff', 'Female': '#ff6b9d', 'Non-binary': '#6bcb77'}
    colors = [colors_map.get(g, '#ffa500') for g in grouped['gender']]
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=grouped['gender'],
        y=grouped['mean'],
        name='Average Stress',
        marker=dict(color=colors, line=dict(color='white', width=2)),
        error_y=dict(type='data', array=grouped['std'], visible=True, color='#718096'),
        text=grouped['mean'].round(2),
        textposition='outside',
        textfont=dict(size=12, color='#2d3748', family='Inter')
    ))
    
    fig.update_layout(
        title={'text': '<b>Gender vs Stress Level</b>', 'font': {'size': 20, 'color': '#1a202c', 'family': 'Inter'}},
        xaxis=dict(
            title={'text': '<b>Gender</b>', 'font': {'size': 14, 'color': '#2d3748'}},
            showgrid=False,
            linecolor='#2d3748',
            linewidth=2,
            tickfont=dict(size=13, color='#1a202c'),
            showline=True
        ),
        yaxis=dict(
            title={'text': '<b>Average Stress Level</b>', 'font': {'size': 14, 'color': '#2d3748'}},
            showgrid=True,
            gridcolor='#cbd5e0',
            gridwidth=1,
            linecolor='#2d3748',
            linewidth=2,
            tickfont=dict(size=13, color='#1a202c'),
            showline=True
        ),
        template='plotly_white',
        height=450,
        barmode='group',
        plot_bgcolor='#ffffff',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Inter', color='#2d3748', size=12),
        hovermode='x unified',
        hoverlabel=dict(
            bgcolor='white',
            font_size=14,
            font_family='Inter',
            font_color='#1a202c'
        ),
        margin=dict(l=70, r=30, t=90, b=70)
    )
    return fig

def plot_phone_unlocks_vs_focus(df):
    """7. Phone Unlocks vs Focus Score - Line Chart"""
    df['unlock_category'] = df['phone_unlocks'].apply(categorize_unlocks)
    
    category_order = ["0-20", "21-50", "51-80", ">80"]
    grouped = df.groupby('unlock_category')['focus_score'].mean().reindex(category_order)
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=grouped.index,
        y=grouped.values,
        mode='lines+markers',
        name='Avg Focus Score',
        line=dict(color='#ffa500', width=4, shape='spline'),
        marker=dict(size=12, color='#ffa500', line=dict(color='white', width=2)),
        fill='tozeroy',
        fillcolor='rgba(255, 165, 0, 0.1)'
    ))
    
    fig.update_layout(
        title={'text': '<b>Phone Unlocks vs Focus Score</b>', 'font': {'size': 20, 'color': '#1a202c', 'family': 'Inter'}},
        xaxis=dict(
            title={'text': '<b>Daily Phone Unlocks</b>', 'font': {'size': 14, 'color': '#2d3748'}},
            showgrid=True,
            gridcolor='#cbd5e0',
            gridwidth=1,
            linecolor='#2d3748',
            linewidth=2,
            tickfont=dict(size=13, color='#1a202c'),
            showline=True
        ),
        yaxis=dict(
            title={'text': '<b>Average Focus Score</b>', 'font': {'size': 14, 'color': '#2d3748'}},
            showgrid=True,
            gridcolor='#cbd5e0',
            gridwidth=1,
            linecolor='#2d3748',
            linewidth=2,
            tickfont=dict(size=13, color='#1a202c'),
            showline=True
        ),
        template='plotly_white',
        height=450,
        plot_bgcolor='#ffffff',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Inter', color='#2d3748', size=12),
        hovermode='x unified',
        hoverlabel=dict(
            bgcolor='white',
            font_size=14,
            font_family='Inter',
            font_color='#1a202c'
        ),
        margin=dict(l=70, r=30, t=90, b=70)
    )
    return fig

def plot_income_vs_anxiety(df):
    """8. Income Level vs Anxiety Score - Box Plot"""
    income_order = ['Low', 'Lower-Mid', 'Upper-Mid', 'High']
    
    fig = go.Figure()
    
    colors = {'Low': '#ff6b9d', 'Lower-Mid': '#ffa500', 'Upper-Mid': '#6bcb77', 'High': '#4d96ff'}
    
    for income in income_order:
        data = df[df['income_level'] == income]['anxiety_score']
        fig.add_trace(go.Box(
            y=data,
            name=income,
            marker=dict(color=colors.get(income, '#999999')),
            boxmean='sd',
            line=dict(width=2)
        ))
    
    fig.update_layout(
        title={'text': '<b>Income Level vs Anxiety Score Distribution</b>', 'font': {'size': 20, 'color': '#1a202c', 'family': 'Inter'}},
        xaxis=dict(
            title={'text': '<b>Income Level</b>', 'font': {'size': 14, 'color': '#2d3748'}},
            showgrid=False,
            linecolor='#2d3748',
            linewidth=2,
            tickfont=dict(size=13, color='#1a202c'),
            showline=True
        ),
        yaxis=dict(
            title={'text': '<b>Anxiety Score</b>', 'font': {'size': 14, 'color': '#2d3748'}},
            showgrid=True,
            gridcolor='#cbd5e0',
            gridwidth=1,
            linecolor='#2d3748',
            linewidth=2,
            tickfont=dict(size=13, color='#1a202c'),
            showline=True
        ),
        template='plotly_white',
        height=450,
        plot_bgcolor='#ffffff',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Inter', color='#2d3748', size=12),
        showlegend=True,
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=1.02,
            xanchor='right',
            x=1,
            font=dict(size=12, color='#1a202c')
        ),
        hovermode='closest',
        hoverlabel=dict(
            bgcolor='white',
            font_size=14,
            font_family='Inter',
            font_color='#1a202c'
        ),
        margin=dict(l=70, r=30, t=110, b=70)
    )
    return fig

# ========== MAIN APP ==========

def main():
    # Load data
    with st.spinner("Loading data from Supabase..."):
        df = load_data()
    
    if df is not None and not df.empty:
        # Sidebar navigation
        st.sidebar.title("📊 Dashboard")
        st.sidebar.markdown("---")
        
        page = st.sidebar.radio(
            "Navigation",
            ["Dashboard", "Device Usage", "Sleep & Mental Health", "Demographics", "Behavioral Patterns", "Raw Data"],
            index=0
        )
        
        st.sidebar.markdown("---")
        st.sidebar.markdown(f"""
            <div style='background-color: rgba(255, 255, 255, 0.15); 
                        padding: 20px; 
                        border-radius: 12px; 
                        border: 2px solid rgba(255, 255, 255, 0.3);
                        text-align: center;
                        margin: 10px 0;'>
                <p style='color: #ffffff; 
                          font-size: 14px; 
                          font-weight: 500; 
                          margin: 0;
                          text-transform: uppercase;
                          letter-spacing: 1px;'>Total Records</p>
                <p style='color: #ffffff; 
                          font-size: 32px; 
                          font-weight: 700; 
                          margin: 8px 0 0 0;'>{len(df)}</p>
            </div>
        """, unsafe_allow_html=True)
        
        # Main title
        st.title("📊 Mental Health & Digital Usage Analytics")
        
        # Filters di bagian atas
        st.markdown("### 🔍 Filters")
        filter_col1, filter_col2, filter_col3 = st.columns([1, 1, 2])
        
        with filter_col1:
            gender_options = ['All'] + list(df['gender'].unique())
            selected_gender = st.selectbox("Gender", gender_options)
        
        with filter_col2:
            region_options = ['All'] + list(df['region'].unique())
            selected_region = st.selectbox("Region", region_options)
        
        # Apply filters
        filtered_df = df.copy()
        if selected_gender != 'All':
            filtered_df = filtered_df[filtered_df['gender'] == selected_gender]
        if selected_region != 'All':
            filtered_df = filtered_df[filtered_df['region'] == selected_region]
        
        with filter_col3:
            st.metric("Filtered Records", len(filtered_df), delta=f"{len(filtered_df) - len(df)}")
        
        st.markdown("---")
        
        # Dashboard content based on selected page
        if page == "Dashboard":
            st.markdown("### 📈 Key Metrics")
            
            # Display statistics
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Avg Stress Level", f"{filtered_df['stress_level'].mean():.2f}", 
                         help="Average stress level from all respondents")
            with col2:
                st.metric("Avg Anxiety Score", f"{filtered_df['anxiety_score'].mean():.2f}",
                         help="Average anxiety score from all respondents")
            with col3:
                st.metric("Avg Device Hours", f"{filtered_df['device_hours_per_day'].mean():.2f}",
                         help="Average daily device usage in hours")
            with col4:
                st.metric("Avg Happiness", f"{filtered_df['happiness_score'].mean():.2f}",
                         help="Average happiness score from all respondents")
            
            st.markdown("---")
            st.markdown("### 📊 Overview Charts")
            
            # Key visualizations
            col1, col2 = st.columns(2)
            with col1:
                st.plotly_chart(plot_device_usage_vs_stress(filtered_df), use_container_width=True)
                st.plotly_chart(plot_region_vs_happiness(filtered_df), use_container_width=True)
            
            with col2:
                st.plotly_chart(plot_sleep_vs_anxiety(filtered_df), use_container_width=True)
                st.plotly_chart(plot_gender_vs_stress(filtered_df), use_container_width=True)
        
        elif page == "Device Usage":
            st.markdown("### 📱 Device Usage Analysis")
            col1, col2 = st.columns(2)
            with col1:
                st.plotly_chart(plot_device_usage_vs_stress(filtered_df), use_container_width=True)
            with col2:
                st.plotly_chart(plot_device_type_vs_productivity(filtered_df), use_container_width=True)
        
        elif page == "Sleep & Mental Health":
            st.markdown("### 😴 Sleep & Mental Health Insights")
            col1, col2 = st.columns(2)
            with col1:
                st.plotly_chart(plot_sleep_vs_anxiety(filtered_df), use_container_width=True)
            with col2:
                st.plotly_chart(plot_income_vs_anxiety(filtered_df), use_container_width=True)
        
        elif page == "Demographics":
            st.markdown("### 🎓 Demographic Insights")
            col1, col2 = st.columns(2)
            with col1:
                st.plotly_chart(plot_region_vs_happiness(filtered_df), use_container_width=True)
            with col2:
                st.plotly_chart(plot_gender_vs_stress(filtered_df), use_container_width=True)
            
            st.plotly_chart(plot_education_vs_dependence(filtered_df), use_container_width=True)
        
        elif page == "Behavioral Patterns":
            st.markdown("### 📊 Behavioral Patterns")
            st.plotly_chart(plot_phone_unlocks_vs_focus(filtered_df), use_container_width=True)
        
        elif page == "Raw Data":
            st.markdown("### 📋 Raw Data")
            st.dataframe(filtered_df, use_container_width=True)
            
            # Download button
            csv = filtered_df.to_csv(index=False)
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name="mental_health_data.csv",
                mime="text/csv"
            )
            
    else:
        st.error("❌ Failed to load data. Please check your Supabase connection or CSV file.")

if __name__ == "__main__":
    main()
