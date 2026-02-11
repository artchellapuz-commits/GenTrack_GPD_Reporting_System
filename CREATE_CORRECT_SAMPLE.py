import pandas as pd
from datetime import datetime, timedelta

# Create sample data with correct column names
data = []
start_date = datetime(2026, 2, 1)

# Create 10 days of data for AGUS1 units (1, 2, 3, 4)
for day in range(10):
    current_date = start_date + timedelta(days=day)
    for unit in [1, 2, 3, 4]:
        data.append({
            'Date': current_date.strftime('%Y-%m-%d'),
            'Unit Number': unit,
            'Generation kWh': 20000 + (unit * 1000) + (day * 500),
            'Operating Hours': 22 + (day % 3),
            'Availability Hours': 24,
            'Forced Outage Hours': day % 2,
            'Scheduled Outage Hours': 0
        })

# Create DataFrame
df = pd.DataFrame(data)

# Save to Excel
output_file = 'CORRECT_SAMPLE_AGUS1.xlsx'
df.to_excel(output_file, index=False, sheet_name='Generation Report')

print(f"✓ Created sample file: {output_file}")
print(f"✓ Total records: {len(data)}")
print(f"\nColumn names in file:")
for col in df.columns:
    print(f"  - {col}")
print(f"\nFirst few rows:")
print(df.head())
print(f"\n✓ Upload this file for AGUS1 plant")
