@echo off
echo ========================================
echo   PSR REPORT IMPORT
echo ========================================
echo.

cd backend
call venv\Scripts\activate.bat
python manage.py import_historical_data --historical "..\..\REPORTS\8. PSR\PSR REPORT-8AM.xlsx"

echo.
echo ========================================
echo   IMPORT COMPLETE
echo ========================================
pause
