"""
Climate Data Scheduler

This script can be scheduled to run automatically (e.g., daily, weekly)
to keep your climate data up-to-date with the World Bank API.

You can set this up using:
- Windows Task Scheduler (Windows)
- Cron (Linux/Mac)
- Or run it manually whenever you want fresh data
"""

import sys
import os
from datetime import datetime

# Add the current directory to the path to import climate module
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import functions from the main climate.py module
from climate import auto_update_data, load_local_data, display_climate_data


def scheduled_update():
    """
    Perform a scheduled update of climate data.
    This function is designed to be called by task schedulers.
    """
    print("="*60)
    print(f"SCHEDULED CLIMATE DATA UPDATE - {datetime.now()}")
    print("="*60)
    
    # API endpoint
    api_url = "https://cckpapi.worldbank.org/api/v1/cru-x0.5_timeseries_tas_timeseries_annual_1901-2024_mean_historical_cru_ts4.09_mean/global_countries?_format=json"
    data_file = "climate_data.json"
    
    # Attempt to update
    try:
        updated = auto_update_data(api_url, data_file, force=False)
        
        if updated:
            print("\n✅ SUCCESS: Climate data has been updated!")
            
            # Optionally display summary
            climate_data, metadata = load_local_data(data_file)
            if climate_data and 'data' in climate_data:
                data_section = climate_data['data']
                print(f"\nTotal countries in dataset: {len(data_section)}")
                if metadata and 'fetch_timestamp' in metadata:
                    print(f"Update timestamp: {metadata['fetch_timestamp']}")
        else:
            print("\n✅ SUCCESS: Data is already up-to-date. No update needed.")
        
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR: Failed to update climate data: {e}")
        return False


if __name__ == "__main__":
    """
    Run the scheduled update.
    Exit with code 0 on success, 1 on failure (useful for schedulers).
    """
    success = scheduled_update()
    sys.exit(0 if success else 1)
