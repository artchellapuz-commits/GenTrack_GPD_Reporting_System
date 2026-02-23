# 📍 Where to Find the "Run Now" Button

## Step-by-Step Visual Guide

### Step 1: Navigate to Automated Reports Page

**In the Sidebar Menu:**
```
┌─────────────────────────────┐
│  NPC System                 │
├─────────────────────────────┤
│  🏠 Dashboard               │
│  📤 Upload Excel            │
│  📊 View Reports            │
│  📥 Generate Report         │
│  📅 Water Nomination        │
│                             │
│  Analytics & Automation     │  ← Look for this section
│  ─────────────────────────  │
│  📈 Advanced Analytics      │
│  🕐 Automated Reports       │  ← CLICK HERE!
│                             │
└─────────────────────────────┘
```

**OR** type in browser:
```
http://localhost:8080/scheduled-reports
```

---

### Step 2: You'll See Report Cards

Each scheduled report appears as a card like this:

```
┌─────────────────────────────────────────────────────────────┐
│  Daily Generation Report                        [ACTIVE]    │
│  Generation Summary                                         │
│                                                             │
│  🕐 Daily at 08:00                                         │
│  📅 Next run: Feb 20, 2026 8:00 AM                        │
│  📧 3 recipients                                           │
│  ✓ 45 executions                                          │
│                                                             │
│  ┌─────────┐ ┌──────┐ ┌───────┐ ┌──────────┐            │
│  │ History │ │ Edit │ │ Pause │ │ Run Now  │  ← HERE!   │
│  └─────────┘ └──────┘ └───────┘ └──────────┘            │
└─────────────────────────────────────────────────────────────┘
```

---

### Step 3: The "Run Now" Button Location

**The "Run Now" button is:**
- ✅ At the bottom of each report card
- ✅ On the right side (last button)
- ✅ Blue colored (primary button)
- ✅ Has a play icon (▶️) next to the text

**Button appearance:**
```
┌──────────────────┐
│  ▶️  Run Now     │  ← Blue button with play icon
└──────────────────┘
```

---

## What You'll See on the Page

### If You Have Reports (You have 3):

```
╔═══════════════════════════════════════════════════════════╗
║                    Automated Reports                       ║
║                                                           ║
║  [+ Schedule New Report]                                  ║
╚═══════════════════════════════════════════════════════════╝

┌─────────────────────────────────────────────────────────┐
│  Report #1                                   [ACTIVE]   │
│  Generation Summary                                     │
│  🕐 Daily at 08:00                                     │
│  📅 Next run: Feb 20, 2026 8:00 AM                    │
│  📧 3 recipients  |  ✓ 45 executions                  │
│  [History] [Edit] [Pause] [▶️ Run Now]  ← HERE        │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│  Report #2                                   [ACTIVE]   │
│  Capacity Factor Analysis                              │
│  🕐 Weekly at 09:00                                    │
│  📅 Next run: Feb 24, 2026 9:00 AM                    │
│  📧 5 recipients  |  ✓ 12 executions                  │
│  [History] [Edit] [Pause] [▶️ Run Now]  ← HERE        │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│  Report #3                                   [PAUSED]   │
│  Monthly Performance Report                            │
│  🕐 Monthly at 10:00                                   │
│  📅 Next run: Mar 1, 2026 10:00 AM                    │
│  📧 10 recipients  |  ✓ 3 executions                  │
│  [History] [Edit] [Activate] [▶️ Run Now]  ← HERE     │
└─────────────────────────────────────────────────────────┘
```

---

## What Happens When You Click "Run Now"

### 1. Click the Button
```
[▶️ Run Now]  ← Click this
```

### 2. System Response
```
✅ Alert appears: "Report execution started"
```

### 3. Backend Processing
- Fetches data from database
- Generates Excel/PDF file
- Saves to `backend/media/automated_reports/`
- Creates execution record
- (Would send email if configured)

### 4. Check Results
Click the **[History]** button to see the execution record:
```
┌─────────────────────────────────────────────────────┐
│  Execution History                                  │
├─────────────────────────────────────────────────────┤
│  ✅ Feb 20, 2026 2:30 PM - SUCCESS                 │
│     File: report_123.xlsx                          │
│     Duration: 2.5 seconds                          │
│                                                     │
│  ✅ Feb 19, 2026 8:00 AM - SUCCESS                 │
│     File: report_122.xlsx                          │
│     Duration: 2.3 seconds                          │
└─────────────────────────────────────────────────────┘
```

---

## Troubleshooting: Can't Find the Button?

### Issue 1: Page is Empty
**Problem**: No reports showing  
**Solution**: You need to create a report first
```
Click [+ Schedule New Report] button at the top
```

### Issue 2: Don't See "Automated Reports" in Menu
**Problem**: Menu item missing  
**Possible Causes**:
1. Not logged in as Manager or Admin
2. Frontend not updated
3. Need to refresh page

**Solution**:
```bash
# Check your role
- Login as admin user
- Or ask admin to change your role to Manager

# Refresh frontend
cd frontend
npm run serve
```

### Issue 3: Button is Grayed Out
**Problem**: Button disabled  
**Cause**: Backend not running  
**Solution**:
```bash
cd backend
python manage.py runserver
```

---

## Quick Test Right Now

### 1. Open Browser
```
http://localhost:8080/scheduled-reports
```

### 2. Look for This Layout
```
Header: "Automated Reports"
Button: "+ Schedule New Report"
Cards: 3 report cards (you have 3 in database)
```

### 3. Scroll Down on Any Card
```
You'll see 4 buttons at the bottom:
[History] [Edit] [Pause/Activate] [Run Now]
                                    ^^^^^^^^
                                    This one!
```

### 4. Click "Run Now"
```
- Alert will show: "Report execution started"
- Check browser console for activity
- Check backend terminal for processing logs
```

---

## Visual Reference: Button Styles

The "Run Now" button looks like this in the code:

```vue
<button @click="runNow(report)" class="btn-primary">
  <i class="pi pi-play"></i> Run Now
</button>
```

**Styling**:
- Background: Blue (#3b82f6)
- Text: White
- Icon: Play symbol (▶️)
- Hover: Darker blue
- Cursor: Pointer (hand icon)

---

## Alternative: If You Still Can't Find It

### Option 1: Check Browser Console
1. Press F12 to open DevTools
2. Go to Console tab
3. Type: `window.location.href = '/scheduled-reports'`
4. Press Enter

### Option 2: Direct API Test
Open browser and go to:
```
http://localhost:8000/api/scheduled-reports/
```

You should see JSON with your 3 reports. Each report has an `id`.

To run report with id=1:
```
POST http://localhost:8000/api/scheduled-reports/1/run/
```

### Option 3: Check if Page Loaded
Look at the page title in browser tab:
```
Should say: "Automated Reports - NPC System"
```

---

## Summary

**Location**: `/scheduled-reports` page  
**Position**: Bottom of each report card  
**Appearance**: Blue button with play icon  
**Text**: "Run Now"  
**Action**: Generates report immediately

**You have 3 reports in database, so you should see 3 "Run Now" buttons - one on each card!**

---

## Need Help?

If you still can't find it:
1. Take a screenshot of what you see
2. Check if backend is running
3. Check browser console for errors
4. Verify you're logged in as Manager or Admin
