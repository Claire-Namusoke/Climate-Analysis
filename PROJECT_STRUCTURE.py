"""
Climate Analysis Project - Code Inventory

All Python scripts in the Climate-Analysis project.
Author: Claire Namusoke
Date: November 9, 2025
"""

# =============================================================================
# MAIN APPLICATION FILES
# =============================================================================

"""
1. climate.py
   - Fetches World Bank climate data (temperature anomalies)
   - Smart caching with hash-based update detection
   - Covers 246 countries, 1901-2024
   - Output: climate_data.json

2. CO2.py
   - Fetches OECD maritime CO2 emissions data
   - Two tables: World Total and OECD Countries
   - Covers 2019-2024 monthly data
   - 19 vessel types (Container, Bulk carrier, Oil tanker, etc.)
   - Output: maritime_world_total.csv, maritime_oecd_countries.csv

3. dashboard.py
   - Interactive Streamlit web dashboard
   - 6 analysis sections:
     * Global Overview - Temperature trends and statistics
     * World Map - Interactive choropleth with drill-through by continent
     * Country Analysis - Detailed country-specific analysis
     * Trends & Comparisons - Compare multiple countries
     * Statistics - Global statistical analysis
     * Climate & Shipping Emissions - Correlation analysis showing 
       how maritime CO2 emissions relate to temperature rise
   - Dual-axis charts, scatter plots, correlation coefficients
   - Run with: streamlit run dashboard.py
"""

# =============================================================================
# DATA FETCHING UTILITIES
# =============================================================================

"""
4. fetch_world.py
   - Standalone script to fetch only World Total maritime emissions
   - Useful when OECD API times out
   - Output: maritime_world_total.csv

5. fetch_oecd.py
   - Standalone script to fetch only OECD Countries maritime emissions
   - Complements fetch_world.py
   - Output: maritime_oecd_countries.csv
"""

# =============================================================================
# DATA VIEWING UTILITIES
# =============================================================================

"""
6. view_climate_data.py
   - Display climate data from climate_data.json
   - Shows first 20 rows in table format
   - Quick data inspection tool

7. view_maritime_data.py
   - Display maritime emissions data
   - Shows first 20 rows of both tables
   - Summary statistics and top vessel types

8. show_countries.py
   - List country codes with their names
   - Shows first 10 countries from climate data
   - Explains ISO 3166-1 alpha-3 codes
"""

# =============================================================================
# INTEGRATION & ANALYSIS
# =============================================================================

"""
9. integrated_analysis.py
   - Framework for combining climate and maritime data
   - Correlation analysis
   - Ready for advanced statistical analysis

10. maritime_multi_source.py
    - Multi-source data integration module
    - Combines different maritime data sources
"""

# =============================================================================
# AUTOMATION
# =============================================================================

"""
11. scheduler.py
    - Automates climate data updates
    - Uses Windows Task Scheduler
    - Can run daily/weekly to keep data fresh

12. update_climate.bat
    - Batch file to run climate.py
    - Used by scheduler for automated updates
"""

# =============================================================================
# DATA FILES
# =============================================================================

"""
Data Files:
- climate_data.json (815 KB) - World Bank temperature data
- maritime_world_total.csv (530 KB) - Global maritime emissions
- maritime_oecd_countries.csv (1.06 MB) - OECD countries emissions

Configuration:
- requirements.txt - Python dependencies
- .gitignore - Files to exclude from Git

Documentation:
- README.md - Project overview
- CO2_GUIDE.md - Maritime data guide
- AUTO_UPDATE_GUIDE.md - Automation guide
- QUICKSTART.md - Getting started
- FEATURE_SUMMARY.md - Feature list
- SHIPPING_INTEGRATION_GUIDE.md - Integration guide
- PUSH_TO_GITHUB.md - GitHub setup
- BEFORE_AFTER.md - Comparison
"""

# =============================================================================
# FILE STRUCTURE
# =============================================================================

print("""
Climate-Analysis/
│
├── 📊 DATA COLLECTION
│   ├── climate.py              # World Bank climate data fetcher
│   ├── CO2.py                  # OECD maritime emissions fetcher
│   ├── fetch_world.py          # World total only
│   └── fetch_oecd.py           # OECD countries only
│
├── 🎨 VISUALIZATION
│   └── dashboard.py            # Interactive Streamlit dashboard
│
├── 👁️ DATA VIEWERS
│   ├── view_climate_data.py   # View climate table
│   ├── view_maritime_data.py  # View maritime tables
│   └── show_countries.py      # List country codes
│
├── 🔬 ANALYSIS
│   ├── integrated_analysis.py # Climate + Maritime correlation
│   └── maritime_multi_source.py # Multi-source integration
│
├── ⚙️ AUTOMATION
│   ├── scheduler.py           # Automated updates
│   └── update_climate.bat     # Batch runner
│
├── 📁 DATA FILES
│   ├── climate_data.json      # Temperature data
│   ├── maritime_world_total.csv    # World emissions
│   └── maritime_oecd_countries.csv # OECD emissions
│
└── 📚 DOCUMENTATION
    ├── README.md
    ├── CO2_GUIDE.md
    ├── AUTO_UPDATE_GUIDE.md
    └── [other guides]

TOTAL: 12 Python scripts + 3 data files + 8 documentation files
""")
