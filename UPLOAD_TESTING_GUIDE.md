# Excel Upload Testing Guide

## ✅ System is Ready for Upload Testing!

### What's Been Fixed:

1. **CORS Configuration** - Fixed to allow frontend-backend communication
2. **Authentication** - Configured to work without requiring login
3. **Upload Handler** - Fixed to handle unauthenticated uploads
4. **Sample Data** - Created test Excel file with realistic data

---

## 📁 Sample Excel File Created

**Location**: `sample_data/AGUS1_Sample_Report.xlsx`

**Contents**:
- 5 days of data (February 1-5, 2026)
- 4 units (AGUS1 Units 1-4)
- Total: 20 records
- All required columns included

---

## 🧪 How to Test Upload

### Step 1: Access the Application
Open your browser and go to: **http://localhost:8080/**

### Step 2: Navigate to Upload Page
Click on "Upload Excel Report" in the navigation menu

### Step 3: Select Plant
From the dropdown, select: **Agus 1 Hydroelectric Plant**

### Step 4: Choose File
Click "Select Excel File" and browse to:
```
npc-reporting-system/sample_data/AGUS1_Sample_Report.xlsx
```

### Step 5: Upload
Click the "Upload" button

### Step 6: Verify Success
You should see:
- Success message: "Success! 20 records imported."
- The file appears in the "Recent Uploads" table below
- Status shows as "COMPLETED"

---

## 📊 Excel File Format Requirements

Your Excel file must have these columns (case-insensitive):

| Column Name | Type | Description | Valid Range |
|-------------|------|-------------|-------------|
| Date | Date | Report date | YYYY-MM-DD format |
| Unit Number | Integer | Unit number | 1-4 (AGUS1,2,4,6,7), 1-2 (AGUS5) |
| Generation kWh | Number | Energy generated | >= 0 |
| Operating Hours | Number | Hours unit operated | 0-24 |
| Availability Hours | Number | Hours unit was available | 0-24 |
| Forced Outage Hours | Number | Unplanned downtime | 0-24 |
| Scheduled Outage Hours | Number | Planned downtime | 0-24 |
| Remarks | Text | Optional notes | Any text |

---

## ✅ What Happens During Upload

1. **File Validation**
   - Checks file format (.xlsx)
   - Validates required columns exist
   - Checks for null values
   - Validates data types

2. **Data Processing**
   - Reads Excel file
   - Validates each row
   - Checks unit numbers match plant
   - Verifies date formats
   - Ensures numeric values are in valid ranges

3. **Database Storage**
   - Creates UploadedFile record (audit trail)
   - Imports GenerationReport records
   - Calculates capacity and availability factors
   - Updates existing records if duplicates found

4. **Response**
   - Returns success message with record count
   - Or returns detailed error messages if validation fails

---

## 🔍 Verify Data Was Saved

### Method 1: View Reports Page
1. Go to "View Generation Reports"
2. You should see the 20 imported records
3. Filter by AGUS1 to see only those records

### Method 2: Check Database Directly
Run this command:
```bash
cd backend
venv\Scripts\activate
python manage.py shell
```

Then in the Python shell:
```python
from reports.models import GenerationReport, UploadedFile

# Check uploaded files
print(f"Total uploads: {UploadedFile.objects.count()}")
for upload in UploadedFile.objects.all():
    print(f"- {upload.original_filename}: {upload.records_imported} records, Status: {upload.status}")

# Check generation reports
print(f"\nTotal reports: {GenerationReport.objects.count()}")
for report in GenerationReport.objects.all()[:5]:
    print(f"- {report.plant.code} Unit {report.unit.unit_number} on {report.report_date}: {report.generation_kwh} kWh")
```

### Method 3: Django Admin (After creating superuser)
1. Go to http://127.0.0.1:8000/admin/
2. Login with admin credentials
3. Click "Uploaded files" to see upload history
4. Click "Generation reports" to see imported data

---

## 🐛 Troubleshooting

### Error: "Plant not found"
- Make sure you selected the correct plant from dropdown
- Plant code in Excel must match selected plant

### Error: "Missing required columns"
- Check your Excel file has all required column headers
- Column names are case-insensitive but must match exactly

### Error: "Unit X not found for plant AGUS1"
- AGUS1 has units 1-4 only
- Check your unit numbers in the Excel file

### Error: "Invalid date format"
- Dates must be in YYYY-MM-DD format
- Or use Excel date format (will be auto-converted)

### Error: "Column contains non-numeric values"
- All numeric columns must contain only numbers
- Remove any text or special characters

### Error: "Values outside 0-24 range"
- Operating hours, availability hours, and outage hours must be between 0 and 24

### Upload button is disabled
- Make sure you selected a plant
- Make sure you selected a file
- Both must be selected before upload button activates

### No plants showing in dropdown
- Refresh the page
- Check browser console for errors (F12)
- Verify backend is running at http://127.0.0.1:8000/

---

## 📝 Creating Your Own Excel Files

### Template Structure:
```
Date          | Unit Number | Generation kWh | Operating Hours | Availability Hours | Forced Outage Hours | Scheduled Outage Hours | Remarks
2026-02-01    | 1          | 500000         | 22.5           | 23.0              | 0.5                | 0.0                   | Normal
2026-02-01    | 2          | 510000         | 22.5           | 23.0              | 0.5                | 0.0                   | Normal
```

### Tips:
- Use Excel's date format for the Date column
- One row per unit per day
- You can upload multiple days in one file
- You can re-upload to update existing records
- System prevents duplicate uploads (same file checksum)

---

## 🎯 Next Steps After Successful Upload

1. **View Reports**
   - Go to "View Generation Reports"
   - Filter by plant and date range
   - View summary statistics

2. **Generate Excel Reports**
   - Go to "Generate Excel Report"
   - Select plants and date range
   - Download formatted report

3. **Upload More Data**
   - Create Excel files for other plants (AGUS2, AGUS4, AGUS5, AGUS6, AGUS7)
   - Upload historical data
   - Upload daily reports

---

## 📊 Sample Data Summary

The provided sample file contains:

**Plant**: AGUS1 (Agus 1 Hydroelectric Plant)
**Period**: February 1-5, 2026
**Units**: 1, 2, 3, 4
**Records**: 20 (5 days × 4 units)

**Typical Values**:
- Generation: 500,000 - 540,000 kWh per unit per day
- Operating Hours: 22.5 hours
- Availability Hours: 23.0 hours
- Forced Outage: 0.5 hours
- Scheduled Outage: 0.0 hours

---

## ✨ Success Indicators

After a successful upload, you should see:

1. ✅ Green success message with record count
2. ✅ File appears in "Recent Uploads" table
3. ✅ Status shows "COMPLETED"
4. ✅ Records imported count matches expected
5. ✅ Data visible in "View Reports" page

---

**System Status**: ✅ Ready for Upload Testing
**Sample File**: ✅ Created and Ready
**Backend**: ✅ Running at http://127.0.0.1:8000/
**Frontend**: ✅ Running at http://localhost:8080/

**Start testing now at: http://localhost:8080/**
