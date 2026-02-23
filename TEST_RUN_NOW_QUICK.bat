@echo off
echo ========================================
echo QUICK TEST - RUN NOW BUTTON
echo ========================================
echo.
echo Testing if the fix works...
echo.

cd backend
python test_run_now.py

echo.
echo ========================================
echo If test passed, the Run Now button should work!
echo Go to: http://localhost:8080/scheduled-reports
echo ========================================
pause
