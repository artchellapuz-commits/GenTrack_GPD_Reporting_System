@echo off
echo.
echo ========================================
echo   VERIFYING ARCHIVEFILE METHOD EXISTS
echo ========================================
echo.

cd npc-reporting-system\frontend\src\components

echo Searching for archiveFile method in UploadExcel.vue...
echo.

findstr /n /C:"async archiveFile" UploadExcel.vue

if %ERRORLEVEL% EQU 0 (
    echo.
    color 0A
    echo ========================================
    echo   METHOD EXISTS! ✓
    echo ========================================
    echo.
    echo The archiveFile method is in the file.
    echo The error is 100%% a browser caching issue.
    echo.
    echo SOLUTION:
    echo 1. Run NUCLEAR_FIX.bat
    echo 2. Open browser in Incognito mode
    echo 3. Test the archive button
    echo.
) else (
    color 0C
    echo.
    echo ========================================
    echo   METHOD NOT FOUND! ✗
    echo ========================================
    echo.
    echo The method is missing. This shouldn't happen.
    echo.
)

pause
