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


def fetch_climate_data(url):
    """
    Fetch climate data from the World Bank Climate Change Knowledge Portal API.
    
    Args:
        url (str): API endpoint URL
        
    Returns:
        dict: JSON response data or None if request fails
    """
    try:
        print(f"Fetching data from: {url}")
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes
        
        data = response.json()
        print(f"✓ Successfully fetched data!")
        print(f"Number of countries: {len(data)}")
        
        return data
    
    except requests.exceptions.RequestException as e:
        print(f"✗ Error fetching data: {e}")
        return None


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


def save_data_to_file(climate_data, filename="climate_data.json"):
    """
    Save the fetched climate data to a JSON file for later analysis.
    
    Args:
        climate_data (dict): The climate data to save
        filename (str): Name of the output file (default: "climate_data.json")
        
    Returns:
        bool: True if save successful, False otherwise
    """
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(climate_data, f, indent=2, ensure_ascii=False)
        print(f"\n✓ Data saved to '{filename}'")
        return True
    except Exception as e:
        print(f"\n✗ Error saving data to file: {e}")
        return False


def main():
    """
    Main function for climate data analysis.
    
    This function orchestrates the entire workflow:
    1. Defines the API endpoint
    2. Fetches climate data from the World Bank API
    3. Displays the retrieved data
    4. Saves the data to a JSON file for future reference
    """
    print("="*50)
    print("CLIMATE DATA ANALYSIS TOOL")
    print("="*50)
    
    # World Bank Climate Change Knowledge Portal API
    # Dataset: Temperature anomaly data (CRU TS4.09)
    # Period: 1901-2024 (annual mean)
    # Coverage: Global countries
    api_url = "https://cckpapi.worldbank.org/api/v1/cru-x0.5_timeseries_tas_timeseries_annual_1901-2024_mean_historical_cru_ts4.09_mean/global_countries?_format=json"
    
    # Step 1: Fetch the climate data from the API
    climate_data = fetch_climate_data(api_url)
    
    if climate_data:
        # Step 2: Display the fetched data
        display_climate_data(climate_data)
        
        # Step 3: Save data to file for future analysis
        save_data_to_file(climate_data)
        
        print("\n" + "="*50)
        print("✓ Process completed successfully!")
        print("="*50)
    else:
        print("\n✗ Failed to fetch climate data.")
        print("Please check your internet connection and API URL.")


if __name__ == "__main__":
    # Entry point: Execute main function when script is run directly
    main()
