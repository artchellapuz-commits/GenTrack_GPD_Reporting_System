@echo off
echo ========================================
echo FIX RUN NOW BUTTON ERROR
echo ========================================
echo.
echo This will:
echo 1. Clear Python cache files
echo 2. Reset scheduled reports tables
echo 3. Run migrations fresh
echo.
pause

cd backend

echo.
echo [1/5] Clearing Python cache...
for /d /r . %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d"
del /s /q *.pyc 2>nul

echo.
echo [2/5] Backing up database...
copy db.sqlite3 db.sqlite3.backup_%date:~-4,4%%date:~-10,2%%date:~-7,2%_%time:~0,2%%time:~3,2%%time:~6,2%

echo.
echo [3/5] Dropping scheduled reports tables...
python -c "import sqlite3; conn = sqlite3.connect('db.sqlite3'); conn.execute('DROP TABLE IF EXISTS report_executions'); conn.execute('DROP TABLE IF EXISTS scheduled_reports_plants'); conn.execute('DROP TABLE IF EXISTS scheduled_reports_recipients'); conn.execute('DROP TABLE IF EXISTS scheduled_reports'); conn.commit(); conn.close(); print('Tables dropped successfully')"

echo.
echo [4/5] Running migrations...
python manage.py migrate reports 0009
python manage.py migrate reports 0010

echo.
echo [5/5] Creating sample scheduled reports...
python -c "from django.utils import timezone; from datetime import time; from reports.models_scheduled import ScheduledReport; from django.contrib.auth.models import User; admin = User.objects.filter(is_superuser=True).first(); if admin: [ScheduledReport.objects.get_or_create(name=f'Daily {t} Report', defaults={'report_type': t, 'frequency': 'DAILY', 'schedule_time': time(8, 0), 'date_range_days': 30, 'format': 'EXCEL', 'status': 'ACTIVE', 'created_by': admin, 'next_run': timezone.now()}) for t in ['GENERATION_SUMMARY', 'CAPACITY_FACTOR', 'AVAILABILITY', 'PERFORMANCE_METRICS']]; print('Sample reports created')"

echo.
echo ========================================
echo DONE! Now:
echo 1. RESTART your backend server (Ctrl+C then START_BACKEND.bat)
echo 2. Refresh the Scheduled Reports page
echo 3. Click "Run Now" button
echo ========================================
pause
