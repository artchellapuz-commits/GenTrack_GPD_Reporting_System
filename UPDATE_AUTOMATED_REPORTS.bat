@echo off
echo ========================================
echo UPDATE AUTOMATED REPORTS TO PSR ONLY
echo ========================================
echo.
echo This will update the Automated Reports system to only generate PSR reports.
echo.
echo CHANGES:
echo - Report type options reduced to PSR only
echo - All existing scheduled reports will be updated to PSR type
echo - Automated reports will use PSRExporter for proper formatting
echo.
pause

cd backend

echo.
echo Running database migration...
python manage.py migrate reports 0011_update_report_types_to_psr
echo.

if %ERRORLEVEL% EQU 0 (
    echo ========================================
    echo SUCCESS! Automated Reports Updated
    echo ========================================
    echo.
    echo WHAT CHANGED:
    echo 1. Report type is now PSR only
    echo 2. All scheduled reports updated to PSR
    echo 3. Generated reports use official PSR format
    echo.
    echo NEXT STEPS:
    echo 1. Restart backend if running
    echo 2. Go to Automated Reports page
    echo 3. Create or edit scheduled reports
    echo 4. Only PSR option will be available
    echo.
) else (
    echo ========================================
    echo ERROR: Migration failed
    echo ========================================
    echo.
    echo Please check the error message above.
    echo.
)

pause
