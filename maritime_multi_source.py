"""
Multi-Source Maritime Emissions Integration

This module fetches data from multiple OECD Maritime emissions URLs
and integrates them with climate data for comprehensive analysis.

Author: Claire Namusoke
Date: November 9, 2025
"""

import requests
import pandas as pd
import json
from typing import List, Dict, Optional, Tuple
from datetime import datetime


class OECDMaritimeAPI:
    """
    Handler for fetching OECD Maritime CO2 emissions data from multiple sources.
    """
    
    def __init__(self):
        """Initialize the OECD Maritime API handler."""
        self.data_sources = {}
        self.fetched_data = {}
    
    def add_data_source(self, name: str, url: str, description: str = ""):
        """
        Add a data source URL.
        
        Args:
            name (str): Identifier for this data source
            url (str): URL to fetch data from
            description (str): Description of what this data contains
        """
        self.data_sources[name] = {
            'url': url,
            'description': description
        }
        print(f"✓ Added data source: {name}")
        if description:
            print(f"  Description: {description}")
    
    def fetch_from_url(self, url: str, format_type: str = 'auto') -> Optional[pd.DataFrame]:
        """
        Fetch data from a URL and parse it.
        
        Args:
            url (str): URL to fetch from
            format_type (str): 'csv', 'json', or 'auto' to detect
            
        Returns:
            DataFrame: Parsed data or None if error
        """
        try:
            print(f"\nFetching from: {url[:80]}...")
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            
            # Auto-detect format
            if format_type == 'auto':
                content_type = response.headers.get('Content-Type', '').lower()
                if 'json' in content_type or url.endswith('.json'):
                    format_type = 'json'
                elif 'csv' in content_type or url.endswith('.csv'):
                    format_type = 'csv'
                else:
                    # Try to detect from content
                    try:
                        json.loads(response.text)
                        format_type = 'json'
                    except:
                        format_type = 'csv'
            
            # Parse based on format
            if format_type == 'json':
                data = response.json()
                
                # Handle different JSON structures
                if isinstance(data, list):
                    df = pd.DataFrame(data)
                elif isinstance(data, dict):
                    # Check for common data keys
                    if 'data' in data:
                        df = pd.DataFrame(data['data'])
                    elif 'results' in data:
                        df = pd.DataFrame(data['results'])
                    elif 'records' in data:
                        df = pd.DataFrame(data['records'])
                    else:
                        # Try to convert dict to DataFrame
                        df = pd.DataFrame([data])
                else:
                    print("✗ Unknown JSON structure")
                    return None
                    
            else:  # CSV
                from io import StringIO
                df = pd.read_csv(StringIO(response.text))
            
            print(f"✓ Successfully fetched data: {len(df)} rows, {len(df.columns)} columns")
            print(f"  Columns: {list(df.columns)[:5]}{'...' if len(df.columns) > 5 else ''}")
            
            return df
            
        except requests.exceptions.RequestException as e:
            print(f"✗ Network error: {e}")
            return None
        except Exception as e:
            print(f"✗ Error parsing data: {e}")
            return None
    
    def fetch_all_sources(self) -> Dict[str, pd.DataFrame]:
        """
        Fetch data from all registered sources.
        
        Returns:
            dict: Dictionary mapping source names to DataFrames
        """
        print("="*70)
        print("FETCHING DATA FROM ALL SOURCES")
        print("="*70)
        
        results = {}
        
        for name, source in self.data_sources.items():
            print(f"\n📊 Source: {name}")
            if source['description']:
                print(f"   {source['description']}")
            
            df = self.fetch_from_url(source['url'])
            if df is not None:
                results[name] = df
                self.fetched_data[name] = df
            else:
                print(f"⚠️  Failed to fetch {name}")
        
        print("\n" + "="*70)
        print(f"✓ Successfully fetched {len(results)}/{len(self.data_sources)} sources")
        print("="*70)
        
        return results
    
    def combine_sources(self, sources: Dict[str, pd.DataFrame], 
                       merge_on: List[str] = None,
                       merge_type: str = 'outer') -> Optional[pd.DataFrame]:
        """
        Combine multiple data sources into one DataFrame.
        
        Args:
            sources (dict): Dictionary of source name -> DataFrame
            merge_on (list): Columns to merge on (e.g., ['Country', 'Year'])
            merge_type (str): 'inner', 'outer', 'left', 'right'
            
        Returns:
            DataFrame: Combined data
        """
        if not sources:
            print("✗ No sources to combine")
            return None
        
        source_names = list(sources.keys())
        
        if len(sources) == 1:
            print(f"ℹ Only one source available: {source_names[0]}")
            return sources[source_names[0]]
        
        print(f"\n🔄 Combining {len(sources)} data sources...")
        
        # Start with first source
        combined = sources[source_names[0]].copy()
        combined['source'] = source_names[0]
        
        # If no merge columns specified, concatenate vertically
        if merge_on is None:
            for name in source_names[1:]:
                df = sources[name].copy()
                df['source'] = name
                combined = pd.concat([combined, df], ignore_index=True, sort=False)
            
            print(f"✓ Concatenated {len(sources)} sources: {len(combined)} total rows")
        else:
            # Merge on specified columns
            for name in source_names[1:]:
                df = sources[name].copy()
                combined = pd.merge(
                    combined, df, 
                    on=merge_on, 
                    how=merge_type,
                    suffixes=('', f'_{name}')
                )
            
            print(f"✓ Merged {len(sources)} sources on {merge_on}: {len(combined)} rows")
        
        return combined


class MultiSourceClimateIntegrator:
    """
    Integrates climate data with multiple maritime emissions sources.
    """
    
    def __init__(self, climate_data: Dict, maritime_data: Dict[str, pd.DataFrame]):
        """
        Initialize with climate and maritime data.
        
        Args:
            climate_data (dict): Climate data from World Bank
            maritime_data (dict): Dictionary of maritime data sources
        """
        self.climate_data = climate_data
        self.maritime_data = maritime_data
    
    def integrate_all(self, country_column: str = 'Country') -> pd.DataFrame:
        """
        Integrate climate data with all maritime sources.
        
        Args:
            country_column (str): Column name for country in maritime data
            
        Returns:
            DataFrame: Integrated dataset
        """
        print("\n" + "="*70)
        print("INTEGRATING CLIMATE + MARITIME EMISSIONS DATA")
        print("="*70)
        
        # Convert climate data to DataFrame
        climate_df = self._climate_to_dataframe()
        
        if climate_df is None:
            print("✗ Could not process climate data")
            return None
        
        print(f"\n📊 Climate data: {len(climate_df)} countries")
        
        # Combine all maritime sources
        api = OECDMaritimeAPI()
        combined_maritime = api.combine_sources(self.maritime_data)
        
        if combined_maritime is None:
            print("✗ Could not combine maritime data")
            return None
        
        print(f"📊 Maritime data: {len(combined_maritime)} records")
        
        # Merge datasets
        print(f"\n🔄 Merging on country codes...")
        
        # Try different merge strategies
        merged = None
        
        # Strategy 1: Direct merge on country code
        if country_column in combined_maritime.columns:
            merged = pd.merge(
                climate_df,
                combined_maritime,
                left_on='country_code',
                right_on=country_column,
                how='outer'
            )
        
        if merged is not None:
            print(f"✓ Integration complete: {len(merged)} rows")
            return merged
        else:
            print("⚠️  Could not merge - column names may not match")
            print(f"   Climate columns: {list(climate_df.columns)[:5]}")
            print(f"   Maritime columns: {list(combined_maritime.columns)[:5]}")
            return combined_maritime
    
    def _climate_to_dataframe(self) -> Optional[pd.DataFrame]:
        """Convert climate data to DataFrame."""
        try:
            if 'data' in self.climate_data and 'data' in self.climate_data['data']:
                data_section = self.climate_data['data']['data']
            elif 'data' in self.climate_data:
                data_section = self.climate_data['data']
            else:
                data_section = self.climate_data
            
            records = []
            for country_code, values in data_section.items():
                record = {'country_code': country_code}
                if isinstance(values, dict):
                    record.update(values)
                records.append(record)
            
            return pd.DataFrame(records)
        except Exception as e:
            print(f"✗ Error converting climate data: {e}")
            return None


def save_integrated_data(data: pd.DataFrame, prefix: str = "integrated"):
    """
    Save integrated data to multiple formats.
    
    Args:
        data (DataFrame): Data to save
        prefix (str): Filename prefix
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # CSV
    csv_file = f"{prefix}_{timestamp}.csv"
    data.to_csv(csv_file, index=False)
    print(f"✓ Saved CSV: {csv_file}")
    
    # JSON
    json_file = f"{prefix}_{timestamp}.json"
    data.to_json(json_file, orient='records', indent=2)
    print(f"✓ Saved JSON: {json_file}")
    
    # Excel (if openpyxl available)
    try:
        excel_file = f"{prefix}_{timestamp}.xlsx"
        data.to_excel(excel_file, index=False)
        print(f"✓ Saved Excel: {excel_file}")
    except ImportError:
        print("ℹ Excel export skipped (install openpyxl for Excel support)")


if __name__ == "__main__":
    print("Multi-Source Maritime Emissions Integration Module")
    print("\nExample usage:")
    print("""
    # Setup
    api = OECDMaritimeAPI()
    
    # Add your data sources
    api.add_data_source(
        'table1', 
        'YOUR_URL_1_HERE',
        'Description of first dataset'
    )
    api.add_data_source(
        'table2',
        'YOUR_URL_2_HERE', 
        'Description of second dataset'
    )
    
    # Fetch all data
    data = api.fetch_all_sources()
    
    # Combine and analyze
    combined = api.combine_sources(data)
    """)
