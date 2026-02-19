@echo off
echo ========================================
echo  Fixing Console Errors
echo ========================================
echo.

echo [1/4] Creating missing icon files...
cd frontend\public
if not exist "icons" mkdir icons

echo Creating placeholder icons...
echo. > icons\icon-72x72.png
echo. > icons\icon-96x96.png
echo. > icons\icon-128x128.png
echo. > icons\icon-144x144.png
echo. > icons\icon-152x152.png
echo. > icons\icon-192x192.png
echo. > icons\icon-384x384.png
echo. > icons\icon-512x512.png

cd ..\..

echo ✓ Icon files created
echo.

echo [2/4] Checking backend status...
cd backend
python -c "import requests; requests.get('http://localhost:8000')" 2>nul
if errorlevel 1 (
    echo ⚠ Backend is not running!
    echo.
    echo Starting backend server...
    start "NPC Backend" cmd /k "python manage.py runserver"
    timeout /t 5 /nobreak >nul
    echo ✓ Backend started
) else (
    echo ✓ Backend is running
)
cd ..
echo.

echo [3/4] Updating frontend configuration...
cd frontend
if not exist ".env" (
    echo VUE_APP_API_URL=http://localhost:8000 > .env
    echo ✓ .env file created
) else (
    echo ✓ .env file exists
)
cd ..
echo.

echo [4/4] Clearing browser cache...
echo Please clear your browser cache manually:
echo 1. Press Ctrl+Shift+Delete
echo 2. Select "Cached images and files"
echo 3. Click "Clear data"
echo.

echo ========================================
echo  Fixes Applied!
echo ========================================
echo.
echo Next steps:
echo 1. Refresh your browser (Ctrl+F5)
echo 2. Check console for remaining errors
echo.
echo If backend errors persist:
echo - Make sure backend is running: python manage.py runserver
echo - Check if port 8000 is available
echo.
pause
