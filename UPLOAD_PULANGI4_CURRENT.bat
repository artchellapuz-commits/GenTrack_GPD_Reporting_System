@echo off
echo ============================================================
echo UPLOAD PULANGI 4 DATA (Feb 10-13, 2026)
echo ============================================================
echo.
echo This will upload Pulangi 4 data for the dates you're viewing
echo in the View Reports page (Feb 10-13, 2026)
echo.
pause

cd backend
python test_upload.py ..\SAMPLE_PULANGI4_FEB10-13.xlsx PULANGI4

echo.
echo ============================================================
echo DONE!
echo ============================================================
echo.
echo Now go to View Reports and filter:
echo   - Plant: Pulangi 4
echo   - Start Date: 2026-02-10
echo   - End Date: 2026-02-13
echo.
echo You should see 12 records (3 units x 4 days)
echo.
pause
