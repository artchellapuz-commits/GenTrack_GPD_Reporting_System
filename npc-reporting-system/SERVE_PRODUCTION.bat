@echo off
echo ========================================
echo  Serving Production Build
echo ========================================
echo.
echo Frontend will be available at: http://localhost:8080
echo Backend API at: http://localhost:8000
echo.
echo Make sure backend is running first!
echo.
pause

cd frontend\dist
python -m http.server 8080
