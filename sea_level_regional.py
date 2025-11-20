"""
Regional Sea Level Data Fetcher - NOAA STAR
Fetches sea level data by ocean region (2019-2024)

Data Source: NOAA STAR Laboratory for Satellite Altimetry
URL: https://www.star.nesdis.noaa.gov/socd/lsa/SeaLevelRise/

Author: Claire Namusoke
Date: November 14, 2025
"""

import requests
import pandas as pd
from typing import Dict, List, Optional
import io


# Ocean regions and their corresponding countries/territories
OCEAN_REGIONS = {
    'Pacific Ocean': {
        'url': 'https://www.star.nesdis.noaa.gov/socd/lsa/SeaLevelRise/slr/slr_sla_pac_free_ref_90.csv',
        'countries': ['United States', 'Japan', 'China', 'Australia', 'New Zealand', 'Philippines', 
                     'Indonesia', 'Chile', 'Peru', 'Ecuador', 'Colombia', 'Mexico', 'Canada',
                     'Papua New Guinea', 'Fiji', 'Samoa', 'Tonga', 'Kiribati', 'Marshall Islands',
                     'Micronesia', 'Palau', 'Vanuatu', 'Solomon Islands', 'Nauru', 'Tuvalu']
    },
    'North Pacific Ocean': {
        'url': 'https://www.star.nesdis.noaa.gov/socd/lsa/SeaLevelRise/slr/slr_sla_npac_free_ref_90.csv',
        'countries': ['United States', 'Canada', 'Japan', 'Russia', 'China', 'South Korea', 'North Korea']
    },
    'Atlantic Ocean': {
        'url': 'https://www.star.nesdis.noaa.gov/socd/lsa/SeaLevelRise/slr/slr_sla_atl_free_ref_90.csv',
        'countries': ['United States', 'Canada', 'United Kingdom', 'Ireland', 'France', 'Spain', 
                     'Portugal', 'Brazil', 'Argentina', 'Uruguay', 'Venezuela', 'Colombia',
                     'Guyana', 'Suriname', 'French Guiana', 'Morocco', 'Mauritania', 'Senegal',
                     'Gambia', 'Guinea-Bissau', 'Guinea', 'Sierra Leone', 'Liberia', 'Ivory Coast',
                     'Ghana', 'Togo', 'Benin', 'Nigeria', 'Cameroon', 'Gabon', 'Congo', 
                     'Democratic Republic of Congo', 'Angola', 'Namibia', 'South Africa']
    },
    'North Atlantic Ocean': {
        'url': 'https://www.star.nesdis.noaa.gov/socd/lsa/SeaLevelRise/slr/slr_sla_natl_free_ref_90.csv',
        'countries': ['United States', 'Canada', 'United Kingdom', 'Ireland', 'Iceland', 'Norway',
                     'France', 'Spain', 'Portugal', 'Morocco']
    },
    'Indian Ocean': {
        'url': 'https://www.star.nesdis.noaa.gov/socd/lsa/SeaLevelRise/slr/slr_sla_ind_free_ref_90.csv',
        'countries': ['India', 'Pakistan', 'Bangladesh', 'Sri Lanka', 'Maldives', 'Myanmar',
                     'Thailand', 'Indonesia', 'Australia', 'South Africa', 'Mozambique', 'Tanzania',
                     'Kenya', 'Somalia', 'Yemen', 'Oman', 'Iran', 'Madagascar', 'Mauritius',
                     'Seychelles', 'Comoros']
    },
    'Caribbean Sea': {
        'url': 'https://www.star.nesdis.noaa.gov/socd/lsa/SeaLevelRise/slr/slr_sla_car_free_ref_90.csv',
        'countries': ['Cuba', 'Jamaica', 'Haiti', 'Dominican Republic', 'Puerto Rico', 'Trinidad and Tobago',
                     'Barbados', 'Bahamas', 'Grenada', 'Saint Lucia', 'Saint Vincent and the Grenadines',
                     'Antigua and Barbuda', 'Dominica', 'Saint Kitts and Nevis', 'Venezuela', 'Colombia',
                     'Panama', 'Costa Rica', 'Nicaragua', 'Honduras', 'Belize', 'Mexico']
    },
    'Mediterranean Sea': {
        'url': 'https://www.star.nesdis.noaa.gov/socd/lsa/SeaLevelRise/slr/slr_sla_med_free_ref_90.csv',
        'countries': ['Spain', 'France', 'Italy', 'Greece', 'Turkey', 'Cyprus', 'Syria', 'Lebanon',
                     'Israel', 'Egypt', 'Libya', 'Tunisia', 'Algeria', 'Morocco', 'Malta', 'Slovenia',
                     'Croatia', 'Bosnia and Herzegovina', 'Montenegro', 'Albania']
    },
    'Gulf of America': {
        'url': 'https://www.star.nesdis.noaa.gov/socd/lsa/SeaLevelRise/slr/slr_sla_gom_free_ref_90.csv',
        'countries': ['United States', 'Mexico', 'Cuba']
    },
    'South China Sea': {
        'url': 'https://www.star.nesdis.noaa.gov/socd/lsa/SeaLevelRise/slr/slr_sla_scs_free_ref_90.csv',
        'countries': ['China', 'Vietnam', 'Philippines', 'Malaysia', 'Indonesia', 'Singapore',
                     'Brunei', 'Thailand', 'Cambodia']
    },
    'Bay of Bengal': {
        'url': 'https://www.star.nesdis.noaa.gov/socd/lsa/SeaLevelRise/slr/slr_sla_bob_free_ref_90.csv',
        'countries': ['India', 'Bangladesh', 'Myanmar', 'Sri Lanka', 'Thailand']
    },
    'Arabian Sea': {
        'url': 'https://www.star.nesdis.noaa.gov/socd/lsa/SeaLevelRise/slr/slr_sla_ara_free_ref_90.csv',
        'countries': ['India', 'Pakistan', 'Iran', 'Oman', 'Yemen', 'Somalia', 'Maldives']
    },
    'Persian Gulf': {
        'url': 'https://www.star.nesdis.noaa.gov/socd/lsa/SeaLevelRise/slr/slr_sla_pgu_free_ref_90.csv',
        'countries': ['Iran', 'Iraq', 'Kuwait', 'Saudi Arabia', 'Bahrain', 'Qatar', 
                     'United Arab Emirates', 'Oman']
    },
    'North Sea': {
        'url': 'https://www.star.nesdis.noaa.gov/socd/lsa/SeaLevelRise/slr/slr_sla_nos_free_ref_90.csv',
        'countries': ['United Kingdom', 'Norway', 'Denmark', 'Germany', 'Netherlands', 'Belgium', 'France']
    },
    'Baltic Sea': {
        'url': 'https://www.star.nesdis.noaa.gov/socd/lsa/SeaLevelRise/slr/slr_sla_bal_free_ref_90.csv',
        'countries': ['Sweden', 'Finland', 'Russia', 'Estonia', 'Latvia', 'Lithuania', 'Poland',
                     'Germany', 'Denmark']
    },
    'Adriatic Sea': {
        'url': 'https://www.star.nesdis.noaa.gov/socd/lsa/SeaLevelRise/slr/slr_sla_adr_free_ref_90.csv',
        'countries': ['Italy', 'Slovenia', 'Croatia', 'Bosnia and Herzegovina', 'Montenegro', 'Albania']
    },
    'Sea of Japan': {
        'url': 'https://www.star.nesdis.noaa.gov/socd/lsa/SeaLevelRise/slr/slr_sla_soj_free_ref_90.csv',
        'countries': ['Japan', 'Russia', 'South Korea', 'North Korea']
    },
    'Yellow Sea': {
        'url': 'https://www.star.nesdis.noaa.gov/socd/lsa/SeaLevelRise/slr/slr_sla_yes_free_ref_90.csv',
        'countries': ['China', 'South Korea', 'North Korea']
    },
    'Bering Sea': {
        'url': 'https://www.star.nesdis.noaa.gov/socd/lsa/SeaLevelRise/slr/slr_sla_ber_free_ref_90.csv',
        'countries': ['United States', 'Russia']
    },
    'Sea of Okhotsk': {
        'url': 'https://www.star.nesdis.noaa.gov/socd/lsa/SeaLevelRise/slr/slr_sla_oko_free_ref_90.csv',
        'countries': ['Russia', 'Japan']
    },
    'Andaman Sea': {
        'url': 'https://www.star.nesdis.noaa.gov/socd/lsa/SeaLevelRise/slr/slr_sla_and_free_ref_90.csv',
        'countries': ['Myanmar', 'Thailand', 'Indonesia', 'India']
    },
    'Indonesian Seas': {
        'url': 'https://www.star.nesdis.noaa.gov/socd/lsa/SeaLevelRise/slr/slr_sla_ins_free_ref_90.csv',
        'countries': ['Indonesia', 'Malaysia', 'Philippines', 'Singapore', 'Brunei', 'Timor-Leste']
    },
    'Southern Ocean': {
        'url': 'https://www.star.nesdis.noaa.gov/socd/lsa/SeaLevelRise/slr/slr_sla_soc_free_ref_90.csv',
        'countries': ['Antarctica', 'Chile', 'Argentina', 'South Africa', 'Australia', 'New Zealand']
    }
}


def fetch_regional_sea_level(region_name: str, url: str) -> Optional[pd.DataFrame]:
    """
    Fetch sea level data for a specific ocean region from NOAA STAR.
    
    Args:
        region_name: Name of the ocean region
        url: CSV download URL
        
    Returns:
        DataFrame with columns: year, Sea_Level_mm
    """
    try:
        print(f"  >> Downloading {region_name}...")
        response = requests.get(url, timeout=30)
        
        if response.status_code == 200:
            # Parse CSV - NOAA STAR format has header rows, skip them
            lines = response.text.strip().split('\n')
            
            # Skip header/comment lines (usually start with non-numeric characters)
            data_lines = []
            for line in lines:
                if line and line[0].isdigit():
                    data_lines.append(line)
            
            if not data_lines:
                print(f"     [X] No data lines found")
                return None
            
            # Parse data
            df = pd.read_csv(io.StringIO('\n'.join(data_lines)), header=None)
            
            # Convert first column to numeric to identify year
            df.iloc[:, 0] = pd.to_numeric(df.iloc[:, 0], errors='coerce')
            
            # Filter to rows from 2019+ to see which columns have recent data
            recent_rows = df[df.iloc[:, 0] >= 2018]  # Start from 2018 to catch partial 2019 data
            
            if len(recent_rows) == 0:
                print(f"     [WARN]  No data from 2019 onwards")
                return None
            
            #Find the last column with data in recent rows
            gmsl_col_idx = None
            for i in range(len(df.columns) - 1, 0, -1):  # Check from last to first
                if recent_rows.iloc[:, i].notna().sum() > 10:
                    gmsl_col_idx = i
                    break
            
            if gmsl_col_idx is None:
                print(f"     [X] No valid GMSL column in recent data")
                return None
            
            # Extract year and GMSL - combine last two columns if both have data
            # (NOAA STAR uses different satellite missions in adjacent columns)
            if gmsl_col_idx > 1 and recent_rows.iloc[:, gmsl_col_idx-1].notna().sum() > 10:
                # Combine the two columns (use fillna to merge)
                gmsl_data = df.iloc[:, gmsl_col_idx].fillna(df.iloc[:, gmsl_col_idx-1])
            else:
                gmsl_data = df.iloc[:, gmsl_col_idx]
            
            df_clean = pd.DataFrame({
                'year_decimal': df.iloc[:, 0],
                'Sea_Level_mm': gmsl_data
            })
            
            # Convert to numeric, coercing errors
            df_clean['year_decimal'] = pd.to_numeric(df_clean['year_decimal'], errors='coerce')
            df_clean['Sea_Level_mm'] = pd.to_numeric(df_clean['Sea_Level_mm'], errors='coerce')
            
            # Drop rows where either value is null
            df_clean = df_clean.dropna()
            
            if len(df_clean) == 0:
                print(f"     [X] No valid data after cleaning")
                return None
            
            # Convert decimal year to integer year
            df_clean['year'] = df_clean['year_decimal'].astype(float).apply(lambda x: int(x))
            
            # DEBUG: Show year range
            year_range = f"{df_clean['year'].min()}-{df_clean['year'].max()}"
            
            # Filter to 2019-2024
            df_filtered = df_clean[(df_clean['year'] >= 2019) & (df_clean['year'] <= 2024)].copy()
            
            if len(df_filtered) > 0:
                print(f"     [OK] {len(df_filtered)} records (2019-2024) from {year_range}")
                return df_filtered[['year', 'Sea_Level_mm']]
            else:
                print(f"     [WARN]  No 2019-2024 data (available: {year_range}, {len(df_clean)} total records)")
                return None
        else:
            print(f"     [X] HTTP {response.status_code}")
            return None
            
    except Exception as e:
        print(f"     [X] Error: {str(e)[:60]}")
        return None


def fetch_all_regions() -> Dict[str, pd.DataFrame]:
    """
    Fetch sea level data for all ocean regions.
    
    Returns:
        Dictionary mapping region names to DataFrames
    """
    print("\n" + "="*70)
    print("WAVE NOAA STAR REGIONAL SEA LEVEL DATA FETCHER")
    print("="*70)
    print(f"\n-> Fetching data from {len(OCEAN_REGIONS)} ocean regions...")
    print("   Time period: 2019-2024")
    print("   Data source: NOAA STAR Laboratory for Satellite Altimetry\n")
    
    regional_data = {}
    
    for region_name, region_info in OCEAN_REGIONS.items():
        df = fetch_regional_sea_level(region_name, region_info['url'])
        if df is not None:
            regional_data[region_name] = df
    
    return regional_data


def create_country_region_mapping() -> pd.DataFrame:
    """
    Create a mapping of countries to their ocean regions.
    
    Returns:
        DataFrame with columns: Country, Ocean_Regions
    """
    country_regions = {}
    
    for region_name, region_info in OCEAN_REGIONS.items():
        for country in region_info['countries']:
            if country not in country_regions:
                country_regions[country] = []
            country_regions[country].append(region_name)
    
    # Convert to DataFrame
    mapping_data = []
    for country, regions in sorted(country_regions.items()):
        mapping_data.append({
            'Country': country,
            'Ocean_Regions': ', '.join(sorted(regions)),
            'Number_of_Oceans': len(regions)
        })
    
    return pd.DataFrame(mapping_data)


def aggregate_regional_data(regional_data: Dict[str, pd.DataFrame]) -> pd.DataFrame:
    """
    Aggregate all regional data into a single DataFrame.
    
    Returns:
        DataFrame with yearly sea level data for all regions
    """
    all_data = []
    
    for region_name, df in regional_data.items():
        df_copy = df.copy()
        df_copy['Region'] = region_name
        df_copy.rename(columns={'GMSL_noGIA': 'Sea_Level_mm'}, inplace=True)
        all_data.append(df_copy)
    
    if all_data:
        combined = pd.concat(all_data, ignore_index=True)
        
        # Rebase to 2019 = 0 for each region
        for region in combined['Region'].unique():
            mask = combined['Region'] == region
            baseline = combined[mask & (combined['year'] == 2019)]['Sea_Level_mm'].mean()
            combined.loc[mask, 'Sea_Level_mm'] = combined.loc[mask, 'Sea_Level_mm'] - baseline
        
        return combined
    else:
        return pd.DataFrame()


def main():
    """Main execution"""
    
    # Fetch all regional data
    regional_data = fetch_all_regions()
    
    print("\n" + "="*70)
    print(f"📊 RESULTS: Successfully fetched {len(regional_data)} regions")
    print("="*70)
    
    if len(regional_data) == 0:
        print("\n❌ No data could be fetched. Check network connection.")
        return
    
    # Aggregate data
    print("\n- Processing data...")
    combined_df = aggregate_regional_data(regional_data)
    
    # Create country-region mapping
    country_mapping = create_country_region_mapping()
    
    # Save files
    print("\n- Saving files...")
    
    # 1. Combined regional data
    combined_df.to_csv('sea_level_regional_2019_2024.csv', index=False)
    print(f"   [OK] sea_level_regional_2019_2024.csv ({len(combined_df)} records)")
    
    # 2. Country-region mapping
    country_mapping.to_csv('country_ocean_mapping.csv', index=False)
    print(f"   [OK] country_ocean_mapping.csv ({len(country_mapping)} countries)")
    
    # 3. Yearly summary by region
    yearly_summary = combined_df.groupby(['Region', 'year']).agg({
        'Sea_Level_mm': 'mean'
    }).reset_index()
    yearly_summary.to_csv('sea_level_by_region_yearly.csv', index=False)
    print(f"   [OK] sea_level_by_region_yearly.csv")
    
    # Display summary statistics
    print("\n" + "="*70)
    print("- SUMMARY STATISTICS (2019-2024)")
    print("="*70)
    
    summary = combined_df.groupby('Region').agg({
        'Sea_Level_mm': ['min', 'max', 'mean']
    }).round(2)
    summary.columns = ['Min (mm)', 'Max (mm)', 'Mean (mm)']
    
    print("\nTop 5 regions by sea level rise:")
    top5 = summary.sort_values('Max (mm)', ascending=False).head(5)
    for region, row in top5.iterrows():
        print(f"  {region:30s}: {row['Max (mm)']:6.2f} mm (2019-2024)")
    
    print("\n* Files ready for dashboard integration!")
    print("   Next: Import into dashboard.py for visualization")


if __name__ == "__main__":
    main()
