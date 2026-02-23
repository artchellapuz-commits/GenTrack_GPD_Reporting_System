@echo off
echo ========================================
echo OPENING GENERATED REPORTS FOLDER
echo ========================================
echo.
echo Opening: backend\media\automated_reports\
echo.

cd backend\media\automated_reports
start .

echo.
echo Folder opened in File Explorer!
echo.
echo You should see Excel files like:
echo - GENERATION_SUMMARY_YYYYMMDD_HHMMSS.xlsx
echo - CAPACITY_FACTOR_YYYYMMDD_HHMMSS.xlsx
echo - AVAILABILITY_YYYYMMDD_HHMMSS.xlsx
echo - PERFORMANCE_METRICS_YYYYMMDD_HHMMSS.xlsx
echo.
echo Double-click any file to open in Excel.
echo ========================================
pause
