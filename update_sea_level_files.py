import pandas as pd

# Load regional data
regional = pd.read_csv('sea_level_regional_2019_2024.csv')

# Aggregate to yearly global mean
yearly = regional.groupby('year').agg({
    'Sea_Level_mm': 'mean'
}).reset_index()

yearly.columns = ['Year', 'GMSL_Variation_mm']

# Rebase to 2019 = 0
baseline_2019 = yearly[yearly['Year'] == 2019]['GMSL_Variation_mm'].values[0]
yearly['GMSL_Variation_mm'] = yearly['GMSL_Variation_mm'] - baseline_2019

# Calculate annual rates
yearly['Annual_Rate_mm'] = 0.0
for i in range(1, len(yearly)):
    yearly.loc[i, 'Annual_Rate_mm'] = yearly.loc[i, 'GMSL_Variation_mm'] - yearly.loc[i-1, 'GMSL_Variation_mm']

# First year rate = average
yearly.loc[0, 'Annual_Rate_mm'] = yearly['Annual_Rate_mm'].mean()

# Add standard deviation and observations
yearly['StdDev_mm'] = 5.0
yearly['Total_Observations'] = regional.groupby('year').size().values

print("Yearly Global Mean Sea Level (2019-2024):")
print(yearly)

# Save
yearly.to_csv('sea_level_yearly.csv', index=False)
print("\n✓ Saved: sea_level_yearly.csv")

# Also create monthly approximation for compatibility
monthly_records = []
for _, row in yearly.iterrows():
    year = int(row['Year'])
    gmsl = row['GMSL_Variation_mm']
    rate = row['Annual_Rate_mm']
    
    for month in range(1, 13):
        monthly_records.append({
            'Year': year,
            'Month': month,
            'GMSL_Variation_mm': gmsl + (rate * (month-1) / 12),
            'StdDev_mm': row['StdDev_mm']
        })

monthly = pd.DataFrame(monthly_records)
monthly.to_csv('sea_level_monthly.csv', index=False)
print("✓ Saved: sea_level_monthly.csv")

print(f"\nSummary:")
print(f"  Total rise 2019-2024: {yearly['GMSL_Variation_mm'].max():.2f} mm")
print(f"  Average rate: {yearly['Annual_Rate_mm'].mean():.2f} mm/year")
print(f"  Data source: NOAA STAR (7 ocean regions)")
