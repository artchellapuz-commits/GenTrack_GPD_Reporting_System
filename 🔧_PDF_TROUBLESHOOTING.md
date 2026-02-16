# 🔧 PDF Export Troubleshooting Guide

## Problem: "Failed to generate PDF" error persists

You've installed the packages but still getting the error. Here's how to fix it:

---

## ✅ Solution Steps (Do ALL of these)

### Step 1: Verify Packages Are Really Installed

Run this command in the `frontend` folder:
```bash
npm list jspdf jspdf-autotable
```

**Expected output:**
```
├── jspdf@2.x.x
└── jspdf-autotable@3.x.x
```

**If you see "UNMET DEPENDENCY" or "empty":**
```bash
npm install jspdf jspdf-autotable --save
```

---

### Step 2: Clear Browser Cache

The browser might be using the old cached version of the code.

**Option A: Hard Refresh**
- Windows/Linux: `Ctrl + Shift + R` or `Ctrl + F5`
- Mac: `Cmd + Shift + R`

**Option B: Clear Cache Manually**
1. Open DevTools (F12)
2. Right-click the refresh button
3. Select "Empty Cache and Hard Reload"

**Option C: Incognito/Private Mode**
- Open your app in incognito/private browsing mode
- This uses a fresh cache

---

### Step 3: Completely Restart Dev Server

Don't just stop and start - do a FULL restart:

```bash
# Stop the server
Ctrl+C

# Clear the terminal
cls  (Windows) or clear (Mac/Linux)

# Start fresh
npm run serve
```

---

### Step 4: Check Package.json

Open `frontend/package.json` and verify these lines exist in "dependencies":

```json
{
  "dependencies": {
    "jspdf": "^2.5.1",
    "jspdf-autotable": "^3.8.2",
    ...other packages...
  }
}
```

**If they're missing**, add them manually and run:
```bash
npm install
```

---

### Step 5: Delete node_modules and Reinstall (Nuclear Option)

If nothing else works:

```bash
cd frontend

# Delete node_modules folder
rmdir /s /q node_modules  (Windows)
rm -rf node_modules       (Mac/Linux)

# Delete package-lock.json
del package-lock.json     (Windows)
rm package-lock.json      (Mac/Linux)

# Reinstall everything
npm install

# Install PDF packages specifically
npm install jspdf jspdf-autotable --save

# Start server
npm run serve
```

---

## 🔍 Diagnostic Commands

Run these to diagnose the issue:

### Check if packages exist in node_modules
```bash
cd frontend/node_modules
dir jspdf           (Windows)
ls jspdf            (Mac/Linux)
```

### Check npm configuration
```bash
npm config list
```

### Check for errors in package installation
```bash
npm install --verbose
```

---

## 🐛 Common Issues

### Issue 1: Packages installed but import fails

**Cause**: Webpack/Vue CLI not picking up new packages

**Solution**:
```bash
# Stop server
Ctrl+C

# Clear webpack cache
npm run serve -- --no-cache

# Or delete .cache folder
rmdir /s /q node_modules/.cache  (Windows)
rm -rf node_modules/.cache       (Mac/Linux)

# Restart
npm run serve
```

---

### Issue 2: "Cannot find module 'jspdf'"

**Cause**: Package not in dependencies

**Solution**:
```bash
npm install jspdf jspdf-autotable --save
```

Note the `--save` flag - this adds it to package.json

---

### Issue 3: Version conflicts

**Cause**: Incompatible package versions

**Solution**:
```bash
npm install jspdf@latest jspdf-autotable@latest --save
```

---

### Issue 4: Browser console shows import error

**Cause**: ES6 import not supported or webpack issue

**Solution**: Check browser console (F12) for specific error message

---

## 📋 Verification Checklist

After following the steps, verify:

- [ ] `npm list jspdf` shows version number
- [ ] `npm list jspdf-autotable` shows version number
- [ ] `frontend/node_modules/jspdf` folder exists
- [ ] `frontend/node_modules/jspdf-autotable` folder exists
- [ ] `frontend/package.json` includes both packages
- [ ] Dev server restarted completely
- [ ] Browser cache cleared (hard refresh)
- [ ] No console errors in browser DevTools (F12)

---

## 🎯 Alternative: Use CSV Export Instead

If PDF export continues to fail, you can use CSV export which works without additional packages:

1. Click "Export CSV" button (green button)
2. CSV file downloads
3. Open in Excel
4. Save as PDF from Excel (File → Save As → PDF)

This achieves the same result!

---

## 💡 Quick Test

To test if jspdf is working, open browser console (F12) and type:

```javascript
import('jspdf').then(module => {
  console.log('jsPDF loaded:', module);
}).catch(err => {
  console.error('jsPDF failed:', err);
});
```

If you see "jsPDF loaded", the package is working.

---

## 🚀 Last Resort: Manual Installation

If npm install keeps failing:

1. Download jspdf manually from: https://github.com/parallax/jsPDF/releases
2. Download jspdf-autotable from: https://github.com/simonbengtsson/jsPDF-AutoTable/releases
3. Place in `frontend/node_modules/` folder
4. Restart dev server

---

## 📞 Still Not Working?

If you've tried everything and it still doesn't work:

1. Check browser console (F12) for specific error messages
2. Check terminal where dev server is running for errors
3. Try a different browser
4. Check if antivirus is blocking npm
5. Check if you have write permissions in the project folder

---

## ✅ Success Indicators

You'll know it's working when:

1. No error toast appears
2. "Generating PDF..." toast shows
3. "PDF downloaded successfully!" toast appears
4. PDF file appears in Downloads folder
5. PDF opens and shows dashboard data

---

## 🎉 Final Note

The most common fix is:
1. Clear browser cache (Ctrl+Shift+R)
2. Restart dev server completely
3. Try in incognito mode

This solves 90% of cases!
