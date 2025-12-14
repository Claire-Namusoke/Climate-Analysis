def plot_monthly_percent_change(df: pd.DataFrame):
    """
    Plot the percent change in sea level (GMSL_Variation_mm) month-to-month.
    """
    import matplotlib.pyplot as plt
    df_sorted = df.sort_values(['Year', 'Month'])
    df_sorted['Percent_Change'] = df_sorted['GMSL_Variation_mm'].pct_change() * 100
    # Create a date label for x-axis
    df_sorted['Date'] = pd.to_datetime(df_sorted['Year'].astype(str) + '-' + df_sorted['Month'].astype(str))
    plt.figure(figsize=(12, 5))
    plt.bar(df_sorted['Date'], df_sorted['Percent_Change'], color='dodgerblue')
    plt.title('Monthly % Change in Global Mean Sea Level')
    plt.xlabel('Date')
    plt.ylabel('% Change from Previous Month')
    plt.grid(axis='y', linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.show()

"""
Sea Level Data Fetcher - REAL DATA VERSION v2

This script tries MULTIPLE NASA datasets to find accessible sea level data.
It retrieves real satellite altimetry measurements from trusted sources.

Author: Claire Namusoke
Date: November 12, 2025
Data Sources: 
- NASA CMR (Multiple datasets)
- NASA JPL Sea Level Portal
- NOAA CO-OPS
"""

import requests
import pandas as pd
from datetime import datetime
from typing import Optional
import numpy as np
import json


def fetch_copernicus_sea_level() -> Optional[pd.DataFrame]:
    """
    Fetch sea level data from Copernicus Climate Data Store.
    Uses the publicly accessible Copernicus Marine Service API.
    """
    try:
        print("\n" + "="*70)
        print("FETCHING COPERNICUS CLIMATE DATA STORE")
        print("="*70)
        
        print(f"\n🌍 Data Source: Copernicus Climate Data Store")
        print(f"   Service: Copernicus Marine Environment Monitoring Service")
        
        # Try Copernicus Marine Service public API endpoints
        urls_to_try = [
            # Global Ocean Gridded Sea Surface Heights
            'https://my.cmems-du.eu/thredds/dodsC/cmems_obs-sl_glo_phy-ssh_my_allsat-l4-duacs-0.25deg_P1D',
            # Alternative: AVISO+ (part of Copernicus)
            'https://www.aviso.altimetry.fr/fileadmin/documents/data/products/sea-level-anomalies/global/msla_h_global.txt',
            # Marine Data Store API
            'https://data.marine.copernicus.eu/product/SEALEVEL_GLO_PHY_L4_MY_008_047',
        ]
        
        print(f"\n📡 Attempting to access Copernicus data...\n")
        
        for i, url in enumerate(urls_to_try, 1):
            try:
                print(f"   {i}. Trying: {url[:70]}...")
                
                # For THREDDS/OPeNDAP endpoints, try to get metadata first
                if 'thredds' in url.lower() or 'opendap' in url.lower():
                    print(f"      (OPeNDAP endpoint - checking metadata)")
                    response = requests.get(url + '.das', timeout=30)
                    if response.status_code == 200:
                        print(f"      ✓ OPeNDAP service available")
                        print(f"      ⚠️  Note: OPeNDAP requires specialized client library")
                        print(f"      💡 Install: pip install netCDF4 xarray")
                        continue
                    else:
                        print(f"      ✗ HTTP {response.status_code}")
                        continue
                
                # Try direct HTTP access
                response = requests.get(url, timeout=30, allow_redirects=True)
                
                if response.status_code == 200:
                    content_type = response.headers.get('content-type', '')
                    
                    # Check if it's HTML (likely a portal page, not data)
                    if 'text/html' in content_type:
                        print(f"      ✗ Portal page (requires login or different access method)")
                        continue
                    
                    # Check if it's actual data
                    if 'text/plain' in content_type or 'text/csv' in content_type:
                        print(f"      ✓ Downloaded {len(response.text)} bytes")
                        parsed = parse_nasa_sea_level_data(response.text)
                        if parsed and len(parsed) > 0:
                            print(f"      ✅ SUCCESS! Parsed {len(parsed)} records")
                            return pd.DataFrame(parsed)
                    elif 'application/netcdf' in content_type or 'application/x-netcdf' in content_type:
                        print(f"      ⚠️  NetCDF format requires netCDF4/xarray library")
                        print(f"      💡 Install: pip install netCDF4 xarray")
                        continue
                    else:
                        print(f"      ✗ Unexpected format: {content_type}")
                elif response.status_code == 401 or response.status_code == 403:
                    print(f"      ✗ Authentication required (HTTP {response.status_code})")
                else:
                    print(f"      ✗ HTTP {response.status_code}")
                    
            except requests.exceptions.Timeout:
                print(f"      ✗ Connection timeout")
            except Exception as e:
                print(f"      ✗ Error: {str(e)[:50]}")
                continue
        
        print("\n💡 Copernicus data requires:")
        print("   1. Free registration at https://data.marine.copernicus.eu/")
        print("   2. NetCDF4/xarray libraries for data access")
        print("   3. Or manual download via their web portal")
        
        return None
        
    except Exception as e:
        print(f"✗ Error: {e}")
        return None


def fetch_nasa_cmr_sea_level() -> Optional[pd.DataFrame]:
    """
    Try MULTIPLE NASA datasets through CMR API.
    Tests different dataset identifiers to find accessible data.
    
    Returns:
        DataFrame: Real satellite measurements or None if all fail
    """
    cmr_url = "https://cmr.earthdata.nasa.gov/search/granules.json"
    
    # Try multiple datasets in order of likelihood
    datasets_to_try = [
        ('SEA_LEVEL_GMSL', 'Global Mean Sea Level'),
        ('MERGED_TP_J1_OSTM_OST_GMSL_ASCII_V51', 'Merged Altimetry ASCII'),
        ('MERGED_TP_J1_OSTM_OST_GMSL_ASCII_V42', 'Merged Altimetry v4.2'),
        ('SEA_SURFACE_HEIGHT_ALT_GRIDS_L4_2SATS_5DAY_6THDEG_V_JPL2205', 'Surface Height Grids'),
        ('Jason_CS_S6A_L2_ALT_HR_NTC', 'Jason-CS Sentinel-6A'),
    ]
    
    try:
        print("\n" + "="*70)
        print("🔍 TRYING MULTIPLE NASA DATASETS")
        print("="*70)
        
        for dataset_id, dataset_name in datasets_to_try:
            print(f"\n📡 Dataset: {dataset_name}")
            print(f"   ID: {dataset_id}")
            
            params = {
                'short_name': dataset_id,
                'page_size': 20,
                'sort_key': '-start_date',
            }
            
            try:
                response = requests.get(cmr_url, params=params, timeout=30)
                
                if response.status_code != 200:
                    print(f"   ✗ HTTP {response.status_code}")
                    continue
                
                data = response.json()
                
                if 'feed' not in data or 'entry' not in data['feed']:
                    print("   ✗ No entries in response")
                    continue
                
                entries = data['feed']['entry']
                if len(entries) == 0:
                    print("   ✗ No granules found")
                    continue
                
                print(f"   ✓ Found {len(entries)} granules")
                
                # Look for accessible data URLs
                records = []
                public_urls = []
                protected_urls = []
                
                for entry in entries[:10]:  # Check first 10 granules
                    if 'links' not in entry:
                        continue
                    
                    for link in entry['links']:
                        href = link.get('href', '')
                        if not href:
                            continue
                        
                        # Categorize URLs
                        if 'public' in href.lower():
                            if any(ext in href.lower() for ext in ['.txt', '.csv', '.ascii']):
                                public_urls.append(href)
                        elif 'protected' in href.lower():
                            protected_urls.append(href)
                
                if public_urls:
                    print(f"   ✓ Found {len(public_urls)} PUBLIC data files!")
                    print(f"   📥 Attempting downloads...")
                    
                    for url in public_urls[:3]:
                        try:
                            print(f"      Trying: {url[:70]}...")
                            file_resp = requests.get(url, timeout=30)
                            
                            if file_resp.status_code == 200:
                                content = file_resp.text
                                print(f"      ✓ Downloaded {len(content)} bytes")
                                
                                # Try to parse
                                parsed = parse_nasa_sea_level_data(content)
                                if parsed and len(parsed) > 0:
                                    print(f"      ✅ SUCCESS! Parsed {len(parsed)} records")
                                    df = pd.DataFrame(parsed)
                                    print(f"\n✅ REAL DATA OBTAINED!")
                                    print(f"   Dataset: {dataset_name}")
                                    print(f"   Records: {len(df)}")
                                    print(f"   Range: {df['Year'].min():.1f} - {df['Year'].max():.1f}")
                                    return df
                                else:
                                    print(f"      ✗ Could not parse data")
                        except Exception as e:
                            print(f"      ✗ Error: {str(e)[:50]}")
                            continue
                
                if protected_urls:
                    print(f"   ⚠️  Found {len(protected_urls)} PROTECTED files (need auth)")
                
                print(f"   ✗ No accessible data in this dataset")
                
            except Exception as e:
                print(f"   ✗ Error: {str(e)[:60]}")
                continue
        
        print("\n❌ All datasets tried - none have publicly accessible data")
        print("   💡 NASA datasets require Earthdata Login for access")
        return None
        
    except Exception as e:
        print(f"✗ CMR Error: {e}")
        return None


def parse_nasa_sea_level_data(text_data: str) -> list:
    """
    Parse NASA sea level data from text format.
    Handles multiple NASA data formats.
    
    Expected formats:
    1. year_fraction gmsl_variation std_dev
    2. year month day gmsl
    3. decimal_year gmsl
    """
    records = []
    
    for line in text_data.split('\n'):
        line = line.strip()
        
        # Skip comments and headers
        if not line or line.startswith('#') or line.startswith('HDR') or 'year' in line.lower():
            continue
        
        try:
            parts = line.split()
            if len(parts) < 2:
                continue
            
            # Try different formats
            if len(parts) >= 3:
                # Format: year_fraction gmsl_variation std_dev
                year_frac = float(parts[0])
                gmsl_mm = float(parts[1])
                std_dev = float(parts[2]) if len(parts) > 2 else 0.5
                
                year = int(year_frac)
                month = int((year_frac - year) * 12) + 1
                
                records.append({
                    'Year': year,
                    'Month': month,
                    'GMSL_Variation_mm': gmsl_mm,
                    'StdDev_mm': std_dev
                })
            
        except (ValueError, IndexError):
            continue
    
    return records


def fetch_nasa_jpl_sea_level() -> Optional[pd.DataFrame]:
    """
    Priority 2: Direct NASA JPL download.
    """
    try:
        print("\n" + "="*70)
        print("FETCHING REAL NASA JPL SEA LEVEL DATA")
        print("="*70)
        
        # Try multiple JPL URLs
        urls_to_try = [
            'https://podaac-tools.jpl.nasa.gov/drive/files/allData/merged_alt/L2/TP_J1_OSTM/global_mean_sea_level/GMSL_TPJAOS_5.1_199209_202312.txt',
            'https://sealevel.jpl.nasa.gov/data/gmsl_2024rel2_global.txt',
        ]
        
        for url in urls_to_try:
            try:
                print(f"\n🛰️  URL: {url[:80]}...")
                print(f"📡 Downloading...")
                
                response = requests.get(url, timeout=30)
                
                if response.status_code == 200:
                    print(f"✓ Downloaded {len(response.text)} bytes")
                    
                    parsed = parse_nasa_sea_level_data(response.text)
                    if parsed and len(parsed) > 0:
                        print(f"✓ Parsed {len(parsed)} measurements")
                        return pd.DataFrame(parsed)
                else:
                    print(f"✗ HTTP {response.status_code}")
                    
            except Exception as e:
                print(f"✗ Error: {str(e)[:60]}")
                continue
        
        return None
        
    except Exception as e:
        print(f"✗ Error: {e}")
        return None


def fetch_noaa_tide_gauge() -> Optional[pd.DataFrame]:
    """
    Priority 3: NOAA tide gauge data.
    """
    try:
        print("\n" + "="*70)
        print("FETCHING REAL NOAA TIDE GAUGE DATA")
        print("="*70)
        
        # The Battery, New York - long-term tide gauge
        station_id = "8518750"
        
        print(f"🌊 Station: The Battery, New York ({station_id})")
        print(f"📡 Downloading monthly mean sea level...")
        
        records = []
        
        # Fetch year by year for 2019-2024
        for year in range(2019, 2025):
            try:
                url = "https://api.tidesandcurrents.noaa.gov/api/prod/datagetter"
                params = {
                    'product': 'monthly_mean',
                    'application': 'NOS.COOPS.TAC.WL',
                    'begin_date': f'{year}01',
                    'end_date': f'{year}12',
                    'datum': 'MSL',
                    'station': station_id,
                    'time_zone': 'GMT',
                    'units': 'metric',
                    'format': 'json'
                }
                
                response = requests.get(url, params=params, timeout=30)
                
                if response.status_code == 200:
                    data = response.json()
                    if 'data' in data and len(data['data']) > 0:
                        for entry in data['data']:
                            records.append({
                                'Year': year,
                                'Month': int(entry['month']),
                                'GMSL_Variation_mm': float(entry['v']) * 1000,  # Convert m to mm
                                'StdDev_mm': 5.0
                            })
                        print(f"   ✓ {year}: {len(data['data'])} months")
                    else:
                        print(f"   ✓ {year}: 0 months")
                else:
                    print(f"   ✗ {year}: HTTP {response.status_code}")
                    
            except Exception as e:
                print(f"   ✗ {year}: {str(e)[:40]}")
                continue
        
        if len(records) > 0:
            print(f"✓ Got {len(records)} NOAA measurements")
            return pd.DataFrame(records)
        else:
            print("✗ No valid records from NOAA")
            return None
            
    except Exception as e:
        print(f"✗ Error: {e}")
        return None


def create_fallback_data() -> pd.DataFrame:
    """
    Priority 4: Create synthesized data based on documented NASA rates.
    """
    print("\n⚠️  Creating SYNTHESIZED data (NOT REAL)...")
    print("   Based on NASA/NOAA documented rates: 3.85-4.0 mm/year")
    
    # Create monthly data for 2019-2024
    data = []
    base_rate = 3.85  # mm/year
    
    for year in range(2019, 2025):
        rate = base_rate + (year - 2019) * 0.025  # Slight acceleration
        
        for month in range(1, 13):
            data.append({
                'Year': year,
                'Month': month,
                'GMSL_Variation_mm': (year - 2019) * rate + (month / 12) * rate,
                'StdDev_mm': 0.39
            })
    
    return pd.DataFrame(data)


def process_to_yearly(df: pd.DataFrame) -> pd.DataFrame:
    """
    Convert monthly data to yearly averages with annual rates.
    """
    yearly = df.groupby('Year').agg({
        'GMSL_Variation_mm': 'mean',
        'StdDev_mm': 'mean',
        'Month': 'count'  # Count months instead of Year
    }).reset_index()
    
    yearly.columns = ['Year', 'GMSL_Variation_mm', 'StdDev_mm', 'Total_Observations']
    
    # Calculate annual rates
    yearly['Annual_Rate_mm'] = 0.0
    for i in range(1, len(yearly)):
        curr_val = float(yearly.loc[i, 'GMSL_Variation_mm'])  # type: ignore
        prev_val = float(yearly.loc[i-1, 'GMSL_Variation_mm'])  # type: ignore
        yearly.loc[i, 'Annual_Rate_mm'] = curr_val - prev_val
    
    if len(yearly) > 0:
        yearly.loc[0, 'Annual_Rate_mm'] = yearly['Annual_Rate_mm'].mean()
    
    return yearly


def main():
    """
    Main execution - try all data sources in priority order.
    """
    print("\n" + "="*70)
    print("🌊 REAL SEA LEVEL DATA FETCHER")
    print("="*70)
    print("\nAttempting to fetch ACTUAL measurements from multiple sources...\n")
    
    df = None
    source = None
    
    # Priority 1: Copernicus Climate Data Store
    print("🎯 Priority 1: Copernicus Climate Data Store...")
    df = fetch_copernicus_sea_level()
    if df is not None:
        source = "Copernicus Climate Data Store (✅ REAL DATA)"
    
    # Priority 2: NASA CMR (multiple datasets)
    if df is None:
        print("\n🎯 Priority 2: NASA CMR API (Testing multiple datasets)...")
        df = fetch_nasa_cmr_sea_level()
        if df is not None:
            source = "NASA Common Metadata Repository (✅ REAL DATA)"
    
    # Priority 3: NASA JPL Direct
    if df is None:
        print("\n🎯 Priority 3: NASA JPL Direct Download...")
        df = fetch_nasa_jpl_sea_level()
        if df is not None:
            source = "NASA JPL Sea Level Portal (✅ REAL DATA)"
    
    # Priority 4: NOAA
    if df is None:
        print("\n🎯 Priority 4: NOAA Tide Gauge...")
        df = fetch_noaa_tide_gauge()
        if df is not None:
            source = "NOAA CO-OPS Tide Gauge (✅ REAL DATA)"
    
    # Priority 5: Fallback
    if df is None:
        print("\n⚠️  All real data sources unavailable")
        print("   This could be due to:")
        print("   - Network connectivity issues")
        print("   - Server maintenance")
        print("   - API authentication requirements")
        print("\n💡 Falling back to synthesized data...")
        df = create_fallback_data()
        source = "Synthesized (❌ NOT REAL DATA)"
    
    # Filter to 2019-2024
    df = df[(df['Year'] >= 2019) & (df['Year'] <= 2024)]
    
    print("\n" + "="*70)
    print(f"📊 DATA SOURCE: {source}")
    print("="*70)
    
    print(f"\n🔧 Filtered to 2019-2024: {len(df)} records (from {len(df)})")
    
    # Rebase to 2019 = 0
    if len(df) > 0:
        baseline = df[df['Year'] == 2019]['GMSL_Variation_mm'].mean()
        df['GMSL_Variation_mm'] = df['GMSL_Variation_mm'] - baseline
        print("✓ Rebased to 2019 = 0 mm")
    
    # Convert to yearly
    yearly = process_to_yearly(df)
    
    print(f"\n📊 Summary:")
    print(f"   Years: {yearly['Year'].min()} - {yearly['Year'].max()}")
    print(f"   Records: {len(yearly)}")
    print(f"   Total rise: {yearly['GMSL_Variation_mm'].max():.2f} mm")
    print(f"   Avg rate: {yearly['Annual_Rate_mm'].mean():.2f} mm/year")
    
    # Save both monthly and yearly
    print(f"\n📁 Saving data...")
    df.to_csv('sea_level_monthly.csv', index=False)
    yearly.to_csv('sea_level_yearly.csv', index=False)
    print("✓ Saved: sea_level_monthly.csv, sea_level_yearly.csv")

    # Plot monthly percent change if monthly data is available
    if df is not None and not df.empty:
        plot_monthly_percent_change(df)
    
    if source and "NOT REAL" in source:
        print("\n" + "="*70)
        print("⚠️  WARNING: USING SYNTHESIZED DATA")
        print("   Real data sources were unavailable")
        print("="*70)
    
    print("\n💡 Next step: Run dashboard with data!")
    print("   Command: streamlit run dashboard.py")


if __name__ == "__main__":
    main()
