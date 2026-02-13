"""
Generate sample Excel file for AGUS7 with recent data
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

# AGUS7 has 4 units (200 MW total capacity)
units = [
    {"number": 1, "name": "Unit 1", "capacity": 50},
    {"number": 2, "name": "Unit 2", "capacity": 50},
    {"number": 3, "name": "Unit 3", "capacity": 50},
    {"number": 4, "name": "Unit 4", "capacity": 50},
]

# Generate data for last 15 days (recent data)
start_date = datetime(2026, 1, 27)  # Recent dates

for day in range(15):
    current_date = start_date + timedelta(days=day)
    date_str = current_date.strftime("%Y-%m-%d")
    
    for unit in units:
        # AGUS7 pattern: Consistent high performance (70-95%)
        operating_hours = random.uniform(22, 24)
        availability = random.uniform(90, 99)
        capacity_factor = random.uniform(70, 95)
        
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
            "Optimal operation"
        ]
        ws.append(row)

# Save file in backend folder
import os
filename = "SAMPLE_AGUS7_15DAYS.xlsx"
filepath = os.path.join("backend", filename)
wb.save(filepath)
print(f"✓ Created {filepath}")
print(f"  - Plant: AGUS7")
print(f"  - Units: 4")
print(f"  - Days: 15")
print(f"  - Records: {15 * 4} = 60")
print(f"  - Pattern: Recent data with high performance (70-95%)")
