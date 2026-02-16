@echo off
echo ========================================
echo Update Pulangi 4 Plant Name
echo ========================================
echo.

cd backend

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo Running update script...
python update_pulangi4_name.py

echo.
echo ========================================
echo Update Complete!
echo ========================================
echo.
pause
