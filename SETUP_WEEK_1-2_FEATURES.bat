@echo off
echo ========================================
echo  Week 1-2 Features Setup
echo  - User Roles & Permissions
echo  - Email Notifications
echo  - Better Error Handling
echo ========================================
echo.

cd backend

echo [1/4] Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)
echo.

echo [2/4] Running migrations...
python manage.py makemigrations
python manage.py migrate
if errorlevel 1 (
    echo ERROR: Migration failed
    pause
    exit /b 1
)
echo.

echo [3/4] Creating logs directory...
if not exist "logs" mkdir logs
echo.

echo [4/4] Setup complete!
echo.
echo ========================================
echo  Next Steps:
echo ========================================
echo  1. Create admin user: python manage.py createsuperuser
echo  2. Start server: python manage.py runserver
echo  3. Read guide: WEEK_1-2_IMPLEMENTATION_GUIDE.md
echo.
echo  For email notifications (production):
echo  - Update backend/.env with SMTP settings
echo.
pause
