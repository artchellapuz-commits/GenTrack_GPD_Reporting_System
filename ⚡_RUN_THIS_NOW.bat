@echo off
echo.
echo ================================================================
echo   GET PLANT STATUS - QUICK TEST
echo ================================================================
echo.
echo Running command...
echo.

cd backend
python manage.py get_plant_status --format text --days 30

echo.
echo ================================================================
echo   DONE! See the plant status above.
echo ================================================================
echo.
pause
