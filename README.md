# Climate Analysis 🌍

A Python tool for fetching and analyzing climate data from the World Bank Climate Change Knowledge Portal API.

## Description

This project retrieves temperature anomaly data (1901-2024) from the World Bank's Climate Change Knowledge Portal and saves it for analysis. The data includes historical temperature measurements across global countries using the CRU TS4.09 dataset.

## Features

- ✅ Fetch climate data from World Bank API
- ✅ Display formatted data with metadata
- ✅ Save data to JSON file for future analysis
- ✅ Error handling for network issues
- ✅ Well-documented code with docstrings

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

Run the main script:
```bash
python climate.py
```

The script will:
1. Fetch climate data from the World Bank API
2. Display API metadata and sample country data
3. Save the complete dataset to `climate_data.json`

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
├── climate.py           # Main script
├── climate_data.json    # Output data file (generated)
├── README.md           # Project documentation
└── .venv/              # Virtual environment (optional)
```

## Functions

### `fetch_climate_data(url)`
Fetches climate data from the specified API endpoint.

### `display_climate_data(climate_data)`
Displays formatted climate data including metadata and sample countries.

### `save_data_to_file(climate_data, filename)`
Saves the fetched data to a JSON file.

### `main()`
Orchestrates the entire workflow.

## Author

**Claire Namusoke**  
Date: November 9, 2025

## License

This project is open source and available for educational purposes.

## Acknowledgments

- Data provided by the World Bank Climate Change Knowledge Portal
- CRU (Climatic Research Unit) for the temperature dataset
