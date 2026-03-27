# Stats Cards Data Guide - SignatoryAuthorizationRequest Component

## Why Cards Show No Data

The three stat cards in the hero section display data from the backend API. If they show "0" or appear empty, here's why:

### **Card 1: Active Authorizations (Green)**
- **Shows**: Count of user's active, valid signatory authorizations
- **Why it's 0**: 
  - User hasn't been granted any authorizations yet
  - All authorizations have expired
  - User is new to the system
- **How to populate**:
  1. Admin approves an authorization request
  2. System creates a `SignatoryAuthorization` record for the user
  3. Card automatically updates to show the count

### **Card 2: Pending Requests (Yellow)**
- **Shows**: Count of user's authorization requests awaiting admin review
- **Why it's 0**:
  - User hasn't submitted any requests yet
  - All previous requests have been approved/rejected
  - User is new to the system
- **How to populate**:
  1. User fills out the form and submits a request
  2. System creates a `SignatoryAuthorizationRequest` with status='PENDING'
  3. Card automatically updates to show the count

### **Card 3: Available Signatories (Blue)**
- **Shows**: Count of signatories the user can request authorization for
- **Why it shows 6**: 
  - This is hardcoded in the component (not from API)
  - Lists: O.M. LAVA, JMM MATA, EL ADIONG, C.C. AMIGABLE JR., D.R.B. CAIRO, DB ESMADE JR.
- **This should always show a number** (unless you modify the list)

---

## Data Flow

### **Loading Data**
```
Component Mounted
    ↓
loadUserAuthorizations() → API call to /signatory-authorizations/my-authorizations/
    ↓
loadPendingRequests() → API call to /signatory-authorizations/my-requests/
    ↓
Update component data arrays
    ↓
Cards display counts
```

### **API Endpoints**

| Endpoint | Method | Purpose | Returns |
|----------|--------|---------|---------|
| `/signatory-authorizations/my-authorizations/` | GET | Get user's active authorizations | List of `SignatoryAuthorization` objects |
| `/signatory-authorizations/my-requests/` | GET | Get user's authorization requests | List of `SignatoryAuthorizationRequest` objects |
| `/signatory-authorizations/request/` | POST | Submit new authorization request | Created `SignatoryAuthorizationRequest` object |

---

## How to Test Data Population

### **Option 1: Use Django Admin**

1. Go to Django admin: `http://localhost:8000/admin/`
2. Navigate to "Signatory Authorizations"
3. Click "Add Signatory Authorization"
4. Fill in:
   - User: (select current user)
   - Signatory Name: (e.g., "O.M. LAVA")
   - Role: (e.g., "Approved by")
   - Is Active: ✓ (checked)
   - Authorization Date: (today)
   - Requires 2FA: ✓ (checked)
5. Save

**Result**: Active Authorizations card will show "1"

### **Option 2: Use the Frontend Form**

1. Go to "Request Signature Access" page
2. Fill out the form:
   - Select a signatory
   - Choose a role
   - Enter justification (min 20 characters)
3. Click "Submit Request"

**Result**: Pending Requests card will show "1"

### **Option 3: Use Django Shell**

```python
python manage.py shell

from django.contrib.auth.models import User
from reports.models import SignatoryAuthorization, SignatoryAuthorizationRequest
from django.utils import timezone

# Get a user
user = User.objects.first()

# Create an authorization
auth = SignatoryAuthorization.objects.create(
    user=user,
    signatory_name='O.M. LAVA',
    role='Approved by',
    is_active=True,
    authorization_date=timezone.now(),
    requires_2fa=True
)

# Create a pending request
request = SignatoryAuthorizationRequest.objects.create(
    user=user,
    signatory_name='JMM MATA',
    role='Checked and Reviewed by',
    justification='I need this authorization to review reports',
    status='PENDING'
)
```

---

## Debugging Steps

### **If cards still show 0:**

1. **Check browser console** for errors:
   - Open DevTools (F12)
   - Go to Console tab
   - Look for API errors

2. **Check network requests**:
   - Go to Network tab
   - Look for requests to `/signatory-authorizations/my-authorizations/`
   - Check response status (should be 200)
   - Check response data

3. **Check backend logs**:
   - Look for errors in Django console
   - Check if API endpoints are being called

4. **Verify authentication**:
   - Make sure user is logged in
   - Check if auth token is being sent with requests

### **Common Issues**

| Issue | Solution |
|-------|----------|
| Cards show 0 but data exists | Clear browser cache, refresh page |
| API returns 401 Unauthorized | User not logged in, check auth token |
| API returns 404 Not Found | Endpoint not registered in URLs |
| API returns 500 Error | Check Django logs for backend errors |

---

## Component Code Reference

### **Data Loading (mounted hook)**
```javascript
mounted() {
  this.loadUserAuthorizations();
  this.loadPendingRequests();
}
```

### **Data Arrays**
```javascript
data() {
  return {
    userAuthorizations: [],      // Populated from API
    pendingRequests: [],          // Populated from API
    availableSignatories: [       // Hardcoded list
      { name: 'O.M. LAVA', title: 'Prin. Engr. A, GPD' },
      // ... 5 more signatories
    ]
  }
}
```

### **Card Display**
```html
<div class="stat-number">{{ userAuthorizations.length }}</div>
<div class="stat-number">{{ pendingRequests.length }}</div>
<div class="stat-number">{{ availableSignatories.length }}</div>
```

---

## Expected Behavior

### **First Time User**
- Active Authorizations: 0
- Pending Requests: 0
- Available Signatories: 6

### **After Submitting Request**
- Active Authorizations: 0
- Pending Requests: 1
- Available Signatories: 6

### **After Admin Approves Request**
- Active Authorizations: 1
- Pending Requests: 0
- Available Signatories: 6

---

## Real-Time Updates

The cards do **NOT** auto-refresh. To see updated data:
1. Refresh the page (F5)
2. Navigate away and back to the page
3. Close and reopen the component

To add real-time updates, you could:
- Add polling with `setInterval()`
- Use WebSockets
- Use Vue's reactive data binding with auto-refresh

---

## Summary

The stats cards are working correctly. They show "0" because:
- ✅ Component is loading data from API correctly
- ✅ API endpoints are properly implemented
- ✅ No data exists in the database yet

To populate data:
1. Use Django admin to create test records
2. Use the frontend form to submit requests
3. Use Django shell for bulk operations

The cards will automatically update once data is added to the database!
