# Email Notification System - How It Works

## Overview
The authorization request system sends email notifications automatically using the email address from the user's account profile, not from a form field.

---

## How Email Notifications Work

### **1. Email Source**
The system retrieves the user's email from their **Django User account**:

```python
# From views_authorization.py
if not auth_request.user.email:
    return  # No email, skip notification

send_mail(
    subject,
    message,
    from_email,
    [auth_request.user.email],  # ← Email from user's account
    fail_silently=True,
)
```

### **2. Where Does the Email Come From?**

The user's email is stored in the Django User model and can be set in several ways:

#### **Option A: Admin Creates User**
When an administrator creates a user account in Django Admin:
1. Go to Django Admin → Users → Add User
2. Fill in username, password
3. **Add email address** in the user profile
4. Save

#### **Option B: User Registration**
If your system has user registration:
1. User signs up with email
2. Email is stored in their account
3. Used for all notifications

#### **Option C: User Profile Update**
Users or admins can update the email:
1. Django Admin → Users → Select User
2. Update email field
3. Save

---

## Email Notification Flow

### **When User Submits Request:**

```
User Submits Form
    ↓
Backend receives request
    ↓
Creates SignatoryAuthorizationRequest record
    ↓
Gets user from request.user (authenticated user)
    ↓
Sends email to request.user.email
    ↓
User receives notification
```

### **Code Flow:**

```python
# 1. User submits request (frontend)
await api.requestSignatoryAuthorization({
  signatory_name: 'O.M. LAVA',
  role: 'Approved by',
  justification: 'I need this authorization...'
});

# 2. Backend receives request (views_authorization.py)
def request_authorization(self, request):
    serializer = SignatoryAuthorizationRequestSerializer(data=data)
    auth_request = serializer.save(user=request.user)  # ← User from session
    
    # 3. Send notification
    self._notify_admins_of_request(auth_request)
    
# 4. Email notification method
def _notify_admins_of_request(self, auth_request):
    # Gets email from user account
    user_email = auth_request.user.email  # ← From Django User model
    
    if not user_email:
        return  # Skip if no email
    
    send_mail(
        subject='Authorization Request Submitted',
        message=f'User {auth_request.user.username} submitted a request...',
        from_email='noreply@npc-reporting.com',
        recipient_list=[user_email],
        fail_silently=True
    )
```

---

## Email Notifications Sent

### **1. When User Submits Request**
- **To**: Administrators (all staff users with email addresses)
- **Subject**: "New Signatory Authorization Request - [Signatory Name]"
- **Content**: User details, signatory name, role, justification

### **2. When Admin Approves Request**
- **To**: User who submitted the request (`auth_request.user.email`)
- **Subject**: "Signatory Authorization Approved - [Signatory Name]"
- **Content**: Approval details, 2FA requirements, expiry date, next steps

### **3. When Admin Rejects Request**
- **To**: User who submitted the request (`auth_request.user.email`)
- **Subject**: "Signatory Authorization Request - Update Required"
- **Content**: Rejection reason, admin notes, contact information

---

## What If User Has No Email?

### **Scenario 1: User Account Has No Email**
```python
if not auth_request.user.email:
    return  # Email notification is skipped
```

**Result**: 
- ✅ Request is still created successfully
- ❌ No email notification is sent
- ℹ️ User can still check status in the UI

### **Scenario 2: Email Sending Fails**
```python
send_mail(..., fail_silently=True)
```

**Result**:
- ✅ Request is still created successfully
- ❌ Email fails silently (doesn't crash the system)
- ℹ️ Error is logged to console

---

## How to Ensure Users Receive Emails

### **For Administrators:**

1. **Check User Has Email**:
   ```bash
   python manage.py shell
   from django.contrib.auth.models import User
   user = User.objects.get(username='testuser')
   print(user.email)  # Should show email address
   ```

2. **Add Email to User Account**:
   - Django Admin → Users → Select User
   - Add email address
   - Save

3. **Verify Email Settings**:
   ```python
   # In settings.py
   EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
   EMAIL_HOST = 'smtp.gmail.com'
   EMAIL_PORT = 587
   EMAIL_USE_TLS = True
   EMAIL_HOST_USER = 'your-email@gmail.com'
   EMAIL_HOST_PASSWORD = 'your-app-password'
   DEFAULT_FROM_EMAIL = 'noreply@npc-reporting.com'
   ```

### **For Users:**

1. **Check Your Profile**:
   - Ask admin to verify your email is set
   - Or check in user profile settings (if available)

2. **Update Email**:
   - Contact administrator to update email
   - Or update in profile settings (if available)

---

## Success Message Explanation

### **Current Message:**
```
🎉 Authorization request submitted successfully! 
You will receive an email notification when it is reviewed.
```

### **What It Means:**

| Condition | Email Sent? | Message Accurate? |
|-----------|-------------|-------------------|
| User has email in account | ✅ Yes | ✅ Yes |
| User has no email | ❌ No | ⚠️ Misleading |
| Email sending fails | ❌ No | ⚠️ Misleading |

### **Improved Message Options:**

**Option 1: Conditional Message**
```javascript
// Check if user has email
if (currentUser.email) {
  toast.success('🎉 Request submitted! You will receive an email notification.');
} else {
  toast.success('🎉 Request submitted! Check this page for status updates.');
}
```

**Option 2: Generic Message**
```javascript
toast.success('🎉 Authorization request submitted successfully! Check this page or your email for updates.');
```

**Option 3: Honest Message**
```javascript
toast.success('🎉 Request submitted! You will be notified when reviewed (via email if configured).');
```

---

## Testing Email Notifications

### **1. Test with Console Backend (Development)**
```python
# In settings.py
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```
**Result**: Emails printed to console instead of sent

### **2. Test with File Backend (Development)**
```python
# In settings.py
EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = 'tmp/emails'
```
**Result**: Emails saved to files

### **3. Test with Real SMTP (Production)**
```python
# In settings.py
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
# ... other settings
```
**Result**: Real emails sent

---

## Summary

✅ **Email comes from user's account** - Not from a form field  
✅ **Set by administrator** - When creating user account  
✅ **Automatic notifications** - No user input needed  
✅ **Fail-safe design** - System works even if email fails  
⚠️ **Message could be clearer** - Should indicate email is conditional  

### **Key Point:**
The success message says "You will receive an email notification" because the system **assumes** the user has an email address in their account. If they don't, the notification is silently skipped, but the request is still created successfully.

### **Recommendation:**
Update the success message to be more accurate:
```javascript
toast.success('🎉 Request submitted successfully! You can track its status on this page.');
```

This way, the message is always accurate regardless of whether the user has an email configured.
