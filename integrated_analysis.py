"""
Integrated Climate & Shipping Analysis Tool

This script combines climate data from World Bank with shipping CO2 emissions data
for comprehensive environmental analysis.

Author: Claire Namusoke
Date: November 9, 2025
"""

from climate import (
    fetch_climate_data, 
    auto_update_data, 
    load_local_data,
    display_climate_data
)
from shipping_integration import (
    ShippingEmissionsAPI,
    ClimateShippingIntegrator,
    integrate_shipping_with_climate
)
import pandas as pd
import json


def display_integrated_analysis(merged_data: pd.DataFrame, climate_data: dict, shipping_data: pd.DataFrame):
    """
    Display analysis of integrated climate and shipping emissions data.
    
    Args:
        merged_data (DataFrame): Merged dataset
        climate_data (dict): Original climate data
        shipping_data (DataFrame): Original shipping data
    """
    print("\n" + "="*70)
    print("INTEGRATED CLIMATE & SHIPPING EMISSIONS ANALYSIS")
    print("="*70)
    
    # Dataset summaries
    print("\n📊 Dataset Summary:")
    print(f"  Climate data: {len(climate_data.get('data', {}).get('data', {}))} countries")
    print(f"  Shipping data: {len(shipping_data)} records")
    print(f"  Merged data: {len(merged_data)} combined records")
    
    # Column information
    print(f"\n📋 Available Data Columns:")
    for i, col in enumerate(merged_data.columns, 1):
        print(f"  {i}. {col}")
    
    # Sample merged data
    print(f"\n🔍 Sample Merged Data (First 5 Rows):")
    print(merged_data.head().to_string())
    
    # Basic statistics
    print(f"\n📈 Data Statistics:")
    numeric_cols = merged_data.select_dtypes(include=['float64', 'int64']).columns
    if len(numeric_cols) > 0:
        print(merged_data[numeric_cols].describe().to_string())
    
    # Missing data analysis
    print(f"\n⚠️  Missing Data:")
    missing = merged_data.isnull().sum()
    missing_pct = (missing / len(merged_data) * 100).round(2)
    for col in merged_data.columns:
        if missing[col] > 0:
            print(f"  {col}: {missing[col]} ({missing_pct[col]}%)")


def save_integrated_data(merged_data: pd.DataFrame, filename: str = "integrated_climate_shipping.csv"):
    """
    Save integrated data to CSV file.
    
    Args:
        merged_data (DataFrame): Integrated dataset
        filename (str): Output filename
    """
    try:
        merged_data.to_csv(filename, index=False)
        print(f"\n✓ Integrated data saved to '{filename}'")
        return True
    except Exception as e:
        print(f"\n✗ Error saving integrated data: {e}")
        return False


def main():
    """
    Main function for integrated climate and shipping analysis.
    """
    print("="*70)
    print("INTEGRATED CLIMATE & SHIPPING EMISSIONS ANALYSIS TOOL")
    print("="*70)
    
    # Configuration
    climate_api_url = "https://cckpapi.worldbank.org/api/v1/cru-x0.5_timeseries_tas_timeseries_annual_1901-2024_mean_historical_cru_ts4.09_mean/global_countries?_format=json"
    climate_file = "climate_data.json"
    
    # You need to specify the correct path to your shipping data file in the repo
    # Common names might be: "data.csv", "emissions.csv", "shipping_emissions.csv"
    shipping_file_path = "emissions.csv"  # UPDATE THIS with actual filename
    
    print("\n📥 STEP 1: Fetching Climate Data...")
    print("-" * 70)
    
    # Fetch/update climate data
    updated = auto_update_data(climate_api_url, climate_file, force=False)
    climate_data, metadata = load_local_data(climate_file)
    
    if not climate_data:
        print("✗ Failed to load climate data. Exiting.")
        return
    
    print(f"✓ Climate data loaded ({len(climate_data.get('data', {}).get('data', {}))} countries)")
    
    print("\n📥 STEP 2: Fetching Shipping Emissions Data...")
    print("-" * 70)
    
    # Fetch shipping data from GitHub
    shipping_api = ShippingEmissionsAPI(
        github_username="Claire-Namusoke",
        repo_name="CO2_Emissions_from-Shippping"
    )
    
    # Try common filenames if the specified one doesn't work
    shipping_data = None
    common_filenames = [
        shipping_file_path,
        "data/emissions.csv",
        "emissions.csv",
        "data.csv",
        "shipping_emissions.csv",
        "CO2_emissions.csv"
    ]
    
    for filename in common_filenames:
        print(f"\nTrying: {filename}")
        shipping_data = shipping_api.fetch_csv_data(filename)
        if shipping_data is not None:
            print(f"✓ Found data at: {filename}")
            break
    
    if shipping_data is None:
        print("\n⚠️  Could not fetch shipping data from GitHub repository.")
        print("Please check:")
        print("  1. Repository name: CO2_Emissions_from-Shippping")
        print("  2. File path in the repository")
        print("  3. Repository is public")
        print("\nShowing climate data only...")
        display_climate_data(climate_data)
        return
    
    print(f"✓ Shipping data loaded ({len(shipping_data)} rows)")
    print(f"  Columns: {list(shipping_data.columns)}")
    
    print("\n🔄 STEP 3: Integrating Datasets...")
    print("-" * 70)
    
    # Integrate the datasets
    integrator = ClimateShippingIntegrator(climate_data, shipping_data)
    merged_data = integrator.merge_by_country()
    
    if merged_data is None:
        print("✗ Failed to integrate datasets")
        return
    
    print(f"✓ Integration successful!")
    
    print("\n📊 STEP 4: Analysis & Display...")
    print("-" * 70)
    
    # Display integrated analysis
    display_integrated_analysis(merged_data, climate_data, shipping_data)
    
    # Save integrated data
    save_integrated_data(merged_data, "integrated_climate_shipping.csv")
    
    # Save as JSON too
    try:
        merged_data.to_json("integrated_climate_shipping.json", orient="records", indent=2)
        print(f"✓ Integrated data also saved as JSON")
    except Exception as e:
        print(f"⚠️  Could not save JSON: {e}")
    
    print("\n" + "="*70)
    print("✓ ANALYSIS COMPLETE!")
    print("="*70)
    print("\n📁 Output Files:")
    print("  • climate_data.json - Raw climate data")
    print("  • integrated_climate_shipping.csv - Merged data (CSV)")
    print("  • integrated_climate_shipping.json - Merged data (JSON)")


if __name__ == "__main__":
    main()
