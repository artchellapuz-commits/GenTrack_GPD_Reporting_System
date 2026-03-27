@echo off
echo ========================================
echo NPC Reporting System - Startup Script
echo ========================================
echo.

echo Starting Backend Server (Django)...
start "NPC Backend" cmd /k "cd backend && .\venv\Scripts\activate && python manage.py runserver"
timeout /t 3 /nobreak >nul

echo Starting Frontend Server (Vue.js)...
start "NPC Frontend" cmd /k "cd frontend && npm run serve"

echo.
echo ========================================
echo System Starting...
echo ========================================
echo.
echo Backend will be available at: http://localhost:8000
echo Frontend will be available at: http://localhost:8081
echo.
echo Please wait 10-15 seconds for both servers to start.
echo.
echo Press any key to open the application in your browser...
pause >nul

start http://localhost:8081

echo.
echo System is running!
echo Close the terminal windows to stop the servers.
echo.
