# ✅ YES! Files ARE Generated Automatically

## Quick Answer

**Q: After clicking "Run Now", did it output automatically and where can I find it?**

**A: YES! Excel files are automatically generated and saved to:**
```
npc-reporting-system/backend/media/automated_reports/
```

---

## 🎯 Fastest Way to Access

**Double-click:** `OPEN_REPORTS_FOLDER.bat`

This will open the folder containing all generated reports.

---

## 📂 Manual Navigation

1. Open File Explorer
2. Navigate to your project folder
3. Go to: `backend` → `media` → `automated_reports`
4. You'll see Excel files with timestamps
5. Double-click any file to open in Excel

---

## 📊 Files Currently Generated

Based on the folder check, you already have these files:

| File | Generated | Size |
|------|-----------|------|
| `GENERATION_SUMMARY_20260220_091904.xlsx` | Feb 20, 09:19 AM | ~15 KB |
| `PERFORMANCE_METRICS_20260220_091852.xlsx` | Feb 20, 09:18 AM | ~12 KB |
| `PERFORMANCE_METRICS_20260220_091934.xlsx` | Feb 20, 09:19 AM | ~12 KB |

These were created when you clicked "Run Now"!

---

## 📋 What Happens When You Click "Run Now"

1. **Frontend** sends request to backend
2. **Backend** queries generation data (last 30 days)
3. **Service** creates Excel file with:
   - Report header
   - Data table
   - Formatted columns
   - Totals/averages
4. **File** saved to `automated_reports/` folder
5. **Database** records execution details
6. **Success** message shown to user

**All automatic - no manual steps needed!**

---

## 📄 File Contents

### GENERATION_SUMMARY
```
Date       | Plant | Unit | Generation | Operating Hours | Capacity Factor
2026-02-01 | AGUS1 | 1    | 45000 kWh  | 22.5 hrs       | 85.2%
2026-02-02 | AGUS1 | 1    | 48000 kWh  | 24.0 hrs       | 90.5%
...
```

### CAPACITY_FACTOR
```
Plant | Avg Capacity Factor | Total Generation | Avg Operating Hours
AGUS1 | 87.5%              | 1,350 MWh        | 23.2 hrs
AGUS2 | 82.3%              | 1,200 MWh        | 21.8 hrs
...
```

### AVAILABILITY
```
Plant | Avg Availability | Forced Outage | Scheduled Outage
AGUS1 | 92.5%           | 12 hrs        | 24 hrs
AGUS2 | 88.3%           | 18 hrs        | 30 hrs
...
```

### PERFORMANCE_METRICS
```
Plant | Capacity | Avg CF | Avg Avail | Total Gen | Operating Hrs | Days
AGUS1 | 50 MW    | 87.5%  | 92.5%     | 1,350 MWh | 696 hrs      | 30
AGUS2 | 45 MW    | 82.3%  | 88.3%     | 1,200 MWh | 654 hrs      | 30
...
```

---

## 🔍 How to View Execution History

In the Scheduled Reports page:

1. Click **"History"** button on any report
2. Popup shows:
   - Execution date/time
   - Status (Completed/Failed)
   - Records processed
   - **Filename** ← This is the file you can open
3. Note the filename
4. Go to `automated_reports` folder
5. Open that file in Excel

---

## 🎨 File Features

Each generated Excel file has:

✅ **Professional Header**
- Report title
- Generation timestamp
- NPC branding

✅ **Formatted Data Table**
- Column headers with blue background
- White text for headers
- Auto-sized columns
- Proper alignment

✅ **Data Rows**
- All generation data from last 30 days
- Formatted numbers
- Date formatting

✅ **Totals/Averages** (where applicable)
- Sum of generation
- Average capacity factor
- Average availability

---

## 📍 Full Path Examples

**Relative path from project root:**
```
npc-reporting-system\backend\media\automated_reports\
```

**Absolute path (example):**
```
C:\Users\YourName\Projects\npc-reporting-system\backend\media\automated_reports\
```

**File examples:**
```
GENERATION_SUMMARY_20260220_091904.xlsx
CAPACITY_FACTOR_20260220_143022.xlsx
AVAILABILITY_20260220_150315.xlsx
PERFORMANCE_METRICS_20260220_152045.xlsx
```

---

## ⚡ Quick Commands

**Open folder:**
```batch
cd npc-reporting-system\backend\media\automated_reports
start .
```

**List files:**
```batch
cd npc-reporting-system\backend\media\automated_reports
dir *.xlsx
```

**Or just double-click:**
```
OPEN_REPORTS_FOLDER.bat
```

---

## 🔧 Troubleshooting

### Folder doesn't exist?
- Run "Run Now" button once to create it
- Backend creates folder automatically on first report

### No files in folder?
- Check backend console for errors
- Verify you have generation data in database
- Check execution history for error messages

### Can't open Excel file?
- Install Microsoft Excel, or
- Use Google Sheets (upload file), or
- Use LibreOffice Calc (free alternative)

### File is empty or has no data?
- Upload generation data first using "Upload Excel" feature
- Check if plants are active in database
- Verify date range has data

---

## 📧 Email Delivery (Optional)

If you configure email settings, reports can also be:
- ✅ Emailed to recipients automatically
- ✅ Sent on schedule (daily/weekly/monthly)
- ✅ Delivered to multiple users

Currently using console email backend (prints to console instead of sending).

---

## 🎯 Next Steps

1. **Open the folder:**
   - Double-click `OPEN_REPORTS_FOLDER.bat`

2. **View the files:**
   - Double-click any `.xlsx` file
   - Verify data is correct

3. **Test different report types:**
   - Click "Run Now" on each report type
   - Check that files are generated
   - Compare the data

4. **Check execution history:**
   - Click "History" button
   - See list of all executions
   - Note filenames and timestamps

---

## 📊 Summary

| Question | Answer |
|----------|--------|
| Are files generated? | ✅ YES, automatically |
| Where are they saved? | `backend/media/automated_reports/` |
| What format? | Excel (.xlsx) |
| When are they created? | Immediately when you click "Run Now" |
| How to access? | File Explorer or `OPEN_REPORTS_FOLDER.bat` |
| Can I download from UI? | Coming soon (next update) |

---

## 🎉 It's Working!

The "Run Now" button is fully functional:
- ✅ Generates Excel files
- ✅ Saves to correct folder
- ✅ Records execution in database
- ✅ Shows success message
- ✅ Files ready to open

**Just navigate to the folder and open the files!**
