@echo off
echo ========================================
echo Installing Frontend Dependencies
echo ========================================
echo.

cd /d "%~dp0frontend"

echo Installing npm packages...
echo This may take a few minutes...
echo.

cmd /c npm install

if errorlevel 1 (
    echo.
    echo ========================================
    echo ERROR: npm install failed!
    echo ========================================
    echo.
    echo This might be due to PowerShell execution policy.
    echo.
    echo SOLUTION:
    echo 1. Open PowerShell as Administrator
    echo 2. Run: Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
    echo 3. Run this script again
    echo.
    pause
    exit /b 1
)

echo.
echo ========================================
echo Frontend dependencies installed!
echo ========================================
echo.
echo You can now run: START_FRONTEND.bat
echo.
pause
