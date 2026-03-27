# Admin Guide: Password Reset Request Notifications

## How Admins Are Notified

When a user forgets their password and submits a reset request, admins are notified through multiple channels:

---

## 1. 📧 Email Notification (Automatic)

### What Happens:
- **Instant email** sent to all admin users when a password reset request is submitted
- Email includes all relevant information for quick action

### Email Contains:
```
Subject: Password Reset Request - [username]

A password reset request has been submitted.

Details:
- Username: john.doe
- Reason: Forgot password after vacation
- Request Date: 2026-03-05 09:45
- IP Address: 192.168.1.100

Please review this request in the admin panel and contact the user 
to reset their password.

Contact Information:
Email: gpd.support@npc.gov.ph

NPC Reporting System
```

### Who Receives Emails:
1. All users with **Admin role** in the system
2. All users with **is_staff = True**
3. Fallback: **gpd.support@npc.gov.ph** (if no admin emails configured)

### Current Email Configuration:
- **Backend**: Console (for development) - emails print to console
- **Production**: Configure SMTP in `.env` file (see setup below)

---

## 2. 🖥️ Django Admin Panel (Manual Check)

### Access Admin Panel:
1. Navigate to: `http://localhost:8000/admin/`
2. Login with admin credentials
3. Look for **"Password Reset Requests"** in the sidebar

### Admin Panel Features:

#### List View:
- See all password reset requests
- Columns displayed:
  - Username
  - Status (Pending/Approved/Rejected/Completed)
  - Created At
  - Processed By
  - Processed At

#### Filters Available:
- **Status**: Pending, Approved, Rejected, Completed
- **Created Date**: Filter by date range
- **Processed Date**: When admin handled it

#### Search Functionality:
- Search by username
- Search by reason text
- Search by admin notes

#### Bulk Actions:
- Select multiple requests
- Mark as Approved (bulk)
- Mark as Rejected (bulk)
- Mark as Completed (bulk)

---

## 3. 📋 Request Details View

When admin clicks on a request, they see:

### Request Information:
- **Username**: User requesting reset
- **Reason**: Why they need reset (optional)
- **IP Address**: Where request came from
- **Status**: Current status
- **Created At**: When submitted
- **Updated At**: Last modification

### Admin Actions:
- **Processed By**: Auto-filled with admin username
- **Processed At**: Auto-filled with timestamp
- **Admin Notes**: Internal notes (not visible to user)

### Status Options:
1. **PENDING** - Just submitted, needs review
2. **APPROVED** - Admin verified, ready to reset
3. **REJECTED** - Request denied
4. **COMPLETED** - Password has been reset

---

## 4. 🔄 Admin Workflow

### Step-by-Step Process:

#### Step 1: Receive Notification
- Check email inbox for password reset notification
- OR check admin panel for pending requests

#### Step 2: Review Request
- Log into admin panel
- Navigate to "Password Reset Requests"
- Click on the pending request
- Review:
  - Username
  - Reason provided
  - IP address
  - Request timestamp

#### Step 3: Verify User Identity
- Contact user via:
  - Email (from user profile)
  - Phone (from user profile)
  - In person (if internal staff)
- Verify identity before proceeding

#### Step 4: Reset Password
- Go to "Users" section in admin panel
- Find the user
- Click on username
- Scroll to password section
- Click "this form" link to change password
- Enter new password (or generate one)
- Save changes

#### Step 5: Update Request Status
- Go back to "Password Reset Requests"
- Open the request
- Change status to "COMPLETED"
- Add admin notes (e.g., "Password reset via phone verification")
- Save

#### Step 6: Notify User
- Contact user with new password
- Instruct them to change password on first login
- Mark request as completed

---

## 5. ⚙️ Email Setup for Production

### Current Status:
- **Development**: Emails print to console/terminal
- **Production**: Needs SMTP configuration

### To Enable Real Email Notifications:

#### Option A: Gmail SMTP (Recommended for Testing)

1. Edit `.env` file in `backend/` folder:
```env
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=npc-reporting@npc.gov.ph
```

2. **Important**: Use Gmail App Password, not regular password
   - Go to Google Account Settings
   - Security → 2-Step Verification → App Passwords
   - Generate app password for "Mail"
   - Use that password in EMAIL_HOST_PASSWORD

#### Option B: Office 365 / Outlook SMTP

```env
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.office365.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@npc.gov.ph
EMAIL_HOST_PASSWORD=your-password
DEFAULT_FROM_EMAIL=npc-reporting@npc.gov.ph
```

#### Option C: Custom SMTP Server

```env
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=mail.your-domain.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=noreply@your-domain.com
EMAIL_HOST_PASSWORD=your-password
DEFAULT_FROM_EMAIL=npc-reporting@npc.gov.ph
```

### After Configuration:
1. Restart Django server
2. Test by submitting a password reset request
3. Check admin email inbox

---

## 6. 🔍 Monitoring & Reports

### Check Pending Requests:
```
Admin Panel → Password Reset Requests → Filter: Status = Pending
```

### View Request History:
```
Admin Panel → Password Reset Requests → Filter by date range
```

### Export Requests:
- Select requests in admin panel
- Use Django admin export functionality
- Generate reports for audit purposes

---

## 7. 🛡️ Security Features

### Built-in Security:
1. **Username Validation**: System verifies username exists before creating request
2. **IP Logging**: Records IP address of requester
3. **Timestamp Tracking**: Records when request was made
4. **Admin Audit Trail**: Tracks which admin processed each request
5. **Status Tracking**: Full lifecycle of each request
6. **No Automatic Reset**: Requires manual admin verification

### Best Practices:
- Always verify user identity before resetting password
- Use admin notes to document verification method
- Review IP address for suspicious activity
- Check request timestamp for urgency
- Mark requests as completed after reset

---

## 8. 📞 Contact Information

### For Password Reset Support:
- **Email**: gpd.support@npc.gov.ph
- **Phone**: +63 (XX) XXXX-XXXX
- **Admin Panel**: http://localhost:8000/admin/

### For Technical Issues:
- Contact IT Department
- Check system logs in `backend/logs/app.log`
- Review Django admin panel for errors

---

## 9. 🚨 Troubleshooting

### Email Not Received?

**Check 1**: Email Configuration
```bash
# In backend folder
python manage.py shell
>>> from django.core.mail import send_mail
>>> send_mail('Test', 'Test message', 'from@example.com', ['to@example.com'])
```

**Check 2**: Admin User Email
- Verify admin users have email addresses in their profiles
- Check User → Profile → Email field

**Check 3**: Console Output
- If using console backend, check terminal/console output
- Emails will be printed there during development

### Request Not Showing in Admin Panel?

**Check 1**: Database Migration
```bash
python manage.py migrate
```

**Check 2**: Admin Registration
- Verify PasswordResetRequest is registered in admin.py
- Restart Django server

**Check 3**: Permissions
- Ensure admin user has proper permissions
- Check is_staff = True

---

## 10. 📊 Sample Admin Dashboard View

```
┌─────────────────────────────────────────────────────────┐
│ Password Reset Requests                                  │
├─────────────────────────────────────────────────────────┤
│ Filter: [Status: Pending ▼] [Date: Today ▼]            │
├──────────┬──────────┬─────────────┬──────────┬─────────┤
│ Username │ Status   │ Created At  │ Proc. By │ Actions │
├──────────┼──────────┼─────────────┼──────────┼─────────┤
│ john.doe │ PENDING  │ 2026-03-05  │ -        │ [View]  │
│ jane.sm  │ APPROVED │ 2026-03-04  │ admin    │ [View]  │
│ bob.j    │ COMPLETE │ 2026-03-03  │ admin    │ [View]  │
└──────────┴──────────┴─────────────┴──────────┴─────────┘

Bulk Actions: [Mark as Approved ▼] [Go]
```

---

## Summary

Admins are notified through:
1. ✅ **Automatic email** to all admin users
2. ✅ **Admin panel** with pending requests list
3. ✅ **Detailed request view** with all information
4. ✅ **Bulk actions** for efficient processing
5. ✅ **Audit trail** for compliance

The system is designed to be secure, efficient, and easy to manage!
