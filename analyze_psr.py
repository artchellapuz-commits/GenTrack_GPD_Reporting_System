"""
Analyze the PSR REPORT-8AM.xlsx file structure
"""
import openpyxl
from openpyxl.utils import get_column_letter

# Load the workbook
wb = openpyxl.load_workbook(r'C:\Users\eladiong\Desktop\OJT Intern\REPORTS\8. PSR\PSR REPORT-8AM.xlsx')
ws = wb.active

print(f"Sheet name: {ws.title}")
print(f"Dimensions: {ws.dimensions}")
print("\n" + "="*80)
print("CELL CONTENTS (First 100 rows):")
print("="*80 + "\n")

# Print cell contents for first 100 rows
for row in range(1, min(101, ws.max_row + 1)):
    row_data = []
    has_content = False
    for col in range(1, min(15, ws.max_column + 1)):  # Check first 15 columns
        cell = ws.cell(row=row, column=col)
        if cell.value is not None:
            has_content = True
            col_letter = get_column_letter(col)
            # Get cell formatting info
            font_color = cell.font.color.rgb if cell.font.color else "None"
            bg_color = cell.fill.fgColor.rgb if cell.fill.fgColor else "None"
            row_data.append(f"{col_letter}{row}: '{cell.value}' (Font:{font_color}, BG:{bg_color})")
    
    if has_content:
        print(f"Row {row}:")
        for data in row_data:
            print(f"  {data}")
        print()

print("\n" + "="*80)
print("MERGED CELLS:")
print("="*80)
for merged_range in ws.merged_cells.ranges:
    print(f"  {merged_range}")

print("\n" + "="*80)
print("COLUMN WIDTHS:")
print("="*80)
for col in range(1, min(15, ws.max_column + 1)):
    col_letter = get_column_letter(col)
    width = ws.column_dimensions[col_letter].width
    print(f"  Column {col_letter}: {width}")

print("\n" + "="*80)
print("ROW HEIGHTS:")
print("="*80)
for row in range(1, min(101, ws.max_row + 1)):
    height = ws.row_dimensions[row].height
    if height:
        print(f"  Row {row}: {height}")
