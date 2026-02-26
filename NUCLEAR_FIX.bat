@echo off
color 0C
echo.
echo ========================================
echo   NUCLEAR FIX - ARCHIVE BUTTON
echo ========================================
echo.
echo This will AGGRESSIVELY fix the issue by:
echo 1. Killing ALL Node processes
echo 2. Deleting ALL cache folders
echo 3. Restarting EVERYTHING fresh
echo.
pause

cd npc-reporting-system\frontend

echo.
echo [1/8] KILLING ALL NODE PROCESSES...
taskkill /F /IM node.exe /T 2>nul
taskkill /F /IM npm.cmd /T 2>nul
timeout /t 3 /nobreak >nul
echo DONE!

echo.
echo [2/8] DELETING DIST FOLDER...
if exist dist (
    rmdir /s /q dist
    echo DELETED!
) else (
    echo Already clean
)

echo.
echo [3/8] DELETING NODE_MODULES CACHE...
if exist node_modules\.cache (
    rmdir /s /q node_modules\.cache
    echo DELETED!
) else (
    echo Already clean
)

echo.
echo [4/8] DELETING WEBPACK CACHE...
if exist node_modules\.cache\webpack (
    rmdir /s /q node_modules\.cache\webpack
    echo DELETED!
) else (
    echo Already clean
)

echo.
echo [5/8] DELETING BABEL CACHE...
if exist node_modules\.cache\babel-loader (
    rmdir /s /q node_modules\.cache\babel-loader
    echo DELETED!
) else (
    echo Already clean
)

echo.
echo [6/8] DELETING VUE CACHE...
if exist node_modules\.cache\vue-loader (
    rmdir /s /q node_modules\.cache\vue-loader
    echo DELETED!
) else (
    echo Already clean
)

echo.
echo [7/8] CLEARING TEMP FILES...
if exist .temp (
    rmdir /s /q .temp
    echo DELETED!
)

echo.
echo [8/8] STARTING FRESH DEV SERVER...
echo.
color 0A
echo ========================================
echo   SERVER STARTING - WAIT FOR SUCCESS
echo ========================================
echo.
echo After you see "Compiled successfully":
echo.
echo 1. Close your browser COMPLETELY
echo 2. Open a NEW browser window
echo 3. Go to: http://localhost:8080
echo 4. Login
echo 5. Go to Upload page
echo 6. Click Archive button
echo.
echo IT WILL WORK! 
echo ========================================
echo.

npm run serve
