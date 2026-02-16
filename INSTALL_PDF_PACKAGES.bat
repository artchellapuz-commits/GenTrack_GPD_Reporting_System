@echo off
echo ========================================
echo Installing PDF Export Packages
echo ========================================
echo.

cd frontend

echo Installing jspdf and jspdf-autotable...
call npm install jspdf jspdf-autotable

echo.
echo ========================================
echo Installation Complete!
echo ========================================
echo.
echo PDF export is now ready to use.
echo Please restart your dev server:
echo   npm run serve
echo.
pause
