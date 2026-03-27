# Setup Real Email Delivery - Step by Step Guide

## Current Issue
The system is using `console.EmailBackend` which only prints emails to the terminal instead of sending real emails.

## Solution: Configure SMTP Email Backend

### Option 1: Gmail SMTP (Recommended for Testing)

1. **Enable 2-Factor Authentication** on your Gmail account
2. **Generate App Password**:
   - Go to Google Account settings
   - Security → 2-Step Verification → App passwords
   - Generate password for "Mail"
   - Copy the 16-character password

3. **Update .env file**:
```env
# Add these lines to backend/.env
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-gmail@gmail.com
EMAIL_HOST_PASSWORD=your-16-char-app-password
DEFAULT_FROM_EMAIL=your-gmail@gmail.com
```

### Option 2: Outlook/Hotmail SMTP

```env
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp-mail.outlook.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@outlook.com
EMAIL_HOST_PASSWORD=your-password
DEFAULT_FROM_EMAIL=your-email@outlook.com
```

### Option 3: Yahoo SMTP

```env
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.mail.yahoo.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@yahoo.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=your-email@yahoo.com
```

## Quick Setup Script

Run this interactive setup:

```bash
cd npc-reporting-system/backend
python setup_email.py
```

## Manual Setup Steps

1. **Edit the .env file**:
```bash
cd npc-reporting-system/backend
notepad .env
```

2. **Add email configuration** (example with Gmail):
```env
SECRET_KEY=django-insecure-test-key-for-development-only-change-in-production
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Email Configuration
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-gmail@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=your-gmail@gmail.com

# Database Configuration
DB_NAME=npc_reporting
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432

# AI Chatbot Configuration
AI_PROVIDER=
OPENAI_API_KEY=your-openai-api-key-here
OPENAI_MODEL=gpt-3.5-turbo
```

3. **Restart Django server**:
```bash
python manage.py runserver
```

4. **Test email delivery**:
```bash
cd ..
python test_email_notifications.py
```

## Troubleshooting

### Gmail Issues
- **"Username and password not accepted"**: Use App Password, not regular password
- **"Less secure app access"**: Enable 2FA and use App Password instead
- **"Authentication failed"**: Double-check App Password

### General Issues
- **Connection timeout**: Check firewall/antivirus
- **TLS errors**: Try `EMAIL_USE_SSL=True` and `EMAIL_PORT=465`
- **Authentication failed**: Verify credentials

## Test Real Email Delivery

After configuration, test with a real email:

```bash
cd npc-reporting-system
python -c "
import os, sys, django
sys.path.insert(0, 'backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'npc_reporting.settings')
django.setup()

from django.core.mail import send_mail
from django.conf import settings

print('Testing real email delivery...')
try:
    send_mail(
        'Test Email from NPC System',
        'This is a test email to verify real email delivery works.',
        settings.DEFAULT_FROM_EMAIL,
        ['your-real-email@example.com'],  # Replace with your email
        fail_silently=False,
    )
    print('✅ Email sent successfully!')
except Exception as e:
    print(f'❌ Email failed: {e}')
"
```

## Security Notes

- **Never commit email passwords to git**
- **Use App Passwords for Gmail**
- **Consider using environment variables in production**
- **Enable TLS/SSL for secure connections**

## Next Steps

1. Choose an email provider (Gmail recommended for testing)
2. Get credentials (App Password for Gmail)
3. Update .env file with SMTP settings
4. Restart Django server
5. Test email delivery
6. Submit authorization request to test full flow

Once configured, users will receive **real emails** at the addresses they provide in the authorization request form.