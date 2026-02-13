@echo off
echo ========================================
echo NPC Historical Data Import Tool
echo ========================================
echo.

cd backend

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo Running database migrations...
python manage.py migrate

echo.
echo ========================================
echo Import Historical Data
echo ========================================
echo.
echo This script will import historical data from Excel files.
echo.
echo Expected files:
echo   1. 0PLANT DEPCAP.xlsx - Plant capacity data
echo   2. 1DATA APAO.xlsx - Historical operational data
echo.
echo Place these files in the backend folder before continuing.
echo.
pause

echo.
echo Starting import...
echo.

REM Check if files exist
if exist "0PLANT DEPCAP.xlsx" (
    if exist "1DATA APAO.xlsx" (
        python manage.py import_historical_data --capacity "0PLANT DEPCAP.xlsx" --historical "1DATA APAO.xlsx"
    ) else (
        python manage.py import_historical_data --capacity "0PLANT DEPCAP.xlsx"
        echo.
        echo WARNING: 1DATA APAO.xlsx not found, only imported capacity data
    )
) else (
    if exist "1DATA APAO.xlsx" (
        python manage.py import_historical_data --historical "1DATA APAO.xlsx"
        echo.
        echo WARNING: 0PLANT DEPCAP.xlsx not found, only imported historical data
    ) else (
        echo.
        echo ERROR: No data files found!
        echo Please place the Excel files in the backend folder.
        pause
        exit /b 1
    )
)

echo.
echo ========================================
echo Import Complete!
echo ========================================
echo.
echo You can now view the imported data through the API:
echo   - Historical Data: http://localhost:8000/api/historical-data/
echo   - Plant Capacity: http://localhost:8000/api/plant-capacity/
echo.
pause
