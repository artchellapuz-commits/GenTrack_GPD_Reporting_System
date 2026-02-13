@echo off
REM Import PLANT STATUS Historical Data
REM This script imports data from PLANT STATUS.xlsx

echo ========================================
echo   PLANT STATUS DATA IMPORT
echo ========================================
echo.

REM Check if virtual environment exists
if not exist "backend\venv\Scripts\activate.bat" (
    echo ERROR: Virtual environment not found!
    echo Please run AUTOMATED_SETUP.bat first.
    pause
    exit /b 1
)

REM Activate virtual environment
call backend\venv\Scripts\activate.bat

REM Change to backend directory
cd backend

echo Importing PLANT STATUS data...
echo.

REM Import the PLANT STATUS file
python manage.py import_historical_data --historical "..\REPORTS\8. PSR\PLANT STATUS.xlsx"

echo.
echo ========================================
echo   IMPORT COMPLETE
echo ========================================
echo.
echo Check the output above for any errors or warnings.
echo.

pause
