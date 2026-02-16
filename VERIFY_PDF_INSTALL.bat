@echo off
echo ========================================
echo Verifying PDF Packages Installation
echo ========================================
echo.

cd frontend

echo Checking if jspdf is installed...
call npm list jspdf
echo.

echo Checking if jspdf-autotable is installed...
call npm list jspdf-autotable
echo.

echo ========================================
echo Verification Complete
echo ========================================
echo.
echo If you see version numbers above, packages are installed.
echo If you see "UNMET DEPENDENCY" or errors, run:
echo   npm install jspdf jspdf-autotable --save
echo.
pause
