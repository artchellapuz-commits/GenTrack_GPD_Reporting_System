# 🔍 Debug: Why Role Changes Aren't Showing

## Current Situation

You're logged in as `operator1` but still seeing all menu items (Upload Excel, Water Nomination, etc.) which should be visible for operators.

**Wait... that's CORRECT!** Operators SHOULD see those items!

---

## ✅ Let Me Clarify What Each Role Should See:

### VIEWER (viewer1) - LIMITED ACCESS
- ✅ Dashboard
- ✅ View Reports
- ✅ Generate Report
- ❌ Upload Excel **HIDDEN**
- ❌ Water Nomination **HIDDEN**

### OPERATOR (operator1) - CAN UPLOAD
- ✅ Dashboard
- ✅ Upload Excel **SHOWN** ← You should see this!
- ✅ View Reports
- ✅ Generate Report
- ✅ Water Nomination **SHOWN** ← You should see this!

### MANAGER (manager1) - CAN APPROVE
- ✅ Dashboard
- ✅ Upload Excel **SHOWN**
- ✅ View Reports
- ✅ Generate Report
- ✅ Water Nomination **SHOWN**

---

## 🎯 The Real Test

To see the DIFFERENCE, you need to:

1. **Login as viewer1** (password: test123)
   - Upload Excel should be **HIDDEN**
   - Water Nomination should be **HIDDEN**

2. **Login as operator1** (password: test123)
   - Upload Excel should be **VISIBLE**
   - Water Nomination should be **VISIBLE**

---

## 🔍 Quick Check

Open browser console (F12) and run:

```javascript
// Check what's in localStorage
const user = JSON.parse(localStorage.getItem('user'));
console.log('Role:', user?.profile?.role);
console.log('Can Upload:', user?.profile?.permissions?.can_upload_data);
```

**Expected for operator1:**
```
Role: OPERATOR
Can Upload: true
```

**Expected for viewer1:**
```
Role: VIEWER
Can Upload: false
```

---

## 🚀 Steps to Verify

1. **Logout** from current session

2. **Clear localStorage:**
   - F12 → Application → Local Storage → Clear All

3. **Login as viewer1:**
   ```
   Username: viewer1
   Password: test123
   ```
   
4. **Check sidebar:**
   - Should NOT see "Upload Excel"
   - Should NOT see "Water Nomination"
   - Should see blue "Viewer" badge

5. **Logout and login as operator1:**
   ```
   Username: operator1
   Password: test123
   ```
   
6. **Check sidebar:**
   - SHOULD see "Upload Excel"
   - SHOULD see "Water Nomination"
   - Should see green "Operator" badge

---

## 🎨 Visual Indicators to Look For

### Role Badge
Look for a colored badge under your username in the sidebar:
- **Blue badge** = Viewer
- **Green badge** = Operator
- **Orange badge** = Manager

### Menu Items Count
- **Viewer**: 5 items (Dashboard, View, Generate, Profile, Logout)
- **Operator**: 7 items (Dashboard, Upload, View, Generate, Water Nomination, Profile, Logout)
- **Manager**: 7 items (same as Operator)

---

## 🐛 If Still Not Working

### Check 1: Is frontend running with latest code?
```bash
# Stop frontend (Ctrl+C)
cd frontend
npm run serve
```

### Check 2: Check browser console for errors
```
F12 → Console tab
Look for any red errors
```

### Check 3: Check Network tab
```
F12 → Network tab
Login
Check /api/auth/login/ response
Should include profile object with role
```

### Check 4: Hard refresh
```
Windows: Ctrl + Shift + R
Mac: Cmd + Shift + R
```

### Check 5: Try different browser
Sometimes cache issues persist. Try:
- Chrome Incognito
- Firefox Private Window
- Different browser entirely

---

## 📊 Expected API Response

When you login, the API should return:

```json
{
  "access": "token...",
  "refresh": "token...",
  "user": {
    "id": 2,
    "username": "operator1",
    "profile": {
      "role": "OPERATOR",
      "role_display": "Operator",
      "plant": "AGUS1",
      "plant_name": "Agus 1 Hydroelectric Power Plant",
      "permissions": {
        "can_upload_data": true,
        "can_approve_data": false,
        "can_manage_users": false,
        "can_export_data": true
      }
    }
  }
}
```

---

## ✅ Summary

**If you're logged in as operator1 and seeing Upload/Water Nomination:**
- ✅ **This is CORRECT!** Operators should see these items.

**To see the difference:**
- Login as **viewer1** - should NOT see Upload/Water Nomination
- Login as **operator1** - SHOULD see Upload/Water Nomination
- Login as **manager1** - SHOULD see Upload/Water Nomination

**The role-based UI IS working if:**
1. viewer1 doesn't see Upload menu
2. operator1 DOES see Upload menu
3. You see colored role badges

---

## 🎯 Action Items

1. [ ] Logout completely
2. [ ] Clear browser cache/localStorage
3. [ ] Login as viewer1
4. [ ] Verify Upload is HIDDEN
5. [ ] Logout
6. [ ] Login as operator1
7. [ ] Verify Upload is SHOWN
8. [ ] Check for role badge colors

If viewer1 still sees Upload menu, then we have an issue.
If viewer1 doesn't see Upload menu, then it's working correctly!

---

**Last Updated**: February 19, 2026
**Status**: Awaiting verification with viewer1 login
