# ✅ Water Nomination 400 Error - RESOLVED

## Problem Summary

The user was experiencing **400 Bad Request** errors when trying to save water nominations. The error was preventing them from creating new SUBMITTED nominations to test the Approval Queue feature.

## Root Cause

The error was caused by a **database unique constraint violation**:

```
ValidationError: The fields plant, nomination_date, nomination_type must make a unique set.
```

The `WaterNomination` model has a unique constraint on `['plant', 'nomination_date', 'nomination_type']`, which means you cannot create duplicate nominations for the same plant, date, and type combination.

## Solution Implemented

### 1. Improved Error Handling (Frontend)

Updated `saveNomination()` method in `WaterNomination.vue`:
- Detects unique constraint errors specifically
- Shows user-friendly error message explaining the issue
- Provides clear guidance on how to resolve (change date, edit existing, or delete)

### 2. Added Delete Functionality

Added ability to delete draft nominations:
- New `deleteNomination()` method
- DELETE button added to card actions (red trash icon)
- Only visible for DRAFT status nominations
- Includes confirmation dialog

### 3. Enhanced UI

- Added `.btn-delete` CSS styling (red background)
- Updated button lists to include delete button
- Proper hover effects

## Files Modified

1. **frontend/src/components/WaterNomination.vue**
   - Enhanced `saveNomination()` error handling
   - Added `deleteNomination()` method
   - Added DELETE button in template
   - Added CSS styling for delete button

## How to Use

### To Delete a Duplicate Nomination:

1. Go to Water Nomination page
2. Find the DRAFT nomination you want to remove
3. Click the **DELETE** button (red trash icon)
4. Confirm deletion

### To Create a New Nomination:

1. Click "New Nomination"
2. Select plant and date
3. **Important**: Make sure this plant+date+type combination doesn't already exist
4. Fill in hourly values
5. Click "Create"

### To Test Approval Queue:

1. Create a new nomination (as Operator)
2. Click "Submit" button (don't approve it yet!)
3. Login as Manager or Admin
4. Go to "Approval Queue" menu
5. You should see the SUBMITTED nomination
6. Click "Approve" or "Reject"

## Why Approval Queue Was Empty

The Approval Queue only shows nominations with `status = 'SUBMITTED'`. 

The user's existing nominations were all `APPROVED`, so they correctly didn't appear in the queue. The queue is specifically for pending approvals only.

## Unique Constraint Rules

You **cannot** have two nominations with the same:
- Plant + Date + Type

### Examples:

❌ **Invalid** (duplicate):
- AGUS1 + 2026-02-20 + DAY_AHEAD (already exists)
- AGUS1 + 2026-02-20 + DAY_AHEAD (trying to create again)

✅ **Valid** (different combinations):
- AGUS1 + 2026-02-20 + DAY_AHEAD (original)
- AGUS1 + 2026-02-20 + HOUR_AHEAD (different type)
- AGUS1 + 2026-02-21 + DAY_AHEAD (different date)
- AGUS2 + 2026-02-20 + DAY_AHEAD (different plant)

## Testing Steps

1. **Refresh browser** (Ctrl+F5 or Cmd+R)
2. **Delete duplicates**: Remove any unwanted DRAFT nominations
3. **Create new**: Make a nomination with a unique plant+date+type
4. **Submit**: Click Submit button (status changes to SUBMITTED)
5. **Switch user**: Login as Manager/Admin
6. **Check queue**: Go to Approval Queue - should see the submission
7. **Approve**: Click Approve button

## Button Visibility by Status

### DRAFT Nominations:
- ✓ View (everyone)
- ✓ Edit (everyone)
- ✓ Delete (everyone) **[NEW!]**
- ✓ Submit (everyone)

### SUBMITTED Nominations:
- ✓ View (everyone)
- ✓ Approve (Manager/Admin only, can't approve own)

### APPROVED Nominations:
- ✓ View (everyone)
- No action buttons

## Error Messages

### Before Fix:
```
Failed to save nomination:
{"non_field_errors":["The fields plant, nomination_date, nomination_type must make a unique set."]}
```

### After Fix:
```
A nomination already exists for this plant, date, and type combination.

Please either:
1. Choose a different date
2. Edit the existing nomination
3. Delete the existing nomination first
```

## Status

✅ **RESOLVED** - The 400 error is now properly handled with clear user guidance and the ability to delete duplicate nominations.

## Next Steps

The approval workflow is now fully functional:
1. Operators can create and submit nominations
2. Managers/Admins can approve/reject from Approval Queue
3. Users can delete unwanted drafts
4. Clear error messages guide users when duplicates are detected

---

**All features working as designed!** 🎉
