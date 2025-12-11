import streamlit as st
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

# --- Horizontal Analysis Category Selection ---
def get_analysis_options(world_maritime, sea_level_df):
    options = []
    if world_maritime is not None:
        options.append("🚢 CO2 Emissions")
    options.append("🌡️ Climate Temperature")
    if sea_level_df is not None:
        options.append("🌊 Sea Level")
    return options

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #d62728;
        text-align: center;
        margin-bottom: 0px;
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
    /* Sidebar background color and text color to match dashboard */
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
    # Force clean and convert Year column to int
    df['Year'] = df['Year'].astype(str).str.replace(',', '').astype(int)
    st.markdown('<div class="main-header" style="color:#4b5e4b; margin-top:0; padding-top:0;"> Climate Analysis Dashboard</div>', unsafe_allow_html=True)

    # Animated subtitle (appears for a few seconds, then fades out)
    
   
    
    # Load maritime data
    world_maritime, oecd_maritime = load_maritime_data()
    
    # Load sea level data
    sea_level_df = load_sea_level_data()

    # --- Horizontal Analysis Category Selection ---
    analysis_options = get_analysis_options(world_maritime, sea_level_df)
    if 'analysis_type' not in st.session_state or st.session_state['analysis_type'] not in analysis_options:
        # Default to Climate Temperature if available, else first
        default = "🌡️ Climate Temperature" if "🌡️ Climate Temperature" in analysis_options else analysis_options[0]
        st.session_state['analysis_type'] = default

    st.markdown("""
        <div style='margin-bottom:2rem;'></div>
    """, unsafe_allow_html=True)
    cols = st.columns(len(analysis_options))
    for i, (col, opt) in enumerate(zip(cols, analysis_options)):
        with col:
            color = "#d62728" if st.session_state['analysis_type'] == opt else "#fff"
            font_weight = "bold" if st.session_state['analysis_type'] == opt else "normal"
            if st.button(opt, key=f"analysis_btn_{i}", help=opt, use_container_width=True):
                st.session_state['analysis_type'] = opt
            # Removed repeated label below filter button for cleaner UI
    analysis_type = st.session_state['analysis_type']
    
    # Main content area
    if analysis_type == "🌡️ Climate Temperature":
        
        # Create tabs for different views (no icons or labels)
        tab1, tab2, tab3, tab4, tab5 = st.tabs(["", "", "", "", ""])

        with tab1:
            # Removed redundant subheader for cleaner UI
            # Calculate global average by year
            global_avg = df.groupby('Year')['Temperature'].mean().reset_index()
            
            # Key metrics
            col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            latest_year = global_avg['Year'].max()
            latest_temp = global_avg[global_avg['Year'] == latest_year]['Temperature'].values[0]
            st.markdown(f"""
                <div style='text-align:center;'>
                    <span style='font-size:1.1em;'>Latest Year</span><br>
                    <span style='color:#ff7f0e; font-size:2em;'>{latest_year}</span>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
                <div style='text-align:center;'>
                    <span style='font-size:1.1em;'>Latest Avg Temp</span><br>
                    <span style='color:#ff7f0e; font-size:2em;'>{latest_temp:.2f}°C</span>
                </div>
            """, unsafe_allow_html=True)
        
        with col3:
            earliest_temp = global_avg[global_avg['Year'] == global_avg['Year'].min()]['Temperature'].values[0]
            temp_change = latest_temp - earliest_temp
            st.markdown(f"""
                <div style='text-align:center;'>
                    <span style='font-size:1.1em;'>Temperature Change</span><br>
                    <span style='color:#ff7f0e; font-size:2em;'>{temp_change:+.2f}°C</span>
                </div>
            """, unsafe_allow_html=True)
        
        with col4:
            max_temp = df['Temperature'].max()
            st.markdown(f"""
                <div style='text-align:center;'>
                    <span style='font-size:1.1em;'>Highest Recorded</span><br>
                    <span style='color:#ff7f0e; font-size:2em;'>{max_temp:.2f}°C</span>
                </div>
            """, unsafe_allow_html=True)
        

        
        # Global temperature trend
        # Removed redundant subheader for cleaner UI
        
        # Show global temperature trend and top 5 tables side by side
        # Show only the global temperature trend (top hottest/coldest visuals removed)
        # Two columns: left = global trend, right = country selector + historical trend
        col_trend, col_country = st.columns([1, 1])
        with col_trend:
            fig = px.line(
                global_avg,
                x='Year',
                y='Temperature',
                title='Global Average Temperature Over Time',
                labels={'Temperature': 'Temperature (°C)', 'Year': 'Year'}
            )
            fig.update_traces(line_color='#ff7f0e', line_width=2)
            fig.update_layout(height=500)
            fig.update_layout(
                xaxis=dict(
                    showline=False,
                    zeroline=False,
                    showgrid=False,
                    tickformat='d'  # No commas for years
                ),
                yaxis=dict(showline=False, zeroline=False, showgrid=False)
            )
            st.plotly_chart(fig, use_container_width=True)
        with col_country:
            # Country selector for detailed view (reduced width)
            available_country_names = sorted(df['Country_Name'].unique())
            selected_country_name = st.selectbox(
                "Select a country for detailed analysis",
                available_country_names,
                index=available_country_names.index('United States') if 'United States' in available_country_names else 0,
                key='main_country_selector'
            )
            # Get country data for all years
            country_all_years = df[df['Country_Name'] == selected_country_name].sort_values('Year')
            country_name_detail = selected_country_name

            # Historical stats directly under filter bar
            stats_col1, stats_col2, stats_col3 = st.columns(3)
            with stats_col1:
                st.markdown(f"""
                    <div style='text-align:center;'>
                        <span style='font-size:1.1em;'>All-time Average</span><br>
                        <span style='color:#ff7f0e; font-size:0.67em;'>{country_all_years['Temperature'].mean():.2f}°C</span>
                    </div>
                """, unsafe_allow_html=True)
            with stats_col2:
                st.markdown(f"""
                    <div style='text-align:center;'>
                        <span style='font-size:1.1em;'>Highest Ever</span><br>
                        <span style='color:#ff7f0e; font-size:0.67em;'>{country_all_years['Temperature'].max():.2f}°C</span>
                    </div>
                """, unsafe_allow_html=True)
            with stats_col3:
                st.markdown(f"""
                    <div style='text-align:center;'>
                        <span style='font-size:1.1em;'>Lowest Ever</span><br>
                        <span style='color:#ff7f0e; font-size:0.67em;'>{country_all_years['Temperature'].min():.2f}°C</span>
                    </div>
                """, unsafe_allow_html=True)

            # Historical trend for selected country (full width below)
            fig_country = px.line(
                country_all_years,
                x='Year',
                y='Temperature',
                title=f'Historical Temperature Trend: {country_name_detail}',
                labels={'Temperature': 'Temperature (°C)', 'Year': 'Year', 'Country_Name': 'Country'}
            )
            fig_country.update_traces(line_color='#ff7f0e', line_width=2)
            fig_country.update_layout(height=400, hovermode='x unified')
            fig_country.update_layout(xaxis=dict(showline=False, zeroline=False), yaxis=dict(showline=False, zeroline=False))
            st.plotly_chart(fig_country, config={"responsive": True})
        
        with tab2:
            # Compact year and continent filters above the map section
            filter_col1, filter_col2, _ = st.columns([1, 1, 2])
            with filter_col1:
                selected_year = st.slider(
                    "Year",
                    min_value=2019,
                    max_value=2024,
                    value=2024,
                    step=1,
                    key="map_year_slider"
                )
            with filter_col2:
                selected_continent = st.selectbox(
                    "Continent",
                    ["World", "Africa", "Asia", "Europe", "North America", "South America", "Oceania"],
                    index=0,
                    key="map_continent_select"
                )
            continents = {
                'World': {'scope': 'world', 'center': None},
                'Africa': {'scope': 'africa', 'center': {'lat': 0, 'lon': 20}},
                'Asia': {'scope': 'asia', 'center': {'lat': 30, 'lon': 90}},
                'Europe': {'scope': 'europe', 'center': {'lat': 50, 'lon': 10}},
                'North America': {'scope': 'north america', 'center': {'lat': 40, 'lon': -100}},
                'South America': {'scope': 'south america', 'center': {'lat': -15, 'lon': -60}},
                'Oceania': {'scope': 'world', 'center': {'lat': -25, 'lon': 140}}
            }

            # Filter the main dataset for year and continent
            if selected_continent == "World":
                df_filtered = df[df['Year'] == selected_year].copy()
            else:
                df_filtered = df[(df['Year'] == selected_year) & (df['Continent'] == selected_continent)].copy()

            # Calculate average temperature by country for filtered data
            country_avg = df_filtered.groupby('Country_Code')['Temperature'].mean().reset_index()
            country_avg.columns = ['Country_Code', 'Avg_Temperature']
            country_avg['Country_Name'] = country_avg['Country_Code'].map(
                dict(zip(df['Country_Code'], df['Country_Name']))
            )
        
     

        # Place metrics, map, and tables in a single row, map width matches both tables
        metrics_col, map_col, hot_col, cold_col = st.columns([1, 2, 1, 1], gap="small")

        with metrics_col:
            global_avg_year = country_avg['Avg_Temperature'].mean()
            hottest_country = country_avg.loc[country_avg['Avg_Temperature'].idxmax()]
            coldest_country = country_avg.loc[country_avg['Avg_Temperature'].idxmin()]
            display_name = coldest_country['Country_Code'] if str(coldest_country['Country_Name']) == 'Unknown' else coldest_country['Country_Name']
            temp_value = coldest_country['Avg_Temperature']
            if isinstance(temp_value, pd.Series) or hasattr(temp_value, 'values'):
                temp_value_float = float(temp_value.values[0])
            else:
                temp_value_float = float(temp_value)
            temp_color = '#313695' if temp_value_float < 0 else "#593e27"
            temp_range = country_avg['Avg_Temperature'].max() - country_avg['Avg_Temperature'].min()

            st.markdown(f"""
                <div style='text-align:left; margin-bottom:0.2em;'>
                    <span style='font-size:0.90em; color:#888;'>Global Avg</span><br>
                    <span style='color:#ff7f0e; font-size:1em;'>{global_avg_year:.2f}°C</span>
                </div>
                <div style='text-align:left; margin-bottom:0.2em;'>
                    <span style='font-size:0.90em; color:#888;'>Hottest</span><br>
                    <span style='color:#ff7f0e; font-size:1em;'>{hottest_country['Country_Name']}: {hottest_country['Avg_Temperature']:.1f}°C</span>
                </div>
                <div style='text-align:left; margin-bottom:0.2em;'>
                    <span style='font-size:0.90em; color:#888;'>Coldest</span><br>
                    <span style='color:{temp_color}; font-size:1em;'>{display_name}: {temp_value:.1f}°C</span>
                </div>
                <div style='text-align:left; margin-bottom:0.2em;'>
                    <span style='font-size:0.90em; color:#888;'>Temp Range</span><br>
                    <span style='color:#ff7f0e; font-size:1em;'>{temp_range:.1f}°C</span>
                </div>
            """, unsafe_allow_html=True)

        with map_col:
            continent_config = continents[selected_continent]
            fig = px.choropleth(
                country_avg,
                locations='Country_Code',
                locationmode='ISO-3',
                color='Avg_Temperature',
                hover_name='Country_Name',
                hover_data={
                    'Country_Name': True,
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
                labels={'Avg_Temperature': 'Temperature (°C)'}
            )
            fig.update_layout(
                height=420,
                geo=dict(
                    scope=continent_config['scope'],
                    center=continent_config['center'],
                    showframe=True,
                    showcoastlines=True,
                    showland=True,
                    landcolor="rgb(243, 243, 243)",
                    showcountries=True,
                    countrycolor="rgb(204, 204, 204)",
                    projection_type='natural earth',
                    bgcolor='rgba(0,0,0,0)',
                ),
                margin=dict(l=0, r=0, t=30, b=0),
                coloraxis_colorbar=dict(
                    title="Temp (°C)",
                    thickness=10,
                    len=0.45,
                    x=1.01
                )
            )
            fig.update_traces(
                marker_line_color='darkgray',
                marker_line_width=0.5
            )
            st.plotly_chart(fig, config={"responsive": True, "displayModeBar": False, "use_container_width": True})

        with hot_col:
            if country_avg.empty:
                st.info("No data for year/continent.")
            else:
                hottest = country_avg.nlargest(5, 'Avg_Temperature').copy()
                hottest['Display_Name'] = hottest.apply(lambda row: row['Country_Code'] if row['Country_Name'] == 'Unknown' else row['Country_Name'], axis=1)
                st.markdown("<div style='text-align:center; font-size:1em; font-weight:600; margin-bottom:0.2em;'>Top 5 Hottest</div>", unsafe_allow_html=True)
                df_hot = hottest[['Display_Name', 'Avg_Temperature']].rename(columns={'Display_Name': 'Country', 'Avg_Temperature': 'Avg Temp (°C)'})
                html = '<table style="width:100%; text-align:center; border-collapse:collapse; font-size:0.95em;">'
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
                st.markdown("<div style='text-align:center; font-size:1em; font-weight:600; margin-bottom:0.2em;'>Top 5 Coldest</div>", unsafe_allow_html=True)
                df_cold = coldest[['Display_Name', 'Avg_Temperature']].rename(columns={'Display_Name': 'Country', 'Avg_Temperature': 'Avg Temp (°C)'})
                html = '<table style="width:100%; text-align:center; border-collapse:collapse; font-size:0.95em;">'
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
            # Prepare data for correlation analysis
            # Get annual global temperature average
            annual_temp = df.groupby('Year')['Temperature'].mean().reset_index()
            annual_temp.columns = ['Year', 'Avg_Temperature']

            # Get annual maritime emissions (in tonnes, not millions)
            annual_maritime = world_maritime.groupby('Year')['CO2_Emissions'].sum().reset_index()
            annual_maritime.columns = ['Year', 'Total_CO2_Emissions']

            # Merge for overlapping years (maritime data is 2019-2024)
            correlation_data = pd.merge(annual_temp, annual_maritime, on='Year', how='inner')

            # Key metrics
            col1, col2, col3, col4, col5, col6 = st.columns(6)
            with col1:
                avg_emissions = correlation_data['Total_CO2_Emissions'].mean()
                st.markdown(f"""
                    <div style='text-align:center;'>
                        <span style='font-size:1.2em;'>Avg Annual Shipping CO₂</span><br>
                        <span style='color:#4b5e4b; font-size:2em; font-weight:bold;'>{avg_emissions:,.0f} tonnes</span>
                    </div>
                """, unsafe_allow_html=True)
            with col2:
                avg_temp = correlation_data['Avg_Temperature'].mean()
                st.markdown(f"""
                    <div style='text-align:center;'>
                        <span style='font-size:1.2em;'>Avg Global Temperature</span><br>
                        <span style='color:#4b5e4b; font-size:2em; font-weight:bold;'>{avg_temp:.2f}°C</span>
                    </div>
                """, unsafe_allow_html=True)
            with col3:
                st.markdown(f"""
                    <div style='text-align:center;'>
                        <span style='font-size:1.2em;'>Total Records</span><br>
                        <span style='color:#4b5e4b; font-size:2em; font-weight:bold;'>{len(df):,}</span>
                    </div>
                """, unsafe_allow_html=True)
            with col4:
                st.markdown(f"""
                    <div style='text-align:center;'>
                        <span style='font-size:1.2em;'>Countries</span><br>
                        <span style='color:#4b5e4b; font-size:2em; font-weight:bold;'>{df['Country_Code'].nunique()}</span>
                    </div>
                """, unsafe_allow_html=True)
            with col5:
                st.markdown(f"""
                    <div style='text-align:center;'>
                        <span style='font-size:1.2em;'>Year Range</span><br>
                        <span style='color:#4b5e4b; font-size:2em; font-weight:bold;'>{df['Year'].min()} - {df['Year'].max()}</span>
                    </div>
                """, unsafe_allow_html=True)
            # col6 left empty for spacing

            # Dual-axis chart showing both temperature and emissions (CO2 in tonnes)
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
                    tickfont=dict(color='#fff', size=18, family='Arial Black, Arial, sans-serif'),
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
                showlegend=True,
                legend=dict(x=0.01, y=0.99)
            )
            # Move Global Average Temperature & Maritime CO2 Emissions and Monthly Maritime Emissions Trend side by side
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
                # Add a trend line (linear regression)
                x = np.arange(len(monthly_emissions)).astype(float)
                y = monthly_emissions['CO2_Emissions'].values.astype(float)
                slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
                trend = intercept + slope * x
                fig_monthly.add_scatter(
                    x=monthly_emissions['YearMonth'],
                    y=trend,
                    mode='lines',
                    line=dict(color="#3B5D53", width=2)
                    
                )
                fig_monthly.update_layout(
                    xaxis=dict(tickfont=dict(size=14), showline=False, zeroline=False),
                    yaxis=dict(title=None, showline=False, zeroline=False),
                    margin=dict(l=30, r=30, t=40, b=30),
                    showlegend=True
                )
                st.plotly_chart(fig_monthly, config={"responsive": True}, key="monthly_emissions_chart")


            # Move Top 10 Vessel Types, pie chart, and stacked chart below
            col_viz1, col_viz2, col_viz3 = st.columns([2, 1, 1], gap="medium")
            with col_viz1:
                vessel_df = world_maritime.groupby('VESSEL')['CO2_Emissions'].sum().reset_index()
                top10_vessels = vessel_df.nlargest(10, 'CO2_Emissions').copy()
                top10_vessels['CO2_Mt'] = top10_vessels['CO2_Emissions'] / 1_000_000
                # Gradient: start from dashboard title color (#4b5e4b) and fade to a lighter shade
                base_color = np.array([75, 94, 75])  # #4b5e4b
                dark_color = np.array([45, 58, 45])  # darker shade
                light_color = np.array([200, 220, 200])  # much lighter green
                n = len(top10_vessels)
                gradient_colors = []
                # First three bars: interpolate between dark_color and base_color
                for i in range(3):
                    factor = i / 2 if 2 > 0 else 0
                    color = dark_color + (base_color - dark_color) * factor
                    gradient_colors.append(f"rgb({int(color[0])}, {int(color[1])}, {int(color[2])})")
                # Remaining bars: interpolate between base_color and light_color
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
                # Stacked column chart: CO2 emission by year
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
            

            
            # Temperature vs Sea Level correlation (2019-2024)
            # Removed redundant subheader for cleaner UI
            
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
            

            
            # Triple correlation (if maritime data available)
            if world_maritime is not None:
                # Removed redundant subheader for cleaner UI
                
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