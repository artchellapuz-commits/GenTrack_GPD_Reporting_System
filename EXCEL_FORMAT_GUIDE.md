# Excel File Format Guide

## Required Column Headers

Your Excel file MUST have these exact column headers (case-insensitive):

| Column Header | Alternative Names | Data Type | Description |
|---------------|-------------------|-----------|-------------|
| Date | date, DATE | Date | Report date (YYYY-MM-DD) |
| Unit Number | unit_number, Unit_Number | Integer | Unit number (1-4 for most plants, 1-2 for AGUS5) |
| Generation kWh | generation_kwh, Generation_kWh | Number | Energy generated in kilowatt-hours |
| Operating Hours | operating_hours, Operating_Hours | Number | Hours the unit operated (0-24) |
| Availability Hours | availability_hours, Availability_Hours | Number | Hours the unit was available (0-24) |
| Forced Outage Hours | forced_outage_hours, Forced_Outage_Hours | Number | Unplanned downtime hours (0-24) |
| Scheduled Outage Hours | scheduled_outage_hours, Scheduled_Outage_Hours | Number | Planned downtime hours (0-24) |
| Remarks | remarks, REMARKS | Text | Optional notes (can be empty) |

## Column Name Rules

The system automatically normalizes column names by:
1. Converting to lowercase
2. Removing extra spaces
3. Replacing spaces with underscores
4. Replacing hyphens with underscores

So these are all valid:
- "Date" → date
- "Unit Number" → unit_number
- "Generation kWh" → generation_kwh
- "Operating Hours" → operating_hours

## Sample Excel Structure

```
| Date       | Unit Number | Generation kWh | Operating Hours | Availability Hours | Forced Outage Hours | Scheduled Outage Hours | Remarks |
|------------|-------------|----------------|-----------------|--------------------|--------------------|------------------------|---------|
| 2026-02-01 | 1           | 500000         | 22.5            | 23.0               | 0.5                | 0.0                    | Normal  |
| 2026-02-01 | 2           | 510000         | 22.5            | 23.0               | 0.5                | 0.0                    | Normal  |
| 2026-02-01 | 3           | 520000         | 22.5            | 23.0               | 0.5                | 0.0                    | Normal  |
| 2026-02-01 | 4           | 530000         | 22.5            | 23.0               | 0.5                | 0.0                    | Normal  |
```

## Data Validation Rules

### Date Column
- Must be a valid date
- Recommended format: YYYY-MM-DD (e.g., 2026-02-01)
- Excel date format is also accepted

### Unit Number
- Must be an integer
- Valid range depends on plant:
  - AGUS1: 1-4
  - AGUS2: 1-4
  - AGUS4: 1-4
  - AGUS5: 1-2
  - AGUS6: 1-4
  - AGUS7: 1-4

### Numeric Columns
- Must contain only numbers (no text)
- Cannot be negative
- Generation kWh: Any positive number
- Hours columns: Must be between 0 and 24

### Remarks
- Optional text field
- Can be empty
- Any text is accepted

## Common Errors and Solutions

### Error: "Missing required columns"
**Cause**: Column headers don't match expected names

**Solution**: 
- Check spelling of column headers
- Make sure there are no extra spaces
- Column names are case-insensitive but must match the structure

### Error: "Column contains non-numeric values"
**Cause**: Text or special characters in numeric columns

**Solution**:
- Remove any text from numeric columns
- Remove currency symbols ($, ₱)
- Remove commas from numbers
- Use plain numbers only

### Error: "Values outside 0-24 range"
**Cause**: Hours columns have values > 24 or < 0

**Solution**:
- Operating Hours must be 0-24
- Availability Hours must be 0-24
- Outage Hours must be 0-24
- Check for data entry errors

### Error: "Unit X not found for plant AGUSY"
**Cause**: Unit number doesn't exist for the selected plant

**Solution**:
- Check unit numbers match the plant
- AGUS5 only has 2 units (1-2)
- Other plants have 4 units (1-4)

### Error: "Invalid date format"
**Cause**: Date column has invalid or missing dates

**Solution**:
- Use YYYY-MM-DD format (e.g., 2026-02-01)
- Or use Excel's date format
- Make sure all date cells are filled

## Tips for Creating Excel Files

1. **Use the Sample File as Template**
   - Copy `sample_data/AGUS1_Sample_Report.xlsx`
   - Replace the data with your actual data
   - Keep the column headers exactly as they are

2. **One Row Per Unit Per Day**
   - Each row represents one unit's data for one day
   - If you have 4 units and 5 days, you'll have 20 rows

3. **Don't Skip Columns**
   - All required columns must be present
   - You can leave Remarks empty, but the column must exist

4. **Use Excel's Data Validation**
   - Set date format for Date column
   - Set number format for numeric columns
   - This helps prevent data entry errors

5. **Check Before Uploading**
   - Make sure all required columns are present
   - Check for any empty cells in required columns
   - Verify unit numbers are correct for the plant

## Creating Your Own Excel File

### Method 1: Copy the Sample
1. Copy `sample_data/AGUS1_Sample_Report.xlsx`
2. Open in Excel
3. Replace the data (keep headers!)
4. Save with a new name

### Method 2: Create from Scratch
1. Create new Excel file
2. Add headers in first row (see table above)
3. Add your data starting from row 2
4. Save as .xlsx format

### Method 3: Use the Script
Run `CREATE_SAMPLE_EXCEL.py` to generate a template:
```bash
cd backend
venv\Scripts\activate
python ..\CREATE_SAMPLE_EXCEL.py
```

## Verification Checklist

Before uploading, verify:
- [ ] All 7 required column headers are present
- [ ] Column headers match the expected names (case-insensitive)
- [ ] Date column has valid dates
- [ ] Unit Number column has integers only
- [ ] All numeric columns have numbers only (no text)
- [ ] Hours columns have values between 0-24
- [ ] Unit numbers match the selected plant
- [ ] File is saved as .xlsx format
- [ ] No completely empty rows

## Example: Valid Excel File

Here's what a valid file looks like:

**Filename**: AGUS1_February_2026.xlsx

**Sheet 1**: Generation Report

| Date       | Unit Number | Generation kWh | Operating Hours | Availability Hours | Forced Outage Hours | Scheduled Outage Hours | Remarks          |
|------------|-------------|----------------|-----------------|--------------------|--------------------|------------------------|------------------|
| 2026-02-01 | 1           | 500000         | 22.5            | 23.0               | 0.5                | 0.0                    | Normal operation |
| 2026-02-01 | 2           | 510000         | 23.0            | 23.5               | 0.5                | 0.0                    | Normal operation |
| 2026-02-01 | 3           | 520000         | 22.0            | 23.0               | 1.0                | 0.0                    | Minor issue      |
| 2026-02-01 | 4           | 530000         | 24.0            | 24.0               | 0.0                | 0.0                    | Full operation   |

This file will successfully import 4 records into the database.

---

**Need Help?**
- Check `UPLOAD_TESTING_GUIDE.md` for step-by-step upload instructions
- Use `sample_data/AGUS1_Sample_Report.xlsx` as a reference
- Run `CREATE_SAMPLE_EXCEL.py` to generate a new template
