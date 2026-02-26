# ⚡ Archive Link Added to Sidebar!

## What Was Fixed

The Archive link was in the code but wasn't showing because it didn't have the proper permission check.

### Change Made:

**Before:**
```vue
<!-- Archive -->
<router-link to="/archive" @click="closeSidebar" class="nav-item">
  <i class="pi pi-inbox"></i>
  <span class="nav-text">Archive</span>
</router-link>
```

**After:**
```vue
<!-- Archive - Show for everyone who can upload -->
<router-link v-if="canUpload" to="/archive" @click="closeSidebar" class="nav-item">
  <i class="pi pi-inbox"></i>
  <span class="nav-text">Archive</span>
</router-link>
```

### Why This Fix?

- Archive link now has `v-if="canUpload"` condition
- Only users with upload permissions can see archived files
- Makes sense: if you can upload, you can archive
- Matches the Upload Excel permission logic

## How to See the Archive Link

### Step 1: Restart Frontend Dev Server

**Option A: Use Batch File (EASIEST)**
```bash
# From npc-reporting-system folder:
🔥_RESTART_FRONTEND_CLEAN.bat
```

**Option B: Manual Restart**
```bash
# 1. Stop dev server (Ctrl+C in the terminal)

# 2. Clear caches
cd frontend
rmdir /s /q node_modules\.cache
rmdir /s /q dist

# 3. Start fresh
npm run serve

# 4. Wait for "Compiled successfully"
```

### Step 2: Hard Refresh Browser

After the dev server restarts:
1. Go to: http://localhost:8080
2. Press: **Ctrl+Shift+R** (hard refresh)
3. Or: **Ctrl+F5**

### Step 3: Check Sidebar

The Archive link should now appear in the sidebar:

```
📊 Dashboard
📤 Upload Excel
📥 Archive          ← NEW! Should appear here
👁️ View Reports
⬇️ Generate Report
📅 Water Nomination
...
```

## Who Can See the Archive Link?

Users with these roles can see Archive:
- ✅ **OPERATOR** - Can upload and archive
- ✅ **MANAGER** - Can upload and archive
- ✅ **ADMIN** - Can upload and archive
- ❌ **VIEWER** - Cannot see Archive (no upload permission)

## If You Still Don't See It

### Check 1: Are You Logged In?
- Archive requires authentication
- Make sure you're logged in

### Check 2: Do You Have Upload Permission?
- Log in as OPERATOR, MANAGER, or ADMIN
- VIEWER role won't see the Archive link

### Check 3: Did You Restart Properly?
- Make sure you stopped the old dev server
- Cleared the cache folders
- Started a fresh dev server
- Hard refreshed the browser

### Check 4: Check Browser Console
1. Press F12 to open DevTools
2. Go to Console tab
3. Look for any errors
4. If you see errors, share them

## Testing the Archive Feature

Once you see the Archive link:

1. **Click Archive in sidebar**
   - Should go to: http://localhost:8080/archive

2. **Archive a file from Upload page**
   - Go to Upload page
   - Click the amber inbox icon on a file
   - File should disappear from Recent Uploads

3. **View archived file**
   - Click Archive in sidebar
   - Should see the archived file in the table

4. **Restore or Delete**
   - Click green restore button to move back to uploads
   - Click red delete button to permanently delete

## File Modified

- `frontend/src/components/Sidebar.vue` - Added `v-if="canUpload"` to Archive link

---

**The Archive link is now properly configured!** Just restart the dev server and hard refresh your browser. 🎉
