@echo off
echo ========================================
echo Installing Pandas for Excel Support
echo ========================================
echo.

cd /d "%~dp0backend"
call venv\Scripts\activate.bat

echo Installing pandas and dependencies...
echo This may take a few minutes...
echo.

pip install pandas

if errorlevel 1 (
    echo.
    echo ========================================
    echo ERROR: Failed to install pandas
    echo ========================================
    echo.
    pause
    exit /b 1
)

echo.
echo ========================================
echo Pandas installed successfully!
echo ========================================
echo.
echo Excel import/export is now fully functional.
echo You can now upload Excel files to the system.
echo.
echo Restart the backend server if it's running:
echo 1. Close the backend terminal
echo 2. Run START_BACKEND.bat
echo.
pause
