# Report Generation Guide - Understanding Dates

## How the System Works

### Upload Process
When you upload an Excel file:
1. The system uses the **upload date** (when you clicked upload) as the `report_date`
2. **The date column in your Excel file is IGNORED**
3. All records from that upload get the same `report_date` = upload date

### Example
- You upload a file on **May 4, 2026** at 2:52 PM
- Your Excel file contains data for March 1-31, 2026
- **Result**: All records are stored with `report_date = 2026-05-04` (NOT March dates!)

## Your Current Data

### Uploaded Files
1. **AGUS1_Sample_Report.xlsx**
   - Uploaded: May 4, 2026
   - Records created with date: **2026-05-04**
   - Plant: AGUS1
   - Units: 1, 2

2. **AGUS4_Sample_Report.xlsx**
   - Uploaded: April 30, 2026
   - Records created with date: **2026-04-30**
   - Plant: AGUS4
   - Units: 1, 2

3. **AGUS2_Sample_Report.xlsx**
   - Uploaded: April 30, 2026
   - Records created with date: **2026-04-30**
   - Plant: AGUS2
   - Units: 1, 2

4. **AGUS1_Clean_Sample.xlsx**
   - Uploaded: April 30, 2026
   - Records created with date: **2026-04-30**
   - Plant: AGUS1
   - Units: 1, 2

### Available Report Dates
You can ONLY generate reports for these dates:
- ✅ **May 4, 2026** - AGUS1 only (2 units)
- ✅ **April 30, 2026** - AGUS1, AGUS2, AGUS4 (2 units each)

## Why Report Generation Fails

### Scenario 1: Wrong Date Selected
**Problem**: You select May 5, 2026 but no data exists for that date
**Solution**: Select May 4 or April 30

### Scenario 2: Wrong Plant Selected
**Problem**: You select AGUS2 for May 4, but AGUS2 data is only for April 30
**Solution**: 
- For May 4: Select AGUS1
- For April 30: Select AGUS1, AGUS2, or AGUS4

### Scenario 3: Date Range Too Narrow
**Problem**: You select May 1-3, but data only exists for April 30 and May 4
**Solution**: Expand date range to include April 30 or May 4

## How to Generate Reports Successfully

### Step 1: Check What Data You Have
Run this command to see available dates:
```bash
cd backend
python check_report_dates.py
```

### Step 2: Select Matching Criteria
When generating a report:
1. **Select a plant** that has data for your chosen date
2. **Select a date range** that includes dates with data
3. **Select report type** (PSR or Daily Status)

### Example: Generate Report for May 4
```
Plant: AGUS1
Start Date: 2026-05-04
End Date: 2026-05-04
Report Type: PSR
```
✅ This will work because AGUS1 has data for May 4

### Example: Generate Report for April 30
```
Plants: AGUS1, AGUS2, AGUS4
Start Date: 2026-04-30
End Date: 2026-04-30
Report Type: PSR
```
✅ This will work because all three plants have data for April 30

## How to Upload Data for Specific Dates

### Important: Upload Date = Report Date
The system currently uses the upload date as the report date. This means:

**If you want data for March 15, 2026:**
1. You would need to upload the file ON March 15, 2026
2. OR the system needs to be modified to read dates from Excel

### Current Limitation
You cannot "backdate" reports by uploading old data. The upload date becomes the report date.

## Solution Options

### Option 1: Upload Files on the Correct Date
- Upload daily data files on the actual day
- This ensures report_date matches the actual date

### Option 2: Modify the System (Recommended)
Change the Excel importer to use the date from the Excel file instead of upload date.

**Current behavior:**
```python
# Line 507 in excel_importer.py
report_date = self.uploaded_file.uploaded_at.date()  # Uses upload date
```

**Proposed change:**
```python
# Use date from Excel file
if pd.notna(row.get('date')):
    report_date = pd.to_datetime(row['date']).date()
else:
    report_date = self.uploaded_file.uploaded_at.date()  # Fallback
```

### Option 3: Manual Date Entry
Add a date picker when uploading files to specify the report date.

## Troubleshooting

### Error: "No data found for the specified criteria"

**Check 1: Do you have data for that date?**
```bash
cd backend
python check_report_dates.py
```

**Check 2: Does the plant have data for that date?**
Look at the output - each plant shows its date range.

**Check 3: Is your date range correct?**
Make sure start_date and end_date include dates with data.

### Error: "No data found" but I just uploaded a file

**Possible causes:**
1. **File upload failed** - Check backend logs
2. **Wrong plant selected** - File was uploaded for AGUS1 but you selected AGUS2
3. **Date mismatch** - File was uploaded today but you're trying to generate for yesterday

**Solution:**
1. Check uploaded files list to confirm upload succeeded
2. Note which plant the file was uploaded for
3. Use today's date (upload date) when generating the report

## Quick Reference

### Available Data (as of May 4, 2026)
| Date | Plants | Units | Records |
|------|--------|-------|---------|
| 2026-05-04 | AGUS1 | 1, 2 | 2 |
| 2026-04-30 | AGUS1, AGUS2, AGUS4 | 1, 2 each | 6 |

### To Generate Report for Today (May 4)
1. Go to "Generate Report"
2. Select Plant: **AGUS1**
3. Select Date: **May 4, 2026**
4. Click "Generate Report"
5. ✅ Report will be generated

### To Generate Report for April 30
1. Go to "Generate Report"
2. Select Plants: **AGUS1, AGUS2, AGUS4** (or any combination)
3. Select Date: **April 30, 2026**
4. Click "Generate Report"
5. ✅ Report will be generated

## Recommended Fix

To make the system use dates from Excel files instead of upload dates, I can modify the `excel_importer.py` file. This would allow you to:
- Upload historical data
- Have the correct dates in reports
- Generate reports for any date in the Excel file

Would you like me to implement this fix?

---

**Current Status**: System uses upload date as report date
**Impact**: Can only generate reports for dates when files were uploaded
**Recommendation**: Modify system to read dates from Excel files
