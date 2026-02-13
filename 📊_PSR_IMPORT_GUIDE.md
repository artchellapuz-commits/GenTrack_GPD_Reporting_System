# 📊 PSR Report Import Guide

## Overview

This guide explains how to import historical data from PSR (Plant Status Report) Excel files into the NPC Reporting System.

## What is a PSR Report?

PSR (Plant Status Report) is a complex Excel format used by NPC that contains:
- Plant codes and names
- Generation data
- Capacity information
- Plant status information
- Multiple data columns with various metrics

## File Format

### Expected Structure

```
Row 1-10:  Headers, titles, date information
Row 11+:   Plant data rows
Column A:  Plant codes (e.g., AGUS1, AGUS2, etc.)
Column B+: Numeric data (generation, capacity, etc.)
```

### Example

```
| Plant Code | Data 1 | Data 2 | Data 3 |
|------------|--------|--------|--------|
| AGUS1      | 123.45 | 150.00 | 98.5   |
| AGUS2      | 234.56 | 200.00 | 87.3   |
| AGUS3      | 345.67 | 180.00 | 92.1   |
```

## Import Methods

### Method 1: Using Batch File (Easiest)

1. **Place your PSR report file** in the `REPORTS\8. PSR\` folder

2. **Run the import script:**
   ```batch
   IMPORT_PSR_REPORT.bat
   ```

3. **Or specify a custom file:**
   ```batch
   IMPORT_PSR_REPORT.bat "path\to\your\psr_report.xlsx"
   ```

### Method 2: Using Python Script

1. **Activate virtual environment:**
   ```batch
   cd backend
   venv\Scripts\activate
   cd ..
   ```

2. **Run the import script:**
   ```bash
   python IMPORT_PSR_REPORT.py
   ```

3. **Or with custom file:**
   ```bash
   python IMPORT_PSR_REPORT.py "REPORTS\8. PSR\your_file.xlsx"
   ```

### Method 3: Using Django Management Command

1. **Activate virtual environment:**
   ```batch
   cd backend
   venv\Scripts\activate
   ```

2. **Run the management command:**
   ```bash
   python manage.py import_historical_data "path\to\psr_report.xlsx"
   ```

## What Gets Imported

### Plant Information
- **Plant Code**: Extracted from first column
- **Plant Name**: Initially set to plant code (can be updated later)

### Historical Data
- **Date**: Extracted from file headers or filename
- **Actual Generation**: Numeric data from data columns
- **Remarks**: "Imported from PSR Report"

### Plant Capacity (if available)
- **Dependable Capacity**: From capacity columns
- **Installed Capacity**: From capacity columns

## Import Process

### Step 1: File Analysis
The importer analyzes the file structure:
- Detects where plant data starts
- Identifies data columns
- Extracts report date

### Step 2: Data Extraction
For each plant row:
- Validates plant code format
- Extracts numeric data
- Parses generation values

### Step 3: Database Import
- Creates or updates plant records
- Creates or updates historical data
- Updates plant capacity if available

### Step 4: Validation
- Checks for duplicate entries
- Validates data ranges
- Reports errors and warnings

## Supported File Formats

### PSR Report Format
- **File**: `MGG-IMS-004.F01, Report Review Rev. 0.xlsx`
- **Structure**: Complex multi-column format
- **Data**: Generation, capacity, status

### Daily Data Format
- **File**: `1DATA APAO.xlsx`
- **Structure**: Days as columns (1-31)
- **Data**: Daily generation values

### Plant Capacity Format
- **File**: `0PLANT DEPCAP.xlsx`
- **Structure**: Plant list with capacities
- **Data**: Dependable and installed capacity

## Troubleshooting

### Issue: "Could not find plant data"

**Solution:**
- Check if file has plant codes in first column
- Verify plant codes follow pattern (letters + numbers)
- Ensure data starts within first 50 rows

### Issue: "Could not determine report date"

**Solution:**
- Add date in file headers (first 20 rows)
- Use format: MM/DD/YYYY or "Month DD, YYYY"
- Or accept default (today's date)

### Issue: "No numeric data columns found"

**Solution:**
- Verify columns B onwards contain numbers
- Check for merged cells
- Ensure data is not formatted as text

### Issue: "Invalid plant code"

**Solution:**
- Plant codes must be 2-15 characters
- Must contain both letters and numbers
- Examples: AGUS1, AGUS2, BAKUN1

## Data Validation

### Plant Code Validation
```python
# Valid plant codes:
AGUS1, AGUS2, BAKUN1, AMBUKLAO1

# Invalid plant codes:
TOTAL, SUBTOTAL, GRAND TOTAL, (empty)
```

### Generation Data Validation
```python
# Valid values:
0, 123.45, 1000.00

# Invalid values:
-100 (negative), "N/A", (empty)
```

## Import Results

### Success Output
```
========================================
PSR REPORT IMPORTER
========================================

📂 File: MGG-IMS-004.F01, Report Review Rev. 0.xlsx
📊 Sheets found: Sheet1

Processing sheet: Sheet1
--------------------------------------------------
  Data starts at row: 12
  Report date: 2026-02-11
  Data columns found: 5
  ✓ Imported 25 plants, 125 data records

========================================
IMPORT SUMMARY
========================================
✓ Plants imported/updated: 25
✓ Data records imported: 125

========================================
```

### With Warnings
```
⚠ Warnings: 3
  - Sheet 'Sheet1', Row 15, Col 3: Invalid value
  - Sheet 'Sheet1', Row 20, Col 5: Could not parse
  - Report date not found, using today
```

### With Errors
```
❌ Errors: 2
  - Sheet 'Sheet1', Row 18: Invalid plant code
  - Sheet 'Sheet1', Row 25: Database error
```

## Best Practices

### 1. File Preparation
- ✅ Keep original file format
- ✅ Ensure plant codes are in first column
- ✅ Include date information in headers
- ✅ Remove extra sheets if not needed

### 2. Data Quality
- ✅ Verify plant codes are correct
- ✅ Check numeric values are valid
- ✅ Remove summary rows (TOTAL, SUBTOTAL)
- ✅ Ensure no merged cells in data area

### 3. Import Process
- ✅ Test with small file first
- ✅ Review import summary
- ✅ Check warnings and errors
- ✅ Verify data in dashboard

### 4. After Import
- ✅ Verify plant list in dashboard
- ✅ Check generation data
- ✅ Update plant names if needed
- ✅ Add missing capacity data

## Advanced Usage

### Import Multiple Files

Create a batch script:
```batch
@echo off
for %%f in ("REPORTS\8. PSR\*.xlsx") do (
    echo Importing %%f
    python IMPORT_PSR_REPORT.py "%%f"
)
```

### Custom Date Override

Modify the script to use specific date:
```python
# In IMPORT_PSR_REPORT.py
report_date = date(2026, 2, 11)  # Override date
```

### Filter by Plant Type

Add filtering logic:
```python
# Only import hydro plants
if plant_code.startswith('AGUS') or plant_code.startswith('BAKUN'):
    # Import this plant
```

## Database Schema

### Plants Table
```sql
CREATE TABLE plants (
    id INTEGER PRIMARY KEY,
    code VARCHAR(50) UNIQUE,
    name VARCHAR(200),
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);
```

### Historical Data Table
```sql
CREATE TABLE historical_data (
    id INTEGER PRIMARY KEY,
    plant_id INTEGER,
    date DATE,
    actual_generation DECIMAL(10,2),
    remarks TEXT,
    created_at TIMESTAMP,
    UNIQUE(plant_id, date)
);
```

### Plant Capacity Table
```sql
CREATE TABLE plant_capacity (
    id INTEGER PRIMARY KEY,
    plant_id INTEGER UNIQUE,
    dependable_capacity DECIMAL(10,2),
    installed_capacity DECIMAL(10,2),
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);
```

## API Integration

After import, data is available via API:

### Get Historical Data
```http
GET /api/reports/historical-data/?plant_code=AGUS1&start_date=2026-02-01&end_date=2026-02-28
```

### Get Plant Capacity
```http
GET /api/reports/plant-capacity/
```

## Support

### Need Help?

1. Check this guide first
2. Review error messages
3. Check `TROUBLESHOOTING.md`
4. Contact system administrator

### Report Issues

Include:
- File name and format
- Error messages
- Import summary output
- Screenshots if applicable

## Related Documentation

- `HISTORICAL_DATA_IMPORT_GUIDE.md` - General historical data import
- `EXCEL_FORMAT_GUIDE.md` - Excel file format specifications
- `API_DOCUMENTATION.md` - API usage
- `TROUBLESHOOTING.md` - Common issues

---

**Last Updated**: February 2026
**Version**: 1.0
