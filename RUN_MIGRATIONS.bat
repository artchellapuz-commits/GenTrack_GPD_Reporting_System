@echo off
echo Running database migrations...
cd backend
call venv\Scripts\activate.bat
python manage.py migrate
pause
