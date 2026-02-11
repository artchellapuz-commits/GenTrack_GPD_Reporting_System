@echo off
echo ========================================
echo NPC Reporting System - Backend Setup
echo ========================================
echo.

cd backend

echo Step 1: Creating virtual environment...
python -m venv venv
if %errorlevel% neq 0 (
    echo [ERROR] Failed to create virtual environment
    pause
    exit /b 1
)
echo [OK] Virtual environment created
echo.

echo Step 2: Activating virtual environment...
call venv\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo [ERROR] Failed to activate virtual environment
    pause
    exit /b 1
)
echo [OK] Virtual environment activated
echo.

echo Step 3: Upgrading pip...
python -m pip install --upgrade pip
echo.

echo Step 4: Installing dependencies (this may take a few minutes)...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo [ERROR] Failed to install dependencies
    pause
    exit /b 1
)
echo [OK] Dependencies installed
echo.

echo ========================================
echo Backend Setup Complete!
echo ========================================
echo.
echo IMPORTANT: You need PostgreSQL installed to continue.
echo.
echo Next steps:
echo 1. Install PostgreSQL from: https://www.postgresql.org/download/windows/
echo 2. Create database: CREATE DATABASE npc_reporting;
echo 3. Update backend\.env with your PostgreSQL password
echo 4. Run: python manage.py migrate
echo 5. Run: python manage.py createsuperuser
echo 6. Run: python manage.py runserver
echo.
pause
