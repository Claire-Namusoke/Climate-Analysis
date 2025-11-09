"""
Fetch OECD World Total Maritime Emissions Only

This script fetches only the World Total maritime CO2 emissions data.
Lighter load, faster, more likely to succeed.

Author: Claire Namusoke
Date: November 9, 2025
"""

import requests
import pandas as pd
from datetime import datetime
from typing import Optional


# World data only - Global maritime emissions totals
URL_WORLD = "https://sdmx.oecd.org/public/rest/data/OECD.SDD.NAD.SEEA,DSD_MARITIME_TRANSPORT@DF_MARITIME_TRANSPORT,2.0/W.M.....EMISSIONS_POD..BULK_CARRIER+CHEM_TANKER+CONTAINER+GEN_CARGO+LIQ_GAS_TANKER+OIL_TANKER+OTHER_LIQ_TANKER+FERRY_PAX+CRUISE+FERRY_ROPAX+REFRIG_BULK+RO_RO+VEHICLE+YACHT+SERVICE_TUG+OFFSHORE+SERVICE_OTHER+MISC_FISH+MISC_OTHER.TER_DOM+TER_INT?dimensionAtObservation=AllDimensions"

HEADERS = {"Accept": "application/vnd.sdmx.data+json;version=1.0.0-wd"}


def fetch_world_data(timeout: int = 180, retries: int = 3) -> Optional[pd.DataFrame]:
    """Fetch World Total maritime emissions data."""
    
    for attempt in range(retries):
        try:
            print(f"\n📡 Fetching World Total Data (Attempt {attempt + 1}/{retries})...")
            print(f"   ⏱️  Timeout: {timeout} seconds")
            print(f"   Please wait...")
            
            response = requests.get(URL_WORLD, headers=HEADERS, timeout=timeout)
            
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
            df["Group"] = "World Total"
            
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
    print("FETCH WORLD TOTAL MARITIME EMISSIONS")
    print("="*70)
    
    world_df = fetch_world_data()
    
    if world_df is not None:
        # Display summary
        print(f"\n{'='*70}")
        print("WORLD TOTAL EMISSIONS - SUMMARY")
        print(f"{'='*70}")
        print(f"\n📊 Shape: {world_df.shape[0]} rows × {world_df.shape[1]} columns")
        print(f"\n📋 Columns: {list(world_df.columns)}")
        
        if 'CO2_Emissions' in world_df.columns:
            print(f"\n💨 Emissions Stats:")
            print(f"   Total: {world_df['CO2_Emissions'].sum():,.2f}")
            print(f"   Mean: {world_df['CO2_Emissions'].mean():,.2f}")
        
        print(f"\n🔍 Sample (first 10 rows):")
        print(world_df.head(10).to_string())
        
        # Save
        filename = "maritime_world_total.csv"
        world_df.to_csv(filename, index=False)
        print(f"\n✓ Saved to '{filename}'")
        
        print("\n" + "="*70)
        print("✓ SUCCESS!")
        print("="*70)
    else:
        print("\n✗ Failed to fetch World data")
        print("The OECD server might be overloaded. Try again later.")


if __name__ == "__main__":
    main()
