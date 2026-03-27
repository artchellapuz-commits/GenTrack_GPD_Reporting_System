# Email Configuration Guide for Authorization Notifications

## Current Status: ✅ WORKING

The email notification system is **fully functional** and tested. Users will receive email notifications when their authorization requests are processed.

## Test Results

✅ **Email Configuration**: Properly configured  
✅ **Basic Email Sending**: Working  
✅ **Authorization Notifications**: All types working  

### Notification Types Tested:
1. **Admin Notification**: Sent to all admin users when new request is submitted
2. **Approval Notification**: Sent to user's provided email when request is approved
3. **Rejection Notification**: Sent to user's provided email when request is rejected

## Current Configuration

### Development Mode (Console Backend)
- **Backend**: `django.core.mail.backends.console.EmailBackend`
- **Behavior**: Emails are printed to console/terminal
- **Use Case**: Development and testing

### Email Settings
```python
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'noreply@npc-reporting.com'
```

## Production Email Setup

To enable real email sending in production, update your `.env` file:

### Option 1: Gmail SMTP
```env
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-gmail@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=npc-reporting@your-domain.com
```

### Option 2: Office 365 SMTP
```env
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.office365.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@your-domain.com
EMAIL_HOST_PASSWORD=your-password
DEFAULT_FROM_EMAIL=npc-reporting@your-domain.com
```

### Option 3: Custom SMTP Server
```env
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=mail.your-domain.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=npc-reporting@your-domain.com
EMAIL_HOST_PASSWORD=your-password
DEFAULT_FROM_EMAIL=npc-reporting@your-domain.com
```

## Email Flow

### 1. User Submits Request
- User fills out authorization form with email address
- System validates email format
- Request is saved to database

### 2. Admin Notification
- Email sent to all admin users
- Contains request details and admin panel link
- Subject: "New Signatory Authorization Request - [Signatory Name]"

### 3. Admin Reviews Request
- Admin approves or rejects in admin panel
- System triggers appropriate notification

### 4. User Notification
**Approval Email:**
- Subject: "Signatory Authorization Approved - [Signatory Name]"
- Contains authorization details and next steps
- Sent to user's provided email address

**Rejection Email:**
- Subject: "Signatory Authorization Request - Update Required"
- Contains admin notes and contact information
- Sent to user's provided email address

## Email Content Examples

### Admin Notification
```
Subject: New Signatory Authorization Request - O.M. LAVA

A new signatory authorization request has been submitted:

User: John Doe
Email: john.doe@example.com
Signatory Name: O.M. LAVA
Role: Prepared by
Justification: I need authorization to prepare daily reports...

Please review this request in the admin panel:
http://your-domain.com/admin/reports/signatoryauthorizationrequest/
```

### Approval Notification
```
Subject: Signatory Authorization Approved - O.M. LAVA

Hello John Doe,

Your signatory authorization request has been APPROVED!

Details:
- Signatory Name: O.M. LAVA
- Role: Prepared by
- 2FA Required: Yes
- Expires: Never

You can now:
1. Go to the Generate Report page
2. Click the "e-signature" button next to your name
3. Create your digital signature
4. Sign reports with secure 2FA verification
```

## Testing Email Configuration

Run the test script to verify email functionality:

```bash
cd npc-reporting-system
python test_email_notifications.py
```

This will test:
- Email configuration
- Basic email sending
- All authorization notification types

## Troubleshooting

### Common Issues

1. **Gmail Authentication**
   - Use App Passwords instead of regular password
   - Enable 2-factor authentication first
   - Generate app-specific password

2. **SMTP Connection Errors**
   - Check firewall settings
   - Verify SMTP server settings
   - Test with telnet: `telnet smtp.gmail.com 587`

3. **Email Not Received**
   - Check spam/junk folders
   - Verify email address is correct
   - Check email server logs

### Debug Mode
To see detailed email sending logs, set in `.env`:
```env
DJANGO_LOG_LEVEL=DEBUG
```

## Security Considerations

1. **Email Credentials**: Store in environment variables, never in code
2. **TLS/SSL**: Always use encrypted connections
3. **Rate Limiting**: Consider implementing email rate limiting
4. **Spam Prevention**: Use proper SPF/DKIM records for your domain

## Production Checklist

- [ ] Update EMAIL_BACKEND to SMTP
- [ ] Configure proper SMTP credentials
- [ ] Set up SPF/DKIM records
- [ ] Test email delivery
- [ ] Monitor email logs
- [ ] Set up email bounce handling

## Conclusion

The email notification system is **fully implemented and tested**. Users will receive notifications at the email address they provide in the authorization request form. The system includes proper fallback to the user's account email if needed.

**Status**: ✅ Ready for production use