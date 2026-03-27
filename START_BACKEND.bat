@echo off
echo ========================================
echo Starting NPC Backend Server
echo ========================================
echo.

cd backend

if not exist "venv\" (
    echo [ERROR] Virtual environment not found!
    echo Please run AUTOMATED_SETUP.bat first
    pause
    exit /b 1
)

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo Starting Django development server...
echo Backend will be available at: http://localhost:8000
echo Admin panel: http://localhost:8000/admin
echo.
echo Press Ctrl+C to stop the server
echo.

python manage.py runserver
