@echo off
echo ========================================
echo PULANGI 4 DIAGNOSTIC
echo ========================================
echo.

cd backend

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo Checking if Pulangi 4 exists in database...
python manage.py shell -c "from reports.models import Plant, Unit; p = Plant.objects.get(code='PULANGI4'); print(f'\nPlant: {p.name}'); print(f'Code: {p.code}'); print(f'Units: {p.units.count()}'); print(f'\nPlant Choices:'); print([c[0] for c in Plant.PLANT_CHOICES])"

echo.
echo ========================================
echo.
echo If you see PULANGI4 in the list above, the database is correct.
echo.
echo NEXT STEP: Restart the backend server!
echo   1. Stop the backend (Ctrl+C in terminal)
echo   2. Run: START_BACKEND.bat
echo.
pause
