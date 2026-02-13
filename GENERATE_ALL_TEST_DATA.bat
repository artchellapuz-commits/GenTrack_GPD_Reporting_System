@echo off
echo ============================================================
echo GENERATING TEST DATA FOR ALL PLANTS
echo ============================================================
echo.

echo [1/4] Generating AGUS4 data (30 days, high CF)...
python CREATE_TEST_DATA_AGUS4.py
echo.

echo [2/4] Generating AGUS5 data (45 days, with maintenance)...
python CREATE_TEST_DATA_AGUS5.py
echo.

echo [3/4] Generating AGUS6 data (60 days, seasonal variation)...
python CREATE_TEST_DATA_AGUS6.py
echo.

echo [4/4] Generating AGUS7 data (15 days, recent high performance)...
python CREATE_TEST_DATA_AGUS7.py
echo.

echo ============================================================
echo ALL TEST FILES GENERATED!
echo ============================================================
echo.
echo Files created in backend folder:
echo   - SAMPLE_AGUS4_30DAYS.xlsx  (120 records)
echo   - SAMPLE_AGUS5_45DAYS.xlsx  (90 records)
echo   - SAMPLE_AGUS6_60DAYS.xlsx  (240 records)
echo   - SAMPLE_AGUS7_15DAYS.xlsx  (60 records)
echo.
echo TOTAL: 510 new records across 4 plants
echo.
echo ============================================================
echo HOW TO USE:
echo ============================================================
echo.
echo 1. Go to Upload page in your browser
echo 2. Select plant (AGUS4, AGUS5, AGUS6, or AGUS7)
echo 3. Upload the corresponding Excel file
echo 4. Check Dashboard to see the new data and charts!
echo.
echo ============================================================
pause
