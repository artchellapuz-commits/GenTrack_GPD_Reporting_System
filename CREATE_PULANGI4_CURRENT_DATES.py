"""
Create a sample Excel file for Pulangi 4 with CURRENT dates (Feb 10-13, 2026)
This matches the date range you're filtering in View Reports
"""
import pandas as pd
from datetime import datetime, timedelta

# Create sample data for Pulangi 4 (3 units, 85 MW each)
data = []

# Generate data for Feb 10-13, 2026 (4 days)
start_date = datetime(2026, 2, 10)

for day in range(4):  # 4 days: Feb 10, 11, 12, 13
    current_date = start_date + timedelta(days=day)
    
    # Unit 1 - 85 MW
    data.append({
        'Date': current_date.strftime('%Y-%m-%d'),
        'Unit Number': 1,
        'Generation kWh': 1850000,  # ~91% capacity factor
        'Operating Hours': 23.0,
        'Availability Hours': 23.5,
        'Forced Outage Hours': 0.5,
        'Scheduled Outage Hours': 0,
        'Remarks': 'Normal operation'
    })
    
    # Unit 2 - 85 MW
    data.append({
        'Date': current_date.strftime('%Y-%m-%d'),
        'Unit Number': 2,
        'Generation kWh': 1900000,  # ~93% capacity factor
        'Operating Hours': 23.5,
        'Availability Hours': 24.0,
        'Forced Outage Hours': 0,
        'Scheduled Outage Hours': 0,
        'Remarks': 'Normal operation'
    })
    
    # Unit 3 - 85 MW
    data.append({
        'Date': current_date.strftime('%Y-%m-%d'),
        'Unit Number': 3,
        'Generation kWh': 1950000,  # ~96% capacity factor
        'Operating Hours': 24.0,
        'Availability Hours': 24.0,
        'Forced Outage Hours': 0,
        'Scheduled Outage Hours': 0,
        'Remarks': 'Excellent operation'
    })

# Create DataFrame
df = pd.DataFrame(data)

# Save to Excel
output_file = 'SAMPLE_PULANGI4_FEB10-13.xlsx'
df.to_excel(output_file, index=False, sheet_name='Pulangi 4')

print(f"✓ Sample Excel file created: {output_file}")
print(f"\nFile contains:")
print(f"  - Date range: Feb 10-13, 2026 (4 days)")
print(f"  - 3 units (85 MW each)")
print(f"  - Total: {len(data)} records")
print(f"\nColumns:")
for col in df.columns:
    print(f"  - {col}")
print(f"\nData preview:")
print(df.head(9))
print(f"\nTotal Generation: {df['Generation kWh'].sum():,.0f} kWh")
print(f"\nNow upload this file for Pulangi 4 and it will show in View Reports!")
