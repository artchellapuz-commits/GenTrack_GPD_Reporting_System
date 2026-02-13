@echo off
echo ========================================
echo PRIORITY 1 FEATURES SETUP
echo ========================================
echo.
echo This will:
echo 1. Install Chart.js (already installed)
echo 2. Install JWT library (already installed)
echo 3. Run database migrations
echo 4. Verify setup
echo.
pause

echo.
echo [1/3] Checking Chart.js...
cd frontend
call npm list chart.js
if %errorlevel% neq 0 (
    echo Installing Chart.js...
    call npm install chart.js
)
cd ..

echo.
echo [2/3] Checking Django JWT...
cd backend
call venv\Scripts\activate.bat
pip show djangorestframework-simplejwt
if %errorlevel% neq 0 (
    echo Installing JWT...
    pip install djangorestframework-simplejwt
)

echo.
echo [3/3] Running migrations...
python manage.py makemigrations
python manage.py migrate

echo.
echo ========================================
echo SETUP COMPLETE!
echo ========================================
echo.
echo Next steps:
echo 1. Start backend: cd backend ^&^& venv\Scripts\activate ^&^& python manage.py runserver
echo 2. Start frontend: cd frontend ^&^& npm run serve
echo 3. Open http://localhost:8081
echo 4. Try logging in or registering
echo.
pause
