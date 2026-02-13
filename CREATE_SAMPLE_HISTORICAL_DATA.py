"""
Create sample historical data Excel files for testing the import functionality

This script creates two sample Excel files:
1. 0PLANT DEPCAP.xlsx - Sample plant capacity data
2. 1DATA APAO.xlsx - Sample historical operational data

Run this script to generate test files for import.
"""

import pandas as pd
from datetime import datetime, timedelta
import random

def create_plant_capacity_file():
    """Create sample plant capacity file"""
    data = {
        'Plant Name': ['Agus 1', 'Agus 2', 'Agus 4', 'Agus 5', 'Agus 6', 'Agus 7'],
        'Installed Capacity (MW)': [100.00, 180.00, 200.00, 52.00, 120.00, 8.50],
        'Dependable Capacity (MW)': [95.00, 170.00, 190.00, 48.00, 110.00, 7.50],
        'Type': ['Hydro', 'Hydro', 'Hydro', 'Hydro', 'Hydro', 'Hydro'],
        'Location': ['Lanao del Sur', 'Lanao del Sur', 'Lanao del Sur', 
                     'Lanao del Sur', 'Lanao del Sur', 'Lanao del Sur']
    }
    
    df = pd.DataFrame(data)
    filename = '0PLANT DEPCAP.xlsx'
    df.to_excel(filename, index=False, sheet_name='Plant Capacity')
    print(f"✓ Created {filename}")
    return filename

def create_historical_data_file():
    """Create sample historical operational data file"""
    plants = ['Agus 1', 'Agus 2', 'Agus 4', 'Agus 5', 'Agus 6', 'Agus 7']
    capacities = {
        'Agus 1': 100.00,
        'Agus 2': 180.00,
        'Agus 4': 200.00,
        'Agus 5': 52.00,
        'Agus 6': 120.00,
        'Agus 7': 8.50
    }
    
    # Create data for 30 days
    start_date = datetime(2024, 1, 1)
    dates = [start_date + timedelta(days=i) for i in range(30)]
    
    all_data = []
    
    for date in dates:
        for plant in plants:
            capacity = capacities[plant]
            # Generate realistic data
            availability = random.uniform(85, 99)
            generation = capacity * 24 * (availability / 100) * random.uniform(0.9, 1.0)
            
            all_data.append({
                'Date': date.strftime('%Y-%m-%d'),
                'Plant Name': plant,
                'Generation (MWh)': round(generation, 2),
                'Availability (%)': round(availability, 2),
                'Status': 'Operating' if availability > 90 else 'Partial Operation',
                'Remarks': '' if availability > 95 else 'Minor maintenance'
            })
    
    df = pd.DataFrame(all_data)
    
    # Create Excel file with multiple sheets (by month)
    filename = '1DATA APAO.xlsx'
    with pd.ExcelWriter(filename, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='January 2024', index=False)
        
        # Add a second sheet with different data
        df2 = df.copy()
        df2['Date'] = pd.to_datetime(df2['Date']) + timedelta(days=31)
        df2['Date'] = df2['Date'].dt.strftime('%Y-%m-%d')
        df2.to_excel(writer, sheet_name='February 2024', index=False)
    
    print(f"✓ Created {filename}")
    return filename

def main():
    print("========================================")
    print("Creating Sample Historical Data Files")
    print("========================================")
    print()
    
    try:
        capacity_file = create_plant_capacity_file()
        historical_file = create_historical_data_file()
        
        print()
        print("========================================")
        print("Sample Files Created Successfully!")
        print("========================================")
        print()
        print("Files created:")
        print(f"  1. {capacity_file}")
        print(f"  2. {historical_file}")
        print()
        print("Next steps:")
        print("  1. Move these files to the 'backend' folder")
        print("  2. Run IMPORT_HISTORICAL_DATA.bat")
        print()
        print("Or import using command:")
        print(f'  python manage.py import_historical_data --capacity "{capacity_file}" --historical "{historical_file}"')
        print()
        
    except Exception as e:
        print(f"✗ Error creating files: {e}")
        return 1
    
    return 0

if __name__ == '__main__':
    exit(main())
