@echo off
echo ========================================
echo  Serving Production Build with Node
echo ========================================
echo.
echo Installing 'serve' package if needed...
cd frontend
call npm install -g serve

echo.
echo Starting production server...
echo Frontend: http://localhost:8080
echo Backend API: http://localhost:8000
echo.
echo Press Ctrl+C to stop
echo.

serve -s dist -l 8080
