@echo off
echo ========================================
echo Verify Pulangi 4 Plant Name
echo ========================================
echo.

cd backend

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo Checking database...
python verify_pulangi4_name.py

echo.
pause
