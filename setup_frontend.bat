@echo off
echo ========================================
echo NPC Reporting System - Frontend Setup
echo ========================================
echo.

cd frontend

echo Installing dependencies (this may take 5-10 minutes)...
echo Please wait...
echo.

npm install
if %errorlevel% neq 0 (
    echo [ERROR] Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo ========================================
echo Frontend Setup Complete!
echo ========================================
echo.
echo To start the frontend server, run:
echo   cd frontend
echo   npm run serve
echo.
pause
