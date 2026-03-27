# Excel Upload System - Maximum Flexibility

## Overview
The NPC Reporting System now accepts virtually ANY Excel file format!

## What Makes It Flexible?

### 1. File Format Support
- ✅ .xlsx (Excel 2007+)
- ✅ .xls (Excel 97-2003)
- ✅ Up to 25MB file size

### 2. Automatic Sheet Detection
- Searches ALL sheets in your workbook
- Tries multiple header row positions (rows 0-5)
- Scores each possibility and uses the best match
- Works with multi-sheet workbooks

### 3. Column Name Recognition (60+ variations)
The system recognizes these column names and many more:

**Date:** date, report_date, day, datetime, timestamp, dt
**Unit:** unit, unit_number, unitno, unit_id
**Generation:** generation, gen_kwh, kwh, energy, power, output
**Operating Hours:** operating_hours, op_hours, run_hours, runtime
**Availability:** availability_hours, avail_hours, available_hours
**Forced Outage:** forced_outage_hours, fo_hours, forced, outage
**Scheduled Outage:** scheduled_outage_hours, so_hours, maintenance

### 4. Flexible Requirements
**Minimum Required:**
- Date column (any variation)
- Unit number column (any variation)

**Optional (will default to 0 if missing):**
- Generation kWh
- Operating hours
- Availability hours  
- Forced outage hours
- Scheduled outage hours

### 5. Smart Data Cleaning
- Removes empty rows automatically
- Handles multiple date formats
- Parses numbers with commas, currency symbols
- Caps hours to 0-24 range
- Sets negative values to 0
- Fills missing values with sensible defaults

### 6. Forgiving Error Handling
- Skips invalid rows instead of failing
- Imports all valid data
- Provides detailed warnings
- Shows helpful suggestions

### 7. Layout Flexibility
- Columns can be in ANY order
- Can have title rows, logos, headers
- Extra columns are ignored
- Works with merged cells (mostly)
- Handles various Excel templates

## What Gets Imported?

For each valid row:
- ✅ Report date (required)
- ✅ Unit number (required)
- ✅ Generation in kWh (optional, defaults to 0)
- ✅ Operating hours (optional, defaults to 0)
- ✅ Availability hours (optional, defaults to 0)
- ✅ Forced outage hours (optional, defaults to 0)
- ✅ Scheduled outage hours (optional, defaults to 0)
- ✅ Remarks (optional)

## Example Formats That Work

### Format 1: Standard
```
date       | unit | generation_kwh | operating_hours
2026-02-20 | 1    | 540000        | 22.5
```

### Format 2: With Title
```
National Power Corporation

Date       | Unit No | Gen (kWh) | Op Hours
02/20/2026 | 1       | 540,000   | 22.5
```

### Format 3: Minimal
```
date       | unit
2026-02-20 | 1
2026-02-20 | 2
```
(All other fields will be 0)

### Format 4: Different Names
```
report_date | unitno | energy | runtime
20-Feb-2026 | 1      | 540000 | 22.5
```

## Tips for Best Results

1. **Clear headers** - Use descriptive column names
2. **Consistent data** - Keep the same format throughout
3. **Valid dates** - Use recognizable date formats
4. **Correct units** - Match unit numbers to your plant
5. **One plant per file** - Don't mix plants in one file

## Troubleshooting

### "Could not find valid data"
- Check that you have at least "date" and "unit" columns
- Make sure data starts within first 6 rows
- Verify the sheet isn't completely empty

### "Unit X not found for plant Y"
- Check that the unit numbers match your plant's units
- Run `python manage.py verify_plant_units` to see valid units

### "No valid records imported"
- Check that dates are in a recognizable format
- Verify unit numbers are numeric
- Make sure there's actual data (not just headers)

## System Behavior

✅ **Accepts:** Any Excel file with date and unit columns
✅ **Skips:** Invalid rows (logs warnings)
✅ **Defaults:** Missing optional columns to 0
✅ **Updates:** Existing records if duplicate date/unit found
✅ **Imports:** All valid rows even if some rows fail

## Need Help?

The system provides detailed error messages with:
- What columns were found
- What columns are missing
- Accepted alternative names
- Tips for fixing the issue

Just read the error message carefully - it will guide you!
