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

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 0rem 1rem;
    }
    .stPlotlyChart {
        background-color: #f0f2f6;
        border-radius: 10px;
        padding: 10px;
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
        line=dict(color='#FF6B6B', width=3),
        marker=dict(size=10, color='#FF6B6B')
    ))
    
    fig.update_layout(
        title='Device Usage vs Stress Level',
        xaxis_title='Daily Device Usage',
        yaxis_title='Average Stress Level',
        template='plotly_white',
        height=400
    )
    return fig

def plot_sleep_vs_anxiety(df):
    """2. Sleep Duration vs Anxiety Score - Column Bar Chart"""
    df['sleep_category'] = df['sleep_duration'].apply(categorize_sleep)
    
    category_order = ["<6 hours", "6-7 hours", "7-8 hours", ">8 hours"]
    grouped = df.groupby('sleep_category')['anxiety_score'].mean().reindex(category_order)
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=grouped.index,
        y=grouped.values,
        marker=dict(color='#4ECDC4', line=dict(color='#2C7873', width=1.5)),
        text=grouped.values.round(2),
        textposition='outside'
    ))
    
    fig.update_layout(
        title='Sleep Duration vs Anxiety Score',
        xaxis_title='Sleep Duration',
        yaxis_title='Average Anxiety Score',
        template='plotly_white',
        height=400
    )
    return fig

def plot_device_type_vs_productivity(df):
    """3. Device Type vs Productivity Score - Horizontal Bar Chart"""
    grouped = df.groupby('device_type')['productivity_score'].mean().sort_values()
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=grouped.index,
        x=grouped.values,
        orientation='h',
        marker=dict(color='#95E1D3', line=dict(color='#38A3A5', width=1.5)),
        text=grouped.values.round(2),
        textposition='outside'
    ))
    
    fig.update_layout(
        title='Device Type vs Productivity Score',
        xaxis_title='Average Productivity Score',
        yaxis_title='Device Type',
        template='plotly_white',
        height=400
    )
    return fig

def plot_region_vs_happiness(df):
    """4. Region vs Happiness Score - Pie Chart"""
    grouped = df.groupby('region')['happiness_score'].mean()
    
    fig = go.Figure()
    fig.add_trace(go.Pie(
        labels=grouped.index,
        values=grouped.values,
        hole=0.3,
        marker=dict(colors=['#FFD93D', '#6BCB77', '#4D96FF', '#FF6B9D', '#C780FA', '#FFA500']),
        textinfo='label+percent',
        textposition='outside'
    ))
    
    fig.update_layout(
        title='Region vs Happiness Score Distribution',
        template='plotly_white',
        height=400
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
        line=dict(color='#A463F2', width=2),
        fillcolor='rgba(164, 99, 242, 0.3)'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, grouped.max() * 1.2])
        ),
        title='Education Level vs Digital Dependence Score',
        template='plotly_white',
        height=500
    )
    return fig

def plot_gender_vs_stress(df):
    """6. Gender vs Stress Level - Clustered Bar Chart"""
    grouped = df.groupby('gender')['stress_level'].agg(['mean', 'std']).reset_index()
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=grouped['gender'],
        y=grouped['mean'],
        name='Average Stress',
        marker=dict(color='#FF9671'),
        error_y=dict(type='data', array=grouped['std'], visible=True),
        text=grouped['mean'].round(2),
        textposition='outside'
    ))
    
    fig.update_layout(
        title='Gender vs Stress Level',
        xaxis_title='Gender',
        yaxis_title='Average Stress Level',
        template='plotly_white',
        height=400,
        barmode='group'
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
        line=dict(color='#FFA07A', width=3),
        marker=dict(size=10, color='#FFA07A')
    ))
    
    fig.update_layout(
        title='Phone Unlocks vs Focus Score',
        xaxis_title='Daily Phone Unlocks',
        yaxis_title='Average Focus Score',
        template='plotly_white',
        height=400
    )
    return fig

def plot_income_vs_anxiety(df):
    """8. Income Level vs Anxiety Score - Box Plot"""
    income_order = ['Low', 'Lower-Mid', 'Upper-Mid', 'High']
    
    fig = go.Figure()
    
    colors = {'Low': '#FF6B6B', 'Lower-Mid': '#FFD93D', 'Upper-Mid': '#6BCB77', 'High': '#4D96FF'}
    
    for income in income_order:
        data = df[df['income_level'] == income]['anxiety_score']
        fig.add_trace(go.Box(
            y=data,
            name=income,
            marker=dict(color=colors.get(income, '#999999')),
            boxmean='sd'
        ))
    
    fig.update_layout(
        title='Income Level vs Anxiety Score Distribution',
        xaxis_title='Income Level',
        yaxis_title='Anxiety Score',
        template='plotly_white',
        height=400
    )
    return fig

# ========== MAIN APP ==========

def main():
    st.title("📊 Mental Health & Digital Usage Analytics Dashboard")
    st.markdown("---")
    
    # Load data
    with st.spinner("Loading data from Supabase..."):
        df = load_data()
    
    if df is not None and not df.empty:
        st.success(f"✅ Data loaded successfully! Total records: {len(df)}")
        
        # Sidebar filters
        st.sidebar.header("🔍 Filters")
        
        # Gender filter
        gender_options = ['All'] + list(df['gender'].unique())
        selected_gender = st.sidebar.selectbox("Gender", gender_options)
        
        # Region filter
        region_options = ['All'] + list(df['region'].unique())
        selected_region = st.sidebar.selectbox("Region", region_options)
        
        # Apply filters
        filtered_df = df.copy()
        if selected_gender != 'All':
            filtered_df = filtered_df[filtered_df['gender'] == selected_gender]
        if selected_region != 'All':
            filtered_df = filtered_df[filtered_df['region'] == selected_region]
        
        st.sidebar.markdown(f"**Filtered records:** {len(filtered_df)}")
        
        # Display statistics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Avg Stress Level", f"{filtered_df['stress_level'].mean():.2f}")
        with col2:
            st.metric("Avg Anxiety Score", f"{filtered_df['anxiety_score'].mean():.2f}")
        with col3:
            st.metric("Avg Device Hours", f"{filtered_df['device_hours_per_day'].mean():.2f}")
        with col4:
            st.metric("Avg Happiness", f"{filtered_df['happiness_score'].mean():.2f}")
        
        st.markdown("---")
        
        # Visualizations in tabs
        tab1, tab2, tab3, tab4 = st.tabs(["📱 Device Usage", "😴 Sleep & Mental Health", "🎓 Demographics", "📊 Behavioral Patterns"])
        
        with tab1:
            st.subheader("Device Usage Analysis")
            col1, col2 = st.columns(2)
            with col1:
                st.plotly_chart(plot_device_usage_vs_stress(filtered_df), use_container_width=True)
            with col2:
                st.plotly_chart(plot_device_type_vs_productivity(filtered_df), use_container_width=True)
        
        with tab2:
            st.subheader("Sleep & Mental Health Insights")
            col1, col2 = st.columns(2)
            with col1:
                st.plotly_chart(plot_sleep_vs_anxiety(filtered_df), use_container_width=True)
            with col2:
                st.plotly_chart(plot_income_vs_anxiety(filtered_df), use_container_width=True)
        
        with tab3:
            st.subheader("Demographic Insights")
            col1, col2 = st.columns(2)
            with col1:
                st.plotly_chart(plot_region_vs_happiness(filtered_df), use_container_width=True)
            with col2:
                st.plotly_chart(plot_gender_vs_stress(filtered_df), use_container_width=True)
            
            st.plotly_chart(plot_education_vs_dependence(filtered_df), use_container_width=True)
        
        with tab4:
            st.subheader("Behavioral Patterns")
            st.plotly_chart(plot_phone_unlocks_vs_focus(filtered_df), use_container_width=True)
        
        # Raw data view
        with st.expander("📋 View Raw Data"):
            st.dataframe(filtered_df, use_container_width=True)
            
    else:
        st.error("❌ Failed to load data. Please check your Supabase connection or CSV file.")

if __name__ == "__main__":
    main()
