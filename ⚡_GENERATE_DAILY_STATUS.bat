@echo off
echo ================================================================
echo   GENERATE DAILY PLANT STATUS REPORT
echo ================================================================
echo.

cd backend

echo Generating report for today...
echo.

python manage.py generate_daily_status

echo.
echo ================================================================
echo   DONE
echo ================================================================
echo.
echo Report saved in backend folder
echo.

pause
