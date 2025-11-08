# Climate Analysis 🌍

A Python tool for fetching and analyzing climate data from the World Bank Climate Change Knowledge Portal API.

## Description

This project retrieves temperature anomaly data (1901-2024) from the World Bank's Climate Change Knowledge Portal and saves it for analysis. The data includes historical temperature measurements across global countries using the CRU TS4.09 dataset.

## Features

- ✅ Fetch climate data from World Bank API
- ✅ **Automatic update detection** - Only downloads when data changes
- ✅ **Smart caching** - Uses local data when up-to-date
- ✅ Display formatted data with metadata
- ✅ Save data to JSON file with timestamps
- ✅ **Scheduled updates** - Can run automatically via Task Scheduler
- ✅ Error handling for network issues
- ✅ Well-documented code with docstrings
- ✅ Data freshness tracking

## Requirements

- Python 3.7+
- requests library

## Installation

1. Clone this repository:
```bash
git clone https://github.com/Claire-Namusoke/Climate-Analysis.git
cd Climate-Analysis
```

2. Create a virtual environment (optional but recommended):
```bash
python -m venv .venv
.venv\Scripts\activate  # On Windows
# source .venv/bin/activate  # On macOS/Linux
```

3. Install required packages:
```bash
pip install requests
```

## Usage

### Basic Usage (Automatic Updates)

Run the main script - it automatically checks for updates:
```bash
python climate.py
```

The script will:
1. Check if local data exists and is up-to-date
2. Download new data ONLY if World Bank has updated their dataset
3. Display API metadata and sample country data
4. Save the complete dataset to `climate_data.json` with timestamps

**Smart Features:**
- ⚡ Fast - Uses cached data when available
- 🔄 Efficient - Only downloads when data actually changes
- 📅 Tracks - Shows when data was last fetched

### Manual Update

Force a fresh download even if data appears current:
```python
# Run the scheduler script
python scheduler.py
```

### Automated Scheduling

For automatic daily/weekly updates, see [AUTO_UPDATE_GUIDE.md](AUTO_UPDATE_GUIDE.md)

**Quick Setup (Windows):**
```bash
# Double-click update_climate.bat
# Or schedule it in Task Scheduler for automatic updates
```

## Output

The script creates a `climate_data.json` file containing:
- API metadata (version, status)
- Climate data for all countries
- Temperature measurements from 1901-2024

## API Information

**Data Source:** World Bank Climate Change Knowledge Portal  
**API Endpoint:** https://cckpapi.worldbank.org  
**Dataset:** CRU TS4.09 Temperature Anomaly Data  
**Time Period:** 1901-2024  
**Resolution:** Annual Mean  

## Project Structure

```
Climate-Analysis/
│
├── climate.py              # Main script with auto-update
├── scheduler.py            # Automated update scheduler
├── update_climate.bat      # Windows batch file for scheduling
├── climate_data.json       # Output data file (generated)
├── README.md              # Project documentation
├── AUTO_UPDATE_GUIDE.md   # Detailed auto-update setup guide
└── .venv/                 # Virtual environment (optional)
```

## Functions

### Core Functions

#### `fetch_climate_data(url)`
Fetches climate data from the API and captures metadata (timestamps, headers).

#### `check_for_updates(api_url, local_filename)`
Compares local data with API to detect if updates are available.

#### `auto_update_data(api_url, filename, force)`
Automatically updates local data only if API has newer information.

#### `load_local_data(filename)`
Loads previously saved climate data and metadata from JSON file.

#### `display_climate_data(climate_data)`
Displays formatted climate data including metadata and sample countries.

#### `save_data_to_file(climate_data, filename, metadata)`
Saves the fetched data to a JSON file with timestamps and metadata.

#### `calculate_data_hash(data)`
Generates a hash of the data to detect content changes.

#### `main()`
Orchestrates the entire workflow with automatic update checking.

## Author

**Claire Namusoke**  
Date: November 9, 2025

## License

This project is open source and available for educational purposes.

## Acknowledgments

- Data provided by the World Bank Climate Change Knowledge Portal
- CRU (Climatic Research Unit) for the temperature dataset
