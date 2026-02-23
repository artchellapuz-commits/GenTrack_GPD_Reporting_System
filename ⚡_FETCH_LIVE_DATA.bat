@echo off
echo ================================================================
echo   FETCH LIVE DATA FROM NPC
echo ================================================================
echo.

cd backend

echo Fetching live plant data...
echo.

python manage.py fetch_live_data --sync --output live_data.json

echo.
echo ================================================================
echo   DONE
echo ================================================================
echo.
echo Data synced to database and saved to live_data.json
echo.

pause
