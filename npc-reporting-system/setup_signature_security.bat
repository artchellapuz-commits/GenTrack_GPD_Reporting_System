@echo off
REM Setup script for E-Signature Security Implementation
REM Run this from the npc-reporting-system directory

echo ========================================
echo E-Signature Security Setup
echo ========================================
echo.

cd backend

echo Step 1: Installing new dependencies...
pip install cryptography>=41.0.0 pyotp>=2.9.0
echo.

echo Step 2: Generating security keys...
echo.
echo SIGNATURE_SECRET_KEY:
python -c "import secrets; print(secrets.token_urlsafe(32))"
echo.
echo SIGNATURE_ENCRYPTION_KEY:
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
echo.
echo IMPORTANT: Copy these keys to your .env file!
echo.
pause

echo Step 3: Running migrations...
python manage.py makemigrations
python manage.py migrate
echo.

echo Step 4: Creating security settings...
python -c "from reports.models import SignatureSecuritySettings; settings = SignatureSecuritySettings.get_settings(); print(f'Security settings created: ID={settings.id}')"
echo.

echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Update your .env file with the generated keys
echo 2. Configure email settings for 2FA
echo 3. Grant signatory authorizations in Django admin
echo 4. Test the implementation
echo.
echo See SIGNATURE_SECURITY_IMPLEMENTATION_GUIDE.md for details
echo.
pause
