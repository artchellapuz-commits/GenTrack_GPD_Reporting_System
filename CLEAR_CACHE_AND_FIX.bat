@echo off
echo ========================================
echo CLEAR PYTHON CACHE - FIX RUN NOW BUTTON
echo ========================================
echo.
echo This will clear Python cache files that are causing the error.
echo.
echo IMPORTANT: Make sure backend server is STOPPED before running this!
echo Press Ctrl+C in the backend terminal first.
echo.
pause

cd backend

echo.
echo Clearing Python cache...
echo.

REM Delete __pycache__ directories
for /d /r . %%d in (__pycache__) do @if exist "%%d" (
    echo Deleting: %%d
    rd /s /q "%%d"
)

REM Delete .pyc files
echo.
echo Deleting .pyc files...
del /s /q *.pyc 2>nul

echo.
echo ========================================
echo CACHE CLEARED!
echo ========================================
echo.
echo Now:
echo 1. Start backend: START_BACKEND.bat
echo 2. Refresh Scheduled Reports page
echo 3. Click "Run Now" button
echo.
echo It should work now!
echo ========================================
pause
