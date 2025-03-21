# Loads and prepares data from the multi-sheet Excel file

import re
import pandas as pd

# Load all sheets from the Excel file into a dictionary
all_sheets = pd.read_excel("predicate_data_main.xlsx", sheet_name=None)

# Extract numeric family identifier from device name
def get_family(device):
    match = re.match(r'(\d+)', str(device))
    return int(match.group(1)) if match else None

# Clean and process each sheet
for sheet_name, df in all_sheets.items():
    df.columns = df.columns.str.strip()
    df['family'] = df['Device'].apply(get_family)
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

    # Ensure all expected columns exist and are filled
    for col in ['FDA', 'Creep', 'Predicate_Location', 'Device_Name', 'Device_Summary',
                'Short_Description', 'Secondary_Specialty', 'Classification',
                'Predicate', 'Company', 'Lead_Specialty']:
        if col not in df.columns:
            df[col] = ''
        df[col] = df[col].fillna('')

# Determine the min and max approval years from all sheets
all_dates = [df['Date'].dropna() for df in all_sheets.values() if 'Date' in df.columns]

if all_dates:
    combined_dates = pd.concat(all_dates)
    min_year = combined_dates.dt.year.min()
    max_year = combined_dates.dt.year.max()
else:
    min_year, max_year = 2000, 2025
