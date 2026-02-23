# 🔍 Diagnose: Why No Reports Are Showing

## Quick Diagnostic Steps

### Step 1: Open Browser Console
1. Press **F12** on your keyboard
2. Click the **Console** tab
3. Refresh the page (`http://localhost:8080/scheduled-reports`)
4. Look for these messages:

**What you should see:**
```
Loading reports from: http://localhost:8000/api/scheduled-reports/
API Response: {data: Array(3), status: 200, ...}
Response data: [{id: 1, name: "...", ...}, {...}, {...}]
Processed data: (3) [{...}, {...}, {...}]
Final scheduledReports: (3) [{...}, {...}, {...}]
```

**If you see errors instead:**
- ❌ `Failed to load reports: Error: Network Error` → Backend not running
- ❌ `401 Unauthorized` → Not logged in or token expired
- ❌ `404 Not Found` → API endpoint doesn't exist
- ❌ `CORS error` → CORS not configured

### Step 2: Check Backend is Running
Open a new terminal and run:
```bash
cd backend
python manage.py runserver
```

You should see:
```
Starting development server at http://127.0.0.1:8000/
```

### Step 3: Test API Directly in Browser
Open a new browser tab and go to:
```
http://localhost:8000/api/scheduled-reports/
```

**Expected Result:**
You should see JSON data with 3 reports:
```json
[
  {
    "id": 1,
    "name": "Report 1",
    "report_type": "GENERATION_SUMMARY",
    ...
  },
  {
    "id": 2,
    ...
  },
  {
    "id": 3,
    ...
  }
]
```

**If you see:**
- ❌ "Connection refused" → Backend not running
- ❌ "Authentication credentials were not provided" → Need to login first
- ❌ Empty array `[]` → No reports in database

### Step 4: Check if You're Logged In
In browser console, type:
```javascript
localStorage.getItem('access_token')
```

**Expected:** Should return a long string (JWT token)  
**If null:** You need to login first

### Step 5: Check Database
In backend terminal:
```bash
cd backend
python manage.py shell -c "from reports.models_scheduled import ScheduledReport; print(ScheduledReport.objects.count())"
```

**Expected:** Should show `3`  
**If 0:** Database is empty, need to create reports

---

## Common Issues & Solutions

### Issue 1: Backend Not Running
**Symptom:** Console shows "Network Error"  
**Solution:**
```bash
cd backend
python manage.py runserver
```

### Issue 2: Not Logged In
**Symptom:** Console shows "401 Unauthorized"  
**Solution:**
1. Go to `http://localhost:8080/login`
2. Login with your credentials
3. Go back to `/scheduled-reports`

### Issue 3: CORS Error
**Symptom:** Console shows CORS policy error  
**Solution:** Check `backend/npc_reporting/settings.py`:
```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:8080",
    "http://127.0.0.1:8080",
]
```

### Issue 4: Database Empty
**Symptom:** API returns empty array `[]`  
**Solution:** Create a test report:
```bash
cd backend
python manage.py shell
```
Then in Python shell:
```python
from reports.models_scheduled import ScheduledReport
from django.contrib.auth.models import User

user = User.objects.first()
ScheduledReport.objects.create(
    name="Test Report",
    report_type="GENERATION_SUMMARY",
    frequency="DAILY",
    schedule_time="08:00",
    format="EXCEL",
    date_range_days=30,
    status="ACTIVE",
    created_by=user
)
print("Report created!")
```

### Issue 5: Service Worker Errors
**Symptom:** Red errors about service worker in console  
**Solution:** These are warnings, not the main issue. Ignore for now.

---

## What to Do Right Now

1. **Open browser console (F12)**
2. **Refresh the page**
3. **Look for the console.log messages I added**
4. **Tell me what you see**

The console will now show exactly what's happening:
- Is the API being called?
- What response is coming back?
- Is the data being processed correctly?

---

## Quick Test Commands

### Test 1: Check Backend
```bash
curl http://localhost:8000/api/plants/
```
Should return JSON data.

### Test 2: Check Scheduled Reports (with auth)
First get your token from browser console:
```javascript
localStorage.getItem('access_token')
```

Then test:
```bash
curl -H "Authorization: Bearer YOUR_TOKEN_HERE" http://localhost:8000/api/scheduled-reports/
```

### Test 3: Check Database
```bash
cd backend
python manage.py shell -c "from reports.models_scheduled import ScheduledReport; for r in ScheduledReport.objects.all(): print(f'{r.id}: {r.name}')"
```

---

## Next Steps

After you check the browser console and tell me what you see, I can:
1. Fix the specific error
2. Create test data if database is empty
3. Fix authentication if that's the issue
4. Fix CORS if that's the problem

**The console logs will tell us exactly what's wrong!**
