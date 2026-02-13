"""
Create a Data Request Template for Supervisor
This Excel file shows exactly what data format is needed
"""

import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from datetime import datetime, timedelta

# Create workbook
wb = openpyxl.Workbook()

# Remove default sheet
if 'Sheet' in wb.sheetnames:
    wb.remove(wb['Sheet'])

# ============================================================================
# SHEET 1: INSTRUCTIONS
# ============================================================================
ws_instructions = wb.create_sheet("📋 INSTRUCTIONS")

# Title
ws_instructions['A1'] = "NPC REPORTING SYSTEM - DATA REQUEST TEMPLATE"
ws_instructions['A1'].font = Font(size=16, bold=True, color="FFFFFF")
ws_instructions['A1'].fill = PatternFill(start_color="003D82", end_color="003D82", fill_type="solid")
ws_instructions['A1'].alignment = Alignment(horizontal='center', vertical='center')
ws_instructions.merge_cells('A1:G1')
ws_instructions.row_dimensions[1].height = 30

# Instructions
instructions = [
    ("", ""),
    ("PURPOSE:", "This template shows the EXACT format needed for the NPC Reporting System"),
    ("", ""),
    ("WHAT WE NEED:", "Daily generation records for each unit at each plant"),
    ("", ""),
    ("DATA FIELDS REQUIRED:", ""),
    ("  1. Date", "The date of operation (format: YYYY-MM-DD or MM/DD/YYYY)"),
    ("  2. Unit Number", "Which generator unit (1, 2, 3, 4, etc.)"),
    ("  3. Generation kWh", "Total energy generated that day (in kilowatt-hours)"),
    ("  4. Operating Hours", "Hours the unit was actually running (0-24)"),
    ("  5. Availability Hours", "Hours the unit was available to run (24 - total outage hours)"),
    ("  6. Forced Outage Hours", "Unplanned downtime hours"),
    ("  7. Scheduled Outage Hours", "Planned maintenance downtime hours"),
    ("", ""),
    ("WHERE TO GET THIS DATA:", ""),
    ("  • SCADA System exports", ""),
    ("  • Plant operator logbooks", ""),
    ("  • Existing database or spreadsheets", ""),
    ("  • Energy Management System (EMS)", ""),
    ("", ""),
    ("SAMPLE DATA:", "See the 'SAMPLE DATA' sheet for examples"),
    ("", ""),
    ("HOW TO FILL:", ""),
    ("  1. Use the 'DATA ENTRY' sheet", ""),
    ("  2. One row per unit per day", ""),
    ("  3. Fill all required columns", ""),
    ("  4. Save as .xlsx file", ""),
    ("  5. Upload to the NPC Reporting System", ""),
    ("", ""),
    ("QUESTIONS?", "Contact: [Your Name/Email]"),
]

row = 3
for col1, col2 in instructions:
    ws_instructions[f'A{row}'] = col1
    ws_instructions[f'B{row}'] = col2
    if col1.endswith(':'):
        ws_instructions[f'A{row}'].font = Font(bold=True, size=12, color="003D82")
    row += 1

# Adjust column widths
ws_instructions.column_dimensions['A'].width = 30
ws_instructions.column_dimensions['B'].width = 70

# ============================================================================
# SHEET 2: SAMPLE DATA
# ============================================================================
ws_sample = wb.create_sheet("📊 SAMPLE DATA")

# Headers
headers = ["Date", "Unit Number", "Generation kWh", "Operating Hours", 
           "Availability Hours", "Forced Outage Hours", "Scheduled Outage Hours"]

for col, header in enumerate(headers, 1):
    cell = ws_sample.cell(1, col, header)
    cell.font = Font(bold=True, color="FFFFFF")
    cell.fill = PatternFill(start_color="003D82", end_color="003D82", fill_type="solid")
    cell.alignment = Alignment(horizontal='center', vertical='center')

# Sample data for AGUS1 (3 units, 7 days)
start_date = datetime(2026, 1, 1)
sample_data = []

for day in range(7):
    current_date = start_date + timedelta(days=day)
    
    # Unit 1 - Normal operation
    sample_data.append([
        current_date.strftime('%Y-%m-%d'),
        1,
        45000 + (day * 1000),
        22.5,
        24.0,
        1.5,
        0.0
    ])
    
    # Unit 2 - Normal operation
    sample_data.append([
        current_date.strftime('%Y-%m-%d'),
        2,
        44500 + (day * 950),
        22.0,
        24.0,
        2.0,
        0.0
    ])
    
    # Unit 3 - Had scheduled maintenance on day 3
    if day == 3:
        sample_data.append([
            current_date.strftime('%Y-%m-%d'),
            3,
            0,
            0.0,
            16.0,
            0.0,
            8.0  # 8 hours scheduled maintenance
        ])
    else:
        sample_data.append([
            current_date.strftime('%Y-%m-%d'),
            3,
            43000 + (day * 900),
            21.0,
            24.0,
            3.0,
            0.0
        ])

# Write sample data
for row_idx, row_data in enumerate(sample_data, 2):
    for col_idx, value in enumerate(row_data, 1):
        cell = ws_sample.cell(row_idx, col_idx, value)
        cell.alignment = Alignment(horizontal='center')
        
        # Add borders
        thin_border = Border(
            left=Side(style='thin'),
            right=Side(style='thin'),
            top=Side(style='thin'),
            bottom=Side(style='thin')
        )
        cell.border = thin_border

# Adjust column widths
for col in range(1, 8):
    ws_sample.column_dimensions[openpyxl.utils.get_column_letter(col)].width = 20

# Add note
ws_sample[f'A{len(sample_data) + 4}'] = "NOTE: This is sample data for AGUS1 with 3 units over 7 days"
ws_sample[f'A{len(sample_data) + 4}'].font = Font(italic=True, color="666666")
ws_sample.merge_cells(f'A{len(sample_data) + 4}:G{len(sample_data) + 4}')

# ============================================================================
# SHEET 3: DATA ENTRY (Blank template)
# ============================================================================
ws_entry = wb.create_sheet("✏️ DATA ENTRY")

# Headers
for col, header in enumerate(headers, 1):
    cell = ws_entry.cell(1, col, header)
    cell.font = Font(bold=True, color="FFFFFF")
    cell.fill = PatternFill(start_color="00A651", end_color="00A651", fill_type="solid")
    cell.alignment = Alignment(horizontal='center', vertical='center')

# Add 50 empty rows for data entry
for row in range(2, 52):
    for col in range(1, 8):
        cell = ws_entry.cell(row, col)
        thin_border = Border(
            left=Side(style='thin', color='CCCCCC'),
            right=Side(style='thin', color='CCCCCC'),
            top=Side(style='thin', color='CCCCCC'),
            bottom=Side(style='thin', color='CCCCCC')
        )
        cell.border = thin_border

# Adjust column widths
for col in range(1, 8):
    ws_entry.column_dimensions[openpyxl.utils.get_column_letter(col)].width = 20

# ============================================================================
# SHEET 4: VALIDATION RULES
# ============================================================================
ws_validation = wb.create_sheet("✅ VALIDATION RULES")

# Title
ws_validation['A1'] = "DATA VALIDATION RULES"
ws_validation['A1'].font = Font(size=14, bold=True, color="FFFFFF")
ws_validation['A1'].fill = PatternFill(start_color="003D82", end_color="003D82", fill_type="solid")
ws_validation['A1'].alignment = Alignment(horizontal='center', vertical='center')
ws_validation.merge_cells('A1:C1')
ws_validation.row_dimensions[1].height = 25

# Validation rules
rules = [
    ("Field", "Rule", "Example"),
    ("Date", "Must be valid date format", "2026-01-15 or 01/15/2026"),
    ("Unit Number", "Must be integer (1, 2, 3, etc.)", "1, 2, 3"),
    ("Generation kWh", "Must be number ≥ 0", "45000, 0"),
    ("Operating Hours", "Must be 0-24", "22.5, 18.0, 0"),
    ("Availability Hours", "Must be 0-24", "24.0, 16.0"),
    ("Forced Outage Hours", "Must be 0-24", "2.0, 0"),
    ("Scheduled Outage Hours", "Must be 0-24", "8.0, 0"),
    ("", "", ""),
    ("IMPORTANT:", "Operating Hours + Forced Outage + Scheduled Outage ≤ 24", ""),
    ("", "Availability Hours = 24 - (Forced Outage + Scheduled Outage)", ""),
]

for row_idx, (field, rule, example) in enumerate(rules, 2):
    ws_validation[f'A{row_idx}'] = field
    ws_validation[f'B{row_idx}'] = rule
    ws_validation[f'C{row_idx}'] = example
    
    if row_idx == 2:  # Header row
        for col in ['A', 'B', 'C']:
            ws_validation[f'{col}{row_idx}'].font = Font(bold=True)
            ws_validation[f'{col}{row_idx}'].fill = PatternFill(start_color="E0E0E0", end_color="E0E0E0", fill_type="solid")

# Adjust column widths
ws_validation.column_dimensions['A'].width = 25
ws_validation.column_dimensions['B'].width = 50
ws_validation.column_dimensions['C'].width = 25

# ============================================================================
# SHEET 5: PLANT INFORMATION
# ============================================================================
ws_plants = wb.create_sheet("🏭 PLANT INFO")

# Title
ws_plants['A1'] = "AGUS HYDROELECTRIC POWER PLANTS"
ws_plants['A1'].font = Font(size=14, bold=True, color="FFFFFF")
ws_plants['A1'].fill = PatternFill(start_color="003D82", end_color="003D82", fill_type="solid")
ws_plants['A1'].alignment = Alignment(horizontal='center', vertical='center')
ws_plants.merge_cells('A1:E1')
ws_plants.row_dimensions[1].height = 25

# Plant information
plant_info = [
    ("Plant Code", "Plant Name", "Location", "Capacity (MW)", "Units"),
    ("AGUS1", "Agus 1 Hydroelectric Power Plant", "Lanao del Sur", "200", "3"),
    ("AGUS2", "Agus 2 Hydroelectric Power Plant", "Lanao del Sur", "180", "3"),
    ("AGUS4", "Agus 4 Hydroelectric Power Plant", "Lanao del Norte", "200", "2"),
    ("AGUS5", "Agus 5 Hydroelectric Power Plant", "Lanao del Norte", "52", "2"),
    ("AGUS6", "Agus 6 Hydroelectric Power Plant", "Lanao del Norte", "200", "4"),
    ("AGUS7", "Agus 7 Hydroelectric Power Plant", "Lanao del Norte", "200", "5"),
]

for row_idx, row_data in enumerate(plant_info, 2):
    for col_idx, value in enumerate(row_data, 1):
        cell = ws_plants.cell(row_idx, col_idx, value)
        if row_idx == 2:  # Header
            cell.font = Font(bold=True)
            cell.fill = PatternFill(start_color="E0E0E0", end_color="E0E0E0", fill_type="solid")
        cell.alignment = Alignment(horizontal='center')

# Adjust column widths
ws_plants.column_dimensions['A'].width = 15
ws_plants.column_dimensions['B'].width = 40
ws_plants.column_dimensions['C'].width = 20
ws_plants.column_dimensions['D'].width = 15
ws_plants.column_dimensions['E'].width = 10

# Add note
ws_plants['A10'] = "NOTE: Create separate Excel files for each plant, or include plant code in filename"
ws_plants['A10'].font = Font(italic=True, color="666666")
ws_plants.merge_cells('A10:E10')

# Save workbook
output_file = "DATA_REQUEST_TEMPLATE.xlsx"
wb.save(output_file)

print(f"✅ Template created: {output_file}")
print("\nThis file contains:")
print("  📋 Instructions - How to use this template")
print("  📊 Sample Data - Example of correct format")
print("  ✏️ Data Entry - Blank sheet to fill in")
print("  ✅ Validation Rules - Data requirements")
print("  🏭 Plant Info - List of all Agus plants")
print("\nGive this file to your supervisor to show what data you need!")
