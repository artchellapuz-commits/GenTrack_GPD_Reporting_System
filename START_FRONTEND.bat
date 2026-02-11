@echo off
echo ========================================
echo Starting NPC Frontend Server
echo ========================================
echo.

cd frontend

if not exist "node_modules\" (
    echo [ERROR] Node modules not found!
    echo Please run AUTOMATED_SETUP.bat first
    pause
    exit /b 1
)

echo.
echo Starting Vue.js development server...
echo Frontend will be available at: http://localhost:8080
echo.
echo Press Ctrl+C to stop the server
echo.

npm run serve
