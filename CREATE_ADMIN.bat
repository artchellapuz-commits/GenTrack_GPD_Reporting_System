@echo off
echo ========================================
echo Creating Django Admin User
echo ========================================
echo.

cd /d "%~dp0backend"
call venv\Scripts\activate.bat

echo.
echo Please enter admin credentials when prompted:
echo.
python manage.py createsuperuser

echo.
echo ========================================
echo Admin user created!
echo ========================================
echo.
echo You can now login at: http://127.0.0.1:8000/admin/
echo.
pause
