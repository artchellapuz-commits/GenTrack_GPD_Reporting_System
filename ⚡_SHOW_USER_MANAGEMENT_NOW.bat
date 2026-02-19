@echo off
echo ================================================================
echo   FIXING USER MANAGEMENT VISIBILITY
echo ================================================================
echo.
echo This will check and fix your admin user configuration...
echo.

cd backend

echo Step 1: Checking admin user...
python check_admin_user.py

echo.
echo ================================================================
echo   DONE!
echo ================================================================
echo.
echo Now do this:
echo 1. Restart the backend server (if running)
echo 2. Go to the frontend and LOGOUT
echo 3. LOGIN again with:
echo    Username: admin
echo    Password: admin123
echo 4. Check the sidebar - User Management should now appear!
echo.
echo ================================================================
pause
