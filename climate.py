"""
Climate Data Analysis Tool

This script fetches climate data from the World Bank Climate Change Knowledge Portal API
and provides basic analysis capabilities for temperature anomaly data (1901-2024).

Author: Claire Namusoke
Date: November 9, 2025
API Source: World Bank Climate Change Knowledge Portal
"""

import requests
import json
import os
from datetime import datetime
import hashlib


def fetch_climate_data(url):
    """
    Fetch climate data from the World Bank Climate Change Knowledge Portal API.
    
    Args:
        url (str): API endpoint URL
        
    Returns:
        tuple: (data dict, metadata dict) - JSON response data and HTTP headers,
               or (None, None) if request fails
    """
    try:
        print(f"Fetching data from: {url}")
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes
        
        data = response.json()
        
        # Extract useful metadata from HTTP headers
        metadata = {
            'last_modified': response.headers.get('Last-Modified'),
            'etag': response.headers.get('ETag'),
            'content_length': response.headers.get('Content-Length'),
            'fetch_timestamp': datetime.now().isoformat(),
            'status_code': response.status_code
        }
        
        print(f"✓ Successfully fetched data!")
        print(f"Number of top-level keys: {len(data)}")
        if metadata['last_modified']:
            print(f"Data last modified: {metadata['last_modified']}")
        
        return data, metadata
    
    except requests.exceptions.RequestException as e:
        print(f"✗ Error fetching data: {e}")
        return None, None


def display_climate_data(climate_data):
    """
    Display formatted climate data retrieved from the API.
    
    This function parses and displays the structure of the climate data,
    including metadata and sample country information.
    
    Args:
        climate_data (dict): The climate data dictionary returned from the API
        
    Returns:
        None
    """
    if not climate_data:
        print("No data to display.")
        return
    
    # Display API metadata if available
    if 'metadata' in climate_data:
        print("\n" + "="*50)
        print("API METADATA")
        print("="*50)
        metadata = climate_data['metadata']
        print(f"API Version: {metadata.get('apiVersion', 'N/A')}")
        print(f"Status: {metadata.get('status', 'N/A')}")
        
        # Display any messages from the API
        messages = metadata.get('messages', [])
        if messages:
            print(f"Messages: {', '.join(messages)}")
    
    # Display actual climate data if available
    if 'data' in climate_data:
        data = climate_data['data']
        
        print("\n" + "="*50)
        print("CLIMATE DATA")
        print("="*50)
        print(f"Total countries/regions: {len(data)}")
        
        # Show first few countries as examples
        country_keys = list(data.keys())[:3]  # Display first 3 countries
        
        print("\n--- Sample Countries ---")
        for country_code in country_keys:
            country_data = data[country_code]
            print(f"\n{country_code}:")
            
            if isinstance(country_data, dict):
                # Display the data structure for each country
                for key, value in list(country_data.items())[:5]:  # First 5 items
                    if isinstance(value, list):
                        print(f"  • {key}: [{len(value)} values]")
                        # Show a sample of the list data
                        if len(value) > 0:
                            print(f"    Sample: {value[:3]}...")
                    else:
                        print(f"  • {key}: {value}")
    else:
        # If data structure is different, show the raw response (truncated)
        print("\n" + "="*50)
        print("RAW RESPONSE (TRUNCATED)")
        print("="*50)
        print(json.dumps(climate_data, indent=2)[:500])


def save_data_to_file(climate_data, filename="climate_data.json", metadata=None):
    """
    Save the fetched climate data to a JSON file for later analysis.
    
    Args:
        climate_data (dict): The climate data to save
        filename (str): Name of the output file (default: "climate_data.json")
        metadata (dict): Optional metadata about the fetch (timestamps, headers, etc.)
        
    Returns:
        bool: True if save successful, False otherwise
    """
    try:
        # Create a combined data structure with metadata
        output_data = {
            'data': climate_data,
            'metadata': metadata or {},
            'local_save_timestamp': datetime.now().isoformat()
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)
        print(f"\n✓ Data saved to '{filename}'")
        return True
    except Exception as e:
        print(f"\n✗ Error saving data to file: {e}")
        return False


def load_local_data(filename="climate_data.json"):
    """
    Load previously saved climate data from a JSON file.
    
    Args:
        filename (str): Name of the file to load from
        
    Returns:
        tuple: (data dict, metadata dict) or (None, None) if file doesn't exist or error
    """
    try:
        if not os.path.exists(filename):
            print(f"ℹ No local data file found: '{filename}'")
            return None, None
        
        with open(filename, 'r', encoding='utf-8') as f:
            file_content = json.load(f)
        
        # Handle both old format (direct data) and new format (with metadata)
        if 'data' in file_content and 'metadata' in file_content:
            return file_content['data'], file_content['metadata']
        else:
            # Old format - just the data
            return file_content, {}
    
    except Exception as e:
        print(f"✗ Error loading local data: {e}")
        return None, None


def calculate_data_hash(data):
    """
    Calculate a hash of the data to detect changes.
    
    Args:
        data (dict): The data to hash
        
    Returns:
        str: SHA256 hash of the data
    """
    # Convert dict to sorted JSON string for consistent hashing
    data_str = json.dumps(data, sort_keys=True)
    return hashlib.sha256(data_str.encode()).hexdigest()


def check_for_updates(api_url, local_filename="climate_data.json"):
    """
    Check if the API has newer data than what's stored locally.
    
    Args:
        api_url (str): The API endpoint URL
        local_filename (str): Path to local data file
        
    Returns:
        tuple: (needs_update: bool, reason: str)
    """
    # Load local data
    local_data, local_metadata = load_local_data(local_filename)
    
    if local_data is None:
        return True, "No local data found"
    
    # Make a HEAD request to check if data has changed (faster than full GET)
    try:
        print("\nChecking for updates...")
        response = requests.head(api_url)
        
        # Check Last-Modified header
        api_last_modified = response.headers.get('Last-Modified')
        local_last_modified = local_metadata.get('last_modified')
        
        if api_last_modified and local_last_modified:
            if api_last_modified != local_last_modified:
                return True, f"API data updated: {api_last_modified}"
        
        # Check ETag (if available)
        api_etag = response.headers.get('ETag')
        local_etag = local_metadata.get('etag')
        
        if api_etag and local_etag and api_etag != local_etag:
            return True, "API data changed (ETag mismatch)"
        
        # If no headers available, fetch and compare data hashes
        if not api_last_modified and not api_etag:
            print("Server doesn't provide update headers. Comparing data...")
            new_data, _ = fetch_climate_data(api_url)
            if new_data:
                local_hash = calculate_data_hash(local_data)
                new_hash = calculate_data_hash(new_data)
                if local_hash != new_hash:
                    return True, "Data content has changed"
        
        return False, "Local data is up to date"
    
    except Exception as e:
        print(f"⚠ Could not check for updates: {e}")
        return True, "Unable to verify - will update to be safe"


def auto_update_data(api_url, filename="climate_data.json", force=False):
    """
    Automatically update local data if API has newer information.
    
    Args:
        api_url (str): The API endpoint URL
        filename (str): Local data file path
        force (bool): Force update even if data appears current
        
    Returns:
        bool: True if data was updated, False otherwise
    """
    if not force:
        needs_update, reason = check_for_updates(api_url, filename)
        print(f"Update check: {reason}")
        
        if not needs_update:
            print("✓ Using existing local data (up to date)")
            return False
    
    print("\n🔄 Updating data from API...")
    climate_data, metadata = fetch_climate_data(api_url)
    
    if climate_data:
        save_data_to_file(climate_data, filename, metadata)
        print("✓ Data updated successfully!")
        return True
    else:
        print("✗ Update failed")
        return False


def main():
    """
    Main function for climate data analysis.
    
    This function orchestrates the entire workflow:
    1. Defines the API endpoint
    2. Checks if local data needs updating
    3. Fetches new data from the World Bank API if needed
    4. Displays the retrieved data
    5. Ensures data is saved locally for future use
    """
    print("="*50)
    print("CLIMATE DATA ANALYSIS TOOL")
    print("="*50)
    
    # World Bank Climate Change Knowledge Portal API
    # Dataset: Temperature anomaly data (CRU TS4.09)
    # Period: 1901-2024 (annual mean)
    # Coverage: Global countries
    api_url = "https://cckpapi.worldbank.org/api/v1/cru-x0.5_timeseries_tas_timeseries_annual_1901-2024_mean_historical_cru_ts4.09_mean/global_countries?_format=json"
    data_file = "climate_data.json"
    
    # Step 1: Automatically check for updates and fetch if needed
    updated = auto_update_data(api_url, data_file, force=False)
    
    # Step 2: Load the data (either newly fetched or existing)
    climate_data, metadata = load_local_data(data_file)
    
    if climate_data:
        # Step 3: Display the data
        display_climate_data(climate_data)
        
        # Display freshness information
        if metadata:
            print("\n" + "="*50)
            print("DATA FRESHNESS")
            print("="*50)
            if 'fetch_timestamp' in metadata:
                print(f"Last fetched: {metadata['fetch_timestamp']}")
            if 'last_modified' in metadata and metadata['last_modified']:
                print(f"API last modified: {metadata['last_modified']}")
        
        print("\n" + "="*50)
        if updated:
            print("✓ Process completed! Data was updated from API.")
        else:
            print("✓ Process completed! Using existing data.")
        print("="*50)
    else:
        print("\n✗ Failed to load climate data.")
        print("Please check your internet connection and try again.")


if __name__ == "__main__":
    # Entry point: Execute main function when script is run directly
    main()
