@echo off
echo ================================================================
echo   GET CURRENT PLANT STATUS FROM DATABASE
echo ================================================================
echo.

cd backend

echo Getting plant status...
echo.
python manage.py get_plant_status --format text

echo.
echo ================================================================
echo   SAVING TO FILES
echo ================================================================
echo.

python manage.py get_plant_status --format json --output plant_status.json
python manage.py get_plant_status --format csv --output plant_status.csv

echo.
echo Done! Check these files:
echo   - plant_status.json
echo   - plant_status.csv
echo.

pause
