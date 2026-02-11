"""
Create a fresh correct sample Excel file for AGUS1
"""
from openpyxl import Workbook
from datetime import datetime, timedelta

# Create workbook
wb = Workbook()
ws = wb.active
ws.title = "AGUS1 Generation Data"

# Add headers
headers = [
    "Date",
    "Unit Number",
    "Generation kWh",
    "Operating Hours",
    "Availability Hours",
    "Forced Outage Hours",
    "Scheduled Outage Hours"
]
ws.append(headers)

# Add sample data for 10 days, 4 units each
start_date = datetime(2026, 2, 1)
for day in range(10):
    current_date = start_date + timedelta(days=day)
    date_str = current_date.strftime("%Y-%m-%d")
    
    for unit in range(1, 5):  # Units 1-4
        row = [
            date_str,
            unit,
            15000 + (unit * 1000) + (day * 500),  # Generation kWh
            20 + (unit * 0.5),  # Operating Hours
            22 + (unit * 0.3),  # Availability Hours
            1.0,  # Forced Outage Hours
            1.0   # Scheduled Outage Hours
        ]
        ws.append(row)

# Save file
filename = "CORRECT_SAMPLE_AGUS1.xlsx"
wb.save(filename)
print(f"✓ Created {filename}")
print(f"✓ Contains 40 records (10 days × 4 units)")
print(f"✓ Ready to upload for AGUS1 plant")
