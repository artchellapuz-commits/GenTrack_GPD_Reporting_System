# 📤 How to Upload Excel File - Step by Step

## ✓ The Error You're Seeing

You're trying to upload a file with the wrong format. The system needs specific columns.

## ✓ Solution: Use the Correct File

**File Location:**
```
C:\Users\eladiong\Desktop\OJT Intern\npc-reporting-system\CORRECT_SAMPLE_AGUS1.xlsx
```

## ✓ Upload Steps

### Step 1: Open the System
- Go to: `http://192.168.120.87:8080`
- Or: `http://localhost:8080`

### Step 2: Navigate to Upload
- Click the **"Upload"** button in the top navigation

### Step 3: Select Plant
- Click on "Select Hydro-electric Power Plant" dropdown
- Choose: **AGUS1 - Agus 1 Hydroelectric Plant**
- You'll see the hover effect (light blue background) when you move your mouse over plants

### Step 4: Choose File
- Click "Choose Excel file..."
- Navigate to: `C:\Users\eladiong\Desktop\OJT Intern\npc-reporting-system\`
- Select: `CORRECT_SAMPLE_AGUS1.xlsx`

### Step 5: Upload
- Click the blue **"Upload Report"** button
- Wait for the upload to complete

### Step 6: Success!
- You should see: ✅ **"40 records imported successfully."**
- The file will appear in the "Recent Uploads" table below

## ✓ What's in the Correct File?

| Column | Example Value | Description |
|--------|---------------|-------------|
| Date | 2026-02-01 | Report date (YYYY-MM-DD) |
| Unit Number | 1 | Generator unit number |
| Generation kWh | 21000 | Power generated in kWh |
| Operating Hours | 22 | Hours the unit operated |
| Availability Hours | 24 | Hours the unit was available |
| Forced Outage Hours | 0 | Unplanned downtime hours |
| Scheduled Outage Hours | 0 | Planned maintenance hours |

## ✓ File Contents

- **40 records** total
- **10 days** of data (Feb 1-10, 2026)
- **4 units** (Unit 1, 2, 3, 4)
- **Plant:** AGUS1

## ❌ Common Mistakes

1. **Wrong file format** - Make sure it's an .xlsx file
2. **Missing columns** - All 7 columns must be present
3. **Wrong column names** - Use the exact names shown above
4. **Wrong plant selected** - The sample file is for AGUS1 only

## ✓ After Upload

You can:
- View the uploaded data in the **"Reports"** section
- Generate Excel reports in the **"Generate"** section
- Delete uploads using the trash icon in the "Recent Uploads" table

## 🆘 Still Having Issues?

Check:
1. Both servers are running (backend and frontend)
2. You're using the CORRECT_SAMPLE_AGUS1.xlsx file
3. You selected AGUS1 as the plant
4. The file hasn't been modified
