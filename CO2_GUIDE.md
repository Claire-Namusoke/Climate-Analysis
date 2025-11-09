# CO2.py - OECD Maritime Emissions Guide 🚢

## Overview

`CO2.py` fetches CO2 emissions data from OECD's maritime transport database via their SDMX-JSON API.

---

## What It Does

### Data Sources

**1. World Total Data**
- Global maritime CO2 emissions
- All vessel types combined
- Domestic and international territories

**2. OECD Countries Data**
- Individual country emissions
- 38 OECD member countries
- Same vessel types and territories

### Vessel Types Included

- Bulk Carrier
- Chemical Tanker
- Container Ship
- General Cargo
- Liquefied Gas Tanker
- Oil Tanker
- Other Liquid Tanker
- Ferry (Passenger)
- Cruise Ship
- Ferry (RoRo/Pax)
- Refrigerated Bulk
- Roll-on/Roll-off
- Vehicle Carrier
- Yacht
- Service Tug
- Offshore Vessel
- Other Service
- Fishing Vessel
- Other Miscellaneous

---

## How to Use

### Basic Usage

```bash
python CO2.py
```

The script will:
1. ✅ Fetch World Total emissions data
2. ✅ Fetch OECD Countries emissions data
3. ✅ Process and clean the data
4. ✅ Save to CSV and JSON formats
5. ✅ Create a combined dataset

### Output Files

After running, you'll get 6 files:

**Individual Datasets:**
- `maritime_world_total.csv` - World data (CSV)
- `maritime_world_total.json` - World data (JSON)
- `maritime_oecd_countries.csv` - OECD countries (CSV)
- `maritime_oecd_countries.json` - OECD countries (JSON)

**Combined Dataset:**
- `maritime_emissions_combined.csv` - Both datasets (CSV)
- `maritime_emissions_combined.json` - Both datasets (JSON)

---

## Data Structure

### Columns

Each dataset contains these columns:

| Column | Description | Example |
|--------|-------------|---------|
| `REF_AREA` | Country/Region code | "USA", "W" (World) |
| `FREQ` | Frequency | "M" (Monthly) |
| `MEASURE` | Measurement type | "EMISSIONS_POD" |
| `SHIP_TYPE` | Type of vessel | "CONTAINER", "OIL_TANKER" |
| `TERRITORY` | Territory type | "TER_DOM", "TER_INT" |
| `TIME_PERIOD` | Year-Month | "2020-01" |
| `CO2_Emissions` | Emissions value | 1234567.89 |
| `Group` | Data source | "World Total", "OECD Country" |

### Sample Data

```csv
REF_AREA,FREQ,MEASURE,SHIP_TYPE,TERRITORY,TIME_PERIOD,CO2_Emissions,Group
W,M,EMISSIONS_POD,CONTAINER,TER_INT,2020-01,5234567.89,World Total
USA,M,EMISSIONS_POD,OIL_TANKER,TER_DOM,2020-01,123456.78,OECD Country
```

---

## Features

### Smart Fetching
- ⏱️ Longer timeout (120 seconds) for large datasets
- 🔄 Automatic retry on failure (3 attempts)
- 📊 Progress indicators
- 💾 Automatic data processing

### Error Handling
- Network timeout recovery
- HTTP error handling
- JSON parsing validation
- Detailed error messages

### Data Processing
- Converts complex SDMX-JSON to flat structure
- Adds group identifiers
- Creates multiple export formats
- Validates data integrity

---

## Troubleshooting

### Issue: "Request timed out"

**Solution:** The OECD API has large datasets. The script automatically retries with longer timeouts.

If still failing:
1. Check internet connection
2. Try running during off-peak hours
3. The script will retry 3 times automatically

### Issue: "Network error"

**Solution:**
1. Verify internet connection
2. Check if OECD website is accessible: https://sdmx.oecd.org
3. Try again in a few minutes

### Issue: "Data structure error"

**Solution:** OECD may have changed their API structure.
- Check OECD API documentation
- Report issue with error details

---

## Integration with Climate Data

Once you have the maritime emissions data, you can integrate it with climate data using:

```python
# Load both datasets
from CO2 import fetch_all_maritime_data
from climate import load_local_data

# Get maritime data
world_df, oecd_df = fetch_all_maritime_data()

# Get climate data
climate_data, _ = load_local_data("climate_data.json")

# Now you can analyze both together!
```

---

## Advanced Usage

### Fetch Only World Data

```python
from CO2 import fetch_sdmx_to_dataframe, URL_WORLD

world_df = fetch_sdmx_to_dataframe(URL_WORLD)
```

### Fetch Only OECD Data

```python
from CO2 import fetch_sdmx_to_dataframe, URL_OECD

oecd_df = fetch_sdmx_to_dataframe(URL_OECD)
```

### Custom Analysis

```python
import pandas as pd

# Load data
df = pd.read_csv("maritime_emissions_combined.csv")

# Analyze by vessel type
by_ship = df.groupby('SHIP_TYPE')['CO2_Emissions'].sum().sort_values(ascending=False)
print(by_ship)

# Analyze by country
by_country = df[df['Group'] == 'OECD Country'].groupby('REF_AREA')['CO2_Emissions'].sum()
print(by_country)

# Time series analysis
df['TIME_PERIOD'] = pd.to_datetime(df['TIME_PERIOD'])
time_series = df.groupby('TIME_PERIOD')['CO2_Emissions'].sum()
time_series.plot()
```

---

## Data Freshness

### When to Re-run

- **Monthly**: OECD updates maritime data monthly
- **After Major Events**: New regulations, policy changes
- **On Demand**: When you need fresh data

### Automated Updates

To schedule automatic updates, use Windows Task Scheduler with `CO2.py`:

```batch
cd C:\Users\clair\OneDrive\OfficeMobile\Desktop\Climate-Analysis
.venv\Scripts\python.exe CO2.py
```

---

## Performance

### Typical Execution Time

- **World Data**: 30-90 seconds
- **OECD Data**: 30-90 seconds
- **Total**: 1-3 minutes

Depends on:
- Internet speed
- OECD server load
- Dataset size

### Data Size

- **World Data**: ~10,000-50,000 observations
- **OECD Data**: ~100,000-500,000 observations
- **Output Files**: 5-50 MB total

---

## API Information

**Data Source:** OECD Statistical Database  
**API Type:** SDMX-JSON (Statistical Data and Metadata eXchange)  
**Format Version:** 1.0.0-wd  
**Update Frequency:** Monthly  
**Coverage:** 1995 - Present  

**Official Documentation:**
- OECD SDMX API: https://data.oecd.org/api/
- Maritime Transport Data: https://stats.oecd.org

---

## Next Steps

1. ✅ Run `CO2.py` to fetch data
2. ✅ Verify output files are created
3. ✅ Open CSV in Excel to explore
4. ⬜ Integrate with `climate.py`
5. ⬜ Create visualizations
6. ⬜ Perform analysis

---

## Questions?

**Common Questions:**

**Q: How often should I update the data?**  
A: Monthly or whenever you need fresh data for analysis.

**Q: Can I modify the vessel types?**  
A: Yes! Edit the URL parameters in `CO2.py` to include/exclude types.

**Q: Can I get data for non-OECD countries?**  
A: The API mainly covers OECD members. Check OECD documentation for coverage.

**Q: How do I combine this with climate data?**  
A: See `integrated_analysis.py` for combining both datasets.

---

**Your maritime emissions data is now ready for analysis!** 🚢💨📊
