# ✅ Pulangi 4 Name Updated to Include "Power"

## What Was Changed

The plant name has been updated from:
- ❌ **Old**: Pulangi 4 Hydroelectric Plant
- ✅ **New**: Pulangi 4 Hydroelectric Power Plant

---

## Files Updated

### Backend Files
1. ✅ `backend/add_pulangi4.py` - Plant creation script
2. ✅ `backend/update_pulangi4_name.py` - New database update script (created)

### Documentation Files
1. ✅ `✅_PULANGI4_ADDED.md`
2. ✅ `✅_SOLUTION_PULANGI4_ERROR.md`
3. ✅ `🔧_PULANGI4_TROUBLESHOOTING.md`
4. ✅ `PULANGI4_SETUP_GUIDE.md`
5. ✅ `PULANGI4_UPLOAD_GUIDE.md`

### Batch Files
1. ✅ `UPDATE_PULANGI4_NAME.bat` - New update script (created)

---

## How to Apply the Update

### Option 1: Update Existing Database (Recommended)

If you already have Pulangi 4 in your database, run this command:

```bash
cd npc-reporting-system
UPDATE_PULANGI4_NAME.bat
```

This will:
1. Connect to your database
2. Find the Pulangi 4 plant record
3. Update the name to "Pulangi 4 Hydroelectric Power Plant"
4. Save the changes

### Option 2: Fresh Installation

If you're setting up Pulangi 4 for the first time:

```bash
cd npc-reporting-system
ADD_PULANGI4.bat
```

The plant will be created with the correct name automatically.

---

## Verification

After running the update, verify the change:

### 1. Check Database
```bash
cd npc-reporting-system/backend
python manage.py shell
```

Then run:
```python
from reports.models import Plant
plant = Plant.objects.get(code='PULANGI4')
print(plant.name)
# Should output: Pulangi 4 Hydroelectric Power Plant
```

### 2. Check Frontend
1. Start the backend and frontend servers
2. Go to "Upload Excel" page
3. Open the plant dropdown
4. You should see "Pulangi 4 Hydroelectric Power Plant"

### 3. Check Dashboard
1. Go to Dashboard
2. Look for the Pulangi 4 card
3. The full name should display as "Pulangi 4 Hydroelectric Power Plant"

---

## What This Affects

### ✅ Will Update
- Plant name in database
- Plant name in dropdown menus
- Plant name in dashboard cards
- Plant name in reports
- Plant name in exports

### ❌ Won't Affect
- Plant code (still PULANGI4)
- Existing data records
- Excel upload format
- API endpoints
- Database structure

---

## Troubleshooting

### Issue: "Plant not found"
**Solution**: Run `ADD_PULANGI4.bat` first to create the plant

### Issue: "Permission denied"
**Solution**: Make sure the backend server is stopped before running the update

### Issue: "Name didn't change in frontend"
**Solution**: 
1. Restart the backend server
2. Clear browser cache (Ctrl + Shift + Delete)
3. Refresh the page (Ctrl + F5)

---

## Technical Details

### Database Update Query
```sql
UPDATE plants 
SET name = 'Pulangi 4 Hydroelectric Power Plant' 
WHERE code = 'PULANGI4';
```

### Python Update Code
```python
plant = Plant.objects.get(code='PULANGI4')
plant.name = 'Pulangi 4 Hydroelectric Power Plant'
plant.save()
```

---

## Summary

The word "Power" has been added to the Pulangi 4 plant name throughout the system:
- ✅ Backend scripts updated
- ✅ Documentation updated
- ✅ Database update script created
- ✅ Batch file created for easy updating

Run `UPDATE_PULANGI4_NAME.bat` to apply the change to your database!
