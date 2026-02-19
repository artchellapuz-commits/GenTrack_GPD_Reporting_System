@echo off
echo ========================================
echo  Month 2 Features Setup
echo  PWA + Automated Reports + Analytics
echo ========================================
echo.

echo [1/4] Running database migrations...
cd backend
python manage.py migrate
if errorlevel 1 (
    echo ERROR: Migration failed!
    pause
    exit /b 1
)
echo ✓ Migrations completed
echo.

echo [2/4] Creating media directories...
if not exist "media\automated_reports" mkdir media\automated_reports
if not exist "media\exports" mkdir media\exports
echo ✓ Directories created
echo.

echo [3/4] Collecting static files...
python manage.py collectstatic --noinput
echo ✓ Static files collected
echo.

echo [4/4] Testing scheduled reports command...
python manage.py run_scheduled_reports
echo ✓ Command tested
echo.

cd ..

echo ========================================
echo  Setup Complete!
echo ========================================
echo.
echo Next Steps:
echo 1. Create icons in frontend/public/icons/
echo 2. Update router to add new routes
echo 3. Configure email settings in settings.py
echo 4. Setup Task Scheduler for automated reports
echo.
echo See MONTH_2_IMPLEMENTATION_GUIDE.md for details
echo.
pause
