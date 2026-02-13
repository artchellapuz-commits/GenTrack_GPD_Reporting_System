@echo off
title NPC Reporting System - Launcher
color 0A

echo ═══════════════════════════════════════════════════════════════
echo   ▶️ NPC REPORTING SYSTEM - LAUNCHER
echo ═══════════════════════════════════════════════════════════════
echo.
echo This will start both Backend and Frontend servers.
echo.
echo Two windows will open:
echo   1. Backend (Django) - http://localhost:8000
echo   2. Frontend (Vue.js) - http://localhost:8080
echo.
echo Press any key to start...
pause >nul

echo.
echo Starting Backend Server...
start "NPC Backend - Django" cmd /k "cd backend && venv\Scripts\activate && python manage.py runserver"

timeout /t 3 /nobreak >nul

echo Starting Frontend Server...
start "NPC Frontend - Vue.js" cmd /k "cd frontend && npm run serve"

echo.
echo ═══════════════════════════════════════════════════════════════
echo   ✅ SYSTEM STARTING!
echo ═══════════════════════════════════════════════════════════════
echo.
echo Two windows have opened:
echo   - Backend: Django server
echo   - Frontend: Vue.js server
echo.
echo Wait 10-15 seconds for servers to start, then open:
echo   http://localhost:8080
echo.
echo To stop: Close both server windows or press Ctrl+C
echo.
echo ═══════════════════════════════════════════════════════════════
pause
