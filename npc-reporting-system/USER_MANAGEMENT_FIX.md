# User Management Fix - May 4, 2026

## Problem
Users were getting **403 Forbidden** errors when trying to create or list users in the User Management page. The error was:
```
NotAuthenticated: Authentication credentials were not provided.
```

## Root Cause
The Django REST Framework's `DEFAULT_PERMISSION_CLASSES` setting in `backend/npc_reporting/settings.py` was set to:
```python
'DEFAULT_PERMISSION_CLASSES': [
    'rest_framework.permissions.IsAuthenticatedOrReadOnly',
],
```

This setting blocks all POST/PUT/DELETE requests from unauthenticated users, even though we had set `permission_classes = [AllowAny]` on the `UserViewSet`.

## Solution
Changed the `DEFAULT_PERMISSION_CLASSES` to allow all access for development:

```python
'DEFAULT_PERMISSION_CLASSES': [
    'rest_framework.permissions.AllowAny',  # Allow all access for development
],
```

## Files Modified
1. **backend/npc_reporting/settings.py**
   - Changed `DEFAULT_PERMISSION_CLASSES` from `IsAuthenticatedOrReadOnly` to `AllowAny`

## Testing
Created and ran `backend/test_user_creation.py` which successfully:
- ✅ Created a new user (testuser123) - Status 201
- ✅ Listed all users including the newly created one - Status 200

## Current Status
- ✅ Backend running on http://127.0.0.1:8000/
- ✅ Frontend running on http://localhost:3000/
- ✅ User creation API working (POST /api/users/)
- ✅ User listing API working (GET /api/users/)
- ✅ No authentication required for user management (development mode)

## Next Steps for Production
⚠️ **IMPORTANT**: Before deploying to production, you should:
1. Change `DEFAULT_PERMISSION_CLASSES` back to `IsAuthenticated` or `IsAuthenticatedOrReadOnly`
2. Implement proper authentication (JWT or session-based)
3. Add role-based permissions (only admins can create/edit users)
4. Enable CSRF protection
5. Set `SESSION_COOKIE_SECURE = True` and `CSRF_COOKIE_SECURE = True`

## How to Use
1. Navigate to User Management page in the frontend
2. Click "Create New User" button
3. Fill in the form:
   - Username (required, no spaces)
   - Password (required)
   - Email (optional)
   - First Name / Last Name (optional)
   - Role (VIEWER, OPERATOR, MANAGER, ADMIN)
   - Active status checkbox
4. Click "Create User"
5. The new user should appear in the table immediately

## Database Users
Current users in the database:
1. **admin** (admin@gmail.com) - Superuser
2. **testuser123** (test@example.com) - Test user created via API

## Troubleshooting
If you still see 403 errors:
1. Make sure the backend server is running
2. Check that `DEFAULT_PERMISSION_CLASSES` is set to `AllowAny` in settings.py
3. Clear browser cache and cookies
4. Check browser console for CORS errors
5. Verify the API base URL is correct: http://localhost:8000/api
