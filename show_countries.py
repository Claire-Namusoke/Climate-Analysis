"""
Show Country Codes from Climate Data

Displays the first 10 country codes and attempts to identify the countries.
"""

import json

# Load the climate data
with open('climate_data.json', 'r') as f:
    data = json.load(f)

# Extract the actual climate data
climate_data = data.get('data', {}).get('data', {})

# Get all country codes
country_codes = list(climate_data.keys())

print("="*70)
print("COUNTRY CODES IN CLIMATE DATA")
print("="*70)
print(f"\nTotal countries/regions: {len(country_codes)}")
print(f"\n{'='*70}")
print("FIRST 10 COUNTRY CODES")
print(f"{'='*70}\n")

# Common country code mappings (ISO 3166-1 alpha-3)
country_names = {
    'ABW': 'Aruba',
    'AFG': 'Afghanistan',
    'AGO': 'Angola',
    'AIA': 'Anguilla',
    'ALA': 'Åland Islands',
    'ALB': 'Albania',
    'AND': 'Andorra',
    'ARE': 'United Arab Emirates',
    'ARG': 'Argentina',
    'ARM': 'Armenia',
    'ASM': 'American Samoa',
    'ATA': 'Antarctica',
    'ATF': 'French Southern Territories',
    'ATG': 'Antigua and Barbuda',
    'AUS': 'Australia',
    'AUT': 'Austria',
    'AZE': 'Azerbaijan',
    'BDI': 'Burundi',
    'BEL': 'Belgium',
    'BEN': 'Benin'
}

print(f"{'Code':<6} {'Country Name':<40}")
print("-" * 70)

for i, code in enumerate(country_codes[:10], 1):
    country_name = country_names.get(code, "Unknown")
    print(f"{code:<6} {country_name:<40}")

print(f"\n{'='*70}")
print(f"Note: These are ISO 3166-1 alpha-3 country codes")
print("="*70)
