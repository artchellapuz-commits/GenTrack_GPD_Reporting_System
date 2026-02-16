# 🔧 Pulangi 4 Upload Troubleshooting

## Problem: "Error: Upload failed" when uploading Excel for Pulangi 4

### ✅ Pulangi 4 is Installed Correctly
- Plant: Pulangi 4 Hydroelectric Plant
- Code: PULANGI4
- Units: 3 (Unit 1, 2, 3 - each 85 MW)
- Location: Bukidnon
- Total Capacity: 255 MW

### 🔍 Common Causes and Solutions

#### 1. Backend Server Not Restarted ⚠️ MOST COMMON

**Problem**: Backend server is running with old code (before Pulangi 4 was added)

**Solution**:
```bash
# Stop the backend server (Ctrl+C in the terminal)
# Then restart it:
cd npc-reporting-system/backend
venv\Scripts\activate
python manage.py runserver
```

**Or use the batch file**:
- Close the backend terminal
- Double-click `START_BACKEND.bat`

---

#### 2. Excel File Has Wrong Number of Units ⚠️ VERY COMMON

**Problem**: Your Excel file has 4 units (like Agus plants), but Pulangi 4 only has 3 units

**Agus Plants** (WRONG for Pulangi 4):
- Agus 1: 4 units
- Agus 2: 4 units  
- Agus 4: 4 units
- Agus 5: 2 units
- Agus 6: 4 units
- Agus 7: 4 units

**Pulangi 4** (CORRECT):
- Pulangi 4: **3 units only!**

**Solution**:
1. Use the sample file: `SAMPLE_PULANGI4.xlsx`
2. Or modify your file to have only 3 units
3. Remove all Unit 4 data if present

---

#### 3. Missing or Incorrect Column Names

**Required Columns** (case-insensitive):
1. Date
2. Unit Number
3. Generation kWh
4. Operating Hours
5. Availability Hours
6. Forced Outage Hours
7. Scheduled Outage Hours

**Common Mistakes**:
- ❌ "Gen kWh" instead of "Generation kWh"
- ❌ "Unit" instead of "Unit Number"
- ❌ "Hours" instead of "Operating Hours"

**Solution**: Use exact column names from `SAMPLE_PULANGI4.xlsx`

---

#### 4. Invalid Unit Numbers

**Problem**: Excel file has Unit 0, Unit 4, or Unit 5

**Valid Unit Numbers for Pulangi 4**: 1, 2, 3 only

**Solution**: Check your Excel file only references Unit 1, 2, and 3

---

#### 5. Invalid Date Format

**Wrong Formats**:
- ❌ 02/13/2026
- ❌ 13-Feb-2026
- ❌ February 13, 2026

**Correct Format**:
- ✅ 2026-02-13 (YYYY-MM-DD)

**Solution**: Format all dates as YYYY-MM-DD

---

### 📋 Pre-Upload Checklist

Before uploading, verify:

- [ ] Backend server has been restarted after installing Pulangi 4
- [ ] Excel file has exactly 3 units (not 4)
- [ ] All 7 required columns are present with correct names
- [ ] Unit numbers are 1, 2, or 3 only
- [ ] Dates are in YYYY-MM-DD format
- [ ] All hours are between 0 and 24
- [ ] All generation values are positive numbers
- [ ] No empty cells in required columns
- [ ] File is saved as .xlsx format

---

### 🧪 Test with Sample File

1. **Use the provided sample**:
   ```
   File: SAMPLE_PULANGI4.xlsx
   Location: npc-reporting-system/
   ```

2. **Upload the sample file**:
   - Go to "Upload Excel" page
   - Select "Pulangi 4 Hydroelectric Plant"
   - Choose `SAMPLE_PULANGI4.xlsx`
   - Click "Upload Report"

3. **If sample works**:
   - Your system is configured correctly
   - Problem is with your Excel file format
   - Compare your file with the sample

4. **If sample fails**:
   - Backend server needs restart
   - Check backend terminal for error messages

---

### 🔍 How to See Detailed Error Messages

#### Method 1: Backend Terminal
1. Look at the terminal where backend is running
2. Error messages will show the exact problem
3. Common errors:
   - "Unit X not found" → Wrong unit number
   - "Missing required columns" → Column names don't match
   - "Invalid date format" → Date format is wrong

#### Method 2: Browser Console
1. Press F12 to open Developer Tools
2. Go to "Console" tab
3. Look for red error messages
4. Check "Network" tab for API response

#### Method 3: Frontend Error Message
- The error message in the UI might show more details
- Look for specific column names or validation errors

---

### 📝 Example: Correct Excel File Structure

```
| Date       | Unit Number | Generation kWh | Operating Hours | Availability Hours | Forced Outage Hours | Scheduled Outage Hours |
|------------|-------------|----------------|-----------------|--------------------|--------------------|------------------------|
| 2026-02-13 | 1           | 1800000        | 22.5            | 23.0               | 0.5                | 0.5                    |
| 2026-02-13 | 2           | 1850000        | 23.0            | 23.5               | 0.5                | 0.0                    |
| 2026-02-13 | 3           | 1900000        | 23.5            | 24.0               | 0.0                | 0.0                    |
```

**Key Points**:
- 3 rows per date (one for each unit)
- Unit numbers: 1, 2, 3
- Date format: YYYY-MM-DD
- All numeric values are valid

---

### 🚀 Quick Fix Steps

1. **Restart Backend**:
   ```bash
   # Stop backend (Ctrl+C)
   # Start again:
   cd npc-reporting-system/backend
   venv\Scripts\activate
   python manage.py runserver
   ```

2. **Use Sample File**:
   - Upload `SAMPLE_PULANGI4.xlsx` first
   - If it works, your system is fine
   - Then fix your actual file

3. **Check Your File**:
   - Open `SAMPLE_PULANGI4.xlsx`
   - Compare with your file
   - Match the structure exactly
   - Remove Unit 4 if present

4. **Try Again**:
   - Select Pulangi 4 from dropdown
   - Upload your corrected file
   - Check backend terminal for errors

---

### 📞 Still Having Issues?

1. **Check Backend Logs**:
   - Look at backend terminal output
   - Copy the full error message

2. **Verify Installation**:
   ```bash
   cd npc-reporting-system/backend
   venv\Scripts\activate
   python manage.py shell
   ```
   ```python
   from reports.models import Plant, Unit
   p = Plant.objects.get(code='PULANGI4')
   print(f"Plant: {p.name}")
   print(f"Units: {p.units.count()}")
   ```
   Should show: "Units: 3"

3. **Re-run Installation**:
   ```bash
   cd npc-reporting-system/backend
   venv\Scripts\activate
   python add_pulangi4.py
   ```

4. **Check Sample File**:
   - If `SAMPLE_PULANGI4.xlsx` doesn't exist:
   ```bash
   cd npc-reporting-system
   python CREATE_PULANGI4_SAMPLE.py
   ```

---

### ✅ Success Indicators

When upload works correctly, you should see:
- ✅ "X records imported successfully" message
- ✅ File appears in "Recent Uploads" table
- ✅ Status shows "COMPLETED"
- ✅ Records count shows number of rows imported
- ✅ Pulangi 4 data appears in Dashboard
- ✅ Can filter by Pulangi 4 in "View Reports"

---

### 📚 Related Files

- `SAMPLE_PULANGI4.xlsx` - Sample Excel file for Pulangi 4
- `PULANGI4_UPLOAD_GUIDE.md` - Detailed upload instructions
- `CREATE_PULANGI4_SAMPLE.py` - Script to create sample file
- `ADD_PULANGI4.bat` - Installation script

---

**Remember**: Pulangi 4 has 3 units, not 4! This is the most common mistake.
