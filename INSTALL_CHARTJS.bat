@echo off
echo ============================================================
echo INSTALLING CHART.JS FOR PLANT DETAIL CHARTS
echo ============================================================
echo.

cd frontend

echo Installing Chart.js and Vue-ChartJS...
call npm install chart.js vue-chartjs

echo.
echo ============================================================
echo INSTALLATION COMPLETE!
echo ============================================================
echo.
echo Chart.js has been installed successfully.
echo.
echo NEXT STEPS:
echo 1. Restart your frontend server (Ctrl+C then npm run serve)
echo 2. Go to Dashboard
echo 3. Click on any plant card with data (AGUS1 or AGUS2)
echo 4. You'll see detailed charts with real data!
echo.
echo ============================================================
pause
