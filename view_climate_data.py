"""
View Climate Data in Table Format

Displays the first 20 rows of climate data from climate_data.json
"""

import json
import pandas as pd

# Load the climate data
with open('climate_data.json', 'r') as f:
    data = json.load(f)

# Extract the actual climate data (skip metadata like 'status', 'api_version')
climate_data = data.get('data', {}).get('data', {})

# Flatten the nested structure into rows
rows = []
for country_code, country_data in climate_data.items():
    if isinstance(country_data, dict):
        for date, temp in country_data.items():
            rows.append({
                'Country_Code': country_code,
                'Date': date,
                'Temperature': temp
            })

# Create DataFrame
df = pd.DataFrame(rows)

# Sort by country and date
df = df.sort_values(['Country_Code', 'Date'])

print("="*70)
print("WORLD BANK CLIMATE DATA - FIRST 20 ROWS")
print("="*70)
print(f"\nTotal records: {len(df):,}")
print(f"Countries: {df['Country_Code'].nunique()}")
print(f"Date range: {df['Date'].min()} to {df['Date'].max()}")
print(f"\n{'='*70}")
print("FIRST 20 ROWS")
print(f"{'='*70}\n")

# Display first 20 rows
print(df.head(20).to_string(index=False))

print(f"\n{'='*70}")
print(f"✓ Showing 20 of {len(df):,} total rows")
print("="*70)
