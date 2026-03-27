# Sample Excel Template for NPC Reporting System

## Required Columns

Your Excel file (.xlsx) must have these columns in the first row:

| Column Name | Data Type | Description | Example | Validation |
|------------|-----------|-------------|---------|------------|
| date | Date | Report date | 2024-01-15 | YYYY-MM-DD format |
| unit_number | Integer | Unit number | 1 | Must exist in database |
| generation_kwh | Decimal | Generation in kWh | 500000.50 | Non-negative |
| operating_hours | Decimal | Operating hours | 23.5 | 0 to 24 |
| availability_hours | Decimal | Availability hours | 24.0 | 0 to 24 |
| forced_outage_hours | Decimal | Forced outage hours | 0.5 | 0 to 24 |
| scheduled_outage_hours | Decimal | Scheduled outage | 0.0 | 0 to 24 |
| remarks | Text | Optional notes | Normal operation | Optional |

---

## Sample Data (Copy to Excel)

### For AGUS1 Plant

```
date          unit_number  generation_kwh  operating_hours  availability_hours  forced_outage_hours  scheduled_outage_hours  remarks
2024-01-15    1           500000          23.5             24.0                0.5                  0.0                     Normal operation
2024-01-15    2           480000          22.0             24.0                2.0                  0.0                     Minor maintenance
2024-01-15    3           510000          24.0             24.0                0.0                  0.0                     Full operation
2024-01-15    4           495000          23.0             24.0                1.0                  0.0                     Normal operation
2024-01-16    1           505000          24.0             24.0                0.0                  0.0                     Full operation
2024-01-16    2           490000          23.0             24.0                1.0                  0.0                     Normal operation
2024-01-16    3           515000          24.0             24.0                0.0                  0.0                     Full operation
2024-01-16    4           500000          24.0             24.0                0.0                  0.0                     Full operation
```

---

## How to Create Excel File

### Method 1: Using Microsoft Excel

1. Open Microsoft Excel
2. Create a new workbook
3. In the first row, type the column headers exactly as shown above
4. Fill in the data rows
5. Save as `.xlsx` format
6. File → Save As → Choose "Excel Workbook (*.xlsx)"

### Method 2: Using Google Sheets

1. Open Google Sheets
2. Create a new spreadsheet
3. Add column headers in first row
4. Fill in data
5. File → Download → Microsoft Excel (.xlsx)

### Method 3: Using LibreOffice Calc

1. Open LibreOffice Calc
2. Create new spreadsheet
3. Add headers and data
4. File → Save As → Choose "Excel 2007-365 (.xlsx)"

---

## Important Notes

### Column Names
- Must be **lowercase**
- Use **underscores** instead of spaces
- Must match exactly: `generation_kwh` not `Generation (kWh)`

### Date Format
- Use YYYY-MM-DD format: `2024-01-15`
- Excel may auto-format dates - ensure they're in correct format
- Avoid formats like: 01/15/2024 or 15-Jan-2024

### Numeric Values
- Use decimal point (.) not comma (,)
- Example: `500000.50` not `500,000.50`
- No currency symbols or units

### Hours Validation
- All hour fields must be between 0 and 24
- Can use decimals: `23.5` means 23 hours 30 minutes
- Total hours in a day = 24

### Unit Numbers
- Must match units defined in the database
- If uploading for AGUS1, ensure units 1-4 exist in database
- Check Django admin to see available units

---

## Sample Data for Testing

### Scenario 1: Normal Operation (All Units Running)
```
date          unit_number  generation_kwh  operating_hours  availability_hours  forced_outage_hours  scheduled_outage_hours  remarks
2024-01-20    1           520000          24.0             24.0                0.0                  0.0                     Full operation
2024-01-20    2           518000          24.0             24.0                0.0                  0.0                     Full operation
2024-01-20    3           522000          24.0             24.0                0.0                  0.0                     Full operation
2024-01-20    4           519000          24.0             24.0                0.0                  0.0                     Full operation
```

### Scenario 2: With Outages
```
date          unit_number  generation_kwh  operating_hours  availability_hours  forced_outage_hours  scheduled_outage_hours  remarks
2024-01-21    1           450000          20.0             24.0                4.0                  0.0                     Equipment failure
2024-01-21    2           0               0.0              24.0                0.0                  24.0                    Scheduled maintenance
2024-01-21    3           520000          24.0             24.0                0.0                  0.0                     Full operation
2024-01-21    4           510000          23.5             24.0                0.5                  0.0                     Minor issue
```

### Scenario 3: Monthly Data (January 2024)
Generate 31 rows for each unit (31 days × 4 units = 124 rows)

---

## Validation Rules

### File Level
- ✅ File extension must be `.xlsx`
- ✅ File size must be under 10MB
- ✅ First row must contain column headers

### Column Level
- ✅ All required columns must be present
- ✅ Column names must match exactly (case-sensitive)
- ✅ No extra columns will cause errors (they're ignored)

### Data Level
- ✅ No null/empty values in required columns
- ✅ Dates must be valid
- ✅ Numbers must be numeric (not text)
- ✅ Hours must be in range 0-24
- ✅ Unit must exist in database for selected plant

### Business Rules
- ✅ No duplicate entries (same plant, unit, date)
- ✅ If duplicate found, existing record will be updated
- ✅ Capacity factor calculated automatically
- ✅ Availability factor calculated automatically

---

## Common Errors and Solutions

### Error: "Missing required columns"
**Solution**: Check column names are exactly as specified (lowercase, underscores)

### Error: "Invalid date format"
**Solution**: Use YYYY-MM-DD format, not MM/DD/YYYY

### Error: "Column contains non-numeric values"
**Solution**: Remove any text, currency symbols, or commas from numeric columns

### Error: "Hours outside 0-24 range"
**Solution**: Check operating_hours, availability_hours, etc. are between 0 and 24

### Error: "Unit not found"
**Solution**: Ensure the unit exists in database for the selected plant

### Error: "File already uploaded"
**Solution**: This exact file (same checksum) was already uploaded

---

## Download Template

You can create your own template using the information above, or:

1. Open Excel/Google Sheets
2. Copy the column headers from the table above
3. Add sample data
4. Save as `.xlsx`

---

## Testing Your File

Before uploading to production:

1. **Check column names**: Exactly match the required names
2. **Check data types**: Numbers are numbers, dates are dates
3. **Check ranges**: Hours between 0-24
4. **Check units**: Units exist in database
5. **Check dates**: Valid date format
6. **Save as .xlsx**: Not .xls or .csv

---

## Example: Creating Test File in Excel

1. Open Excel
2. Row 1: Type headers
   ```
   date | unit_number | generation_kwh | operating_hours | availability_hours | forced_outage_hours | scheduled_outage_hours | remarks
   ```

3. Row 2: Add data
   ```
   2024-01-15 | 1 | 500000 | 23.5 | 24.0 | 0.5 | 0.0 | Normal operation
   ```

4. Add more rows as needed

5. Save As → Excel Workbook (.xlsx)

6. Upload via web interface

---

## Need Help?

- Check SETUP_GUIDE.md for system setup
- Check API_DOCUMENTATION.md for technical details
- Check Django admin to verify plants and units exist
- Review error messages carefully - they indicate what's wrong
