"""
Create a sample Excel file for Pulangi 4 (3 units)
"""
import pandas as pd
from datetime import datetime, timedelta

# Create sample data for Pulangi 4 (3 units, 85 MW each)
data = []

# Generate 7 days of sample data
start_date = datetime(2026, 2, 1)

for day in range(7):
    current_date = start_date + timedelta(days=day)
    
    # Unit 1 - 85 MW
    data.append({
        'Date': current_date.strftime('%Y-%m-%d'),
        'Unit Number': 1,
        'Generation kWh': 1800000,  # ~88% capacity factor
        'Operating Hours': 22.5,
        'Availability Hours': 23.0,
        'Forced Outage Hours': 0.5,
        'Scheduled Outage Hours': 0.5,
        'Remarks': 'Normal operation'
    })
    
    # Unit 2 - 85 MW
    data.append({
        'Date': current_date.strftime('%Y-%m-%d'),
        'Unit Number': 2,
        'Generation kWh': 1850000,  # ~91% capacity factor
        'Operating Hours': 23.0,
        'Availability Hours': 23.5,
        'Forced Outage Hours': 0.5,
        'Scheduled Outage Hours': 0,
        'Remarks': 'Normal operation'
    })
    
    # Unit 3 - 85 MW
    data.append({
        'Date': current_date.strftime('%Y-%m-%d'),
        'Unit Number': 3,
        'Generation kWh': 1900000,  # ~93% capacity factor
        'Operating Hours': 23.5,
        'Availability Hours': 24.0,
        'Forced Outage Hours': 0,
        'Scheduled Outage Hours': 0,
        'Remarks': 'Normal operation'
    })

# Create DataFrame
df = pd.DataFrame(data)

# Save to Excel
output_file = 'SAMPLE_PULANGI4.xlsx'
df.to_excel(output_file, index=False, sheet_name='Pulangi 4')

print(f"✓ Sample Excel file created: {output_file}")
print(f"\nFile contains:")
print(f"  - 7 days of data")
print(f"  - 3 units (85 MW each)")
print(f"  - Total: {len(data)} records")
print(f"\nColumns:")
for col in df.columns:
    print(f"  - {col}")
print(f"\nFirst few rows:")
print(df.head(6))
print(f"\nYou can now upload this file for Pulangi 4!")
