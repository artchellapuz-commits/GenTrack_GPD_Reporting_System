@echo off
echo ========================================
echo Priority 1 Features - Quick Start
echo ========================================
echo.

echo Step 1: Installing Chart.js...
cd frontend
call npm install chart.js
if %errorlevel% neq 0 (
    echo ERROR: Failed to install Chart.js
    pause
    exit /b 1
)
echo ✓ Chart.js installed
echo.

echo Step 2: Checking backend dependencies...
cd ..\backend
call .\venv\Scripts\activate
pip install -q djangorestframework-simplejwt
echo ✓ Backend dependencies OK
echo.

echo Step 3: Running migrations...
python manage.py migrate
echo ✓ Migrations complete
echo.

echo ========================================
echo Installation Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Start backend: python manage.py runserver
echo 2. Start frontend: cd frontend ^&^& npm run serve
echo 3. Open http://localhost:8081
echo 4. Login or register
echo 5. See charts on dashboard!
echo.
echo Press any key to exit...
pause >nul
