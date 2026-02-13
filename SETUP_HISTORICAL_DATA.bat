@echo off
echo ========================================
echo NPC Historical Data Setup
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
echo Setup Complete!
echo ========================================
echo.
echo The historical data tables have been created.
echo.
echo Next steps:
echo   1. Place your Excel files in the backend folder:
echo      - 0PLANT DEPCAP.xlsx
echo      - 1DATA APAO.xlsx
echo.
echo   2. Run: IMPORT_HISTORICAL_DATA.bat
echo.
echo Or generate sample data first:
echo   python CREATE_SAMPLE_HISTORICAL_DATA.py
echo.
pause
