@echo off
echo ========================================
echo 🔄 RESTARTING SYSTEM WITH CACHE CLEAR
echo ========================================
echo.

echo Step 1: Clearing frontend cache...
cd frontend
if exist node_modules\.cache (
    rmdir /s /q node_modules\.cache
    echo ✅ Frontend cache cleared!
) else (
    echo ℹ️  No cache to clear
)
cd ..

echo.
echo ========================================
echo ✅ CACHE CLEARED!
echo ========================================
echo.
echo Now you need to:
echo.
echo 1. Stop backend (Ctrl+C in backend terminal)
echo 2. Stop frontend (Ctrl+C in frontend terminal)
echo.
echo 3. Start backend:
echo    cd backend
echo    python manage.py runserver
echo.
echo 4. Start frontend (in new terminal):
echo    cd frontend
echo    npm run serve
echo.
echo 5. In browser:
echo    - Press F12 (DevTools)
echo    - Right-click refresh button
echo    - Select "Empty Cache and Hard Reload"
echo.
echo 6. Logout and login again with viewer1/test123
echo.
echo ========================================
pause
