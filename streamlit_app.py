"""
STREAMLIT DASHBOARD: Smart-Shamba Decision Dashboard
=====================================================
Purpose: Interactive dashboard for crop planting recommendations
Author: Smart-Shamba Project
"""

import streamlit as st
import duckdb
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import os

# Page configuration
st.set_page_config(
    page_title="Smart-Shamba: Crop Advisor",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Database path - get from secrets or environment
DB_PATH = st.secrets.get("db_path", os.getenv("DB_PATH", "./warehouse/duckdb/agri_analytics.db"))

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #2E7D32;
        text-align: center;
        margin-bottom: 1rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #2E7D32;
    }
    </style>
""", unsafe_allow_html=True)


@st.cache_data(ttl=300)  # Cache for 5 minutes
def load_recommendations():
    """Load the latest crop recommendations from the mart."""
    conn = duckdb.connect(DB_PATH, read_only=True)
    query = """
        SELECT 
            district,
            crop_name,
            overall_recommendation_score,
            recommendation_category,
            weather_suitability_score,
            vegetation_suitability_score,
            market_opportunity_score,
            temperature_celsius,
            rainfall_category,
            vegetation_health,
            soil_moisture_percent,
            current_price_ugx,
            price_trend,
            crop_rank
        FROM dbt_mart_planting_advice
        ORDER BY district, overall_recommendation_score DESC
    """
    df = conn.execute(query).df()
    conn.close()
    return df


@st.cache_data(ttl=300)
def load_weather_summary():
    """Load current weather conditions."""
    conn = duckdb.connect(DB_PATH, read_only=True)
    query = """
        SELECT 
            district,
            temperature_celsius,
            humidity_percent,
            rainfall_mm,
            weather_condition
        FROM dbt_stg_weather
        ORDER BY measurement_timestamp DESC
        LIMIT 10
    """
    df = conn.execute(query).df()
    conn.close()
    return df


# Header
st.markdown('<div class="main-header">🌾 Smart-Shamba Crop Advisor</div>', unsafe_allow_html=True)
st.markdown("### Data-Driven Planting Decisions for Ugandan Farmers")
st.markdown("---")

# Load data
try:
    df_recommendations = load_recommendations()
    df_weather = load_weather_summary()
    
    # Sidebar - District Filter
    st.sidebar.header("🗺️ Select District")
    districts = ['All Districts'] + sorted(df_recommendations['district'].unique().tolist())
    selected_district = st.sidebar.selectbox("Choose a district:", districts)
    
    # Filter data
    if selected_district != 'All Districts':
        df_filtered = df_recommendations[df_recommendations['district'] == selected_district]
    else:
        df_filtered = df_recommendations
    
    # Sidebar - Info
    st.sidebar.markdown("---")
    st.sidebar.info("""
    **How It Works:**
    - Weather data (40%)
    - Soil health (35%)
    - Market prices (25%)
    
    = **Recommendation Score**
    """)
    
    # Main metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        highly_recommended = len(df_filtered[df_filtered['recommendation_category'] == 'Highly Recommended'])
        st.metric("🌟 Highly Recommended Crops", highly_recommended)
    
    with col2:
        avg_score = df_filtered['overall_recommendation_score'].mean()
        st.metric("📊 Avg Recommendation Score", f"{avg_score:.1f}/10")
    
    with col3:
        districts_count = df_filtered['district'].nunique()
        st.metric("🗺️ Districts Analyzed", districts_count)
    
    with col4:
        crops_count = df_filtered['crop_name'].nunique()
        st.metric("🌱 Crops Evaluated", crops_count)
    
    st.markdown("---")
    
    # Tab layout
    tab1, tab2, tab3, tab4 = st.tabs(["📋 Recommendations", "📈 Market Trends", "🌦️ Weather", "🗺️ District Comparison"])
    
    with tab1:
        st.subheader("🌾 Top Crop Recommendations")
        
        if selected_district != 'All Districts':
            # Show top 5 for selected district
            top_crops = df_filtered.nsmallest(5, 'crop_rank')
            
            for idx, row in top_crops.iterrows():
                with st.expander(f"**#{row['crop_rank']} {row['crop_name']}** - {row['recommendation_category']} ({row['overall_recommendation_score']:.1f}/10)", expanded=(row['crop_rank'] == 1)):
                    col_a, col_b, col_c = st.columns(3)
                    
                    with col_a:
                        st.markdown("**🌦️ Weather Suitability**")
                        st.progress(row['weather_suitability_score'] / 10)
                        st.caption(f"{row['weather_suitability_score']:.1f}/10")
                        st.caption(f"Temp: {row['temperature_celsius']:.1f}°C | Rain: {row['rainfall_category']}")
                    
                    with col_b:
                        st.markdown("**🌱 Soil & Vegetation**")
                        st.progress(row['vegetation_suitability_score'] / 10)
                        st.caption(f"{row['vegetation_suitability_score']:.1f}/10")
                        st.caption(f"Health: {row['vegetation_health']} | Moisture: {row['soil_moisture_percent']:.0f}%")
                    
                    with col_c:
                        st.markdown("**💰 Market Opportunity**")
                        st.progress(row['market_opportunity_score'] / 10)
                        st.caption(f"{row['market_opportunity_score']:.1f}/10")
                        st.caption(f"Price: {row['current_price_ugx']:.0f} UGX/kg | Trend: {row['price_trend']}")
        else:
            # Show best crop per district
            st.markdown("**Best Crop by District:**")
            best_per_district = df_filtered[df_filtered['crop_rank'] == 1]
            st.dataframe(
                best_per_district[['district', 'crop_name', 'overall_recommendation_score', 'recommendation_category']],
                use_container_width=True,
                hide_index=True
            )
    
    with tab2:
        st.subheader("💹 Market Price Trends")
        
        # Price distribution by crop
        fig_prices = px.box(
            df_filtered,
            x='crop_name',
            y='current_price_ugx',
            color='price_trend',
            title='Price Distribution by Crop',
            labels={'current_price_ugx': 'Price (UGX/kg)', 'crop_name': 'Crop'}
        )
        st.plotly_chart(fig_prices, use_container_width=True)
        
        # Market opportunity scores
        fig_market = px.bar(
            df_filtered.groupby('crop_name')['market_opportunity_score'].mean().reset_index(),
            x='crop_name',
            y='market_opportunity_score',
            title='Average Market Opportunity Score by Crop',
            labels={'market_opportunity_score': 'Market Score', 'crop_name': 'Crop'},
            color='market_opportunity_score',
            color_continuous_scale='Greens'
        )
        st.plotly_chart(fig_market, use_container_width=True)
    
    with tab3:
        st.subheader("🌦️ Current Weather Conditions")
        
        # Weather table
        st.dataframe(
            df_weather[['district', 'temperature_celsius', 'humidity_percent', 'rainfall_mm', 'weather_condition']],
            use_container_width=True,
            hide_index=True
        )
        
        # Temperature by district
        fig_temp = px.bar(
            df_weather,
            x='district',
            y='temperature_celsius',
            title='Temperature by District',
            labels={'temperature_celsius': 'Temperature (°C)', 'district': 'District'},
            color='temperature_celsius',
            color_continuous_scale='RdYlGn_r'
        )
        st.plotly_chart(fig_temp, use_container_width=True)
    
    with tab4:
        st.subheader("🗺️ District-Level Analysis")
        
        # Recommendation scores by district
        district_summary = df_filtered.groupby('district').agg({
            'overall_recommendation_score': 'mean',
            'weather_suitability_score': 'mean',
            'vegetation_suitability_score': 'mean',
            'market_opportunity_score': 'mean'
        }).reset_index()
        
        fig_district = go.Figure()
        fig_district.add_trace(go.Bar(name='Weather', x=district_summary['district'], y=district_summary['weather_suitability_score']))
        fig_district.add_trace(go.Bar(name='Vegetation', x=district_summary['district'], y=district_summary['vegetation_suitability_score']))
        fig_district.add_trace(go.Bar(name='Market', x=district_summary['district'], y=district_summary['market_opportunity_score']))
        
        fig_district.update_layout(
            barmode='group',
            title='Average Suitability Scores by District',
            xaxis_title='District',
            yaxis_title='Score (0-10)'
        )
        st.plotly_chart(fig_district, use_container_width=True)
        
        # Heatmap of recommendations
        pivot_data = df_filtered.pivot_table(
            values='overall_recommendation_score',
            index='district',
            columns='crop_name',
            aggfunc='mean'
        )
        
        fig_heatmap = px.imshow(
            pivot_data,
            title='Recommendation Heatmap: District vs Crop',
            labels=dict(x="Crop", y="District", color="Score"),
            color_continuous_scale='Greens',
            aspect='auto'
        )
        st.plotly_chart(fig_heatmap, use_container_width=True)
    
    # Footer
    st.markdown("---")
    st.markdown(f"**Last Updated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    st.caption("🌾 Smart-Shamba | Data-Driven Agriculture | Made with ❤️ for Ugandan Farmers")

except Exception as e:
    st.error(f"❌ Error loading data: {str(e)}")
    st.info("Please ensure the DuckDB database is populated with data by running the Mage pipelines first.")
