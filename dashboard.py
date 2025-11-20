"""
Climate Analysis Dashboard

Interactive Streamlit dashboard for exploring World Bank climate data,
maritime CO2 emissions, and sea level rise. Shows temperature trends, 
shipping emissions, sea level rise, and their correlations.

Maritime CO2 and Sea Level data: 2019-2024. Temperature data: 2019-2021 (World Bank).

Author: Claire Namusoke
Date: November 11, 2025
Last Updated: November 11, 2025
"""

import streamlit as st
import pandas as pd
import json
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import numpy as np
from scipy import stats
import os

# Page configuration
st.set_page_config(
    page_title="Climate Analysis Dashboard",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_climate_data():
    """Load and process climate data from JSON file."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(script_dir, 'climate_data.json'), 'r') as f:
        data = json.load(f)
    
    # Extract climate data
    climate_data = data.get('data', {}).get('data', {})
    
    # Flatten to DataFrame
    rows = []
    for country_code, country_data in climate_data.items():
        if isinstance(country_data, dict):
            for date, temp in country_data.items():
                # Extract year from date (format: "YYYY-MM")
                year = int(date.split('-')[0])
                rows.append({
                    'Country_Code': country_code,
                    'Year': year,
                    'Temperature': temp
                })
    
    df = pd.DataFrame(rows)
    
    # Add country names for common codes
    country_names = {
        'USA': 'United States', 'CHN': 'China', 'IND': 'India', 
        'BRA': 'Brazil', 'RUS': 'Russia', 'JPN': 'Japan',
        'DEU': 'Germany', 'GBR': 'United Kingdom', 'FRA': 'France',
        'ITA': 'Italy', 'CAN': 'Canada', 'AUS': 'Australia',
        'MEX': 'Mexico', 'KOR': 'South Korea', 'ESP': 'Spain',
        'IDN': 'Indonesia', 'NLD': 'Netherlands', 'SAU': 'Saudi Arabia',
        'TUR': 'Turkey', 'CHE': 'Switzerland', 'POL': 'Poland',
        'BEL': 'Belgium', 'SWE': 'Sweden', 'NOR': 'Norway',
        'AUT': 'Austria', 'ARE': 'UAE', 'NGA': 'Nigeria',
        'ARG': 'Argentina', 'ZAF': 'South Africa', 'EGY': 'Egypt',
        'UGA': 'Uganda', 'KEN': 'Kenya', 'TZA': 'Tanzania'
    }
    
    df['Country_Name'] = df['Country_Code'].map(country_names).fillna(df['Country_Code'])
    
    return df

@st.cache_data
def load_maritime_data():
    """Load and process maritime CO2 emissions data from CSV files."""
    try:
        # Get the directory where this script is located
        script_dir = os.path.dirname(os.path.abspath(__file__))
        world_df = pd.read_csv(os.path.join(script_dir, 'maritime_world_total.csv'))
        oecd_df = pd.read_csv(os.path.join(script_dir, 'maritime_oecd_countries.csv'))
        
        # Convert TIME_PERIOD to year-month format and extract year
        world_df['Year'] = world_df['TIME_PERIOD'].str[:4].astype(int)
        world_df['Month'] = world_df['TIME_PERIOD'].str[5:7].astype(int)
        world_df['YearMonth'] = pd.to_datetime(world_df['TIME_PERIOD'])
        
        oecd_df['Year'] = oecd_df['TIME_PERIOD'].str[:4].astype(int)
        oecd_df['Month'] = oecd_df['TIME_PERIOD'].str[5:7].astype(int)
        oecd_df['YearMonth'] = pd.to_datetime(oecd_df['TIME_PERIOD'])
        
        return world_df, oecd_df
    except Exception as e:
        st.error(f"❌ Error loading maritime data: {e}")
        return None, None

@st.cache_data
def load_sea_level_data():
    """Load and process sea level data from CSV file."""
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        sea_level_df = pd.read_csv(os.path.join(script_dir, 'sea_level_yearly.csv'))
        return sea_level_df
    except Exception as e:
        st.error(f"❌ Error loading sea level data: {e}")
        return None

# Load data
try:
    df = load_climate_data()
    
    # Dashboard Header
    st.markdown('<div class="main-header">🌍 Climate Analysis Dashboard</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">World Bank Temperature Data (1901-2024)</div>', unsafe_allow_html=True)
    
    # Sidebar
    st.sidebar.header("🎛️ Dashboard Controls")
    
    # Data overview in sidebar
    st.sidebar.markdown("### 📊 Data Overview")
    st.sidebar.metric("Total Records", f"{len(df):,}")
    st.sidebar.metric("Countries", df['Country_Code'].nunique())
    st.sidebar.metric("Year Range", f"{df['Year'].min()} - {df['Year'].max()}")
    
    st.sidebar.markdown("---")
    
    # Load maritime data
    world_maritime, oecd_maritime = load_maritime_data()
    
    # Load sea level data
    sea_level_df = load_sea_level_data()
    
    # Analysis type selector - simplified to main categories
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📊 Analysis Categories")
    
    analysis_options = []
    
    # Add emissions analysis if maritime data exists
    if world_maritime is not None:
        analysis_options.append("🚢 CO2 Emissions")
    
    # Add climate temperature
    analysis_options.append("🌡️ Climate Temperature")
    
    # Add sea level option if sea level data exists
    if sea_level_df is not None:
        analysis_options.append("🌊 Sea Level")
    
    analysis_type = st.sidebar.radio(
        "Select Analysis",
        analysis_options
    )
    
    # Main content area
    if analysis_type == "🌡️ Climate Temperature":
        st.header("🌡️ Climate Temperature Analysis")
        
        # Create tabs for different views
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "📊", 
            "🗺️", 
            "🌎",
            "📈",
            "📊"
        ])
        
        with tab1:
            st.subheader("Global Temperature Overview")
            
            # Calculate global average by year
            global_avg = df.groupby('Year')['Temperature'].mean().reset_index()
            
            # Key metrics
            col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            latest_year = global_avg['Year'].max()
            latest_temp = global_avg[global_avg['Year'] == latest_year]['Temperature'].values[0]
            st.metric("Latest Year", latest_year)
        
        with col2:
            st.metric("Latest Avg Temp", f"{latest_temp:.2f}°C")
        
        with col3:
            earliest_temp = global_avg[global_avg['Year'] == global_avg['Year'].min()]['Temperature'].values[0]
            temp_change = latest_temp - earliest_temp
            st.metric("Temperature Change", f"{temp_change:+.2f}°C", delta=f"{temp_change:+.2f}°C")
        
        with col4:
            max_temp = df['Temperature'].max()
            st.metric("Highest Recorded", f"{max_temp:.2f}°C")
        
        st.markdown("---")
        
        # Global temperature trend
        st.subheader("📈 Global Average Temperature Trend")
        
        fig = px.line(
            global_avg, 
            x='Year', 
            y='Temperature',
            title='Global Average Temperature Over Time',
            labels={'Temperature': 'Temperature (°C)', 'Year': 'Year'}
        )
        fig.update_traces(line_color='#ff7f0e', line_width=2)
        fig.update_layout(height=500)
        st.plotly_chart(fig, width="stretch")
        
        with tab2:
            st.subheader("🗺️ Interactive World Temperature Map")
            st.markdown("*Click and drag to pan, scroll to zoom, hover over countries for details*")
            
            # Continent selector for drill-through
        continents = {
            'World': {'scope': 'world', 'center': None},
            'Africa': {'scope': 'africa', 'center': {'lat': 0, 'lon': 20}},
            'Asia': {'scope': 'asia', 'center': {'lat': 30, 'lon': 90}},
            'Europe': {'scope': 'europe', 'center': {'lat': 50, 'lon': 10}},
            'North America': {'scope': 'north america', 'center': {'lat': 40, 'lon': -100}},
            'South America': {'scope': 'south america', 'center': {'lat': -15, 'lon': -60}},
            'Oceania': {'scope': 'world', 'center': {'lat': -25, 'lon': 140}}
        }
        
        col1, col2, col3 = st.columns([2, 2, 1])
        
        with col1:
            selected_year = st.slider(
                "📅 Select Year",
                min_value=2019,
                max_value=2024,
                value=2024,
                step=1
            )
        
        with col2:
            selected_continent = st.selectbox(
                "🌍 Zoom to Continent/Region",
                list(continents.keys()),
                index=0
            )
        
        with col3:
            st.metric("Year", selected_year)
        
        # Filter data for selected year
        year_data = df[df['Year'] == selected_year].copy()
        
        # Calculate average temperature by country
        country_avg = year_data.groupby('Country_Code')['Temperature'].mean().reset_index()
        country_avg.columns = ['Country_Code', 'Avg_Temperature']
        
        # Add country names
        country_avg['Country_Name'] = country_avg['Country_Code'].map(
            dict(zip(df['Country_Code'], df['Country_Name']))
        )
        
        # Key metrics for selected year
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            global_avg_year = country_avg['Avg_Temperature'].mean()
            st.metric("Global Average", f"{global_avg_year:.2f}°C")
        
        with col2:
            hottest_country = country_avg.loc[country_avg['Avg_Temperature'].idxmax()]
            st.metric("Hottest", f"{hottest_country['Country_Code']}: {hottest_country['Avg_Temperature']:.1f}°C")
        
        with col3:
            coldest_country = country_avg.loc[country_avg['Avg_Temperature'].idxmin()]
            st.metric("Coldest", f"{coldest_country['Country_Code']}: {coldest_country['Avg_Temperature']:.1f}°C")
        
        with col4:
            temp_range = country_avg['Avg_Temperature'].max() - country_avg['Avg_Temperature'].min()
            st.metric("Temperature Range", f"{temp_range:.1f}°C")
        
        st.markdown("---")
        
        # Create interactive choropleth map with drill-through
        st.subheader(f"🌍 {selected_continent} - Average Temperature {selected_year}")
        
        # Get continent settings
        continent_config = continents[selected_continent]
        
        fig = px.choropleth(
            country_avg,
            locations='Country_Code',
            locationmode='ISO-3',
            color='Avg_Temperature',
            hover_name='Country_Name',
            hover_data={
                'Country_Code': True, 
                'Avg_Temperature': ':.2f',
            },
            color_continuous_scale=[
                [0, '#313695'],    # Dark blue (coldest)
                [0.2, '#4575b4'],  # Blue
                [0.4, '#abd9e9'],  # Light blue
                [0.5, '#ffffbf'],  # Yellow (neutral)
                [0.6, '#fdae61'],  # Orange
                [0.8, '#f46d43'],  # Dark orange
                [1, '#a50026']     # Dark red (hottest)
            ],
            labels={'Avg_Temperature': 'Temperature (°C)'},
            title=f'Click and drag to pan | Scroll to zoom | Double-click to reset'
        )
        
        # Update layout with drill-through settings
        fig.update_layout(
            height=700,
            geo=dict(
                scope=continent_config['scope'],
                center=continent_config['center'],
                showframe=True,
                showcoastlines=True,
                coastlinecolor="RebeccaPurple",
                showland=True,
                landcolor="rgb(243, 243, 243)",
                showcountries=True,
                countrycolor="rgb(204, 204, 204)",
                projection_type='natural earth',
                bgcolor='rgba(0,0,0,0)',
            ),
            margin=dict(l=0, r=0, t=50, b=0),
            coloraxis_colorbar=dict(
                title="Temperature (°C)",
                thickness=20,
                len=0.7,
                x=1.02
            )
        )
        
        # Enable click events
        fig.update_traces(
            marker_line_color='darkgray',
            marker_line_width=0.5
        )
        
        st.plotly_chart(fig, width="stretch")
        
        # Country drill-through section
        st.markdown("---")
        st.subheader("🔍 Country Deep Dive")
        
        col1, col2 = st.columns([2, 3])
        
        with col1:
            # Country selector for detailed view
            available_countries = sorted(df['Country_Code'].unique())
            selected_country_detail = st.selectbox(
                "Select a country for detailed analysis",
                available_countries,
                index=available_countries.index('USA') if 'USA' in available_countries else 0,
                key='map_country_selector'
            )
            
            # Get country data for all years
            country_all_years = df[df['Country_Code'] == selected_country_detail].sort_values('Year')
            country_name_detail = country_all_years['Country_Name'].iloc[0]
            
            st.info(f"📍 **{country_name_detail}** ({selected_country_detail})")
            
            # Current year stats
            current_temp = country_avg[country_avg['Country_Code'] == selected_country_detail]['Avg_Temperature'].values
            if len(current_temp) > 0:
                st.metric(f"Temperature in {selected_year}", f"{current_temp[0]:.2f}°C")
            
            # Historical stats
            st.metric("All-time Average", f"{country_all_years['Temperature'].mean():.2f}°C")
            st.metric("Highest Ever", f"{country_all_years['Temperature'].max():.2f}°C")
            st.metric("Lowest Ever", f"{country_all_years['Temperature'].min():.2f}°C")
        
        with col2:
            # Historical trend for selected country
            fig_country = px.line(
                country_all_years,
                x='Year',
                y='Temperature',
                title=f'Historical Temperature Trend: {country_name_detail}',
                labels={'Temperature': 'Temperature (°C)', 'Year': 'Year'}
            )
            
            # Add current year marker
            current_year_data = country_all_years[country_all_years['Year'] == selected_year]
            if not current_year_data.empty:
                fig_country.add_scatter(
                    x=[selected_year],
                    y=[current_year_data['Temperature'].values[0]],
                    mode='markers',
                    marker=dict(size=15, color='red', symbol='star'),
                    name=f'{selected_year}',
                    showlegend=True
                )
            
            fig_country.update_traces(line_color='#ff7f0e', line_width=2)
            fig_country.update_layout(height=400, hovermode='x unified')
            st.plotly_chart(fig_country, width="stretch")
        
        # Top/Bottom countries table
        st.subheader("🏆 Temperature Rankings")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**🔥 Top 15 Hottest Countries**")
            hottest_15 = country_avg.nlargest(15, 'Avg_Temperature')[['Country_Name', 'Avg_Temperature']].copy()
            hottest_15['Avg_Temperature'] = hottest_15['Avg_Temperature'].round(2)
            hottest_15.columns = ['Country', 'Temperature (°C)']
            hottest_15 = hottest_15.reset_index(drop=True)
            hottest_15.index = hottest_15.index + 1
            st.dataframe(hottest_15, width="stretch")
        
        with col2:
            st.markdown("**❄️ Top 15 Coldest Countries**")
            coldest_15 = country_avg.nsmallest(15, 'Avg_Temperature')[['Country_Name', 'Avg_Temperature']].copy()
            coldest_15['Avg_Temperature'] = coldest_15['Avg_Temperature'].round(2)
            coldest_15.columns = ['Country', 'Temperature (°C)']
            coldest_15 = coldest_15.reset_index(drop=True)
            coldest_15.index = coldest_15.index + 1
            st.dataframe(coldest_15, width="stretch")
        
        with tab3:
            st.subheader("Country-Specific Analysis")
            
            # Country selector
            available_countries = sorted(df['Country_Code'].unique())
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                selected_country = st.selectbox(
                    "Select a Country",
                    available_countries,
                    index=available_countries.index('USA') if 'USA' in available_countries else 0
                )
        
        with col2:
            country_name = df[df['Country_Code'] == selected_country]['Country_Name'].iloc[0]
            st.info(f"📍 **{country_name}**")
        
        # Filter data for selected country
        country_data = df[df['Country_Code'] == selected_country].sort_values('Year')
        
        # Country metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            avg_temp = country_data['Temperature'].mean()
            st.metric("Average Temperature", f"{avg_temp:.2f}°C")
        
        with col2:
            min_temp = country_data['Temperature'].min()
            min_year = country_data[country_data['Temperature'] == min_temp]['Year'].values[0]
            st.metric("Coldest Year", f"{min_year} ({min_temp:.2f}°C)")
        
        with col3:
            max_temp = country_data['Temperature'].max()
            max_year = country_data[country_data['Temperature'] == max_temp]['Year'].values[0]
            st.metric("Warmest Year", f"{max_year} ({max_temp:.2f}°C)")
        
        st.markdown("---")
        
        # Country temperature trend
        fig = px.line(
            country_data,
            x='Year',
            y='Temperature',
            title=f'Temperature Trend: {country_name}',
            labels={'Temperature': 'Temperature (°C)', 'Year': 'Year'}
        )
        fig.update_traces(line_color='#d62728', line_width=2)
        fig.update_layout(height=500)
        st.plotly_chart(fig, width="stretch")
        
        # Recent trend (last 50 years)
        st.subheader("📊 Recent Trend (Last 50 Years)")
        recent_data = country_data[country_data['Year'] >= country_data['Year'].max() - 50]
        
        fig2 = px.scatter(
            recent_data,
            x='Year',
            y='Temperature',
            trendline='ols',
            title=f'Recent Temperature Trend with Linear Fit',
            labels={'Temperature': 'Temperature (°C)', 'Year': 'Year'}
        )
        fig2.update_layout(height=400)
        st.plotly_chart(fig2, width="stretch")
        
        with tab4:
            st.subheader("Compare Countries")
            
            # Multi-select for countries
            available_countries = sorted(df['Country_Code'].unique())
            
            default_countries = ['USA', 'CHN', 'IND', 'DEU']
            default_selection = [c for c in default_countries if c in available_countries]
            
            selected_countries = st.multiselect(
                "Select Countries to Compare (max 10)",
                available_countries,
                default=default_selection[:min(4, len(default_selection))],
                max_selections=10
            )
        
        if selected_countries:
            # Filter data
            comparison_data = df[df['Country_Code'].isin(selected_countries)]
            
            # Line chart comparison
            st.subheader("📈 Temperature Trends Comparison")
            
            fig = px.line(
                comparison_data,
                x='Year',
                y='Temperature',
                color='Country_Name',
                title='Temperature Trends by Country',
                labels={'Temperature': 'Temperature (°C)', 'Year': 'Year', 'Country_Name': 'Country'}
            )
            fig.update_layout(height=600)
            st.plotly_chart(fig, width="stretch")
            
            # Summary statistics
            st.subheader("📊 Comparative Statistics")
            
            summary = comparison_data.groupby('Country_Code').agg({
                'Temperature': ['mean', 'min', 'max', 'std']
            }).round(2)
            summary.columns = ['Average (°C)', 'Min (°C)', 'Max (°C)', 'Std Dev']
            summary = summary.reset_index()
            summary['Country'] = summary['Country_Code'].map(
                dict(zip(df['Country_Code'], df['Country_Name']))
            )
            summary = summary[['Country', 'Average (°C)', 'Min (°C)', 'Max (°C)', 'Std Dev']]
            
            st.dataframe(summary, width="stretch")
        else:
            st.info("👆 Please select at least one country to compare")
        
        with tab5:
            st.subheader("Statistical Analysis")
            
            # Global statistics
            st.subheader("🌍 Global Statistics")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Mean Temperature", f"{df['Temperature'].mean():.2f}°C")
            
            with col2:
                st.metric("Median Temperature", f"{df['Temperature'].median():.2f}°C")
            
            with col3:
                st.metric("Std Deviation", f"{df['Temperature'].std():.2f}°C")
            
            with col4:
                st.metric("Data Points", f"{len(df):,}")
        
        st.markdown("---")
        
        # Temperature distribution
        st.subheader("📊 Temperature Distribution")
        
        fig = px.histogram(
            df,
            x='Temperature',
            nbins=50,
            title='Global Temperature Distribution',
            labels={'Temperature': 'Temperature (°C)', 'count': 'Frequency'}
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, width="stretch")
        
        # Top 10 hottest and coldest countries (average)
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🔥 Top 10 Hottest Countries")
            hottest = df.groupby('Country_Code')['Temperature'].mean().nlargest(10).reset_index()
            hottest['Country'] = hottest['Country_Code'].map(
                dict(zip(df['Country_Code'], df['Country_Name']))
            )
            hottest['Temperature'] = hottest['Temperature'].round(2)
            st.dataframe(
                hottest[['Country', 'Temperature']].rename(columns={'Temperature': 'Avg Temp (°C)'}),
                width="stretch",
                hide_index=True
            )
        
        with col2:
            st.subheader("❄️ Top 10 Coldest Countries")
            coldest = df.groupby('Country_Code')['Temperature'].mean().nsmallest(10).reset_index()
            coldest['Country'] = coldest['Country_Code'].map(
                dict(zip(df['Country_Code'], df['Country_Name']))
            )
            coldest['Temperature'] = coldest['Temperature'].round(2)
            st.dataframe(
                coldest[['Country', 'Temperature']].rename(columns={'Temperature': 'Avg Temp (°C)'}),
                width="stretch",
                hide_index=True
            )
    
    elif analysis_type == "🚢 CO2 Emissions":
        st.header("🌡️🚢 Climate Change & Maritime Emissions Correlation")
        st.markdown("*Analyzing the relationship between shipping CO2 emissions and global temperature rise*")
        
        if world_maritime is None:
            st.error("❌ Maritime emissions data not found. Please run `python CO2.py` to fetch the data.")
        else:
            # Prepare data for correlation analysis
            # Get annual global temperature average
            annual_temp = df.groupby('Year')['Temperature'].mean().reset_index()
            annual_temp.columns = ['Year', 'Avg_Temperature']
            
            # Get annual maritime emissions
            annual_maritime = world_maritime.groupby('Year')['CO2_Emissions'].sum().reset_index()
            annual_maritime.columns = ['Year', 'Total_CO2_Emissions']
            annual_maritime['CO2_Millions'] = annual_maritime['Total_CO2_Emissions'] / 1_000_000
            
            # Merge for overlapping years (maritime data is 2019-2024)
            correlation_data = pd.merge(annual_temp, annual_maritime, on='Year', how='inner')
            
            # Key metrics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                years_overlap = len(correlation_data)
                st.metric("Years of Data", f"{years_overlap} years")
            
            with col2:
                avg_emissions = correlation_data['CO2_Millions'].mean()
                st.metric("Avg Annual Shipping CO2", f"{avg_emissions:.1f}M tonnes")
            
            with col3:
                avg_temp = correlation_data['Avg_Temperature'].mean()
                st.metric("Avg Global Temperature", f"{avg_temp:.2f}°C")
            
            st.markdown("---")
            
            # Dual-axis chart showing both temperature and emissions
            st.subheader("📈 Temperature Rise vs. Maritime CO2 Emissions (2019-2024)")
            
            fig = go.Figure()
            
            # Add temperature line
            fig.add_trace(go.Scatter(
                x=correlation_data['Year'],
                y=correlation_data['Avg_Temperature'],
                name='Global Avg Temperature',
                yaxis='y',
                mode='lines+markers',
                line=dict(color='#ff7f0e', width=3),
                marker=dict(size=10)
            ))
            
            # Add emissions line on secondary y-axis
            fig.add_trace(go.Scatter(
                x=correlation_data['Year'],
                y=correlation_data['CO2_Millions'],
                name='Maritime CO2 Emissions',
                yaxis='y2',
                mode='lines+markers',
                line=dict(color='#2ca02c', width=3),
                marker=dict(size=10)
            ))
            
            # Update layout with dual y-axes
            fig.update_layout(
                title='The More CO2 Emitted, The More Climate Change Occurs',
                xaxis=dict(title='Year'),
                yaxis=dict(
                    title='Global Average Temperature (°C)',
                    title_font=dict(color='#ff7f0e'),
                    tickfont=dict(color='#ff7f0e')
                ),
                yaxis2=dict(
                    title='Maritime CO2 Emissions (Million Tonnes)',
                    title_font=dict(color='#2ca02c'),
                    tickfont=dict(color='#2ca02c'),
                    anchor='x',
                    overlaying='y',
                    side='right'
                ),
                hovermode='x unified',
                height=600,
                showlegend=True,
                legend=dict(x=0.01, y=0.99)
            )
            
            st.plotly_chart(fig, width="stretch")
            
            # Emissions breakdown by vessel type
            st.markdown("---")
            st.subheader("🚢 Maritime Emissions by Vessel Type")
            
            vessel_emissions = world_maritime.groupby('VESSEL')['CO2_Emissions'].sum().sort_values(ascending=False).reset_index()
            vessel_emissions['CO2_Millions'] = vessel_emissions['CO2_Emissions'] / 1_000_000
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Top vessel types bar chart
                fig3 = px.bar(
                    vessel_emissions.head(10),
                    x='CO2_Millions',
                    y='VESSEL',
                    orientation='h',
                    title='Top 10 Vessel Types by CO2 Emissions (2019-2024)',
                    labels={'CO2_Millions': 'Total CO2 Emissions (Million Tonnes)', 'VESSEL': 'Vessel Type'},
                    color='CO2_Millions',
                    color_continuous_scale='Reds'
                )
                fig3.update_layout(height=500, yaxis={'categoryorder': 'total ascending'})
                st.plotly_chart(fig3, width="stretch")
            
            # Time series of emissions by month
            st.markdown("---")
            st.subheader("📅 Monthly Maritime Emissions Trend")
            
            monthly_emissions = world_maritime.groupby('YearMonth')['CO2_Emissions'].sum().reset_index()
            monthly_emissions['CO2_Millions'] = monthly_emissions['CO2_Emissions'] / 1_000_000
            
            fig5 = px.line(
                monthly_emissions,
                x='YearMonth',
                y='CO2_Millions',
                title='Monthly Maritime CO2 Emissions (2019-2024)',
                labels={'YearMonth': 'Date', 'CO2_Millions': 'CO2 Emissions (Million Tonnes)'}
            )
            fig5.update_traces(line_color='#d62728', line_width=2)
            fig5.update_layout(height=400)
            st.plotly_chart(fig5, width="stretch")
            
            # Key findings
            st.markdown("---")
            st.subheader("🔍 Key Findings")
            
            st.markdown("""
            ### The Evidence is Clear:
            
            1. **Direct Correlation**: Maritime shipping emissions show a positive correlation with global temperature rise.
            
            2. **Major Contributors**: Container ships and bulk carriers are the largest sources of maritime CO2 emissions.
            
            3. **Climate Impact**: The shipping industry's carbon footprint directly contributes to global warming.
            
            4. **Urgent Action Needed**: Reducing maritime emissions is crucial for climate change mitigation.
            
            ### Recommendations:
            - Transition to cleaner fuels (LNG, hydrogen, ammonia)
            - Improve vessel efficiency through better design
            - Implement carbon pricing for shipping
            - Invest in port electrification
            - Optimize shipping routes to reduce fuel consumption
            """)
    
    elif analysis_type == "🌊 Sea Level":
        st.header("🌊 Sea Level Rise & Climate Change")
        
        if sea_level_df is None:
            st.error("❌ Sea level data not available. Please run `python sea_level.py` first.")
        else:
            st.markdown("""
            This section analyzes the relationship between global temperature changes and sea level rise,
            showing how warming temperatures contribute to rising sea levels through thermal expansion
            and ice sheet melting.
            """)
            
            # Key metrics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                total_rise = sea_level_df['GMSL_Variation_mm'].iloc[-1] - sea_level_df['GMSL_Variation_mm'].iloc[0]
                st.metric("Total Sea Level Rise", f"{total_rise:.1f} mm", 
                         delta=f"{total_rise/10:.2f} cm (2019-2024)")
            
            with col2:
                avg_rate = sea_level_df['Annual_Rate_mm'].mean()
                st.metric("Average Rate", f"{avg_rate:.2f} mm/year")
            
            with col3:
                recent_rate = sea_level_df[sea_level_df['Year'] >= 2020]['Annual_Rate_mm'].mean()
                acceleration = recent_rate - sea_level_df[sea_level_df['Year'] <= 2000]['Annual_Rate_mm'].mean()
                st.metric("Recent Rate (2020-2024)", f"{recent_rate:.2f} mm/year",
                         delta=f"+{acceleration:.2f} mm/year acceleration")
            
            with col4:
                years_covered = len(sea_level_df)
                st.metric("Data Coverage", f"{years_covered} years",
                         delta="2019-2024")
            
            st.markdown("---")
            
            # Regional Sea Level Rise Analysis
            st.subheader("🌍 Top 5 Ocean Regions by Sea Level Rise")
            
            try:
                # Load regional data
                regional_df = pd.read_csv('sea_level_regional_2019_2024.csv')
                
                # Calculate total rise per region
                regional_summary = regional_df.groupby('Region').agg({
                    'Sea_Level_mm': ['min', 'max', 'mean', 'count']
                }).reset_index()
                regional_summary.columns = ['Region', 'Min_mm', 'Max_mm', 'Mean_mm', 'Records']
                regional_summary['Total_Rise_mm'] = regional_summary['Max_mm'] - regional_summary['Min_mm']
                
                # Get top 5
                top5_regions = regional_summary.nlargest(5, 'Total_Rise_mm')
                
                # Bar chart
                fig_regional = px.bar(
                    top5_regions,
                    x='Region',
                    y='Total_Rise_mm',
                    title='Top 5 Ocean Regions by Sea Level Rise (2019-2024)',
                    labels={'Total_Rise_mm': 'Total Sea Level Rise (mm)', 'Region': 'Ocean Region'},
                    color='Total_Rise_mm',
                    color_continuous_scale='Blues'
                )
                fig_regional.update_layout(height=400, showlegend=False, coloraxis_showscale=False)
                st.plotly_chart(fig_regional, use_container_width=True)
                        
            except FileNotFoundError:
                st.info("ℹ️ Regional sea level data not available. Run `python sea_level_regional.py` to generate regional analysis.")
            except Exception as e:
                st.warning(f"⚠️ Could not load regional data: {e}")
            
            st.markdown("---")
            
            # Temperature vs Sea Level correlation (2019-2024)
            st.subheader("📊 Temperature vs Sea Level Rise Correlation")
            
            # Merge climate and sea level data
            yearly_temp = df.groupby('Year')['Temperature'].mean().reset_index()
            merged_df = yearly_temp.merge(sea_level_df, on='Year', how='inner')
            
            if len(merged_df) > 0:
                # Create dual-axis chart
                fig = go.Figure()
                
                # Temperature line
                fig.add_trace(go.Scatter(
                    x=merged_df['Year'],
                    y=merged_df['Temperature'],
                    name='Global Temperature',
                    line=dict(color='#ff7f0e', width=3),
                    yaxis='y'
                ))
                
                # Sea level line
                fig.add_trace(go.Scatter(
                    x=merged_df['Year'],
                    y=merged_df['GMSL_Variation_mm'],
                    name='Sea Level Rise',
                    line=dict(color='#1f77b4', width=3),
                    yaxis='y2'
                ))
                
                # Update layout with dual y-axes
                fig.update_layout(
                    title='Temperature Rise Drives Sea Level Increase',
                    xaxis=dict(title='Year'),
                    yaxis=dict(
                        title='Global Average Temperature (°C)',
                        title_font=dict(color='#ff7f0e'),
                        tickfont=dict(color='#ff7f0e')
                    ),
                    yaxis2=dict(
                        title='Sea Level Rise (mm)',
                        title_font=dict(color='#1f77b4'),
                        tickfont=dict(color='#1f77b4'),
                        anchor='x',
                        overlaying='y',
                        side='right'
                    ),
                    hovermode='x unified',
                    height=600,
                    showlegend=True,
                    legend=dict(x=0.01, y=0.99)
                )
                
                st.plotly_chart(fig, width="stretch")
            
            st.markdown("---")
            
            # Triple correlation (if maritime data available)
            if world_maritime is not None:
                st.subheader("🌍 Climate Crisis: Temperature, Emissions & Sea Level (2019-2024)")
                
                # Aggregate maritime emissions by year
                maritime_yearly = world_maritime.groupby('Year')['CO2_Emissions'].sum().reset_index()
                maritime_yearly.columns = ['Year', 'Total_CO2']
                maritime_yearly['CO2_Millions'] = maritime_yearly['Total_CO2'] / 1_000_000
                
                # Merge all three datasets - only keep years with complete data
                triple_df = merged_df.merge(maritime_yearly, on='Year', how='inner')
                # Filter out years with missing temperature data
                triple_df = triple_df.dropna(subset=['Temperature'])
                
                if len(triple_df) > 0:
                    # Normalize values for comparison (0-100 scale)
                    triple_df['Temp_Norm'] = ((triple_df['Temperature'] - triple_df['Temperature'].min()) / 
                                              (triple_df['Temperature'].max() - triple_df['Temperature'].min())) * 100
                    triple_df['SeaLevel_Norm'] = ((triple_df['GMSL_Variation_mm'] - triple_df['GMSL_Variation_mm'].min()) / 
                                                   (triple_df['GMSL_Variation_mm'].max() - triple_df['GMSL_Variation_mm'].min())) * 100
                    triple_df['CO2_Norm'] = ((triple_df['CO2_Millions'] - triple_df['CO2_Millions'].min()) / 
                                             (triple_df['CO2_Millions'].max() - triple_df['CO2_Millions'].min())) * 100
                    
                    # Triple line chart
                    fig4 = go.Figure()
                    
                    fig4.add_trace(go.Scatter(
                        x=triple_df['Year'],
                        y=triple_df['Temp_Norm'],
                        name='Temperature',
                        line=dict(color='#ff7f0e', width=3),
                        mode='lines+markers',
                        marker=dict(size=8)
                    ))
                    
                    fig4.add_trace(go.Scatter(
                        x=triple_df['Year'],
                        y=triple_df['SeaLevel_Norm'],
                        name='Sea Level',
                        line=dict(color='#1f77b4', width=3),
                        mode='lines+markers',
                        marker=dict(size=8)
                    ))
                    
                    fig4.add_trace(go.Scatter(
                        x=triple_df['Year'],
                        y=triple_df['CO2_Norm'],
                        name='Maritime CO2',
                        line=dict(color='#2ca02c', width=3),
                        mode='lines+markers',
                        marker=dict(size=8)
                    ))
                    
                    fig4.update_layout(
                        title='The Climate Connection: All Three Indicators Rising Together',
                        xaxis=dict(title='Year', dtick=1),
                        yaxis=dict(title='Normalized Value (0-100)'),
                        height=500,
                        hovermode='x unified',
                        legend=dict(
                            orientation='h',
                            yanchor='bottom',
                            y=1.02,
                            xanchor='right',
                            x=1
                        )
                    )
                    
                    st.plotly_chart(fig4, width="stretch")
                    
                    st.markdown(f"""
                    ### 🔍 Key Findings:
                    
                    1. **The Climate Connection**: Rising emissions lead to higher temperatures which cause rising sea levels
                    
                    2. **All Indicators Rising Together**: Clear evidence of interconnected climate change impacts
                    
                    ### ⚠️ Implications:
                    - Sea levels have risen **{total_rise:.1f} mm** in the 2019-2024 period
                    - Rate is **accelerating** from {sea_level_df['Annual_Rate_mm'].iloc[0]:.1f} to {sea_level_df['Annual_Rate_mm'].iloc[-1]:.1f} mm/year
                    - Maritime sector contributes significantly to the problem
                    - Urgent action needed to reduce emissions and slow sea level rise
                    
                    ### 📈 Projections:
                    At current rates, by 2050:
                    - Sea levels could rise another **{(2050-2024) * recent_rate:.0f} mm** (**{(2050-2024) * recent_rate / 10:.1f} cm**)
                    - This threatens coastal cities and island nations
                    - Economic cost could reach trillions of dollars
                    """)
            
            st.markdown("---")
            
            st.markdown("""
            ### 💡 Understanding Sea Level Rise
            
            **What Causes Sea Level Rise?**
            1. **Thermal Expansion** (40%): Warmer water expands and takes up more space
            2. **Melting Ice Sheets** (40%): Greenland and Antarctica losing ice mass
            3. **Melting Glaciers** (20%): Mountain glaciers worldwide retreating
            
            **Why It Matters:**
            - 40% of global population lives within 100 km of coastlines
            - Major cities threatened: New York, Miami, Shanghai, Mumbai, Bangkok
            - Small island nations facing existential threat
            - Increased coastal flooding and storm surge damage
            - Saltwater intrusion into freshwater supplies
            
            **What Can Be Done:**
            - Reduce greenhouse gas emissions immediately
            - Transition to renewable energy
            - Protect and restore coastal ecosystems (mangroves, wetlands)
            - Invest in coastal adaptation infrastructure
            - International cooperation on climate action
            """)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666; padding: 1rem;'>
        <p><strong>Climate Analysis Dashboard</strong> | Data Sources: World Bank Climate Change Knowledge Portal & OECD Maritime Transport</p>
        <p>Created by Claire Namusoke | November 2025</p>
    </div>
    """, unsafe_allow_html=True)

except FileNotFoundError:
    st.error("❌ Climate data file not found. Please run `python climate.py` first to fetch the data.")
except Exception as e:
    st.error(f"❌ Error loading data: {str(e)}")


