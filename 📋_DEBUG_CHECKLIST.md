# 🔍 Role-Based UI Debug Checklist

## Problem
Frontend not showing different UI for different roles (viewer1 still sees Upload and Water Nomination menu items)

---

## ✅ What's Been Fixed

### Backend
- [x] Fixed `UserProfileSerializer.get_profile()` syntax error (removed duplicate code)
- [x] Login endpoint returns full profile with role and permissions
- [x] Role checking methods in UserProfile model working correctly

### Frontend
- [x] `auth.js` has all role checking functions (getUserRole, canUploadData, isAdmin, etc.)
- [x] `AppLayout.vue` imports role checking functions
- [x] `AppLayout.vue` has v-if conditions on Upload and Water Nomination menu items
- [x] Role badge CSS styles added
- [x] Menu divider and section title styles added

---

## 🔧 What You Need To Do

### 1. Test Backend API First ⭐ IMPORTANT
```bash
# Run this to verify backend is returning correct data
TEST_LOGIN_API.bat
```

**Expected output for viewer1:**
```
Role: VIEWER
Can Upload Data: False
Can Approve Data: False
Can Manage Users: False
Can Export Data: True
```

**Expected output for operator1:**
```
Role: OPERATOR
Can Upload Data: True
Can Approve Data: False
Can Manage Users: False
Can Export Data: True
```

If backend test FAILS → Backend issue, check Django server logs
If backend test PASSES → Continue to step 2

---

### 2. Restart Backend
```bash
# Stop backend (Ctrl+C)
cd backend
python manage.py runserver
```

---

### 3. Clear Frontend Cache
```bash
# Stop frontend (Ctrl+C)
cd frontend

# Delete cache folder
rmdir /s /q node_modules\.cache

# Or manually delete: frontend\node_modules\.cache

# Restart frontend
npm run serve
```

---

### 4. Clear Browser Cache
**Option A: Hard Reload**
1. Open browser DevTools (F12)
2. Right-click the refresh button
3. Select "Empty Cache and Hard Reload"

**Option B: Clear All Cache**
1. Press Ctrl+Shift+Delete
2. Check "Cached images and files"
3. Select "All time"
4. Click "Clear data"

---

### 5. Check localStorage (Before Re-login)
Open browser console (F12) and run:
```javascript
// Check what's stored
console.log('User data:', localStorage.getItem('user'));

// Parse it
const user = JSON.parse(localStorage.getItem('user'));
console.log('Has profile?', user.profile);
console.log('Role:', user.profile?.role);
console.log('Permissions:', user.profile?.permissions);
```

**If profile is missing or role is undefined:**
→ You need to re-login to get fresh data

---

### 6. Re-Login ⭐ CRITICAL
1. Click Logout
2. Login again with `viewer1` / `test123`
3. This fetches fresh profile data from backend

---

### 7. Verify It Works
After re-login, check:

**For viewer1:**
- [ ] Role badge shows "Viewer" (blue)
- [ ] Can see: Dashboard, View Reports, Generate Report
- [ ] Cannot see: Upload Excel, Water Nomination

**For operator1:**
- [ ] Role badge shows "Operator" (green)
- [ ] Can see: Dashboard, Upload Excel, View Reports, Generate Report, Water Nomination
- [ ] Cannot see: Admin Panel

**For manager1:**
- [ ] Role badge shows "Manager" (orange)
- [ ] Can see: Dashboard, Upload Excel, View Reports, Generate Report, Water Nomination
- [ ] Cannot see: Admin Panel (unless is_staff=True)

---

## 🐛 Still Not Working?

### Debug in Browser Console
```javascript
// Check if auth.js functions are working
import { getUserRole, canUploadData } from '@/utils/auth';

console.log('Current role:', getUserRole());
console.log('Can upload:', canUploadData());

// Check user data structure
const user = JSON.parse(localStorage.getItem('user'));
console.log('Full user object:', user);
```

### Check Vue DevTools
1. Install Vue DevTools extension
2. Open DevTools → Vue tab
3. Find AppLayout component
4. Check data properties:
   - `userRole` should be 'VIEWER', 'OPERATOR', etc.
   - `canUpload` should be true/false
   - `isAdminUser` should be true/false

### Check Network Tab
1. Open DevTools → Network tab
2. Login with viewer1
3. Find the `/api/auth/login/` request
4. Check Response:
   ```json
   {
     "access": "...",
     "refresh": "...",
     "user": {
       "username": "viewer1",
       "profile": {
         "role": "VIEWER",
         "permissions": {
           "can_upload_data": false,
           ...
         }
       }
     }
   }
   ```

If `profile` is missing from response → Backend issue
If `profile` is present but UI not updating → Frontend cache issue

---

## 📝 Quick Reference

### Test Users
| Username | Password | Role | Can Upload | Can Approve |
|----------|----------|------|------------|-------------|
| viewer1 | test123 | VIEWER | ❌ | ❌ |
| operator1 | test123 | OPERATOR | ✅ | ❌ |
| manager1 | test123 | MANAGER | ✅ | ✅ |

### Menu Visibility Matrix
| Menu Item | Viewer | Operator | Manager | Admin |
|-----------|--------|----------|---------|-------|
| Dashboard | ✅ | ✅ | ✅ | ✅ |
| Upload Excel | ❌ | ✅ | ✅ | ✅ |
| View Reports | ✅ | ✅ | ✅ | ✅ |
| Generate Report | ✅ | ✅ | ✅ | ✅ |
| Water Nomination | ❌ | ✅ | ✅ | ✅ |
| Admin Panel | ❌ | ❌ | ❌ | ✅ |
| Audit Logs | ❌ | ❌ | ❌ | ✅ |

---

## 🎯 Most Common Issues

1. **Backend not restarted** → Serializer fix not applied
2. **Frontend cache not cleared** → Old compiled code still running
3. **Browser cache not cleared** → Old JavaScript files cached
4. **Not re-logged in** → Old user data without profile in localStorage

**All 4 must be done for changes to appear!**

---

## 🚀 Automated Fix

Run this to clear cache automatically:
```bash
RESTART_EVERYTHING.bat
```

Then manually:
1. Stop and restart backend
2. Stop and restart frontend
3. Hard reload browser (Ctrl+Shift+R)
4. Logout and login again
