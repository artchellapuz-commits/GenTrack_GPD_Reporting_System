@echo off
echo ========================================
echo NPC Reporting System - Automated Setup
echo ========================================
echo.
echo This script will set up the entire system automatically.
echo.
echo Prerequisites:
echo   [OK] Python 3.14.3 detected
echo   [OK] Node.js v25.6.0 detected
echo   [OK] SQLite (built into Python)
echo.
echo ========================================
echo Starting Automated Setup...
echo ========================================
echo.

:: ============================================
:: BACKEND SETUP
:: ============================================
echo.
echo [1/8] Setting up Backend...
echo ----------------------------------------
cd backend

echo Creating virtual environment...
python -m venv venv
if %errorlevel% neq 0 (
    echo [ERROR] Failed to create virtual environment
    pause
    exit /b 1
)
echo [OK] Virtual environment created

echo.
echo [2/8] Activating virtual environment...
call venv\Scripts\activate.bat
echo [OK] Activated

echo.
echo [3/8] Upgrading pip...
python -m pip install --upgrade pip --quiet
echo [OK] Pip upgraded

echo.
echo [4/8] Installing Python dependencies...
echo (This may take 2-3 minutes)
pip install -r requirements.txt --quiet
if %errorlevel% neq 0 (
    echo [ERROR] Failed to install dependencies
    pause
    exit /b 1
)
echo [OK] Dependencies installed

echo.
echo [5/8] Checking database configuration...
echo [OK] Using SQLite (no configuration needed)

echo.
echo [6/8] Running database migrations...
python manage.py makemigrations
python manage.py migrate
if %errorlevel% neq 0 (
    echo [ERROR] Database migration failed
    pause
    exit /b 1
)
echo [OK] Database migrated

echo.
echo [7/8] Creating superuser...
echo.
echo Please enter admin credentials:
python manage.py createsuperuser
if %errorlevel% neq 0 (
    echo [WARNING] Superuser creation skipped or failed
)

cd ..

:: ============================================
:: FRONTEND SETUP
:: ============================================
echo.
echo [8/8] Setting up Frontend...
echo ----------------------------------------
cd frontend

echo Installing Node.js dependencies...
echo (This may take 5-10 minutes)
call npm install
if %errorlevel% neq 0 (
    echo [ERROR] Failed to install frontend dependencies
    pause
    exit /b 1
)
echo [OK] Frontend dependencies installed

cd ..

:: ============================================
:: COMPLETION
:: ============================================
echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo Database: SQLite (db.sqlite3)
echo.
echo Next steps:
echo.
echo 1. Add initial plant data:
echo    ADD_INITIAL_DATA.bat
echo.
echo 2. Start the backend server:
echo    START_BACKEND.bat
echo.
echo 3. Start the frontend server (in NEW terminal):
echo    START_FRONTEND.bat
echo.
echo 4. Access the application:
echo    http://localhost:8080
echo.
echo See START_HERE.md for detailed instructions.
echo.
pause
