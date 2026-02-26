@echo off
echo ========================================
echo  CLEARING CACHE AND RESTARTING FRONTEND
echo ========================================
echo.

cd npc-reporting-system\frontend

echo [1/4] Stopping any running dev servers...
taskkill /F /IM node.exe 2>nul
timeout /t 2 /nobreak >nul

echo [2/4] Clearing dist folder...
if exist dist rmdir /s /q dist

echo [3/4] Clearing node_modules/.cache...
if exist node_modules\.cache rmdir /s /q node_modules\.cache

echo [4/4] Starting fresh dev server...
echo.
echo ========================================
echo  Dev server starting...
echo  Once running, open: http://localhost:8080
echo  Press Ctrl+Shift+R to hard refresh
echo ========================================
echo.

npm run serve
