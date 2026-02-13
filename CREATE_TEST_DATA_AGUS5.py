"""
Generate sample Excel file for AGUS5 with maintenance periods
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

# AGUS5 has 2 units (52 MW total capacity)
units = [
    {"number": 1, "name": "Unit 1", "capacity": 26},
    {"number": 2, "name": "Unit 2", "capacity": 26},
]

# Generate data for 45 days with maintenance period
start_date = datetime(2025, 12, 1)

for day in range(45):
    current_date = start_date + timedelta(days=day)
    date_str = current_date.strftime("%Y-%m-%d")
    
    for unit in units:
        # Simulate maintenance on Unit 1 from day 15-20
        if unit["number"] == 1 and 15 <= day <= 20:
            # Maintenance period - zero generation
            row = [
                date_str,
                unit["number"],
                unit["name"],
                unit["capacity"],
                0,
                0,
                0,
                0,
                "Scheduled maintenance"
            ]
        else:
            # Normal operation with moderate capacity factors (45-75%)
            operating_hours = random.uniform(18, 24)
            availability = random.uniform(80, 95)
            capacity_factor = random.uniform(45, 75)
            
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
                "Normal operation"
            ]
        ws.append(row)

# Save file in backend folder
import os
filename = "SAMPLE_AGUS5_45DAYS.xlsx"
filepath = os.path.join("backend", filename)
wb.save(filepath)
print(f"✓ Created {filepath}")
print(f"  - Plant: AGUS5")
print(f"  - Units: 2")
print(f"  - Days: 45")
print(f"  - Records: {45 * 2} = 90")
print(f"  - Pattern: Includes maintenance period (Unit 1, days 15-20)")
