@echo off
REM PSR Report Import Script
REM Imports historical data from PSR (Plant Status Report) Excel files

echo.
echo ========================================
echo PSR REPORT IMPORTER
echo ========================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher
    pause
    exit /b 1
)

REM Check if virtual environment exists
if not exist "backend\venv\Scripts\activate.bat" (
    echo ERROR: Virtual environment not found
    echo Please run AUTOMATED_SETUP.bat first
    pause
    exit /b 1
)

REM Activate virtual environment
call backend\venv\Scripts\activate.bat

REM Check if file path is provided
if "%~1"=="" (
    echo No file specified, using default PSR report...
    python IMPORT_PSR_REPORT.py
) else (
    echo Importing file: %~1
    python IMPORT_PSR_REPORT.py "%~1"
)

echo.
echo ========================================
echo.

pause
