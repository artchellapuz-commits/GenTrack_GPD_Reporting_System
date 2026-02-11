"""
Create a sample Excel file for testing the upload functionality
"""
import openpyxl
from datetime import datetime, timedelta
from pathlib import Path

# Create a new workbook
wb = openpyxl.Workbook()
ws = wb.active
ws.title = "Generation Report"

# Add headers - using exact names that match after normalization
headers = [
    'Date', 'Unit Number', 'Generation kWh', 'Operating Hours',
    'Availability Hours', 'Forced Outage Hours', 'Scheduled Outage Hours', 'Remarks'
]
# After normalization these become:
# date, unit_number, generation_kwh, operating_hours,
# availability_hours, forced_outage_hours, scheduled_outage_hours, remarks
ws.append(headers)

# Add sample data for AGUS1 (4 units) for 5 days
start_date = datetime(2026, 2, 1)
for day in range(5):
    current_date = start_date + timedelta(days=day)
    for unit in range(1, 5):  # Units 1-4
        row = [
            current_date.strftime('%Y-%m-%d'),
            unit,
            500000 + (unit * 10000),  # Generation kWh
            22.5,  # Operating hours
            23.0,  # Availability hours
            0.5,   # Forced outage hours
            0.0,   # Scheduled outage hours
            f'Normal operation - Day {day+1}'
        ]
        ws.append(row)

# Format the date column
for row in ws.iter_rows(min_row=2, max_row=ws.max_row, min_col=1, max_col=1):
    for cell in row:
        cell.number_format = 'YYYY-MM-DD'

# Auto-adjust column widths
for column in ws.columns:
    max_length = 0
    column_letter = column[0].column_letter
    for cell in column:
        try:
            if len(str(cell.value)) > max_length:
                max_length = len(str(cell.value))
        except:
            pass
    adjusted_width = (max_length + 2)
    ws.column_dimensions[column_letter].width = adjusted_width

# Save the file
output_dir = Path(__file__).parent / 'sample_data'
output_dir.mkdir(exist_ok=True)
output_file = output_dir / 'AGUS1_Sample_Report.xlsx'

wb.save(output_file)
print(f"Sample Excel file created: {output_file}")
print(f"\nFile contains:")
print(f"- 5 days of data (Feb 1-5, 2026)")
print(f"- 4 units (AGUS1 Units 1-4)")
print(f"- Total: 20 records")
print(f"\nYou can upload this file to test the system!")
print(f"Select 'AGUS1' as the plant when uploading.")
