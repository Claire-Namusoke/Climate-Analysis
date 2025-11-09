"""
Fetch OECD Countries Maritime Emissions Only

This script fetches only the OECD Countries maritime CO2 emissions data.
Run separately from World data.

Author: Claire Namusoke
Date: November 9, 2025
"""

import requests
import pandas as pd
from datetime import datetime
from typing import Optional


# OECD countries data only
URL_OECD = "https://sdmx.oecd.org/public/rest/data/OECD.SDD.NAD.SEEA,DSD_MARITIME_TRANSPORT@DF_MARITIME_TRANSPORT,/.M.....EMISSIONS_POD..BULK_CARRIER+CHEM_TANKER+CONTAINER+GEN_CARGO+LIQ_GAS_TANKER+OIL_TANKER+OTHER_LIQ_TANKER+FERRY_PAX+CRUISE+FERRY_ROPAX+REFRIG_BULK+RO_RO+VEHICLE+YACHT+SERVICE_TUG+OFFSHORE+SERVICE_OTHER+MISC_FISH+MISC_OTHER.TER_DOM+TER_INT?dimensionAtObservation=AllDimensions"

HEADERS = {"Accept": "application/vnd.sdmx.data+json;version=1.0.0-wd"}


def fetch_oecd_data(timeout: int = 180, retries: int = 3) -> Optional[pd.DataFrame]:
    """Fetch OECD Countries maritime emissions data."""
    
    for attempt in range(retries):
        try:
            print(f"\n📡 Fetching OECD Countries Data (Attempt {attempt + 1}/{retries})...")
            print(f"   ⏱️  Timeout: {timeout} seconds")
            print(f"   Please wait... (this is larger than World data)")
            
            response = requests.get(URL_OECD, headers=HEADERS, timeout=timeout)
            
            if response.status_code != 200:
                print(f"✗ HTTP {response.status_code}")
                if attempt < retries - 1:
                    print(f"   Retrying in 10 seconds...")
                    import time
                    time.sleep(10)
                    timeout = timeout + 60
                    continue
                return None
            
            print(f"✓ Data received: {len(response.content):,} bytes")
            
            # Parse JSON
            data = response.json()
            dataset = data["data"]["dataSets"][0]["observations"]
            structure = data["data"]["structure"]["dimensions"]["observation"]
            dim_names = [d["id"] for d in structure]
            
            print(f"📊 Processing {len(dataset)} observations...")
            
            # Convert to DataFrame
            rows = []
            for key, value in dataset.items():
                dims = key.split(":")
                record = {
                    dim_names[i]: structure[i]["values"][int(dims[i])]["name"] 
                    for i in range(len(dims))
                }
                record["CO2_Emissions"] = value[0]
                rows.append(record)
            
            df = pd.DataFrame(rows)
            df["Group"] = "OECD Country"
            
            print(f"✓ Created DataFrame: {len(df)} rows × {len(df.columns)} columns")
            return df
        
        except requests.exceptions.Timeout:
            print(f"✗ Timeout after {timeout}s")
            if attempt < retries - 1:
                timeout = timeout + 60
                print(f"   Increasing timeout to {timeout}s...")
                continue
            return None
        except Exception as e:
            print(f"✗ Error: {e}")
            if attempt < retries - 1:
                import time
                time.sleep(10)
                continue
            return None
    
    return None


def main():
    print("="*70)
    print("FETCH OECD COUNTRIES MARITIME EMISSIONS")
    print("="*70)
    
    oecd_df = fetch_oecd_data()
    
    if oecd_df is not None:
        # Display summary
        print(f"\n{'='*70}")
        print("OECD COUNTRIES EMISSIONS - SUMMARY")
        print(f"{'='*70}")
        print(f"\n📊 Shape: {oecd_df.shape[0]} rows × {oecd_df.shape[1]} columns")
        print(f"\n📋 Columns: {list(oecd_df.columns)}")
        
        if 'REF_AREA' in oecd_df.columns:
            countries = oecd_df['REF_AREA'].nunique()
            print(f"\n🌍 Countries: {countries}")
            print(f"   Sample: {', '.join(oecd_df['REF_AREA'].unique()[:10].tolist())}...")
        
        if 'CO2_Emissions' in oecd_df.columns:
            print(f"\n💨 Emissions Stats:")
            print(f"   Total: {oecd_df['CO2_Emissions'].sum():,.2f}")
            print(f"   Mean: {oecd_df['CO2_Emissions'].mean():,.2f}")
        
        print(f"\n🔍 Sample (first 10 rows):")
        print(oecd_df.head(10).to_string())
        
        # Save
        filename = "maritime_oecd_countries.csv"
        oecd_df.to_csv(filename, index=False)
        print(f"\n✓ Saved to '{filename}'")
        
        print("\n" + "="*70)
        print("✓ SUCCESS!")
        print("="*70)
    else:
        print("\n✗ Failed to fetch OECD data")
        print("The OECD server might be overloaded. Try again later.")


if __name__ == "__main__":
    main()
