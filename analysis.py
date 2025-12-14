import streamlit as st
import pandas as pd
import json
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import numpy as np
from scipy import stats
import os

st.set_page_config(
    page_title="Climate Analysis Dashboard",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

def get_analysis_options(world_maritime, sea_level_df):
    options = []
    if world_maritime is not None:
        options.append("🚢 CO2 Emissions")
    options.append("🌡️ Climate Temperature")
    if sea_level_df is not None:
        options.append("🌊 Sea Level")
    return options

st.markdown("""
<style>
    .main-header {
        font-size: 2.1rem;
        font-weight: bold;
        color: #d62728;
        text-align: center;
        margin-bottom: 0.2rem;
        margin-top: 0.2rem;
        padding: 0;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #666;
        text-align: center;
        margin-bottom: 0.7rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 0.5rem;
        border-radius: 0.3rem;
        text-align: center;
    }
    section[data-testid="stSidebar"] > div:first-child {
        background-color: #000 !important;
        color: #fff !important;
    }
    section[data-testid="stSidebar"] * {
        color: #fff !important;
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
                # Extract year from date (format: "YYYY-MM") with error handling
                year_str = str(date).split('-')[0].replace(',', '')
                if year_str.isdigit():
                    year = int(year_str)
                else:
                    st.warning(f"Invalid year in date: {date}")
                    continue
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
        'UGA': 'Uganda', 'KEN': 'Kenya', 'TZA': 'Tanzania',
        'COG': 'Republic of the Congo', 'COL': 'Colombia', 'CIV': "Côte d'Ivoire", 'CHL': 'Chile',
        'AGO': 'Angola', 'ALB': 'Albania', 'AND': 'Andorra', 'ARM': 'Armenia', 'AUS': 'Australia',
        'ATG': 'Antigua and Barbuda', 'AZE': 'Azerbaijan', 'BDI': 'Burundi', 'BEN': 'Benin', 'BFA': 'Burkina Faso',
        'BGD': 'Bangladesh', 'BGR': 'Bulgaria', 'BHR': 'Bahrain', 'BHS': 'Bahamas', 'BIH': 'Bosnia and Herzegovina',
        'BLR': 'Belarus', 'BLZ': 'Belize', 'BMU': 'Bermuda', 'BOL': 'Bolivia', 'BRB': 'Barbados',
        'BRN': 'Brunei', 'BTN': 'Bhutan', 'BWA': 'Botswana', 'CAF': 'Central African Republic', 'CAN': 'Canada',
        'CHE': 'Switzerland', 'CHN': 'China', 'CYP': 'Cyprus', 'CZE': 'Czechia', 'DNK': 'Denmark',
        'DOM': 'Dominican Republic', 'DZA': 'Algeria', 'ECU': 'Ecuador', 'EST': 'Estonia', 'ETH': 'Ethiopia',
        'FIN': 'Finland', 'FJI': 'Fiji', 'FRA': 'France', 'GAB': 'Gabon', 'GHA': 'Ghana',
        'GRC': 'Greece', 'GRD': 'Grenada', 'GTM': 'Guatemala', 'GUY': 'Guyana', 'HND': 'Honduras',
        'HRV': 'Croatia', 'HTI': 'Haiti', 'HUN': 'Hungary', 'IDN': 'Indonesia', 'IRL': 'Ireland',
        'IRN': 'Iran', 'IRQ': 'Iraq', 'ISL': 'Iceland', 'ISR': 'Israel', 'JAM': 'Jamaica',
        'JOR': 'Jordan', 'JPN': 'Japan', 'KAZ': 'Kazakhstan', 'KEN': 'Kenya', 'KGZ': 'Kyrgyzstan',
        'KHM': 'Cambodia', 'KOR': 'South Korea', 'KWT': 'Kuwait', 'LAO': 'Laos', 'LBN': 'Lebanon',
        'LBR': 'Liberia', 'LBY': 'Libya', 'LCA': 'Saint Lucia', 'LIE': 'Liechtenstein', 'LKA': 'Sri Lanka',
        'LSO': 'Lesotho', 'LTU': 'Lithuania', 'LUX': 'Luxembourg', 'LVA': 'Latvia', 'MAR': 'Morocco',
        'MDA': 'Moldova', 'MDG': 'Madagascar', 'MDV': 'Maldives', 'MEX': 'Mexico', 'MKD': 'North Macedonia',
        'MLI': 'Mali', 'MLT': 'Malta', 'MMR': 'Myanmar', 'MNE': 'Montenegro', 'MNG': 'Mongolia',
        'MOZ': 'Mozambique', 'MRT': 'Mauritania', 'MUS': 'Mauritius', 'MWI': 'Malawi', 'MYS': 'Malaysia',
        'NAM': 'Namibia', 'NCL': 'New Caledonia', 'NER': 'Niger', 'NGA': 'Nigeria', 'NIC': 'Nicaragua',
        'NLD': 'Netherlands', 'NOR': 'Norway', 'NPL': 'Nepal', 'NZL': 'New Zealand', 'OMN': 'Oman',
        'PAK': 'Pakistan', 'PAN': 'Panama', 'PER': 'Peru', 'PHL': 'Philippines', 'PNG': 'Papua New Guinea',
        'POL': 'Poland', 'PRT': 'Portugal', 'PRY': 'Paraguay', 'QAT': 'Qatar', 'ROU': 'Romania',
        'RUS': 'Russia', 'RWA': 'Rwanda', 'SAU': 'Saudi Arabia', 'SDN': 'Sudan', 'SEN': 'Senegal',
        'SGP': 'Singapore', 'SLB': 'Solomon Islands', 'SLE': 'Sierra Leone', 'SLV': 'El Salvador', 'SMR': 'San Marino',
        'SOM': 'Somalia', 'SRB': 'Serbia', 'SSD': 'South Sudan', 'SUR': 'Suriname', 'SVK': 'Slovakia',
        'SVN': 'Slovenia', 'SWE': 'Sweden', 'SWZ': 'Eswatini', 'SYC': 'Seychelles', 'SYR': 'Syria',
        'TCD': 'Chad', 'TGO': 'Togo', 'THA': 'Thailand', 'TJK': 'Tajikistan', 'TKM': 'Turkmenistan',
        'TLS': 'Timor-Leste', 'TON': 'Tonga', 'TTO': 'Trinidad and Tobago', 'TUN': 'Tunisia', 'TUR': 'Turkey',
        'TWN': 'Taiwan', 'TZA': 'Tanzania', 'UGA': 'Uganda', 'UKR': 'Ukraine', 'URY': 'Uruguay',
        'USA': 'United States', 'UZB': 'Uzbekistan', 'VEN': 'Venezuela', 'VNM': 'Vietnam', 'VUT': 'Vanuatu',
        'WSM': 'Samoa', 'YEM': 'Yemen', 'ZAF': 'South Africa', 'ZMB': 'Zambia', 'ZWE': 'Zimbabwe'
    }
    
    df['Country_Name'] = df['Country_Code'].map(country_names)
    # If any country names are still missing, replace with empty string (or optionally with 'Unknown')
    df['Country_Name'] = df['Country_Name'].fillna('Unknown')

    # Add continent mapping
    country_to_continent = {
        # Africa
        'DZA': 'Africa', 'AGO': 'Africa', 'BEN': 'Africa', 'BWA': 'Africa', 'BFA': 'Africa', 'BDI': 'Africa',
        'CMR': 'Africa', 'CPV': 'Africa', 'CAF': 'Africa', 'TCD': 'Africa', 'COM': 'Africa', 'COG': 'Africa',
        'CIV': 'Africa', 'COD': 'Africa', 'DJI': 'Africa', 'EGY': 'Africa', 'GNQ': 'Africa', 'ERI': 'Africa',
        'SWZ': 'Africa', 'ETH': 'Africa', 'GAB': 'Africa', 'GMB': 'Africa', 'GHA': 'Africa', 'GIN': 'Africa',
        'GNB': 'Africa', 'KEN': 'Africa', 'LSO': 'Africa', 'LBR': 'Africa', 'LBY': 'Africa', 'MDG': 'Africa',
        'MWI': 'Africa', 'MLI': 'Africa', 'MRT': 'Africa', 'MUS': 'Africa', 'MYT': 'Africa', 'MAR': 'Africa',
        'MOZ': 'Africa', 'NAM': 'Africa', 'NER': 'Africa', 'NGA': 'Africa', 'REU': 'Africa', 'RWA': 'Africa',
        'STP': 'Africa', 'SEN': 'Africa', 'SYC': 'Africa', 'SLE': 'Africa', 'SOM': 'Africa', 'ZAF': 'Africa',
        'SSD': 'Africa', 'SDN': 'Africa', 'TZA': 'Africa', 'TGO': 'Africa', 'TUN': 'Africa', 'UGA': 'Africa',
        'COD': 'Africa', 'ZMB': 'Africa', 'ZWE': 'Africa',
        # Asia
        'AFG': 'Asia', 'ARM': 'Asia', 'AZE': 'Asia', 'BHR': 'Asia', 'BGD': 'Asia', 'BTN': 'Asia', 'BRN': 'Asia',
        'KHM': 'Asia', 'CHN': 'Asia', 'CYP': 'Asia', 'GEO': 'Asia', 'IND': 'Asia', 'IDN': 'Asia', 'IRN': 'Asia',
        'IRQ': 'Asia', 'ISR': 'Asia', 'JPN': 'Asia', 'JOR': 'Asia', 'KAZ': 'Asia', 'KWT': 'Asia', 'KGZ': 'Asia',
        'LAO': 'Asia', 'LBN': 'Asia', 'MAC': 'Asia', 'MYS': 'Asia', 'MDV': 'Asia', 'MNG': 'Asia', 'MMR': 'Asia',
        'NPL': 'Asia', 'PRK': 'Asia', 'OMN': 'Asia', 'PAK': 'Asia', 'PSE': 'Asia', 'PHL': 'Asia', 'QAT': 'Asia',
        'SAU': 'Asia', 'SGP': 'Asia', 'KOR': 'Asia', 'LKA': 'Asia', 'SYR': 'Asia', 'TWN': 'Asia', 'TJK': 'Asia',
        'THA': 'Asia', 'TLS': 'Asia', 'TUR': 'Asia', 'TKM': 'Asia', 'ARE': 'Asia', 'UZB': 'Asia', 'VNM': 'Asia',
        'YEM': 'Asia',
        # Europe
        'ALB': 'Europe', 'AND': 'Europe', 'AUT': 'Europe', 'BLR': 'Europe', 'BEL': 'Europe', 'BIH': 'Europe',
        'BGR': 'Europe', 'HRV': 'Europe', 'CZE': 'Europe', 'DNK': 'Europe', 'EST': 'Europe', 'FRO': 'Europe',
        'FIN': 'Europe', 'FRA': 'Europe', 'DEU': 'Europe', 'GIB': 'Europe', 'GRC': 'Europe', 'GGY': 'Europe',
        'HUN': 'Europe', 'ISL': 'Europe', 'IRL': 'Europe', 'IMN': 'Europe', 'ITA': 'Europe', 'JEY': 'Europe',
        'LVA': 'Europe', 'LIE': 'Europe', 'LTU': 'Europe', 'LUX': 'Europe', 'MLT': 'Europe', 'MDA': 'Europe',
        'MCO': 'Europe', 'MNE': 'Europe', 'NLD': 'Europe', 'MKD': 'Europe', 'NOR': 'Europe', 'POL': 'Europe',
        'PRT': 'Europe', 'ROU': 'Europe', 'RUS': 'Europe', 'SMR': 'Europe', 'SRB': 'Europe', 'SVK': 'Europe',
        'SVN': 'Europe', 'ESP': 'Europe', 'SWE': 'Europe', 'CHE': 'Europe', 'UKR': 'Europe', 'GBR': 'Europe',
        'VAT': 'Europe',
        # North America
        'AIA': 'North America', 'ATG': 'North America', 'BHS': 'North America', 'BRB': 'North America',
        'BLZ': 'North America', 'BMU': 'North America', 'CAN': 'North America', 'CYM': 'North America',
        'CRI': 'North America', 'CUB': 'North America', 'DMA': 'North America', 'DOM': 'North America',
        'SLV': 'North America', 'GRL': 'North America', 'GRD': 'North America', 'GLP': 'North America',
        'GTM': 'North America', 'HTI': 'North America', 'HND': 'North America', 'JAM': 'North America',
        'MTQ': 'North America', 'MEX': 'North America', 'MSR': 'North America', 'ANT': 'North America',
        'NIC': 'North America', 'PAN': 'North America', 'PRI': 'North America', 'KNA': 'North America',
        'LCA': 'North America', 'SPM': 'North America', 'VCT': 'North America', 'TTO': 'North America',
        'TCA': 'North America', 'USA': 'North America', 'VIR': 'North America',
        # South America
        'ARG': 'South America', 'BOL': 'South America', 'BRA': 'South America', 'CHL': 'South America',
        'COL': 'South America', 'ECU': 'South America', 'FLK': 'South America', 'GUF': 'South America',
        'GUY': 'South America', 'PRY': 'South America', 'PER': 'South America', 'SUR': 'South America',
        'URY': 'South America', 'VEN': 'South America',
        # Oceania
        'ASM': 'Oceania', 'AUS': 'Oceania', 'COK': 'Oceania', 'FJI': 'Oceania', 'PYF': 'Oceania',
        'GUM': 'Oceania', 'KIR': 'Oceania', 'MHL': 'Oceania', 'FSM': 'Oceania', 'NRU': 'Oceania',
        'NCL': 'Oceania', 'NZL': 'Oceania', 'NIU': 'Oceania', 'NFK': 'Oceania', 'MNP': 'Oceania',
        'PLW': 'Oceania', 'PNG': 'Oceania', 'WSM': 'Oceania', 'SLB': 'Oceania', 'TKL': 'Oceania',
        'TON': 'Oceania', 'TUV': 'Oceania', 'VUT': 'Oceania',
    }
    df['Continent'] = df['Country_Code'].map(country_to_continent).fillna('Unknown')
    return df

@st.cache_data
def load_maritime_data():
    """Load and process maritime CO2 emissions data from CSV files."""
    try:
        # Get the directory where this script is located
        script_dir = os.path.dirname(os.path.abspath(__file__))
        world_df = pd.read_csv(os.path.join(script_dir, 'maritime_world_total.csv'))
        oecd_df = pd.read_csv(os.path.join(script_dir, 'maritime_oecd_countries.csv'))
        
        # Convert TIME_PERIOD to year-month format and extract year, with error handling
        def safe_year(val):
            year_str = str(val)[:4].replace(',', '')
            if year_str.isdigit():
                return int(year_str)
            else:
                st.warning(f"Invalid year in TIME_PERIOD: {val}")
                return None
        world_df['Year'] = world_df['TIME_PERIOD'].apply(safe_year)
        world_df['Month'] = world_df['TIME_PERIOD'].str[5:7].apply(lambda x: int(x) if str(x).isdigit() else None)
        world_df['YearMonth'] = pd.to_datetime(world_df['TIME_PERIOD'], errors='coerce')

        oecd_df['Year'] = oecd_df['TIME_PERIOD'].apply(safe_year)
        oecd_df['Month'] = oecd_df['TIME_PERIOD'].str[5:7].apply(lambda x: int(x) if str(x).isdigit() else None)
        oecd_df['YearMonth'] = pd.to_datetime(oecd_df['TIME_PERIOD'], errors='coerce')
        
        return world_df, oecd_df
    except Exception as e:
        if "'str' object cannot be interpreted as an integer" not in str(e):
            st.error(f"❌ Error loading maritime data: {e}")
        return None, None

@st.cache_data
def load_sea_level_data():
    """Load and process sea level data from CSV file."""
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        sea_level_df = pd.read_csv(os.path.join(script_dir, 'sea_level_yearly_new.csv'))
        # Fix GMSL_Variation_mm: replace commas with dots and convert to float
        if 'GMSL_Variation_mm' in sea_level_df.columns:
            sea_level_df['GMSL_Variation_mm'] = sea_level_df['GMSL_Variation_mm'].astype(str).str.replace(',', '.', regex=False).astype(float)
        return sea_level_df
    except Exception as e:
        if "'str' object cannot be interpreted as an integer" not in str(e):
            st.error(f"❌ Error loading sea level data: {e}")
        return None

# Load data
try:
    df = load_climate_data()
    df['Year'] = df['Year'].astype(str).str.replace(',', '').astype(int)
    st.markdown('<div class="main-header" style="color:#4b5e4b;">Climate Analysis Dashboard</div>', unsafe_allow_html=True)
    world_maritime, oecd_maritime = load_maritime_data()
    sea_level_df = load_sea_level_data()
    analysis_options = get_analysis_options(world_maritime, sea_level_df)
    if 'analysis_type' not in st.session_state or st.session_state['analysis_type'] not in analysis_options:
        default = "🌡️ Climate Temperature" if "🌡️ Climate Temperature" in analysis_options else analysis_options[0]
        st.session_state['analysis_type'] = default

    st.markdown("<div style='margin-bottom:0.5rem;'></div>", unsafe_allow_html=True)
    cols = st.columns(len(analysis_options))
    for i, (col, opt) in enumerate(zip(cols, analysis_options)):
        with col:
            color = "#d62728" if st.session_state['analysis_type'] == opt else "#fff"
            font_weight = "bold" if st.session_state['analysis_type'] == opt else "normal"
            if st.button(opt, key=f"analysis_btn_{i}", help=opt, use_container_width=True):
                st.session_state['analysis_type'] = opt
    analysis_type = st.session_state['analysis_type']

    if analysis_type == "🌡️ Climate Temperature":
        latest_year = int(df['Year'].max())
        earliest_year = int(df['Year'].min())
        latest_avg_temp = df[df['Year'] == latest_year]['Temperature'].mean()
        earliest_avg_temp = df[df['Year'] == earliest_year]['Temperature'].mean()
        temp_change = latest_avg_temp - earliest_avg_temp
        highest_recorded = df['Temperature'].max()
        metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4, gap="small")
        with metric_col1:
            st.markdown(f"<div style='font-size:0.95em; color:#888;'>Latest Year</div><div style='font-size:1.3em; color:#ff7f0e; font-weight:bold;'>{latest_year}</div>", unsafe_allow_html=True)
        with metric_col2:
            st.markdown(f"<div style='font-size:0.95em; color:#888;'>Latest Avg Temp</div><div style='font-size:1.3em; color:#ff7f0e; font-weight:bold;'>{latest_avg_temp:.2f}°C</div>", unsafe_allow_html=True)
        with metric_col3:
            st.markdown(f"<div style='font-size:0.95em; color:#888;'>Temp Change</div><div style='font-size:1.3em; color:#ff7f0e; font-weight:bold;'>{temp_change:+.2f}°C</div><div style='font-size:0.8em; color:#888;'>({earliest_year} to {latest_year})</div>", unsafe_allow_html=True)
        with metric_col4:
            st.markdown(f"<div style='font-size:0.95em; color:#888;'>Highest Recorded</div><div style='font-size:1.3em; color:#ff7f0e; font-weight:bold;'>{highest_recorded:.2f}°C</div>", unsafe_allow_html=True)
        global_avg = df.groupby('Year')['Temperature'].mean().reset_index()
        col_trend, col_country = st.columns([1, 1], gap="small")
        with col_trend:
            fig = px.line(global_avg, x='Year', y='Temperature', title='', labels={'Temperature': 'Temperature (°C)', 'Year': 'Year'})
            fig.update_traces(line_color='#ff7f0e', line_width=2)
            fig.update_layout(height=260, margin=dict(l=10, r=10, t=10, b=10), xaxis=dict(showline=False, zeroline=False, showgrid=False, tickformat='d'), yaxis=dict(showline=False, zeroline=False, showgrid=False))
            st.plotly_chart(fig, use_container_width=True)
        with col_country:
            available_country_names = sorted(df['Country_Name'].unique())
            selected_country_name = st.selectbox("Select a country for detailed analysis", available_country_names, index=available_country_names.index('United States') if 'United States' in available_country_names else 0, key='main_country_selector')
            country_all_years = df[df['Country_Name'] == selected_country_name].sort_values('Year')
            stats_col1, stats_col2, stats_col3 = st.columns(3, gap="small")
            with stats_col1:
                st.markdown(f"<div style='text-align:center;'><span style='font-size:0.95em;'>All-time Avg</span><br><span style='color:#ff7f0e; font-size:0.85em;'>{country_all_years['Temperature'].mean():.2f}°C</span></div>", unsafe_allow_html=True)
            with stats_col2:
                st.markdown(f"<div style='text-align:center;'><span style='font-size:0.95em;'>Highest Ever</span><br><span style='color:#ff7f0e; font-size:0.85em;'>{country_all_years['Temperature'].max():.2f}°C</span></div>", unsafe_allow_html=True)
            with stats_col3:
                st.markdown(f"<div style='text-align:center;'><span style='font-size:0.95em;'>Lowest Ever</span><br><span style='color:#ff7f0e; font-size:0.85em;'>{country_all_years['Temperature'].min():.2f}°C</span></div>", unsafe_allow_html=True)
            fig_country = px.line(country_all_years, x='Year', y='Temperature', title='', labels={'Temperature': 'Temperature (°C)', 'Year': 'Year', 'Country_Name': 'Country'})
            fig_country.update_traces(line_color='#ff7f0e', line_width=2)
            fig_country.update_layout(height=180, hovermode='x unified', margin=dict(l=10, r=10, t=10, b=10), xaxis=dict(showline=False, zeroline=False), yaxis=dict(showline=False, zeroline=False))
            st.plotly_chart(fig_country, config={"responsive": True})
        filter_col1, filter_col2, _ = st.columns([1, 1, 2], gap="small")
        with filter_col1:
            selected_year = st.slider("Year", min_value=int(df['Year'].min()), max_value=int(df['Year'].max()), value=int(df['Year'].max()), step=1, key="map_year_slider")
        with filter_col2:
            selected_continent = st.selectbox("Continent", ["World", "Africa", "Asia", "Europe", "North America", "South America", "Oceania"], index=0, key="map_continent_select")
        continents = {
            'World': {'scope': 'world', 'center': None},
            'Africa': {'scope': 'africa', 'center': {'lat': 0, 'lon': 20}},
            'Asia': {'scope': 'asia', 'center': {'lat': 30, 'lon': 90}},
            'Europe': {'scope': 'europe', 'center': {'lat': 50, 'lon': 10}},
            'North America': {'scope': 'north america', 'center': {'lat': 40, 'lon': -100}},
            'South America': {'scope': 'south america', 'center': {'lat': -15, 'lon': -60}},
            'Oceania': {'scope': 'world', 'center': {'lat': -25, 'lon': 140}}
        }
        if selected_continent == "World":
            df_filtered = df[df['Year'] == selected_year].copy()
        else:
            df_filtered = df[(df['Year'] == selected_year) & (df['Continent'] == selected_continent)].copy()
        country_avg = df_filtered.groupby('Country_Code')['Temperature'].mean().reset_index()
        country_avg.columns = ['Country_Code', 'Avg_Temperature']
        country_avg['Country_Name'] = country_avg['Country_Code'].map(dict(zip(df['Country_Code'], df['Country_Name'])))
        metrics_col, map_col, hot_col, cold_col = st.columns([1, 2, 1, 1], gap="small")
        with metrics_col:
            global_avg_year = country_avg['Avg_Temperature'].mean()
            hottest_country = country_avg.loc[country_avg['Avg_Temperature'].idxmax()]
            coldest_country = country_avg.loc[country_avg['Avg_Temperature'].idxmin()]
            display_name = coldest_country['Country_Code'] if str(coldest_country['Country_Name']) == 'Unknown' else coldest_country['Country_Name']
            temp_value = coldest_country['Avg_Temperature']
            temp_value_float = float(temp_value.values[0]) if isinstance(temp_value, pd.Series) or hasattr(temp_value, 'values') else float(temp_value)
            temp_color = '#313695' if temp_value_float < 0 else "#593e27"
            temp_range = country_avg['Avg_Temperature'].max() - country_avg['Avg_Temperature'].min()
            st.markdown(f"<div style='font-size:0.90em; color:#888;'>Global Avg</div><span style='color:#ff7f0e; font-size:1em;'>{global_avg_year:.2f}°C</span><br><div style='font-size:0.90em; color:#888;'>Hottest</div><span style='color:#ff7f0e; font-size:1em;'>{hottest_country['Country_Name']}: {hottest_country['Avg_Temperature']:.1f}°C</span><br><div style='font-size:0.90em; color:#888;'>Coldest</div><span style='color:{temp_color}; font-size:1em;'>{display_name}: {temp_value:.1f}°C</span><br><div style='font-size:0.90em; color:#888;'>Temp Range</div><span style='color:#ff7f0e; font-size:1em;'>{temp_range:.1f}°C</span>", unsafe_allow_html=True)
        with map_col:
            continent_config = continents[selected_continent]
            fig = px.choropleth(country_avg, locations='Country_Code', locationmode='ISO-3', color='Avg_Temperature', hover_name='Country_Name', hover_data={'Country_Name': True, 'Avg_Temperature': ':.2f'}, color_continuous_scale=[[0, '#313695'], [0.2, '#4575b4'], [0.4, '#abd9e9'], [0.5, '#ffffbf'], [0.6, '#fdae61'], [0.8, '#f46d43'], [1, '#a50026']], labels={'Avg_Temperature': 'Temperature (°C)'})
            fig.update_layout(height=260, geo=dict(scope=continent_config['scope'], center=continent_config['center'], showframe=True, showcoastlines=True, showland=True, landcolor="rgb(243, 243, 243)", showcountries=True, countrycolor="rgb(204, 204, 204)", projection_type='natural earth', bgcolor='rgba(0,0,0,0)'), margin=dict(l=0, r=0, t=10, b=0), coloraxis_colorbar=dict(title="Temp (°C)", thickness=8, len=0.35, x=1.01))
            fig.update_traces(marker_line_color='darkgray', marker_line_width=0.5)
            st.plotly_chart(fig, config={"responsive": True, "displayModeBar": False, "use_container_width": True})
        with hot_col:
            if country_avg.empty:
                st.info("No data for year/continent.")
            else:
                hottest = country_avg.nlargest(5, 'Avg_Temperature').copy()
                hottest['Display_Name'] = hottest.apply(lambda row: row['Country_Code'] if row['Country_Name'] == 'Unknown' else row['Country_Name'], axis=1)
                st.markdown("<div style='text-align:center; font-size:0.95em; font-weight:600; margin-bottom:0.1em;'>Top 5 Hottest</div>", unsafe_allow_html=True)
                df_hot = hottest[['Display_Name', 'Avg_Temperature']].rename(columns={'Display_Name': 'Country', 'Avg_Temperature': 'Avg Temp (°C)'})
                html = '<table style="width:100%; text-align:center; border-collapse:collapse; font-size:0.90em;">'
                html += '<tr><th>Country</th><th>Avg Temp (°C)</th></tr>'
                for _, row in df_hot.iterrows():
                    color = '#313695' if row['Avg Temp (°C)'] < 0 else '#ff7f0e'
                    html += f'<tr><td>{row["Country"]}</td><td style="color:{color};">{row["Avg Temp (°C)"]:.2f}</td></tr>'
                html += '</table>'
                st.markdown(html, unsafe_allow_html=True)
        with cold_col:
            if country_avg.empty:
                st.info("No data for year/continent.")
            else:
                coldest = country_avg.nsmallest(5, 'Avg_Temperature').copy()
                coldest['Display_Name'] = coldest.apply(lambda row: row['Country_Code'] if row['Country_Name'] == 'Unknown' else row['Country_Name'], axis=1)
                st.markdown("<div style='text-align:center; font-size:0.95em; font-weight:600; margin-bottom:0.1em;'>Top 5 Coldest</div>", unsafe_allow_html=True)
                df_cold = coldest[['Display_Name', 'Avg_Temperature']].rename(columns={'Display_Name': 'Country', 'Avg_Temperature': 'Avg Temp (°C)'})
                html = '<table style="width:100%; text-align:center; border-collapse:collapse; font-size:0.90em;">'
                html += '<tr><th>Country</th><th>Avg Temp (°C)</th></tr>'
                for _, row in df_cold.iterrows():
                    color = '#313695' if row['Avg Temp (°C)'] < 0 else '#ff7f0e'
                    html += f'<tr><td>{row["Country"]}</td><td style="color:{color};">{row["Avg Temp (°C)"]:.2f}</td></tr>'
                html += '</table>'
                st.markdown(html, unsafe_allow_html=True)
    elif analysis_type == "🚢 CO2 Emissions":
        
        if world_maritime is None:
            st.error("❌ Maritime emissions data not found. Please run `python CO2.py` to fetch the data.")
        else:
            annual_temp = df.groupby('Year')['Temperature'].mean().reset_index()
            annual_temp.columns = ['Year', 'Avg_Temperature']
            annual_maritime = world_maritime.groupby('Year')['CO2_Emissions'].sum().reset_index()
            annual_maritime.columns = ['Year', 'Total_CO2_Emissions']
            correlation_data = pd.merge(annual_temp, annual_maritime, on='Year', how='inner')
            col1, col2, col3, col4, col5, col6 = st.columns(6)
            with col1:
                avg_emissions = correlation_data['Total_CO2_Emissions'].mean()
                avg_emissions_million = avg_emissions / 1_000_000
                st.markdown(
                    "<div style='text-align:center;'><span style='font-size:1.2em;'>Avg Annual Shipping CO₂</span><br>"
                    f"<span style='color:#4b5e4b; font-size:2em; font-weight:bold;'>{avg_emissions_million:.2f} M tonnes</span></div>",
                    unsafe_allow_html=True)
            with col2:
                avg_temp = correlation_data['Avg_Temperature'].mean()
                st.markdown(
                    "<div style='text-align:center;'><span style='font-size:1.2em;'>Avg Global Temperature</span><br>"
                    f"<span style='color:#4b5e4b; font-size:2em; font-weight:bold;'>{avg_temp:.2f}°C</span></div>",
                    unsafe_allow_html=True)
            with col3:
                st.markdown(
                    "<div style='text-align:center;'><span style='font-size:1.2em;'>Total Records</span><br>"
                    f"<span style='color:#4b5e4b; font-size:2em; font-weight:bold;'>{len(df):,}</span></div>",
                    unsafe_allow_html=True)
            with col4:
                st.markdown(
                    "<div style='text-align:center;'><span style='font-size:1.2em;'>Countries</span><br>"
                    f"<span style='color:#4b5e4b; font-size:2em; font-weight:bold;'>{df['Country_Code'].nunique()}</span></div>",
                    unsafe_allow_html=True)
            with col5:
                st.markdown(
                    "<div style='text-align:center;'><span style='font-size:1.2em;'>Year Range</span><br>"
                    "<span style='color:#4b5e4b; font-size:2em; font-weight:bold;'>2019 - 2024</span></div>",
                    unsafe_allow_html=True)
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=correlation_data['Year'],
                y=correlation_data['Avg_Temperature'],
                name='Global Avg Temperature',
                yaxis='y',
                mode='lines+markers',
                line=dict(color="#ff0e22", width=3),
                marker=dict(size=10)
            ))
            fig.add_trace(go.Scatter(
                x=correlation_data['Year'],
                y=correlation_data['Total_CO2_Emissions'],
                name='Maritime CO2 Emissions',
                yaxis='y2',
                mode='lines+markers',
                line=dict(color="#95a895", width=3),
                marker=dict(size=10)
            ))
            fig.update_layout(
                title='Global Average Temperature and Maritime CO₂ Emissions (2019-2024)',
                xaxis=dict(
                    title=None,
                    showgrid=False,
                    showticklabels=True,
                    tickfont=dict(
                        color='#fff',
                        size=12,
                        family='Arial, sans-serif',
                        weight='normal'
                    ),
                    tickmode='auto',
                    ticks='outside',
                    tickangle=0,
                    showline=False,
                    zeroline=False,
                    type='category'
                ),
                yaxis=dict(
                    title=None,
                    showgrid=False,
                    showticklabels=False,
                    showline=False,
                    zeroline=False
                ),
                yaxis2=dict(
                    title=None,
                    showgrid=False,
                    showticklabels=False,
                    showline=False,
                    zeroline=False,
                    anchor='x',
                    overlaying='y',
                    side='right'
                ),
                hovermode='x unified',
                height=400,
                width=380,
                showlegend=True,
                legend=dict(x=0.01, y=0.99)
            )
            col_top1, col_top2 = st.columns([2, 1], gap="medium")
            with col_top1:
                st.plotly_chart(fig, config={"responsive": True}, key="correlation_chart")
            with col_top2:
                monthly_df = world_maritime.copy()
                monthly_df['YearMonth'] = pd.to_datetime(monthly_df['TIME_PERIOD'])
                monthly_emissions = monthly_df.groupby('YearMonth')['CO2_Emissions'].sum().reset_index()
                fig_monthly = px.line(
                    monthly_emissions,
                    x='YearMonth',
                    y='CO2_Emissions',
                    labels={'YearMonth': '', 'CO2_Emissions': 'CO₂ Emissions (tonnes)'},
                    title='Monthly Maritime CO₂ Emissions (2019-2024)',
                    height=400
                )
                fig_monthly.update_traces(line_color='#4b5e4b', line_width=3)
                fig_monthly.update_layout(
                    xaxis=dict(tickfont=dict(size=14), showline=False, zeroline=False),
                    yaxis=dict(title=None, showline=False, zeroline=False),
                    margin=dict(l=30, r=30, t=40, b=30),
                    showlegend=True
                )
                st.plotly_chart(fig_monthly, config={"responsive": True}, key="monthly_emissions_chart")
            col_viz1, col_viz2, col_viz3 = st.columns([2, 1, 1], gap="medium")
            with col_viz1:
                vessel_df = world_maritime.groupby('VESSEL')['CO2_Emissions'].sum().reset_index()
                top10_vessels = vessel_df.nlargest(10, 'CO2_Emissions').copy()
                top10_vessels['CO2_Mt'] = top10_vessels['CO2_Emissions'] / 1_000_000
                base_color = np.array([75, 94, 75])
                dark_color = np.array([45, 58, 45])
                light_color = np.array([200, 220, 200])
                n = len(top10_vessels)
                gradient_colors = []
                for i in range(3):
                    factor = i / 2 if 2 > 0 else 0
                    color = dark_color + (base_color - dark_color) * factor
                    gradient_colors.append(f"rgb({int(color[0])}, {int(color[1])}, {int(color[2])})")
                for i in range(3, n):
                    factor = (i-3) / (n-4) if (n-4) > 0 else 0
                    color = base_color + (light_color - base_color) * factor
                    gradient_colors.append(f"rgb({int(color[0])}, {int(color[1])}, {int(color[2])})")
                fig_vessel = px.bar(
                    top10_vessels,
                    x='VESSEL',
                    y='CO2_Emissions',
                    labels={'VESSEL': '', 'CO2_Emissions': 'CO₂ Emissions (tonnes)'},
                    height=400
                )
                fig_vessel.update_traces(
                    marker_color=gradient_colors,
                    showlegend=False,
                    text=top10_vessels['CO2_Mt'].round(2).astype(str) + ' Mt',
                    textposition='outside'
                )
                fig_vessel.update_layout(
                    xaxis=dict(tickfont=dict(size=14), showline=False, zeroline=False),
                    yaxis=dict(
                        title=None,
                        showgrid=False,
                        showticklabels=False,
                        showline=False,
                        zeroline=False
                    ),
                    margin=dict(l=30, r=30, t=40, b=30),
                    showlegend=False,
                    title='Top 10 Vessel Types by CO₂ Emissions'
                )
                st.plotly_chart(fig_vessel, config={"responsive": True}, key="top10_vessel_chart")
            with col_viz2:
                domint_df = world_maritime.copy()
                domint_df['Year'] = domint_df['TIME_PERIOD'].str[:4].astype(int)
                domint_df = domint_df[domint_df['VESSEL_EMISSIONS_SOURCE'].isin(['Domestic voyages', 'International voyages'])]
                pie_data = domint_df.groupby('VESSEL_EMISSIONS_SOURCE')['CO2_Emissions'].sum().reset_index()
                fig_pie3d = go.Figure(go.Pie(
                    labels=pie_data['VESSEL_EMISSIONS_SOURCE'],
                    values=pie_data['CO2_Emissions'],
                    marker=dict(colors=["#cac7c7", "#4b5e4b"], line=dict(color='#333', width=2)),
                    hole=0.3,
                    textinfo='label+percent',
                    pull=[0, 0.08],
                    rotation=45,
                    direction='clockwise',
                    sort=False
                ))
                fig_pie3d.update_layout(
                    height=400,
                    margin=dict(l=30, r=30, t=40, b=30),
                    showlegend=False,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)'
                )
                fig_pie3d.update_traces(
                    textfont_size=18,
                    marker=dict(line=dict(color='#333', width=2)),
                    pull=[0.08, 0.12],
                    opacity=0.95
                )
                st.markdown("<div style='text-align:center; font-size:1.2rem; font-weight:bold;'>Emissions from domestic voyages vs International</div>", unsafe_allow_html=True)
                st.plotly_chart(fig_pie3d, config={"responsive": True}, key="pie3d")
            with col_viz3:
                stacked_df = domint_df.groupby(['Year', 'VESSEL_EMISSIONS_SOURCE'])['CO2_Emissions'].sum().reset_index()
                stacked_df['CO2_Millions'] = stacked_df['CO2_Emissions'] / 1_000_000
                common_height = 400
                fig_stacked = px.bar(
                    stacked_df,
                    x='Year',
                    y='CO2_Millions',
                    color='VESSEL_EMISSIONS_SOURCE',
                    barmode='stack',
                    labels={
                        'Year': 'Year',
                        'CO2_Millions': 'CO₂ Emissions (Mt)',
                        'VESSEL_EMISSIONS_SOURCE': 'Voyage Type'
                    },
                    color_discrete_map={
                        'Domestic voyages': "#e7d5d5",
                        'International voyages': '#4b5e4b'
                    },
                    height=common_height
                )
                fig_stacked.update_layout(
                    margin=dict(l=30, r=30, t=40, b=30),
                    xaxis=dict(
                        tickfont=dict(size=16, color='#fff'),
                        title=None
                    ),
                    yaxis=dict(
                        title=None,
                        showgrid=False
                    ),
                    legend=dict(
                        title='',
                        font=dict(size=16, color='#fff'),
                        orientation='h',
                        yanchor='bottom',
                        y=1.02,
                        xanchor='right',
                        x=1
                    ),
                    plot_bgcolor='rgba(0,0,0,0)'
                )
                st.markdown("<div style='text-align:center; font-size:1.2rem; font-weight:bold; margin:0.5rem 0;'>CO2 emission by year</div>", unsafe_allow_html=True)
                st.plotly_chart(fig_stacked, config={"responsive": True}, key="stacked_co2_side")
    elif analysis_type == "🌊 Sea Level":
        
        if sea_level_df is None:
            st.error("❌ Sea level data not available. Please run `python sea_level.py` first.")
        else:
            # Key metrics
            col1, col2, col4 = st.columns(3)

            with col1:
                total_rise = sea_level_df['GMSL_Variation_mm'].iloc[-1] - sea_level_df['GMSL_Variation_mm'].iloc[0]
                st.markdown(f"""
                <div style='font-size:1.3em; color:#fff; font-weight:600; margin-bottom:0.2em;'>Total Sea Level Rise</div>
                <div style='font-size:2em; color:#1f77b4; font-weight:600;'>{total_rise:.1f} mm</div>
                """, unsafe_allow_html=True)

            with col2:
                first_year = sea_level_df['Year'].iloc[0]
                last_year = sea_level_df['Year'].iloc[-1]
                time_span = last_year - first_year
                first_value = sea_level_df['GMSL_Variation_mm'].iloc[0]
                last_value = sea_level_df['GMSL_Variation_mm'].iloc[-1]
                total_rise = last_value - first_value
                avg_rate = total_rise / time_span if time_span > 0 else 0
                st.markdown(f"""
                <div style='font-size:1.3em; color:#fff; font-weight:600; margin-bottom:0.2em;'>Average Rate</div>
                <div style='font-size:2em; color:#1f77b4; font-weight:600;'>{avg_rate:.2f} mm/year</div>
                """, unsafe_allow_html=True)

            with col4:
                first_year = 2019
                last_year = 2023
                years_covered = last_year - first_year + 1
                st.markdown(f"""
                <div style='font-size:1.3em; color:#fff; font-weight:600; margin-bottom:0.2em;'>Data Coverage</div>
                <div style='font-size:2em; color:#1f77b4; font-weight:600;'>{years_covered} years</div>
                <div style='color:#1f77b4; font-size:1.05em;'>{first_year}-{last_year}</div>
                """, unsafe_allow_html=True)

            # Triple correlation (if maritime data available)
            yearly_temp = df.groupby('Year')['Temperature'].mean().reset_index()
            merged_df = yearly_temp.merge(sea_level_df, on='Year', how='inner')
            if world_maritime is not None:
                
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
                    # --- Move Climate Connection and Top 5 Ocean Regions side by side ---
                    col_cc, col_right = st.columns([2, 2], gap="small")
                    with col_cc:
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
                            xaxis=dict(title='Year', dtick=1, showgrid=False, zeroline=False, showline=False),
                            yaxis=dict(title='Normalized Value (0-100)', showgrid=False, zeroline=False, showline=False),
                            height=340,  # reduced height
                            hovermode='x unified',
                            legend=dict(
                                orientation='h',
                                yanchor='bottom',
                                y=1.02,
                                xanchor='right',
                                x=1
                            )
                        )
                        st.plotly_chart(fig4, use_container_width=True)
                    with col_right:
                        col_top5, col_monthly = st.columns([1, 1], gap="small")
                        with col_top5:
                            try:
                                script_dir = os.path.dirname(os.path.abspath(__file__))
                                sea_level_region_df = pd.read_csv(os.path.join(script_dir, 'sea_level_by_region_yearly.csv'))
                                latest_year = sea_level_region_df['year'].max()
                                latest = sea_level_region_df[sea_level_region_df['year'] == latest_year].copy()
                                top5 = latest.nlargest(5, 'Sea_Level_mm').copy()
                                blue_gradient = [
                                    'rgba(31,119,180,1)',
                                    'rgba(52,152,219,0.9)',
                                    'rgba(93,173,226,0.8)',
                                    'rgba(133,193,233,0.7)',
                                    'rgba(174,214,241,0.6)'
                                ]
                                fig_top5 = px.bar(
                                    top5.sort_values('Sea_Level_mm', ascending=False),
                                    x='Region',
                                    y='Sea_Level_mm',
                                    labels={'Region': '', 'Sea_Level_mm': 'Sea Level Rise (mm)'},
                                    title='',
                                    height=340  # reduced height
                                )
                                fig_top5.update_traces(marker_color=blue_gradient, marker_line_color='#1f77b4', marker_line_width=2, text=top5['Sea_Level_mm'].round(1), textposition='outside')
                                fig_top5.update_layout(
                                    xaxis=dict(tickfont=dict(size=16)),
                                    yaxis=dict(title=None, showgrid=False),
                                    margin=dict(l=30, r=30, t=60, b=30),
                                    showlegend=False
                                )
                                st.markdown("<div style='text-align:center; font-size:1.2rem; font-weight:bold; margin:0.5rem 0;'>Top 5 Ocean Regions by Sea Level Rise</div>", unsafe_allow_html=True)
                                st.plotly_chart(fig_top5, config={"responsive": True}, key="top5_ocean_sealevel")
                            except Exception as e:
                                st.warning(f"Could not load regional sea level data: {e}")
                        with col_monthly:
                            try:
                                sea_level_monthly_df = pd.read_csv(os.path.join(script_dir, 'sea_level_monthly.csv'))
                                sea_level_monthly_df = sea_level_monthly_df.sort_values(['Year', 'Month'])
                                sea_level_monthly_df['Monthly_Change_mm'] = sea_level_monthly_df['GMSL_Variation_mm'].diff()
                                month_map = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun', 7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'}
                                sea_level_monthly_df['Month_Name'] = sea_level_monthly_df['Month'].map(month_map)
                                available_years = sorted(sea_level_monthly_df['Year'].unique())
                                selected_year = st.selectbox(
                                    "Select Year",
                                    available_years,
                                    index=available_years.index(max(available_years)),
                                    key="monthly_sea_level_year_selector"
                                )
                                filtered_df = sea_level_monthly_df[sea_level_monthly_df['Year'] == selected_year]
                                fig_monthly_rise = px.bar(
                                    filtered_df,
                                    x='Month_Name',
                                    y='Monthly_Change_mm',
                                    labels={'Month_Name': 'Month', 'Monthly_Change_mm': 'Monthly Sea Level Change (mm)'},
                                    title='',
                                    height=340  # reduced height
                                )
                                fig_monthly_rise.update_traces(marker_color='rgba(31,119,180,0.8)', marker_line_color='#1f77b4', marker_line_width=2, text=filtered_df['Monthly_Change_mm'].round(2), textposition='outside')
                                fig_monthly_rise.update_layout(
                                    xaxis=dict(tickfont=dict(size=16)),
                                    yaxis=dict(title=None, showgrid=True),
                                    margin=dict(l=30, r=30, t=60, b=30),
                                    showlegend=False
                                )
                                st.markdown(f"<div style='text-align:center; font-size:1.2rem; font-weight:bold; margin:0.5rem 0;'>Monthly Sea Level Rise Change ({selected_year})</div>", unsafe_allow_html=True)
                                st.plotly_chart(fig_monthly_rise, config={"responsive": True}, key="monthly_sea_level_rise")
                            except Exception as e:
                                st.warning(f"Could not load monthly sea level data: {e}")
        # ...existing code...
    # --- OpenAI Assistant Section ---
    st.markdown("""
    <hr style='margin:2rem 0;'>
    <div style='text-align:center; font-size:1.5rem; font-weight:bold; color:#1f77b4;'>🤖 Ask OpenAI About This Dashboard</div>
    <div style='text-align:center; color:#888; margin-bottom:1rem;'>Get explanations, insights, or help about any part of the dashboard or the data.</div>
    """, unsafe_allow_html=True)

    if 'openai_chat_history' not in st.session_state:
        st.session_state['openai_chat_history'] = []

    with st.expander("OpenAI Chat", expanded=True):
        col_chat, col_clear = st.columns([4,1])
        with col_chat:
            user_input = st.text_input("Ask a question about the dashboard or data:", key="openai_user_input")
        with col_clear:
            if st.button("Clear History", key="clear_openai_history"):
                st.session_state['openai_chat_history'] = []
                st.experimental_rerun()

        if user_input:
            # Placeholder for OpenAI API call
            # In production, replace the below with an actual OpenAI API call
            response = f"[OpenAI simulated response] You asked: '{user_input}'. (This is a placeholder. Integrate OpenAI API for real answers.)"
            st.session_state['openai_chat_history'].append((user_input, response))
            st.experimental_rerun()

        if st.session_state['openai_chat_history']:
            for i, (q, a) in enumerate(st.session_state['openai_chat_history']):
                st.markdown(f"<div style='margin-bottom:0.5em;'><b>You:</b> {q}</div>", unsafe_allow_html=True)
                st.markdown(f"<div style='margin-bottom:1em; color:#1f77b4;'><b>OpenAI:</b> {a}</div>", unsafe_allow_html=True)

    # Footer
    st.markdown("""
    <div style='text-align: center; color: #666; padding: 1rem;'>
        <p><strong>Climate Analysis Dashboard</strong> | Data Sources: World Bank Climate Change Knowledge Portal & OECD Maritime Transport</p>
        <p>Created by Claire Namusoke | November 2025</p>
    </div>
    """, unsafe_allow_html=True)

except FileNotFoundError:
    st.error("❌ Climate data file not found. Please run `python climate.py` first to fetch the data.")
except Exception as e:
    if "'str' object cannot be interpreted as an integer" not in str(e):
        st.error(f"❌ Error loading data: {str(e)}")

