@echo off
echo ========================================
echo  GENERATE DATA REQUEST TEMPLATE
echo ========================================
echo.
echo This will create an Excel template to give to your supervisor
echo showing exactly what data format is needed.
echo.

cd /d "%~dp0"

echo Checking if openpyxl is installed...
python -c "import openpyxl" 2>nul

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo openpyxl is not installed!
    echo.
    echo Installing openpyxl...
    pip install openpyxl
    echo.
)

echo.
echo Running Python script...
python CREATE_DATA_REQUEST_TEMPLATE.py

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================
    echo  SUCCESS!
    echo ========================================
    echo.
    echo Template created: DATA_REQUEST_TEMPLATE.xlsx
    echo.
    echo This file contains:
    echo   - Instructions on what data is needed
    echo   - Sample data showing correct format
    echo   - Blank data entry sheet
    echo   - Validation rules
    echo   - Plant information
    echo.
    echo NEXT STEPS:
    echo 1. Open DATA_REQUEST_TEMPLATE.xlsx
    echo 2. Review the instructions
    echo 3. Give this file to your supervisor
    echo 4. Use it to explain what data you need
    echo.
) else (
    echo.
    echo ========================================
    echo  ERROR!
    echo ========================================
    echo.
    echo Failed to create template.
    echo.
    echo Possible solutions:
    echo 1. Make sure Python is installed
    echo 2. Try running: pip install openpyxl
    echo 3. Check if you have internet connection
    echo.
)

pause
