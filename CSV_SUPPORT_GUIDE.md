# CSV File Support Guide

## Overview
The NPC Reporting System now accepts CSV files in addition to Excel files!

## Supported File Formats

### Excel Files
- ✅ .xlsx (Excel 2007+)
- ✅ .xls (Excel 97-2003)

### CSV Files
- ✅ .csv (Comma-Separated Values)

All formats up to 25MB file size.

## CSV File Features

### Automatic Detection
The system automatically detects:
- **Encoding**: UTF-8, Latin-1, ISO-8859-1, CP1252
- **Delimiters**: Comma (,), Semicolon (;), Tab (\t), Pipe (|)
- **Header row**: Automatically finds column names

### Flexible CSV Format
Your CSV file can use:
- Any delimiter (comma, semicolon, tab, pipe)
- Any encoding
- Any column order
- Same column name variations as Excel (80+ variations)

## CSV File Examples

### Example 1: Comma-Separated
```csv
date,unit,generation_kwh,operating_hours,availability_hours
2026-02-20,1,540000,22.5,23.0
2026-02-20,2,520000,21.0,22.0
```

### Example 2: Semicolon-Separated
```csv
date;unit;generation;op_hours;avail_hours
20/02/2026;1;540000;22.5;23.0
20/02/2026;2;520000;21.0;22.0
```

### Example 3: Tab-Separated
```csv
date	unit_number	gen_kwh	hours
2026-02-20	1	540000	22.5
2026-02-20	2	520000	21.0
```

### Example 4: Minimal CSV
```csv
date,unit
2026-02-20,1
2026-02-20,2
```
✅ Works! Missing columns default to 0

## How to Create CSV Files

### From Excel
1. Open your Excel file
2. Click "File" → "Save As"
3. Choose "CSV (Comma delimited) (*.csv)"
4. Save the file
5. Upload to the system

### From Google Sheets
1. Open your Google Sheet
2. Click "File" → "Download" → "Comma-separated values (.csv)"
3. Upload to the system

### From Text Editor
1. Create a new text file
2. Add column headers in first row
3. Add data rows (one per line)
4. Save with .csv extension
5. Upload to the system

## CSV vs Excel

### CSV Advantages
- ✅ Smaller file size
- ✅ Opens in any text editor
- ✅ Easy to generate programmatically
- ✅ Universal compatibility
- ✅ Fast to process

### Excel Advantages
- ✅ Multiple sheets
- ✅ Formatting preserved
- ✅ Formulas supported
- ✅ More familiar to users

## Requirements (Same as Excel)

### Minimum Required Columns
1. **Date column** (any variation)
2. **Unit column** (any variation)

### Optional Columns (default to 0 if missing)
- Generation kWh
- Operating hours
- Availability hours
- Forced outage hours
- Scheduled outage hours
- Remarks

## CSV Processing

The system will:
1. **Try multiple encodings** - UTF-8, Latin-1, ISO-8859-1, CP1252
2. **Try multiple delimiters** - Comma, semicolon, tab, pipe
3. **Normalize column names** - Same as Excel (80+ variations)
4. **Clean data** - Remove empty rows, handle missing values
5. **Import valid data** - Skip invalid rows, create placeholders if needed

## Common CSV Issues & Solutions

### Issue: File won't open
**Solution:** The system tries multiple encodings automatically

### Issue: Wrong delimiter detected
**Solution:** The system tries all common delimiters

### Issue: Special characters look wrong
**Solution:** Save CSV as UTF-8 encoding

### Issue: Dates not recognized
**Solution:** Use standard formats (YYYY-MM-DD, MM/DD/YYYY, DD/MM/YYYY)

### Issue: Numbers have commas
**Solution:** The system automatically removes commas from numbers

## Tips for CSV Files

1. **Use UTF-8 encoding** - Best compatibility
2. **Use comma delimiter** - Most common
3. **Clear column headers** - Use descriptive names
4. **Consistent date format** - Stick to one format
5. **No empty rows** - Remove blank rows between data
6. **Quote text with commas** - Use quotes if text contains commas

## Example CSV Templates

### Minimal Template
```csv
date,unit
2026-02-20,1
2026-02-21,1
```

### Standard Template
```csv
date,unit,generation_kwh,operating_hours,availability_hours
2026-02-20,1,540000,22.5,23.0
2026-02-21,1,535000,22.0,23.0
```

### Complete Template
```csv
date,unit,generation_kwh,operating_hours,availability_hours,forced_outage_hours,scheduled_outage_hours,remarks
2026-02-20,1,540000,22.5,23.0,0.5,0,Normal operation
2026-02-21,1,535000,22.0,23.0,1.0,0,Minor maintenance
```

## Upload Process

1. **Select plant** from dropdown
2. **Choose CSV file** (or drag & drop)
3. **Click Upload Report**
4. **System processes** - Detects format, reads data
5. **Import complete** - Shows records imported

## Success Criteria

The upload succeeds if:
- ✅ File is valid CSV format
- ✅ Has at least date and unit columns
- ✅ At least one valid row of data
- ✅ Or creates placeholder if no valid data

## Summary

CSV files are now fully supported with:
- ✅ Automatic encoding detection
- ✅ Automatic delimiter detection
- ✅ Same flexibility as Excel files
- ✅ 80+ column name variations
- ✅ Forgiving error handling
- ✅ Placeholder creation for empty files

**Upload any CSV file - the system will handle it!**
