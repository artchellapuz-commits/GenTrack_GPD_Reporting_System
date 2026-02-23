@echo off
echo.
echo ========================================
echo   OPENING PSR REPORT
echo ========================================
echo.

cd /d "%~dp0"

REM Find the most recent PSR report
for /f "delims=" %%i in ('dir /b /od "backend\media\exports\PSR_REPORT_*.xlsx" 2^>nul') do set "LATEST=%%i"

if defined LATEST (
    echo Opening: %LATEST%
    echo.
    start "" "backend\media\exports\%LATEST%"
    echo.
    echo ✓ PSR Report opened in Excel
) else (
    echo ❌ No PSR reports found
    echo.
    echo To generate a PSR report:
    echo 1. Go to Generate Report page
    echo 2. Select PSR report type
    echo 3. Click Generate Report
    echo.
    echo Or run: python test_psr_generation.py
)

echo.
pause
