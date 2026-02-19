# 🔄 How to See Role-Based UI Changes

## ✅ Backend is Ready!

The API now returns role and permission data correctly:

```
✓ viewer1   - VIEWER role, cannot upload/approve
✓ operator1 - OPERATOR role, can upload, cannot approve  
✓ manager1  - MANAGER role, can upload and approve
```

---

## 🚀 Steps to See the Changes

### 1. Start the Backend

```bash
cd backend
python manage.py runserver
```

Backend will run on: `http://localhost:8000`

### 2. Start the Frontend

Open a NEW terminal:

```bash
cd frontend
npm run serve
```

Frontend will run on: `http://localhost:8080` or `http://localhost:8081`

### 3. Clear Browser Cache

**IMPORTANT:** Clear your browser cache or use Incognito/Private mode

Why? The old user data might be cached in localStorage.

**How to clear:**
- Chrome: F12 → Application → Local Storage → Clear
- Firefox: F12 → Storage → Local Storage → Clear
- Or just use Incognito/Private window

### 4. Login with Different Users

**Test as VIEWER:**
```
Username: viewer1
Password: test123
```

**What you'll see:**
- ✅ Dashboard
- ✅ View Reports  
- ✅ Generate Report
- ❌ Upload Excel (HIDDEN)
- ❌ Water Nomination (HIDDEN)
- Blue "Viewer" badge in sidebar

---

**Test as OPERATOR:**
```
Username: operator1
Password: test123
```

**What you'll see:**
- ✅ Dashboard
- ✅ Upload Excel (SHOWN)
- ✅ View Reports
- ✅ Generate Report
- ✅ Water Nomination (SHOWN)
- Green "Operator" badge in sidebar
- Shows assigned plant: Agus 1

---

**Test as MANAGER:**
```
Username: manager1
Password: test123
```

**What you'll see:**
- ✅ Dashboard
- ✅ Upload Excel (SHOWN)
- ✅ View Reports
- ✅ Generate Report
- ✅ Water Nomination (SHOWN)
- Orange "Manager" badge in sidebar
- Can access all plants

---

## 🔍 What to Look For

### In the Sidebar:

1. **Role Badge** - Color-coded badge showing user role
   - Blue = Viewer
   - Green = Operator
   - Orange = Manager
   - Red = Admin

2. **Menu Items** - Different items based on role
   - Viewer: No Upload or Water Nomination
   - Operator: Has Upload and Water Nomination
   - Manager: Has all operational features
   - Admin: Has Admin section at bottom

3. **User Info** - Shows username and role

### In the Console (F12):

When you login, check the console for:
```javascript
{
  "profile": {
    "role": "OPERATOR",
    "permissions": {
      "can_upload_data": true,
      "can_approve_data": false,
      ...
    }
  }
}
```

---

## 🐛 Troubleshooting

### Problem: Still seeing same menu for all users

**Solution 1: Clear Browser Cache**
```
1. Open DevTools (F12)
2. Go to Application tab
3. Clear Local Storage
4. Refresh page
5. Login again
```

**Solution 2: Use Incognito/Private Mode**
```
1. Open new Incognito/Private window
2. Go to http://localhost:8080
3. Login with test user
```

**Solution 3: Hard Refresh**
```
Windows: Ctrl + Shift + R
Mac: Cmd + Shift + R
```

### Problem: Frontend not updating

**Solution: Restart Frontend**
```bash
# Stop frontend (Ctrl+C)
# Start again
cd frontend
npm run serve
```

### Problem: API not returning profile data

**Solution: Check Backend**
```bash
cd backend
python test_role_api.py
```

Should show:
```
✓ viewer1 profile: Role: VIEWER, Can Upload: False
✓ operator1 profile: Role: OPERATOR, Can Upload: True
✓ manager1 profile: Role: MANAGER, Can Upload: True
```

### Problem: Login not fetching profile

**Solution: Check Network Tab**
```
1. Open DevTools (F12)
2. Go to Network tab
3. Login
4. Check /api/auth/login/ response
5. Should include "profile" object with role
```

---

## 📊 Expected Behavior

### Login Flow:

1. User enters credentials
2. Backend authenticates
3. Backend returns:
   - Access token
   - Refresh token
   - User data WITH profile (role, permissions, plant)
4. Frontend stores user data
5. Frontend reads role from profile
6. Sidebar updates based on role
7. Menu items show/hide based on permissions

### Sidebar Rendering:

```vue
<!-- Upload menu item -->
<router-link v-if="canUpload" to="/upload">
  Upload Excel
</router-link>

<!-- canUpload is true for OPERATOR, MANAGER, ADMIN -->
<!-- canUpload is false for VIEWER -->
```

---

## 🎯 Quick Test Checklist

- [ ] Backend running on port 8000
- [ ] Frontend running on port 8080/8081
- [ ] Browser cache cleared
- [ ] Login as viewer1 - No Upload menu
- [ ] Login as operator1 - Has Upload menu + Green badge
- [ ] Login as manager1 - Has Upload menu + Orange badge
- [ ] Role badge visible in sidebar
- [ ] Different menu items for different roles

---

## 📸 Visual Comparison

### VIEWER Sidebar:
```
┌─────────────────────┐
│  NPC System         │
│  viewer1            │
│  [Viewer] (Blue)    │
├─────────────────────┤
│ 📊 Dashboard        │
│ 👁️ View Reports     │
│ 📥 Generate Report  │
├─────────────────────┤
│ 👤 My Profile       │
│ 🚪 Logout           │
└─────────────────────┘
```

### OPERATOR Sidebar:
```
┌─────────────────────┐
│  NPC System         │
│  operator1          │
│  [Operator] (Green) │
├─────────────────────┤
│ 📊 Dashboard        │
│ 📤 Upload Excel     │ ← ADDED
│ 👁️ View Reports     │
│ 📥 Generate Report  │
│ 📅 Water Nomination │ ← ADDED
├─────────────────────┤
│ 👤 My Profile       │
│ 🚪 Logout           │
└─────────────────────┘
```

### MANAGER Sidebar:
```
┌─────────────────────┐
│  NPC System         │
│  manager1           │
│  [Manager] (Orange) │
├─────────────────────┤
│ 📊 Dashboard        │
│ 📤 Upload Excel     │
│ 👁️ View Reports     │
│ 📥 Generate Report  │
│ 📅 Water Nomination │
├─────────────────────┤
│ 👤 My Profile       │
│ 🚪 Logout           │
└─────────────────────┘
```

---

## 🔧 Developer Tools Check

### Check localStorage:

```javascript
// Open Console (F12)
localStorage.getItem('user')

// Should show:
{
  "username": "operator1",
  "profile": {
    "role": "OPERATOR",
    "permissions": {
      "can_upload_data": true,
      "can_approve_data": false
    }
  }
}
```

### Check Vue DevTools:

If you have Vue DevTools installed:
1. Open Vue tab
2. Select Sidebar component
3. Check data:
   - `userRole`: "OPERATOR"
   - `canUpload`: true
   - `isAdminUser`: false

---

## ✅ Success Indicators

You'll know it's working when:

1. ✅ Role badge appears in sidebar with correct color
2. ✅ Viewer doesn't see Upload or Water Nomination
3. ✅ Operator sees Upload and Water Nomination
4. ✅ Manager sees all operational features
5. ✅ Each user sees their role name in sidebar
6. ✅ Console shows profile data with permissions

---

## 📞 Still Not Working?

### Check These Files Were Updated:

1. `backend/reports/serializers.py` - UserProfileSerializer includes profile
2. `backend/reports/auth_views.py` - Login returns full profile
3. `frontend/src/utils/auth.js` - Role checking functions added
4. `frontend/src/components/Sidebar.vue` - Conditional rendering added

### Verify Backend Changes:

```bash
cd backend
python test_role_api.py
```

Should show correct roles and permissions.

### Verify Frontend Changes:

Check `frontend/src/components/Sidebar.vue` has:
```vue
<router-link v-if="canUpload" to="/upload">
```

### Check Browser Console for Errors:

Look for:
- Network errors
- JavaScript errors
- Missing profile data

---

## 🎉 Summary

**To see the role-based UI:**

1. Start backend: `python manage.py runserver`
2. Start frontend: `npm run serve`
3. Clear browser cache or use Incognito
4. Login with different test users
5. Observe different menus and role badges

**The changes ARE implemented** - you just need to restart the frontend and clear cache to see them!

---

**Last Updated**: February 19, 2026
**Status**: ✅ Fully Implemented
**Test Users**: viewer1, operator1, manager1 (all password: test123)
