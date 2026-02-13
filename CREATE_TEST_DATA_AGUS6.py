"""
Generate sample Excel file for AGUS6 with variable performance
"""
import openpyxl
from datetime import datetime, timedelta
import random

# Create workbook
wb = openpyxl.Workbook()
ws = wb.active
ws.title = "Generation Report"

# Headers
headers = [
    "Date", "Unit Number", "Unit Name", "Capacity (MW)", 
    "Generation (kWh)", "Operating Hours", "Availability Factor (%)", 
    "Capacity Factor (%)", "Remarks"
]
ws.append(headers)

# AGUS6 has 4 units (200 MW total capacity)
units = [
    {"number": 1, "name": "Unit 1", "capacity": 50},
    {"number": 2, "name": "Unit 2", "capacity": 50},
    {"number": 3, "name": "Unit 3", "capacity": 50},
    {"number": 4, "name": "Unit 4", "capacity": 50},
]

# Generate data for 60 days with variable performance
start_date = datetime(2025, 11, 15)

for day in range(60):
    current_date = start_date + timedelta(days=day)
    date_str = current_date.strftime("%Y-%m-%d")
    
    # Simulate seasonal variation - lower in first 20 days, higher in last 20 days
    if day < 20:
        cf_range = (30, 55)  # Low season
        remark = "Low water season"
    elif day < 40:
        cf_range = (50, 70)  # Transition
        remark = "Normal operation"
    else:
        cf_range = (65, 90)  # High season
        remark = "High water season"
    
    for unit in units:
        operating_hours = random.uniform(16, 24)
        availability = random.uniform(75, 98)
        capacity_factor = random.uniform(cf_range[0], cf_range[1])
        
        max_generation = unit["capacity"] * 1000 * 24
        generation = max_generation * (capacity_factor / 100)
        
        row = [
            date_str,
            unit["number"],
            unit["name"],
            unit["capacity"],
            round(generation, 2),
            round(operating_hours, 2),
            round(availability, 2),
            round(capacity_factor, 2),
            remark
        ]
        ws.append(row)

# Save file in backend folder
import os

# Determine correct path based on current directory
if os.path.basename(os.getcwd()) == 'backend':
    filename = "SAMPLE_AGUS6_60DAYS.xlsx"
else:
    filename = os.path.join("backend", "SAMPLE_AGUS6_60DAYS.xlsx")

wb.save(filename)
print(f"✓ Created {filename}")
print(f"  - Plant: AGUS6")
print(f"  - Units: 4")
print(f"  - Days: 60")
print(f"  - Records: {60 * 4} = 240")
print(f"  - Pattern: Seasonal variation (low → normal → high)")
