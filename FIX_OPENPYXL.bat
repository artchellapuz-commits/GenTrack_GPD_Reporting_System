@echo off
echo ========================================
echo FIXING OPENPYXL VERSION
echo ========================================
echo.

cd backend

echo Step 1: Upgrading openpyxl to latest version...
pip install --upgrade openpyxl
echo.

echo Step 2: Verifying installation...
pip show openpyxl
echo.

echo ========================================
echo OPENPYXL UPGRADE COMPLETE!
echo ========================================
echo.
echo Now restart your backend server:
echo 1. Stop the current backend server (Ctrl+C)
echo 2. Run: python manage.py runserver
echo.
pause
