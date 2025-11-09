"""
OECD Maritime CO2 Emissions Data Fetcher

This script fetches CO2 emissions data from OECD SDMX-JSON API for maritime transport.
It retrieves data for both World totals and individual OECD countries.

Author: Claire Namusoke
Date: November 9, 2025
Data Source: OECD Statistical Database (SDMX-JSON API)
"""

import requests
import pandas as pd
import json
from datetime import datetime
from typing import Dict, Tuple, Optional


# OECD SDMX-JSON API Endpoints
# World data - Global maritime emissions totals
URL_WORLD = "https://sdmx.oecd.org/public/rest/data/OECD.SDD.NAD.SEEA,DSD_MARITIME_TRANSPORT@DF_MARITIME_TRANSPORT,2.0/W.M.....EMISSIONS_POD..BULK_CARRIER+CHEM_TANKER+CONTAINER+GEN_CARGO+LIQ_GAS_TANKER+OIL_TANKER+OTHER_LIQ_TANKER+FERRY_PAX+CRUISE+FERRY_ROPAX+REFRIG_BULK+RO_RO+VEHICLE+YACHT+SERVICE_TUG+OFFSHORE+SERVICE_OTHER+MISC_FISH+MISC_OTHER.TER_DOM+TER_INT?dimensionAtObservation=AllDimensions"

# OECD countries data - Individual country emissions
URL_OECD = "https://sdmx.oecd.org/public/rest/data/OECD.SDD.NAD.SEEA,DSD_MARITIME_TRANSPORT@DF_MARITIME_TRANSPORT,/.M.....EMISSIONS_POD..BULK_CARRIER+CHEM_TANKER+CONTAINER+GEN_CARGO+LIQ_GAS_TANKER+OIL_TANKER+OTHER_LIQ_TANKER+FERRY_PAX+CRUISE+FERRY_ROPAX+REFRIG_BULK+RO_RO+VEHICLE+YACHT+SERVICE_TUG+OFFSHORE+SERVICE_OTHER+MISC_FISH+MISC_OTHER.TER_DOM+TER_INT?dimensionAtObservation=AllDimensions"

# HTTP headers for SDMX-JSON format
HEADERS = {"Accept": "application/vnd.sdmx.data+json;version=1.0.0-wd"}


def fetch_sdmx_to_dataframe(url: str, timeout: int = 120, retries: int = 3) -> Optional[pd.DataFrame]:
    """
    Fetch SDMX-JSON data from OECD API and convert to pandas DataFrame.
    
    This function:
    1. Makes HTTP request to OECD SDMX API
    2. Parses the complex SDMX-JSON structure
    3. Extracts observations and dimensions
    4. Converts to a flat pandas DataFrame
    
    Args:
        url (str): OECD SDMX-JSON API endpoint URL
        timeout (int): Request timeout in seconds (default: 120)
        retries (int): Number of retry attempts (default: 3)
        
    Returns:
        DataFrame: Pandas DataFrame with CO2 emissions data, or None if error
    """
    for attempt in range(retries):
        try:
            print(f"\n📡 Fetching data from OECD API (Attempt {attempt + 1}/{retries})...")
            print(f"   URL: {url[:80]}...")
            print(f"   ⏱️  This may take 1-2 minutes for large datasets...")
            
            # Make HTTP request to OECD API with longer timeout
            response = requests.get(url, headers=HEADERS, timeout=timeout)
            
            if response.status_code != 200:
                print(f"✗ Failed to fetch data: HTTP {response.status_code}")
                if attempt < retries - 1:
                    print(f"   Retrying in 5 seconds...")
                    import time
                    time.sleep(5)
                    continue
                return None
            
            print(f"✓ Data received successfully ({len(response.content):,} bytes)")
            
            # Parse JSON response
            data = response.json()
            
            # Extract observations (the actual data points)
            dataset = data["data"]["dataSets"][0]["observations"]
            
            # Extract dimension structure (metadata about the data)
            structure = data["data"]["structure"]["dimensions"]["observation"]
            dim_names = [d["id"] for d in structure]
            
            print(f"📊 Processing {len(dataset)} observations...")
            print(f"   Dimensions: {', '.join(dim_names)}")
            
            # Convert observations to list of dictionaries
            rows = []
            for key, value in dataset.items():
                # Key format: "0:1:2:3:4..." represents dimension indices
                dims = key.split(":")
                
                # Build record by mapping dimension indices to their values
                record = {
                    dim_names[i]: structure[i]["values"][int(dims[i])]["name"] 
                    for i in range(len(dims))
                }
                
                # Add CO2 emissions value
                record["CO2_Emissions"] = value[0]
                
                rows.append(record)
            
            # Convert to pandas DataFrame
            df = pd.DataFrame(rows)
            
            print(f"✓ Created DataFrame: {len(df)} rows × {len(df.columns)} columns")
            print(f"   Columns: {list(df.columns)}")
            
            return df
        
        except requests.exceptions.Timeout:
            print(f"✗ Request timed out after {timeout} seconds")
            if attempt < retries - 1:
                print(f"   Retrying with longer timeout...")
                timeout = timeout + 60  # Add 60 seconds each retry
                continue
            return None
        except requests.exceptions.RequestException as e:
            print(f"✗ Network error: {e}")
            if attempt < retries - 1:
                print(f"   Retrying in 5 seconds...")
                import time
                time.sleep(5)
                continue
            return None
        except KeyError as e:
            print(f"✗ Data structure error: Missing key {e}")
            return None
        except Exception as e:
            print(f"✗ Unexpected error: {e}")
            return None
    
    return None


def add_group_column(df: pd.DataFrame, group_name: str) -> pd.DataFrame:
    """
    Add a 'Group' column to identify the data source.
    
    Args:
        df (DataFrame): Input DataFrame
        group_name (str): Group identifier (e.g., "World Total" or "OECD Country")
        
    Returns:
        DataFrame: DataFrame with added Group column
    """
    df_copy = df.copy()
    df_copy["Group"] = group_name
    return df_copy


def save_to_csv(df: pd.DataFrame, filename: str) -> bool:
    """
    Save DataFrame to CSV file.
    
    Args:
        df (DataFrame): DataFrame to save
        filename (str): Output filename
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        df.to_csv(filename, index=False, encoding='utf-8')
        print(f"✓ Saved to '{filename}'")
        return True
    except Exception as e:
        print(f"✗ Error saving CSV: {e}")
        return False


def save_to_json(df: pd.DataFrame, filename: str) -> bool:
    """
    Save DataFrame to JSON file.
    
    Args:
        df (DataFrame): DataFrame to save
        filename (str): Output filename
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        df.to_json(filename, orient='records', indent=2)
        print(f"✓ Saved to '{filename}'")
        return True
    except Exception as e:
        print(f"✗ Error saving JSON: {e}")
        return False


def display_data_summary(df: pd.DataFrame, title: str):
    """
    Display summary information about the DataFrame.
    
    Args:
        df (DataFrame): DataFrame to summarize
        title (str): Title for the summary
    """
    print(f"\n{'='*70}")
    print(f"{title}")
    print(f"{'='*70}")
    
    print(f"\n📊 Data Shape: {df.shape[0]} rows × {df.shape[1]} columns")
    
    print(f"\n📋 Columns:")
    for col in df.columns:
        print(f"   • {col}")
    
    # Show unique values for key dimensions
    if 'REF_AREA' in df.columns:
        unique_areas = df['REF_AREA'].nunique()
        print(f"\n🌍 Unique Countries/Regions: {unique_areas}")
        print(f"   Sample: {', '.join(df['REF_AREA'].unique()[:5].tolist())}...")
    
    if 'TIME_PERIOD' in df.columns:
        years = sorted(df['TIME_PERIOD'].unique())
        print(f"\n📅 Time Period: {years[0]} to {years[-1]} ({len(years)} periods)")
    
    if 'CO2_Emissions' in df.columns:
        print(f"\n💨 CO2 Emissions Statistics:")
        print(f"   Total: {df['CO2_Emissions'].sum():,.2f}")
        print(f"   Mean: {df['CO2_Emissions'].mean():,.2f}")
        print(f"   Min: {df['CO2_Emissions'].min():,.2f}")
        print(f"   Max: {df['CO2_Emissions'].max():,.2f}")
    
    print(f"\n🔍 Sample Data (first 5 rows):")
    print(df.head().to_string())


def fetch_all_maritime_data() -> Tuple[Optional[pd.DataFrame], Optional[pd.DataFrame]]:
    """
    Fetch both World and OECD countries maritime emissions data.
    
    Returns:
        tuple: (world_df, oecd_df) - Two DataFrames or (None, None) if error
    """
    print("="*70)
    print("OECD MARITIME CO2 EMISSIONS DATA FETCHER")
    print("="*70)
    
    # Fetch World totals
    print("\n📍 STEP 1: Fetching World Total Data")
    print("-" * 70)
    world_df = fetch_sdmx_to_dataframe(URL_WORLD)
    
    if world_df is not None:
        world_df = add_group_column(world_df, "World Total")
        display_data_summary(world_df, "WORLD TOTAL EMISSIONS")
    else:
        print("⚠️  Failed to fetch World data")
    
    # Fetch OECD countries
    print("\n📍 STEP 2: Fetching OECD Countries Data")
    print("-" * 70)
    oecd_df = fetch_sdmx_to_dataframe(URL_OECD)
    
    if oecd_df is not None:
        oecd_df = add_group_column(oecd_df, "OECD Country")
        display_data_summary(oecd_df, "OECD COUNTRIES EMISSIONS")
    else:
        print("⚠️  Failed to fetch OECD data")
    
    return world_df, oecd_df


def combine_datasets(world_df: pd.DataFrame, oecd_df: pd.DataFrame) -> Optional[pd.DataFrame]:
    """
    Combine World and OECD datasets into one DataFrame.
    
    Args:
        world_df (DataFrame): World totals data
        oecd_df (DataFrame): OECD countries data
        
    Returns:
        DataFrame: Combined dataset or None if error
    """
    try:
        print("\n🔄 Combining World and OECD datasets...")
        
        combined = pd.concat([world_df, oecd_df], ignore_index=True)
        
        print(f"✓ Combined dataset created: {len(combined)} total rows")
        print(f"   World Total: {len(world_df)} rows")
        print(f"   OECD Countries: {len(oecd_df)} rows")
        
        return combined
    except Exception as e:
        print(f"✗ Error combining datasets: {e}")
        return None


def main():
    """
    Main function to fetch, process, and save OECD maritime CO2 emissions data.
    """
    # Fetch both datasets
    world_df, oecd_df = fetch_all_maritime_data()
    
    if world_df is None and oecd_df is None:
        print("\n✗ Failed to fetch any data. Please check your internet connection.")
        return
    
    # Save individual datasets
    print("\n" + "="*70)
    print("SAVING DATA")
    print("="*70)
    
    if world_df is not None:
        print("\n📁 Saving World Total data...")
        save_to_csv(world_df, "maritime_world_total.csv")
    
    if oecd_df is not None:
        print("\n📁 Saving OECD Countries data...")
        save_to_csv(oecd_df, "maritime_oecd_countries.csv")
    
    # Summary
    print("\n" + "="*70)
    print("✓ PROCESS COMPLETED!")
    print("="*70)
    print("\n📂 Output Files (2 separate CSV tables):")
    if world_df is not None:
        print("   • maritime_world_total.csv")
    if oecd_df is not None:
        print("   • maritime_oecd_countries.csv")
    
    

if __name__ == "__main__":
    # Entry point: Execute main function when script is run directly
    main()
