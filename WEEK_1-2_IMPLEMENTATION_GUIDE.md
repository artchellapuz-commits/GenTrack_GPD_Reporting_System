# Week 1-2 Priority Features Implementation Guide

## 🎯 Features Implemented

### 1. User Roles & Permissions ✅
### 2. Email Notifications ✅
### 3. Better Error Handling ✅

---

## 1. User Roles & Permissions

### Role Hierarchy

```
ADMIN (Administrator)
  ├─ Full system access
  ├─ User management
  ├─ All data operations
  └─ System configuration

MANAGER
  ├─ Approve/reject nominations
  ├─ View all reports
  ├─ Export data
  └─ Upload data

OPERATOR
  ├─ Upload data for assigned plant
  ├─ Submit nominations
  ├─ View reports
  └─ Export data

VIEWER
  ├─ View reports only
  └─ Export data
```

### User Profile Model

Each user has an extended profile with:
- **Role**: VIEWER, OPERATOR, MANAGER, ADMIN
- **Assigned Plant**: For operators (optional)
- **Contact Info**: Phone, department, position
- **Notification Preferences**: Email settings

### Permission Checks

```python
# In views.py
from reports.permissions import (
    IsAdminUser,
    IsManagerOrAdmin,
    IsOperatorOrAbove,
    CanUploadData,
    CanApproveData,
    CanExportData,
    CanManageUsers,
    IsOwnerOrReadOnly
)

# Example usage
class UploadViewSet(viewsets.ViewSet):
    permission_classes = [CanUploadData]
```

### API Endpoints

#### Get User Profile
```
GET /api/auth/profile/
Response: {
  "id": 1,
  "username": "operator1",
  "role": "OPERATOR",
  "plant": "AGUS1",
  "permissions": {
    "can_upload_data": true,
    "can_approve_data": false,
    "can_manage_users": false,
    "can_export_data": true
  }
}
```

#### Update User Profile
```
PUT /api/auth/update_profile/
Body: {
  "first_name": "Juan",
  "last_name": "Dela Cruz",
  "email": "juan@npc.gov.ph"
}
```

---

## 2. Email Notifications

### Email Service Features

The system sends automatic emails for:

1. **User Registration** - Welcome email
2. **File Upload Success** - Confirmation with details
3. **File Upload Failure** - Error details
4. **Nomination Submitted** - Notify managers
5. **Nomination Approved** - Notify submitter
6. **Nomination Rejected** - Notify submitter with reason
7. **Password Changed** - Security notification
8. **Daily Summary** - For managers (optional)

### Configuration

#### Development (Console Backend)
Emails are printed to console - no SMTP needed.

```python
# settings.py (already configured)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

#### Production (SMTP)
Update `.env` file:

```env
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=noreply@npc-reporting.com
```

### User Notification Preferences

Users can control which emails they receive:

```python
# User profile fields
email_notifications = True/False  # Master switch
notify_on_upload = True/False     # Upload notifications
notify_on_approval = True/False   # Approval notifications
notify_daily_summary = True/False # Daily summaries
```

### Email Service Usage

```python
from reports.email_service import EmailService

# Send upload success notification
EmailService.notify_upload_success(uploaded_file, user)

# Send nomination submitted notification
EmailService.notify_nomination_submitted(nomination, user)

# Send custom email
EmailService.send_email(
    subject="Custom Subject",
    message="Email body",
    recipient_list=["user@example.com"]
)
```

---

## 3. Better Error Handling

### Standardized Error Responses

All errors now return consistent format:

```json
{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable message",
    "details": {
      "field": "Additional context"
    }
  }
}
```

### Error Codes

```python
# Authentication & Authorization
UNAUTHORIZED = 'UNAUTHORIZED'
FORBIDDEN = 'FORBIDDEN'
INVALID_CREDENTIALS = 'INVALID_CREDENTIALS'
TOKEN_EXPIRED = 'TOKEN_EXPIRED'

# Validation
VALIDATION_ERROR = 'VALIDATION_ERROR'
INVALID_INPUT = 'INVALID_INPUT'
MISSING_FIELD = 'MISSING_FIELD'

# File Operations
FILE_TOO_LARGE = 'FILE_TOO_LARGE'
INVALID_FILE_FORMAT = 'INVALID_FILE_FORMAT'
FILE_UPLOAD_FAILED = 'FILE_UPLOAD_FAILED'
FILE_PROCESSING_ERROR = 'FILE_PROCESSING_ERROR'

# Data Operations
DUPLICATE_ENTRY = 'DUPLICATE_ENTRY'
NOT_FOUND = 'NOT_FOUND'
DATABASE_ERROR = 'DATABASE_ERROR'

# Business Logic
INVALID_DATE_RANGE = 'INVALID_DATE_RANGE'
PLANT_NOT_FOUND = 'PLANT_NOT_FOUND'
UNIT_NOT_FOUND = 'UNIT_NOT_FOUND'
NOMINATION_CONFLICT = 'NOMINATION_CONFLICT'

# System
INTERNAL_ERROR = 'INTERNAL_ERROR'
SERVICE_UNAVAILABLE = 'SERVICE_UNAVAILABLE'
```

### Custom Exceptions

```python
from reports.error_handlers import (
    AppError,
    ValidationError,
    AuthenticationError,
    PermissionError,
    NotFoundError,
    FileError
)

# Usage in views
if not plant:
    raise NotFoundError("Plant not found", resource_type="Plant")

if file.size > MAX_SIZE:
    raise FileError(
        "File too large",
        code=ErrorCode.FILE_TOO_LARGE
    )
```

### Success Responses

```python
from reports.error_handlers import success_response

return success_response(
    data={"id": 1, "name": "Plant"},
    message="Operation successful"
)
```

### Logging

All errors are automatically logged:

```
logs/
  └── app.log  # Rotating log file (10MB max, 5 backups)
```

Log levels:
- **DEBUG**: Detailed information
- **INFO**: General information
- **WARNING**: Warning messages
- **ERROR**: Error messages
- **CRITICAL**: Critical errors

---

## 4. Audit Logging

### Audit Trail

All important actions are logged:

```python
class AuditLog:
    user          # Who performed the action
    action        # CREATE, UPDATE, DELETE, UPLOAD, EXPORT, etc.
    model_name    # What was affected
    object_id     # Specific record ID
    description   # Action description
    ip_address    # User's IP
    user_agent    # Browser/client info
    timestamp     # When it happened
```

### Automatic Logging

The `AuditLogMiddleware` automatically logs:
- POST requests (CREATE)
- PUT/PATCH requests (UPDATE)
- DELETE requests (DELETE)

### View Audit Logs

```
GET /api/audit-logs/
GET /api/audit-logs/?user=1
GET /api/audit-logs/?action=UPLOAD
GET /api/audit-logs/?start_date=2026-01-01&end_date=2026-01-31
```

---

## 🚀 Setup Instructions

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. Create Admin User

```bash
python manage.py createsuperuser
```

### 4. Update Settings

Add to `settings.py` (already done):

```python
# Add middleware
MIDDLEWARE = [
    # ... existing middleware
    'reports.middleware.AuditLogMiddleware',
]

# Configure exception handler
REST_FRAMEWORK = {
    'EXCEPTION_HANDLER': 'reports.error_handlers.custom_exception_handler',
}
```

### 5. Configure Email (Optional)

For production, update `.env`:

```env
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=noreply@npc-reporting.com
```

### 6. Test the System

```bash
# Start server
python manage.py runserver

# Test endpoints
curl http://localhost:8000/api/auth/profile/
```

---

## 📝 Frontend Integration

### Update Auth Store

```javascript
// src/utils/auth.js
export const getUserProfile = async () => {
  const response = await api.get('/api/auth/profile/');
  return response.data;
};

export const hasPermission = (user, permission) => {
  return user.profile?.permissions?.[permission] || false;
};
```

### Check Permissions in Components

```vue
<template>
  <div>
    <button v-if="canUpload" @click="uploadFile">
      Upload Data
    </button>
    <button v-if="canApprove" @click="approveNomination">
      Approve
    </button>
  </div>
</template>

<script>
export default {
  computed: {
    canUpload() {
      return this.$store.state.user?.permissions?.can_upload_data;
    },
    canApprove() {
      return this.$store.state.user?.permissions?.can_approve_data;
    }
  }
}
</script>
```

### Handle Errors

```javascript
// src/utils/api.js
api.interceptors.response.use(
  response => response,
  error => {
    const errorData = error.response?.data?.error;
    
    if (errorData) {
      // Show user-friendly error
      showToast({
        severity: 'error',
        summary: errorData.message,
        detail: errorData.details?.message || ''
      });
    }
    
    return Promise.reject(error);
  }
);
```

---

## 🧪 Testing

### Test User Roles

```python
# Create test users
python manage.py shell

from django.contrib.auth.models import User
from reports.models import UserProfile, Plant

# Create operator
operator = User.objects.create_user('operator1', 'op@test.com', 'password')
operator.profile.role = 'OPERATOR'
operator.profile.plant = Plant.objects.get(code='AGUS1')
operator.profile.save()

# Create manager
manager = User.objects.create_user('manager1', 'mgr@test.com', 'password')
manager.profile.role = 'MANAGER'
manager.profile.save()
```

### Test Permissions

```bash
# Login as operator
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"operator1","password":"password"}'

# Try to access admin endpoint (should fail)
curl -X GET http://localhost:8000/api/users/ \
  -H "Authorization: Bearer <token>"
```

### Test Email Notifications

```python
# In Django shell
from reports.email_service import EmailService
from django.contrib.auth.models import User

user = User.objects.first()
EmailService.notify_user_registered(user)
# Check console for email output
```

---

## 📊 Database Schema Updates

### New Tables

1. **user_profiles** - Extended user information
2. **audit_logs** - Action audit trail

### Migration

```bash
python manage.py migrate reports 0008_add_user_roles_and_audit
```

---

## 🔒 Security Considerations

1. **Password Validation**: Django's built-in validators
2. **JWT Tokens**: 8-hour access, 7-day refresh
3. **Permission Checks**: On every sensitive endpoint
4. **Audit Logging**: All important actions tracked
5. **IP Tracking**: User IP addresses logged
6. **Email Verification**: Optional (can be added)

---

## 📈 Next Steps (Week 3-4)

1. **Advanced Reporting**
   - Custom report builder
   - Scheduled reports
   - Report templates

2. **Data Validation**
   - Advanced validation rules
   - Data quality checks
   - Anomaly detection

3. **Performance Optimization**
   - Database indexing
   - Query optimization
   - Caching layer

4. **Mobile App**
   - React Native app
   - Offline support
   - Push notifications

---

## 🆘 Troubleshooting

### Email Not Sending

Check:
1. EMAIL_BACKEND in settings
2. SMTP credentials in .env
3. Firewall/network settings
4. Gmail "Less secure apps" setting

### Permission Denied Errors

Check:
1. User has correct role
2. User profile exists
3. Token is valid
4. Endpoint has correct permission class

### Audit Logs Not Created

Check:
1. Middleware is installed
2. User is authenticated
3. Request method is POST/PUT/PATCH/DELETE

---

## 📞 Support

For issues or questions:
1. Check logs: `backend/logs/app.log`
2. Review error codes in response
3. Check audit logs for action history
4. Contact system administrator

---

**Implementation Date**: February 19, 2026
**Status**: ✅ Complete and Ready for Testing
