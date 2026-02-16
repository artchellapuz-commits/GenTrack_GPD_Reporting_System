# ✅ SOLUTION: Pulangi 4 Upload Error

## Problem
Getting "Error: Upload failed" when trying to upload Excel file for Pulangi 4.

## Root Cause
**The backend server is running with old code** (from before Pulangi 4 was added). Even though Pulangi 4 is in the database, the running server doesn't know about it yet.

## Verification
✅ Database check passed:
- Plant: Pulangi 4 Hydroelectric Power Plant
- Code: PULANGI4
- Units: 3 (Unit 1, 2, 3)
- Plant Choices includes: PULANGI4

## Solution

### Step 1: Restart Backend Server (REQUIRED)

**Option A - Using Batch File (Easiest)**:
1. Go to the terminal where backend is running
2. Press `Ctrl + C` to stop it
3. Double-click `START_BACKEND.bat` to restart

**Option B - Manual**:
```bash
# In the backend terminal, press Ctrl+C to stop
# Then run:
cd npc-reporting-system\backend
venv\Scripts\activate
python manage.py runserver
```

### Step 2: Refresh Browser
1. Press `F5` or `Ctrl + F5` to refresh the page
2. This ensures the frontend gets the updated plant list

### Step 3: Test Upload
1. Go to "Upload Excel" page
2. Select "Pulangi 4 Hydroelectric Power Plant" from dropdown
3. Choose file: `SAMPLE_PULANGI4.xlsx`
4. Click "Upload Report"
5. Should see: "21 records imported successfully"

## Why This Happens

When you add a new plant:
1. ✅ Database is updated (migration ran)
2. ✅ Plant record is created
3. ❌ But running server still has old code in memory

The server needs to restart to:
- Reload the models.py file
- Load the updated PLANT_CHOICES
- Recognize PULANGI4 as a valid plant code

## Verification After Restart

After restarting backend, you should be able to:
- ✅ See "Pulangi 4 Hydroelectric Power Plant" in upload dropdown
- ✅ Upload Excel files for Pulangi 4
- ✅ See Pulangi 4 data in Dashboard
- ✅ Filter by Pulangi 4 in View Reports
- ✅ Include Pulangi 4 in generated reports

## Common Mistakes

### ❌ Mistake 1: Not Restarting Backend
- **Symptom**: Upload fails with 400 error
- **Solution**: Restart backend server

### ❌ Mistake 2: Excel File Has 4 Units
- **Symptom**: "Unit 4 not found" error
- **Solution**: Pulangi 4 has only 3 units, not 4

### ❌ Mistake 3: Wrong Column Names
- **Symptom**: "Missing required columns" error
- **Solution**: Use exact column names from sample file

## Sample File

Use the provided sample file to test:
- **File**: `SAMPLE_PULANGI4.xlsx`
- **Contains**: 7 days of data for 3 units
- **Total Records**: 21 (7 days × 3 units)

If sample file doesn't exist, create it:
```bash
cd npc-reporting-system
python CREATE_PULANGI4_SAMPLE.py
```

## Excel File Requirements for Pulangi 4

### Required Columns:
1. Date (YYYY-MM-DD format)
2. Unit Number (1, 2, or 3 only)
3. Generation kWh
4. Operating Hours (0-24)
5. Availability Hours (0-24)
6. Forced Outage Hours (0-24)
7. Scheduled Outage Hours (0-24)

### Important:
- **3 units only** (not 4 like Agus plants)
- Unit numbers must be 1, 2, or 3
- Each unit has 85 MW capacity
- Total plant capacity: 255 MW

## Testing Checklist

After restarting backend:

- [ ] Backend server restarted successfully
- [ ] Browser refreshed (F5)
- [ ] Can see Pulangi 4 in upload dropdown
- [ ] Sample file uploads successfully
- [ ] See "21 records imported" message
- [ ] Pulangi 4 appears in Dashboard
- [ ] Can filter by Pulangi 4 in View Reports

## Still Having Issues?

### Check Backend Logs
Look at the terminal where backend is running for error messages.

### Verify Installation
```bash
cd npc-reporting-system
.\DIAGNOSE_PULANGI4.bat
```

Should show:
- Plant: Pulangi 4 Hydroelectric Power Plant
- Units: 3
- PULANGI4 in Plant Choices list

### Re-run Installation
If Pulangi 4 is missing:
```bash
cd npc-reporting-system
.\ADD_PULANGI4.bat
```

## Success Indicators

When everything works:
- ✅ Upload shows "X records imported successfully"
- ✅ File appears in "Recent Uploads" with status "COMPLETED"
- ✅ Pulangi 4 card shows data in Dashboard
- ✅ Can view Pulangi 4 reports in "View Reports"
- ✅ Can generate reports including Pulangi 4

## Summary

**The fix is simple**: Restart the backend server!

The database is correct, Pulangi 4 is installed, but the running server needs to restart to load the new code.

---

**Quick Fix**: Stop backend (Ctrl+C) → Run `START_BACKEND.bat` → Refresh browser → Upload works!
