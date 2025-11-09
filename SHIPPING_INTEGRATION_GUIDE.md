# Shipping Emissions Integration Guide 🚢🌍

## Overview

This guide explains how to integrate your CO2_Emissions_from-Shippping repository data with the Climate Analysis tool.

---

## What Was Added

### New Files

1. **`shipping_integration.py`** - Core integration module with:
   - `ShippingEmissionsAPI` - Fetches data from your GitHub repo
   - `ClimateShippingIntegrator` - Merges climate + shipping data
   - Correlation and analysis functions

2. **`integrated_analysis.py`** - Complete analysis script that:
   - Fetches climate data from World Bank
   - Fetches shipping data from your GitHub repo
   - Merges the datasets
   - Performs integrated analysis
   - Saves combined data to CSV and JSON

---

## Quick Start

### Step 1: Find Your Shipping Data File

First, you need to know the exact filename in your `CO2_Emissions_from-Shippping` repository.

**Common locations:**
- `emissions.csv`
- `data/emissions.csv`
- `shipping_emissions.csv`
- `CO2_emissions.csv`

### Step 2: Update the Filename

Edit `integrated_analysis.py` line ~48:

```python
# Change this line to match your actual filename:
shipping_file_path = "emissions.csv"  # UPDATE THIS
```

**Examples:**
```python
# If file is in root
shipping_file_path = "emissions.csv"

# If file is in a data folder
shipping_file_path = "data/emissions.csv"

# If file has different name
shipping_file_path = "shipping_CO2_data.csv"
```

### Step 3: Run the Integration

```bash
python integrated_analysis.py
```

---

## How It Works

### Data Flow

```
┌─────────────────────┐         ┌──────────────────────┐
│  World Bank API     │         │  Your GitHub Repo    │
│  (Climate Data)     │         │  (Shipping Emissions)│
└──────────┬──────────┘         └──────────┬───────────┘
           │                               │
           │ Fetch                 Fetch   │
           ↓                               ↓
    ┌────────────┐              ┌─────────────────┐
    │ climate.py │              │ shipping_       │
    │            │              │ integration.py  │
    └─────┬──────┘              └────────┬────────┘
          │                              │
          │                              │
          └──────────┬───────────────────┘
                     ↓
          ┌─────────────────────┐
          │ Merge by Country    │
          │ (ClimateShipping    │
          │  Integrator)        │
          └─────────┬───────────┘
                    ↓
          ┌──────────────────────┐
          │ Integrated Dataset   │
          │ • CSV output         │
          │ • JSON output        │
          │ • Analysis results   │
          └──────────────────────┘
```

---

## Expected Output

### Console Output

```
==================================================================
INTEGRATED CLIMATE & SHIPPING EMISSIONS ANALYSIS TOOL
==================================================================

📥 STEP 1: Fetching Climate Data...
----------------------------------------------------------------------
Checking for updates...
✓ Using existing local data (up to date)
✓ Climate data loaded (246 countries)

📥 STEP 2: Fetching Shipping Emissions Data...
----------------------------------------------------------------------
Fetching CSV: https://raw.githubusercontent.com/Claire-Namusoke/...
✓ Shipping data loaded (1500 rows)
  Columns: ['country', 'year', 'CO2_emissions', 'vessel_type', ...]

🔄 STEP 3: Integrating Datasets...
----------------------------------------------------------------------
✓ Integration successful!

📊 STEP 4: Analysis & Display...
----------------------------------------------------------------------
[Analysis results...]
```

### Output Files

1. **`integrated_climate_shipping.csv`**
   - Merged data in CSV format
   - Ready for Excel, Tableau, etc.

2. **`integrated_climate_shipping.json`**
   - Merged data in JSON format
   - Ready for web apps, APIs, etc.

3. **`climate_data.json`** (existing)
   - Raw climate data from World Bank

---

## Data Structure Examples

### Before Integration

**Climate Data (from World Bank):**
```json
{
  "ABW": {
    "1901-07": 28.22,
    "1902-07": 27.79,
    ...
  },
  "AFG": {
    "1901-07": 12.78,
    ...
  }
}
```

**Shipping Data (from your repo):**
```csv
country,year,CO2_emissions,vessel_type
USA,2020,150000,Container
CHN,2020,200000,Bulk
...
```

### After Integration

**Merged Data:**
```csv
country_code,1901-07,1902-07,...,country,year,CO2_emissions,vessel_type
USA,15.5,15.6,...,USA,2020,150000,Container
CHN,10.2,10.3,...,CHN,2020,200000,Bulk
...
```

---

## Common Issues & Solutions

### Issue 1: "Could not fetch shipping data"

**Problem:** File not found in GitHub repo

**Solutions:**
1. Check if repo is public
2. Verify exact filename and path
3. Look in repo on GitHub.com to confirm location
4. Update `shipping_file_path` in `integrated_analysis.py`

**Test manually:**
```python
from shipping_integration import ShippingEmissionsAPI

api = ShippingEmissionsAPI()
data = api.fetch_csv_data("YOUR_FILENAME.csv")
print(data.head() if data is not None else "Failed")
```

### Issue 2: "Cannot merge: Missing data"

**Problem:** Data structures don't match for merging

**Solution:** Check column names
```python
# In integrated_analysis.py, after loading data:
print("Climate columns:", list(climate_df.columns))
print("Shipping columns:", list(shipping_data.columns))

# Adjust merge columns accordingly
```

### Issue 3: Pandas not installed

**Solution:**
```bash
pip install pandas
```

---

## Customization Options

### 1. Change Merge Strategy

Edit `shipping_integration.py`, `merge_by_country()`:

```python
# Merge by country AND year
merged = pd.merge(
    climate_df, 
    shipping_data,
    left_on=['country_code', 'year'],
    right_on=['country', 'year'],
    how='inner'  # or 'outer', 'left', 'right'
)
```

### 2. Add Custom Analysis

Add to `integrated_analysis.py`:

```python
def custom_analysis(merged_data):
    """Your custom analysis functions"""
    # Calculate total emissions by country
    total_by_country = merged_data.groupby('country')['CO2_emissions'].sum()
    
    # Find correlations
    climate_col = 'temperature_1990'  # adjust to your columns
    shipping_col = 'CO2_emissions'
    
    correlation = merged_data[climate_col].corr(merged_data[shipping_col])
    print(f"Correlation: {correlation}")
    
    return total_by_country
```

### 3. Add Visualizations

Install matplotlib:
```bash
pip install matplotlib
```

Add to script:
```python
import matplotlib.pyplot as plt

def plot_emissions_vs_temperature(merged_data):
    plt.figure(figsize=(10, 6))
    plt.scatter(
        merged_data['temperature'],
        merged_data['CO2_emissions']
    )
    plt.xlabel('Temperature')
    plt.ylabel('CO2 Emissions')
    plt.title('Shipping Emissions vs Temperature')
    plt.savefig('emissions_vs_temp.png')
    print("✓ Plot saved to emissions_vs_temp.png")
```

---

## Next Steps

### Option 1: Basic Integration
```bash
# Just run it!
python integrated_analysis.py
```

### Option 2: Interactive Exploration
```python
# In Python console
from integrated_analysis import *
from shipping_integration import *

# Load both datasets
climate_data, _ = load_local_data("climate_data.json")
shipping_api = ShippingEmissionsAPI()
shipping_data = shipping_api.fetch_csv_data("YOUR_FILE.csv")

# Explore
print(shipping_data.head())
print(shipping_data.describe())
```

### Option 3: API Endpoint
Create a Flask API to serve integrated data (advanced)

---

## Questions to Help Configure

Please let me know:

1. **What's the exact filename** in your CO2_Emissions_from-Shippping repo?
   - Look at the repo on GitHub.com
   - Is it in the root or in a folder?

2. **What columns does your shipping data have?**
   - Country name/code?
   - Year/date?
   - Emission values?
   - Any other fields?

3. **How do you want to merge the data?**
   - By country only?
   - By country and year?
   - Something else?

4. **What analysis do you want to perform?**
   - Correlations?
   - Trends over time?
   - Country comparisons?
   - Visualizations?

---

**Once you provide these details, I can customize the integration perfectly for your needs!** 🎯
