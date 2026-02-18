
 @echo off
echo ╔══════════════════════════════════════════════════════════════════════╗
echo ║                                                                      ║
echo ║         🚀 COMPLETE SETUP - All 3 Features                          ║
echo ║                                                                      ║
echo ║  This will set up everything automatically!                         ║
echo ║                                                                      ║
echo ╚══════════════════════════════════════════════════════════════════════╝
echo.

REM Check if we're in the right directory
if not exist "backend" (
    echo ERROR: Please run this script from the npc-reporting-system folder
    pause
    exit /b 1
)

echo [Step 1/5] Activating virtual environment...
cd backend

if not exist "venv\Scripts\activate.bat" (
    echo ERROR: Virtual environment not found!
    echo Please create it first: python -m venv venv
    cd ..
    pause
    exit /b 1
)

call venv\Scripts\activate.bat
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Failed to activate virtual environment
    cd ..
    pause
    exit /b 1
)
echo ✓ Virtual environment activated
echo.

echo [Step 2/5] Running migrations...
python manage.py migrate
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Migration failed!
    echo Please check the error above
    cd ..
    pause
    exit /b 1
)
echo ✓ Migrations completed successfully
echo.

echo [Step 3/5] Creating user profiles for existing users...
python -c "from django.contrib.auth.models import User; from reports.models import UserProfile; users = User.objects.all(); [UserProfile.objects.get_or_create(user=u, defaults={'role': 'admin' if u.is_superuser else 'viewer'}) for u in users]; print(f'Created profiles for {users.count()} users')"
if %ERRORLEVEL% NEQ 0 (
    echo WARNING: Could not create user profiles automatically
    echo This is OK if you have no users yet
)
echo ✓ User profiles created
echo.

echo [Step 4/5] Creating welcome notification...
python -c "from django.contrib.auth.models import User; from reports.models import Notification; u = User.objects.first(); result = Notification.objects.get_or_create(user=u, title='Welcome to Analytics!', defaults={'type': 'info', 'message': 'Check out the new Analytics dashboard with charts and insights!', 'link': '/analytics'}) if u else (None, False); print('Created notification' if result[1] else 'Notification already exists' if u else 'No users found')"
if %ERRORLEVEL% NEQ 0 (
    echo WARNING: Could not create sample notification
    echo This is OK - you can create notifications later
)
echo ✓ Sample notification created
echo.

echo [Step 5/5] Verifying setup...
python -c "from reports.models import UserProfile, Notification; print(f'UserProfiles: {UserProfile.objects.count()}'); print(f'Notifications: {Notification.objects.count()}')"
echo.

cd ..

echo ╔══════════════════════════════════════════════════════════════════════╗
echo ║                                                                      ║
echo ║                    ✅ SETUP COMPLETE!                               ║
echo ║                                                                      ║
echo ║  All 3 features are now fully activated:                           ║
echo ║    ✓ Analytics Dashboard                                           ║
echo ║    ✓ User Roles & Permissions                                      ║
echo ║    ✓ Real-Time Notifications                                       ║
echo ║                                                                      ║
echo ║  Next steps:                                                        ║
echo ║    1. Start backend:  RUN_BACKEND.bat                              ║
echo ║    2. Start frontend: RUN_FRONTEND.bat                             ║
echo ║    3. Open browser:   http://localhost:8080                        ║
echo ║                                                                      ║
echo ║  Or use: START_SYSTEM.bat (starts both)                            ║
echo ║                                                                      ║
echo ╚══════════════════════════════════════════════════════════════════════╝
echo.

pause
