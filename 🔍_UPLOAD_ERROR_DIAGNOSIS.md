# 🔍 Upload Error Diagnosis

## The Error You're Seeing

```
❌ POST http://localhost:8000/api/uploaded-files/upload/ 400 (Bad Request)
```

This error appears **4 times**, which means the upload was attempted 4 times.

## Possible Causes

### 1. **Multiple Button Clicks**
You might be clicking the "Upload Report" button multiple times quickly.

**Solution**: Wait for the first upload to complete before clicking again.

### 2. **Missing Required Fields**
The backend requires:
- `file` - The Excel file
- `plant_code` - The plant code (e.g., "AGUS1", "AGUS2")

**Check**: Make sure you selected a plant from the dropdown before uploading.

### 3. **Invalid File Format**
The file must be:
- `.xlsx` format (Excel 2007+)
- Maximum 25MB
- Valid Excel structure with required columns

**Check**: Make sure you're uploading a valid Excel file.

### 4. **Duplicate File**
The system checks for duplicate files using SHA256 checksum.

**Error message**: "This file has already been uploaded"

**Solution**: If you want to upload the same file again, you need to delete or archive the previous upload first.

### 5. **Plant Not Found**
The plant code you selected doesn't exist in the database.

**Error message**: "Plant not found"

**Solution**: Make sure the plants are loaded. Check the dropdown - it should show 7 plants.

## How to See the Actual Error Message

### Method 1: Check Browser Console (Detailed)

1. Open Browser DevTools (F12)
2. Go to **Console** tab
3. Look for red error messages
4. Click on the error to expand it
5. Look for `response.data.error` or `response.data`

### Method 2: Check Network Tab (Most Detailed)

1. Open Browser DevTools (F12)
2. Go to **Network** tab
3. Click on one of the failed `upload/` requests
4. Click on **Response** tab
5. You'll see the exact error message from the backend

Example responses:
```json
{"error": "This file has already been uploaded"}
{"error": "Plant not found"}
{"error": "Missing required columns: ..."}
{"file": ["This field is required"]}
{"plant_code": ["This field is required"]}
```

### Method 3: Check Backend Terminal

1. Go to the terminal where the backend is running
2. Look for error messages or stack traces
3. The backend prints detailed errors there

## Common Error Messages & Solutions

### Error: "This file has already been uploaded"
**Cause**: You're trying to upload a file that's already in the system (same checksum).

**Solution**:
1. Go to Upload page
2. Find the file in "Recent Uploads"
3. Either:
   - Archive it (if you want to keep it)
   - Delete it (if you want to replace it)
4. Then upload the new file

### Error: "Plant not found"
**Cause**: The plant code doesn't exist in the database.

**Solution**:
1. Check if plants are loading in the dropdown
2. If dropdown is empty, restart the backend
3. Make sure you have 7 plants in the database

### Error: "Missing required columns"
**Cause**: The Excel file doesn't have the required column structure.

**Solution**:
1. Download the correct template from the Upload page
2. Use the template to format your data
3. Make sure all required columns are present

### Error: "File size exceeds limit"
**Cause**: File is larger than 25MB.

**Solution**:
1. Compress the Excel file
2. Remove unnecessary sheets or data
3. Split into multiple files if needed

## Quick Fixes

### Fix 1: Clear Browser Cache
```
1. Press Ctrl+Shift+R (hard refresh)
2. Or clear browser cache completely
3. Reload the page
```

### Fix 2: Restart Backend
```bash
# Stop backend (Ctrl+C)
# Then restart:
cd backend
python manage.py runserver
```

### Fix 3: Check File Selection
```
1. Make sure you selected a plant from dropdown
2. Make sure you selected an Excel file
3. Both fields should show green checkmarks
4. Then click "Upload Report"
```

### Fix 4: Don't Click Multiple Times
```
1. Click "Upload Report" ONCE
2. Wait for the progress bar
3. Wait for "Compiled successfully" message
4. Don't click again until upload completes
```

## Testing Steps

### Step 1: Verify Plant Selection
1. Go to Upload page
2. Click on "Select Hydro-Electric Power Plant" dropdown
3. You should see 7 plants:
   - Agus 1
   - Agus 2
   - Agus 3
   - Agus 4
   - Agus 5
   - Agus 6
   - Pulangi 4
4. Select one plant

### Step 2: Verify File Selection
1. Click "Drag & drop your Excel file here" or browse
2. Select a `.xlsx` file
3. You should see:
   - File name
   - File size
   - Green checkmark "Valid Excel file"

### Step 3: Upload
1. Click "Upload Report" button ONCE
2. Wait for progress bar (0% → 100%)
3. Wait for success message
4. File should appear in "Recent Uploads"

## If Error Persists

### Check Backend Logs
```bash
# In the backend terminal, you should see:
# - POST request to /api/uploaded-files/upload/
# - Status code (200, 400, 500, etc.)
# - Error message if any
```

### Check Frontend Console
```javascript
// Open browser console (F12)
// Look for errors like:
// - "Network Error"
// - "400 Bad Request"
// - Detailed error object
```

### Check Network Tab
```
1. F12 → Network tab
2. Click failed request
3. Check:
   - Request Headers (what was sent)
   - Request Payload (file and plant_code)
   - Response (error message)
```

## Most Likely Cause

Based on the screenshot showing **4 identical errors**, the most likely cause is:

**You clicked the "Upload Report" button 4 times quickly**

This happens when:
- The button doesn't disable immediately
- You think it didn't work and click again
- Each click triggers a new upload attempt

**Solution**:
1. Click the button ONCE
2. Wait for the progress bar to appear
3. Don't click again until upload completes
4. The button should disable during upload

## Need More Help?

If the error persists:

1. **Take a screenshot** of:
   - Browser console (F12 → Console tab)
   - Network tab showing the error response
   - Backend terminal output

2. **Check** the exact error message in the Response tab

3. **Share** the error message so I can provide a specific fix

---

**Most likely you just need to click the button once and wait!** 🎯
