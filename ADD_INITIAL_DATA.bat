@echo off
echo ========================================
echo Adding Initial Plant Data to Database
echo ========================================
echo.

cd /d "%~dp0backend"
call venv\Scripts\activate.bat

echo Running Django script...
python add_initial_data.py

echo.
echo ========================================
echo DONE!
echo ========================================
echo.
echo 6 Agus plants have been added to the database:
echo - AGUS1 (4 units)
echo - AGUS2 (4 units)
echo - AGUS4 (4 units)
echo - AGUS5 (2 units)
echo - AGUS6 (4 units)
echo - AGUS7 (4 units)
echo.
echo You can verify at: http://127.0.0.1:8000/admin/
echo.
pause
