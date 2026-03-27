@echo off
echo ========================================
echo  NPC Reporting System - PRODUCTION MODE
echo ========================================
echo.
echo This will start:
echo   1. Django Backend (Port 8000)
echo   2. Production Frontend (Port 8080)
echo.
echo Make sure you have run: npm run build
echo.
pause

echo.
echo Starting Backend Server...
start "NPC Backend" cmd /k "cd backend && venv\Scripts\activate && python manage.py runserver"

timeout /t 3 /nobreak >nul

echo Starting Frontend Server...
start "NPC Frontend" cmd /k "cd frontend && npx serve -s dist -l 8080"

echo.
echo ========================================
echo  System Started!
echo ========================================
echo.
echo Frontend: http://localhost:8080
echo Backend:  http://localhost:8000
echo Admin:    http://localhost:8000/admin
echo.
echo Two windows opened - close them to stop servers
echo.
pause
