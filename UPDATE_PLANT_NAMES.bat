@echo off
echo ============================================================
echo UPDATING PLANT NAMES
echo ============================================================
echo.
echo Adding "Power" to plant names...
echo (Hydroelectric Plant → Hydroelectric Power Plant)
echo.

cd backend
python update_plant_names.py

echo.
echo ============================================================
echo DONE!
echo ============================================================
echo.
echo Plant names have been updated in the database.
echo Refresh your browser to see the changes.
echo.
pause
