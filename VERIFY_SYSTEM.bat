@echo off
echo ========================================
echo NPC Reporting System - Verification
echo ========================================
echo.

echo Checking Python...
python --version
if %errorlevel% neq 0 (
    echo ERROR: Python not found!
    goto :error
)
echo ✓ Python OK
echo.

echo Checking Node.js...
node --version
if %errorlevel% neq 0 (
    echo ERROR: Node.js not found!
    goto :error
)
echo ✓ Node.js OK
echo.

echo Checking Backend...
cd backend
if not exist "venv" (
    echo ERROR: Virtual environment not found!
    cd ..
    goto :error
)
echo ✓ Virtual environment exists

if not exist "db.sqlite3" (
    echo ERROR: Database not found!
    cd ..
    goto :error
)
echo ✓ Database exists
cd ..
echo.

echo Checking Frontend...
cd frontend
if not exist "node_modules" (
    echo ERROR: Node modules not found!
    cd ..
    goto :error
)
echo ✓ Node modules installed
cd ..
echo.

echo Checking Database Content...
cd backend
.\venv\Scripts\python.exe -c "import django; import os; os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'npc_reporting.settings'); django.setup(); from reports.models import Plant, HistoricalData, GenerationReport; print(f'Plants: {Plant.objects.count()}'); print(f'Historical Data: {HistoricalData.objects.count()}'); print(f'Generation Reports: {GenerationReport.objects.count()}')"
cd ..
echo.

echo ========================================
echo ✓ ALL CHECKS PASSED!
echo ========================================
echo.
echo Your system is ready to use!
echo.
echo To start the system, run: START_SYSTEM.bat
echo Or open: http://localhost:8081 (if already running)
echo.
pause
exit /b 0

:error
echo.
echo ========================================
echo ✗ VERIFICATION FAILED
echo ========================================
echo.
echo Please check the error messages above.
echo Refer to SETUP_GUIDE.md for help.
echo.
pause
exit /b 1
