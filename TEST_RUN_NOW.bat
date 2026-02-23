@echo off
echo ========================================
echo Testing Run Now Button Functionality
echo ========================================
echo.

cd backend
python test_run_report.py

echo.
echo ========================================
echo Test Complete!
echo ========================================
echo.
echo If successful, you should see:
echo - Report executed successfully
echo - File created in media/automated_reports/
echo.
echo Now try clicking Run Now in the browser!
echo.
pause
