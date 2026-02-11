@echo off
echo ========================================
echo NPC Reporting System - Prerequisites Check
echo ========================================
echo.

echo Checking Python...
python --version 2>nul
if %errorlevel% neq 0 (
    echo [X] Python NOT found
    echo     Install from: https://www.python.org/downloads/
    echo     IMPORTANT: Check "Add Python to PATH" during installation
) else (
    echo [OK] Python found
)
echo.

echo Checking Node.js...
node --version 2>nul
if %errorlevel% neq 0 (
    echo [X] Node.js NOT found
    echo     Install from: https://nodejs.org/
) else (
    echo [OK] Node.js found
)
echo.

echo Checking npm...
npm --version 2>nul
if %errorlevel% neq 0 (
    echo [X] npm NOT found
    echo     Should be installed with Node.js
) else (
    echo [OK] npm found
)
echo.

echo Checking PostgreSQL...
psql --version 2>nul
if %errorlevel% neq 0 (
    echo [X] PostgreSQL NOT found
    echo     Install from: https://www.postgresql.org/download/windows/
) else (
    echo [OK] PostgreSQL found
)
echo.

echo ========================================
echo Summary
echo ========================================
echo.
echo If any items show [X], please install them first.
echo Then restart your terminal and run this script again.
echo.
echo Once all show [OK], follow INSTALLATION_STEPS.md
echo.
pause
