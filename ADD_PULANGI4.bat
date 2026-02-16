@echo off
echo ========================================
echo Adding Pulangi 4 Hydro-electric Plant
echo ========================================
echo.

cd backend

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo Adding Pulangi 4 to the system...
python add_pulangi4.py

echo.
echo ========================================
echo Pulangi 4 has been added successfully!
echo ========================================
echo.
pause
