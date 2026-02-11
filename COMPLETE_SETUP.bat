@echo off
echo ========================================
echo NPC REPORTING SYSTEM - COMPLETE SETUP
echo ========================================
echo.

echo Step 1: Installing Frontend Dependencies...
echo.
cd frontend
call npm install
if errorlevel 1 (
    echo ERROR: npm install failed!
    echo.
    echo Please run PowerShell as Administrator and execute:
    echo Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
    echo.
    pause
    exit /b 1
)

echo.
echo Step 2: Creating Django Superuser...
echo.
cd ..\backend
call venv\Scripts\activate.bat
echo.
echo Please enter admin credentials:
python manage.py createsuperuser

echo.
echo Step 3: Adding Initial Plant Data...
echo.
python manage.py shell < ..\add_plants.py

echo.
echo ========================================
echo SETUP COMPLETE!
echo ========================================
echo.
echo Backend is running at: http://127.0.0.1:8000/
echo.
echo To start frontend, run: START_FRONTEND.bat
echo.
pause
