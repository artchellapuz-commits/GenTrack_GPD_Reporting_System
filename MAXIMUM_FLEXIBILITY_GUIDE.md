# Maximum Flexibility Excel Upload System

## Overview
The system now accepts virtually ANY Excel file format with minimal requirements!

## What's Required? (ONLY 2 THINGS!)

### Absolute Minimum Requirements:
1. **A date column** - Can be named anything like:
   - date, report_date, day, datetime, timestamp, dt, data, datum, etc.
   
2. **A unit column** - Can be named anything like:
   - unit, unit_number, unitno, unit_id, no, number, num, u, etc.

That's it! Everything else is optional and will be filled with default values (0).

## What Happens to Missing Data?

If your Excel file is missing these columns, they will automatically be set to 0:
- generation_kwh → 0
- operating_hours → 0
- availability_hours → 0
- forced_outage_hours → 0
- scheduled_outage_hours → 0

## Column Recognition (80+ Variations!)

The system recognizes these and many more variations:

### Date Column (14 variations)
date, report_date, reportdate, day, datetime, timestamp, dt, fecha, tanggal, petsa, data, datum, tarikh, ngay

### Unit Column (14 variations)
unit_number, unitnumber, unit, unit_no, unitno, unit_id, unitid, unidad, yunit, no, number, num, u, unit_name

### Generation Column (13 variations)
generation_kwh, generation, gen_kwh, kwh, energy, energy_kwh, generacion, henerasyon, gen, power, output, mwh, total_generation

### Operating Hours (13 variations)
operating_hours, operatinghours, op_hours, ophours, run_hours, runtime, running_hours, oras, horas, hours, hrs, operating, operation

### Availability Hours (8 variations)
availability_hours, availabilityhours, avail_hours, available_hours, avail, availability, available, avl_hrs

### Forced Outage Hours (9 variations)
forced_outage_hours, forcedoutagehours, forced_outage, fo_hours, foh, forced, outage, forced_out, foh_hrs

### Scheduled Outage Hours (10 variations)
scheduled_outage_hours, scheduledoutagehours, scheduled_outage, so_hours, soh, maintenance_hours, scheduled, maintenance, maint, soh_hrs

## Smart Features

### 1. Fuzzy Column Matching
- Recognizes partial matches (60% similarity)
- Case-insensitive
- Handles special characters automatically
- Removes spaces, dashes, parentheses

### 2. Multi-Sheet Support
- Searches ALL sheets in your workbook
- Tries header rows 0-5 in each sheet
- Uses the sheet with the best match

### 3. Flexible Layout
- Columns can be in ANY order
- Can have title rows, logos, headers
- Extra columns are ignored
- Works with merged cells (mostly)

### 4. Smart Data Cleaning
- Removes empty rows
- Handles multiple date formats
- Parses numbers with commas, currency
- Caps hours to 0-24
- Sets negative values to 0
- Fills missing values with 0

### 5. Forgiving Import
- Skips invalid rows
- Imports all valid data
- Shows detailed warnings
- Provides helpful error messages

## Example Files That Work

### Example 1: Minimal File
```
date       | unit
2026-02-20 | 1
2026-02-20 | 2
```
✅ Works! All other fields will be 0

### Example 2: Different Names
```
Day        | No | Gen (kWh) | Hours
02/20/2026 | 1  | 540000    | 22.5
```
✅ Works! System recognizes the columns

### Example 3: With Title
```
National Power Corporation
Generation Report - February 2026

Date       | Unit | Generation
2026-02-20 | 1    | 540000
```
✅ Works! System finds the header row

### Example 4: Extra Columns
```
date | unit | generation | operating | remarks | extra_col1 | extra_col2
...
```
✅ Works! Extra columns are ignored

## What If It Still Doesn't Work?

If the system can't import your file, it will show a helpful error message telling you:
1. What columns it found in your file
2. What columns it needs (date and unit minimum)
3. Examples of acceptable column names
4. Tips for fixing the issue

## Tips for Best Results

1. **Clear headers** - Use descriptive column names in the first few rows
2. **Consistent data** - Keep the same format throughout the file
3. **Valid dates** - Use recognizable date formats (YYYY-MM-DD, MM/DD/YYYY, etc.)
4. **Correct units** - Match unit numbers to your plant's units
5. **One plant per file** - Don't mix plants in one file

## System Behavior

✅ **Accepts:** Any Excel file (.xlsx, .xls) with date and unit columns
✅ **Fills:** Missing optional columns with 0
✅ **Skips:** Invalid rows (logs warnings)
✅ **Updates:** Existing records if duplicate date/unit found
✅ **Imports:** All valid rows even if some rows fail
✅ **Provides:** Detailed, helpful error messages

## File Size & Format

- **Formats:** .xlsx, .xls
- **Max Size:** 25MB
- **Sheets:** Searches all sheets automatically
- **Header:** Can be in rows 0-5

## Need Help?

The system will guide you with detailed error messages that include:
- What was found in your file
- What's needed
- Accepted alternative names
- Actionable tips

Just read the error message - it will tell you exactly what to do!

## Summary

The system is now EXTREMELY flexible:
- Only requires 2 columns (date + unit)
- Recognizes 80+ column name variations
- Searches all sheets and header positions
- Fills missing data with defaults
- Provides helpful error messages
- Accepts almost any Excel file format

**Bottom line:** If your Excel file has dates and unit numbers, it will probably work!
