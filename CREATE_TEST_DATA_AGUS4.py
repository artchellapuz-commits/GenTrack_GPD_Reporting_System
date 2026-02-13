"""
Generate sample Excel file for AGUS4 with different data patterns
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

# AGUS4 has 4 units (158 MW total capacity)
units = [
    {"number": 1, "name": "Unit 1", "capacity": 39.5},
    {"number": 2, "name": "Unit 2", "capacity": 39.5},
    {"number": 3, "name": "Unit 3", "capacity": 39.5},
    {"number": 4, "name": "Unit 4", "capacity": 39.5},
]

# Generate data for 30 days
start_date = datetime(2026, 1, 1)

for day in range(30):
    current_date = start_date + timedelta(days=day)
    date_str = current_date.strftime("%Y-%m-%d")
    
    for unit in units:
        # AGUS4 pattern: Higher capacity factors (60-85%)
        operating_hours = random.uniform(20, 24)
        availability = random.uniform(85, 98)
        capacity_factor = random.uniform(60, 85)
        
        # Calculate generation based on capacity factor
        max_generation = unit["capacity"] * 1000 * 24  # kWh per day
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
            "Normal operation" if capacity_factor > 70 else "Reduced load"
        ]
        ws.append(row)

# Save file in backend folder
import os
filename = "SAMPLE_AGUS4_30DAYS.xlsx"
filepath = os.path.join("backend", filename)
wb.save(filepath)
print(f"✓ Created {filepath}")
print(f"  - Plant: AGUS4")
print(f"  - Units: 4")
print(f"  - Days: 30")
print(f"  - Records: {30 * 4} = 120")
print(f"  - Pattern: High capacity factors (60-85%)")
