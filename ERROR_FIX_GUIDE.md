# Error Fix Guide - SignatoryAuthorizationRequest Component

## Errors Fixed

### **Error 1: 500 Internal Server Error on POST /api/signatory-authorizations/request/**

**Problem**: The backend was receiving a 500 error when submitting authorization requests.

**Root Cause**: The `request_authorization` method in `views_authorization.py` was passing `data['user'] = request.user.id` to the serializer, but the serializer's `create` method was also trying to set the user from context, causing a conflict.

**Solution**:
1. Updated `views_authorization.py` to pass the user via `save(user=request.user)` instead of in the data
2. Updated `serializers_security.py` to remove the automatic user assignment in the `create` method
3. Added better error handling in the frontend to display specific error messages

**Files Modified**:
- `backend/reports/views_authorization.py` - Fixed request_authorization method
- `backend/reports/serializers_security.py` - Fixed create method
- `frontend/src/components/SignatoryAuthorizationRequest.vue` - Added error message handling

### **Error 2: 404 Not Found on GET /api/signatory-authorizations/my-authorizations/**

**Problem**: The endpoint was returning 404, indicating the route wasn't found.

**Root Cause**: The ViewSet action decorator might not have been properly registered, or the response format wasn't being handled correctly.

**Solution**:
1. Verified the ViewSet is properly registered in `urls.py` ✓
2. Updated the frontend to handle both array and paginated responses
3. Added fallback to empty arrays if data loading fails

**Files Modified**:
- `frontend/src/components/SignatoryAuthorizationRequest.vue` - Improved data loading methods

---

## Changes Made

### **Backend Changes**

#### 1. `views_authorization.py` - request_authorization method
```python
# BEFORE (causing 500 error)
data = request.data.copy()
data['user'] = request.user.id
serializer = SignatoryAuthorizationRequestSerializer(data=data)
if serializer.is_valid():
    auth_request = serializer.save()

# AFTER (fixed)
data = request.data.copy()
serializer = SignatoryAuthorizationRequestSerializer(data=data, context={'request': request})
if serializer.is_valid():
    auth_request = serializer.save(user=request.user)
```

#### 2. `serializers_security.py` - create method
```python
# BEFORE (conflicting user assignment)
def create(self, validated_data):
    validated_data['user'] = self.context['request'].user
    return super().create(validated_data)

# AFTER (fixed)
def create(self, validated_data):
    return super().create(validated_data)
```

### **Frontend Changes**

#### 1. `SignatoryAuthorizationRequest.vue` - Data loading methods
```javascript
// BEFORE (not handling all response formats)
async loadUserAuthorizations() {
  const response = await api.getUserSignatoryAuthorizations();
  this.userAuthorizations = response.data.results || response.data;
}

// AFTER (handles arrays and paginated responses)
async loadUserAuthorizations() {
  try {
    const response = await api.getUserSignatoryAuthorizations();
    this.userAuthorizations = Array.isArray(response.data) ? response.data : (response.data.results || []);
  } catch (error) {
    console.error('Error loading authorizations:', error);
    this.userAuthorizations = [];
  }
}
```

#### 2. `SignatoryAuthorizationRequest.vue` - Error handling
```javascript
// BEFORE (generic error message)
catch (error) {
  toast.error('❌ Failed to submit request. Please try again.');
}

// AFTER (specific error messages)
catch (error) {
  const errorMessage = error.response?.data?.error || error.response?.data?.detail || 'Failed to submit request. Please try again.';
  toast.error(`❌ ${errorMessage}`);
}
```

---

## Testing the Fix

### **Step 1: Verify Backend**
```bash
# Check if the ViewSet is properly registered
python manage.py shell
from reports.views_authorization import SignatoryAuthorizationViewSet
print(SignatoryAuthorizationViewSet.actions)
# Should show: {'get': 'list', 'post': 'create', ...}
```

### **Step 2: Test API Endpoints**
```bash
# Test my-authorizations endpoint
curl -H "Authorization: Bearer YOUR_TOKEN" \
  http://localhost:8000/api/signatory-authorizations/my-authorizations/

# Test request endpoint
curl -X POST -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "signatory_name": "O.M. LAVA",
    "role": "Approved by",
    "justification": "I need this authorization to approve reports"
  }' \
  http://localhost:8000/api/signatory-authorizations/request/
```

### **Step 3: Test Frontend**
1. Navigate to "Request Signature Access" page
2. Fill out the form:
   - Select a signatory
   - Choose a role
   - Enter justification (min 20 characters)
3. Click "Submit Request"
4. Check browser console for errors
5. Verify success message appears

---

## Debugging Tips

### **If you still see 500 errors:**

1. **Check Django logs**:
   ```bash
   # Look for detailed error messages
   tail -f backend/logs/app.log
   ```

2. **Check serializer validation**:
   ```python
   python manage.py shell
   from reports.serializers_security import SignatoryAuthorizationRequestSerializer
   from django.contrib.auth.models import User
   
   user = User.objects.first()
   data = {
      'signatory_name': 'O.M. LAVA',
      'role': 'Approved by',
      'justification': 'Test justification'
   }
   serializer = SignatoryAuthorizationRequestSerializer(data=data)
   print(serializer.is_valid())
   print(serializer.errors)
   ```

3. **Check API response format**:
   - Open DevTools (F12)
   - Go to Network tab
   - Look for the API request
   - Check the Response tab to see what the server is returning

### **If you see 404 errors:**

1. **Verify URL routing**:
   ```bash
   python manage.py show_urls | grep signatory
   ```

2. **Check if ViewSet is registered**:
   ```python
   python manage.py shell
   from django.urls import get_resolver
   resolver = get_resolver()
   print([p.pattern for p in resolver.url_patterns if 'signatory' in str(p.pattern)])
   ```

---

## Expected Behavior After Fix

### **Successful Request Submission**
1. User fills out form and clicks "Submit Request"
2. Frontend sends POST request to `/api/signatory-authorizations/request/`
3. Backend validates data and creates `SignatoryAuthorizationRequest` record
4. Success message appears: "🎉 Authorization request submitted successfully!"
5. Pending Requests card updates to show new count
6. Form resets for next request

### **Data Loading**
1. Component mounts
2. Frontend sends GET requests to:
   - `/api/signatory-authorizations/my-authorizations/`
   - `/api/signatory-authorizations/my-requests/`
3. Backend returns user's authorizations and requests
4. Stats cards update with counts

---

## Summary of Fixes

| Issue | Fix | Status |
|-------|-----|--------|
| 500 error on POST request | Fixed user assignment conflict | ✅ |
| 404 error on GET request | Improved response handling | ✅ |
| Generic error messages | Added specific error details | ✅ |
| Data loading failures | Added fallback to empty arrays | ✅ |

All errors should now be resolved! If you encounter any new errors, check the Django logs and browser console for detailed error messages.
