# Gmail App Password Setup Guide

## Issue
Gmail requires App Passwords for third-party applications when 2-Factor Authentication is enabled.

## Step-by-Step Setup

### 1. Enable 2-Factor Authentication
1. Go to [Google Account Settings](https://myaccount.google.com/)
2. Click **Security** in the left sidebar
3. Under "Signing in to Google", click **2-Step Verification**
4. Follow the setup process to enable 2FA

### 2. Generate App Password
1. Still in **Security** settings
2. Under "Signing in to Google", click **App passwords**
3. You might need to sign in again
4. Select app: **Mail**
5. Select device: **Other (Custom name)**
6. Enter name: **NPC Reporting System**
7. Click **Generate**
8. **Copy the 16-character password** (it looks like: `abcd efgh ijkl mnop`)

### 3. Update Email Configuration
Replace the password in your `.env` file with the App Password:

```env
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=zahurtongtong@gmail.com
EMAIL_HOST_PASSWORD=abcd efgh ijkl mnop
DEFAULT_FROM_EMAIL=noreply@gpd.com
```

### 4. Alternative: Use a Different Email Provider

If you don't want to use Gmail, here are other options:

#### Outlook/Hotmail
```env
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp-mail.outlook.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@outlook.com
EMAIL_HOST_PASSWORD=your-regular-password
DEFAULT_FROM_EMAIL=your-email@outlook.com
```

#### Yahoo Mail
```env
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.mail.yahoo.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@yahoo.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=your-email@yahoo.com
```

## Quick Fix

Run the setup script again with the correct App Password:

```bash
cd npc-reporting-system/backend
python setup_email.py
```

When prompted:
1. Select **2** (SMTP Backend)
2. Select **1** (Gmail)
3. Enter your Gmail address: `zahurtongtong@gmail.com`
4. Enter the **16-character App Password** (not your regular password)
5. Press Enter for default from email or enter a custom one

## Test After Setup

```bash
cd npc-reporting-system
python test_email_notifications.py
```

You should see:
```
✅ Basic Email Sending: ✅ OK
✅ Authorization Notifications: ✅ OK
```

## Troubleshooting

### "Application-specific password required"
- You need to generate an App Password from Google Account settings
- Don't use your regular Gmail password

### "Username and password not accepted"
- Double-check the App Password (16 characters with spaces)
- Make sure 2FA is enabled on your Google account

### "Less secure app access"
- This is the old method - use App Passwords instead
- Google no longer supports "less secure apps"

## Security Note
- App Passwords are safer than regular passwords for third-party apps
- You can revoke App Passwords anytime from Google Account settings
- Each app should have its own App Password