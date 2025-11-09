"""
View Maritime CO2 Emissions Data

Displays sample rows from the OECD maritime emissions tables.
"""

import pandas as pd

print("="*80)
print("MARITIME WORLD TOTAL - FIRST 20 ROWS")
print("="*80)

# Load World Total data
world_df = pd.read_csv('maritime_world_total.csv')

print(f"\n📊 Dataset Info:")
print(f"   Total rows: {len(world_df):,}")
print(f"   Columns: {len(world_df.columns)}")
print(f"   Time period: {world_df['TIME_PERIOD'].min()} to {world_df['TIME_PERIOD'].max()}")

print(f"\n🚢 Vessel Types:")
vessel_types = world_df['VESSEL'].unique()
print(f"   {', '.join(vessel_types[:10])}")
if len(vessel_types) > 10:
    print(f"   ... and {len(vessel_types) - 10} more")

print(f"\n💨 Total CO2 Emissions: {world_df['CO2_Emissions'].sum():,.0f} tonnes")

print(f"\n📋 First 20 Rows:")
print(world_df.head(20).to_string(index=True))

print("\n" + "="*80)
print("MARITIME OECD COUNTRIES - FIRST 20 ROWS")
print("="*80)

# Load OECD Countries data
oecd_df = pd.read_csv('maritime_oecd_countries.csv')

print(f"\n📊 Dataset Info:")
print(f"   Total rows: {len(oecd_df):,}")
print(f"   Columns: {len(oecd_df.columns)}")
print(f"   Time period: {oecd_df['TIME_PERIOD'].min()} to {oecd_df['TIME_PERIOD'].max()}")

print(f"\n🌍 Countries/Regions:")
countries = oecd_df['REF_AREA'].unique()
print(f"   {', '.join(countries)}")

print(f"\n💨 Total CO2 Emissions: {oecd_df['CO2_Emissions'].sum():,.0f} tonnes")

print(f"\n📋 First 20 Rows:")
print(oecd_df.head(20).to_string(index=True))

print("\n" + "="*80)
print("SUMMARY STATISTICS")
print("="*80)

print(f"\n🌍 World Total:")
print(f"   Average monthly emissions: {world_df['CO2_Emissions'].mean():,.0f} tonnes")
print(f"   Highest single record: {world_df['CO2_Emissions'].max():,.0f} tonnes")
print(f"   Lowest single record: {world_df['CO2_Emissions'].min():,.0f} tonnes")

print(f"\n🏢 OECD Countries:")
print(f"   Average monthly emissions: {oecd_df['CO2_Emissions'].mean():,.0f} tonnes")
print(f"   Highest single record: {oecd_df['CO2_Emissions'].max():,.0f} tonnes")
print(f"   Lowest single record: {oecd_df['CO2_Emissions'].min():,.0f} tonnes")

# Top 5 vessel types by emissions
print(f"\n🚢 Top 5 Vessel Types by Total Emissions (World):")
top_vessels = world_df.groupby('VESSEL')['CO2_Emissions'].sum().nlargest(5)
for i, (vessel, emissions) in enumerate(top_vessels.items(), 1):
    print(f"   {i}. {vessel}: {emissions:,.0f} tonnes")

print("\n" + "="*80)
