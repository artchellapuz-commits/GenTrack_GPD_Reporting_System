# 📍 How to Access the Archive Page

## Quick Answer

The Archive page is already implemented and accessible in 3 ways:

### 1. **Via Sidebar Navigation** (Easiest)
- Look at the left sidebar
- Click on the **"Archive"** menu item (has an inbox icon 📥)
- Located below the "Upload" menu item

### 2. **Direct URL**
```
http://localhost:8080/archive
```
Just type this in your browser address bar

### 3. **After Archiving a File**
- Go to Upload page: http://localhost:8080/upload
- Click the archive button (📥 inbox icon) on any file in Recent Uploads
- The file will be moved to the Archive page
- You can then navigate to Archive to see it

## What You'll See on the Archive Page

### Page Header
- Title: "Archived Files"
- Description: "View and manage archived uploaded files"

### Archived Files Table
Shows all archived files with:
- File Name
- Plant
- Uploaded At
- Archived At (when it was archived)
- Status
- Records (number of records imported)
- Actions (Restore and Delete buttons)

### Action Buttons
1. **Restore Button** (🔄 replay icon)
   - Green color
   - Restores the file back to Recent Uploads
   - File will disappear from Archive and reappear in Upload page

2. **Delete Button** (🗑️ trash icon)
   - Red color
   - Permanently deletes the file
   - Shows confirmation dialog before deleting
   - Cannot be undone!

### Empty State
If no files are archived, you'll see:
- Large inbox icon
- "No Archived Files" message
- "You haven't archived any files yet" description

## Complete Workflow

### Archiving a File:
1. Go to: http://localhost:8080/upload
2. Scroll to "Recent Uploads" table
3. Click the amber/orange inbox icon (📥) in the Actions column
4. File disappears from Recent Uploads
5. Toast notification: "File archived successfully!"

### Viewing Archived Files:
1. Click "Archive" in the sidebar
   OR
2. Go to: http://localhost:8080/archive
3. See all archived files in a table

### Restoring a File:
1. On Archive page, find the file
2. Click the green restore button (🔄)
3. File moves back to Recent Uploads
4. Toast notification: "File restored successfully!"
5. File disappears from Archive page

### Permanently Deleting:
1. On Archive page, find the file
2. Click the red delete button (🗑️)
3. Confirmation dialog appears (orange header with warning)
4. Click "Delete" to confirm
5. File is permanently deleted
6. Toast notification: "File deleted successfully!"

## Sidebar Location

The Archive link is in the sidebar navigation, typically positioned:
```
Dashboard
Upload
Archive  ← HERE
View Reports
Generate Report
...
```

## Current Status

✅ Archive page exists: `frontend/src/components/ArchivePage.vue`
✅ Route configured: `/archive` in `router/index.js`
✅ Sidebar link added: In `Sidebar.vue`
✅ Archive button added: In Upload page Recent Uploads table
✅ Backend API working: Archive, restore, delete endpoints
✅ All functionality complete!

## If You Don't See the Archive Link

1. **Restart the frontend dev server:**
   ```bash
   # Run this from npc-reporting-system folder:
   🔥_RESTART_FRONTEND_CLEAN.bat
   ```

2. **Hard refresh the browser:**
   - Press: Ctrl+Shift+R
   - Or: Ctrl+F5

3. **Check if you're logged in:**
   - Archive page requires authentication
   - If not logged in, you'll be redirected to login page

## Testing the Archive Feature

1. **Upload a test file** (if you don't have any uploads)
2. **Archive it** from the Upload page
3. **Go to Archive page** via sidebar or URL
4. **Try restoring** the file
5. **Try deleting** a file (use a test file!)

---

**The Archive page is fully functional and ready to use!** 🎉
