import json
import pandas as pd
import os

# Clean climate_data.json
json_path = 'climate_data.json'
if os.path.exists(json_path):
    with open(json_path, 'r') as f:
        data = json.load(f)
    clim = data['data']['data']
    for country in list(clim.keys()):
        if not isinstance(clim[country], dict):
            continue
        for date in list(clim[country].keys()):
            year = int(date.split('-')[0])
            if year < 2019 or year > 2023:
                del clim[country][date]
        if not clim[country]:
            del clim[country]
    with open(json_path, 'w') as f:
        json.dump(data, f, indent=2)
    print(f'{json_path} cleaned to 2019-2023')

# Clean CSV files
csv_files = [
    'maritime_world_total.csv',
    'maritime_oecd_countries.csv',
    'sea_level_monthly.csv',
    'sea_level_regional_2019_2024.csv',
    'sea_level_by_region_yearly.csv',
    'sea_level_yearly_new.csv'
]
for file in csv_files:
    if not os.path.exists(file):
        print(f'{file} not found')
        continue
    df = pd.read_csv(file)
    year_cols = [col for col in df.columns if col.lower().startswith('year') or col.lower() == 'year']
    if year_cols:
        year_col = year_cols[0]
        df = df[(df[year_col] >= 2019) & (df[year_col] <= 2023)]
        df.to_csv(file, index=False)
        print(f'{file} cleaned to 2019-2023')
    else:
        print(f'No year column found in {file}')
