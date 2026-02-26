@echo off
color 0A
echo.
echo ========================================
echo   FIX ARCHIVE BUTTON - CACHE CLEAR
echo ========================================
echo.
echo This will fix the "archiveFile is not a function" error
echo by clearing all cached files and restarting the dev server.
echo.
pause

cd npc-reporting-system\frontend

echo.
echo [Step 1/5] Stopping dev server...
taskkill /F /IM node.exe 2>nul
timeout /t 2 /nobreak >nul
echo Done!

echo.
echo [Step 2/5] Clearing dist folder...
if exist dist (
    rmdir /s /q dist
    echo Cleared dist/
) else (
    echo dist/ already clean
)

echo.
echo [Step 3/5] Clearing node cache...
if exist node_modules\.cache (
    rmdir /s /q node_modules\.cache
    echo Cleared node_modules/.cache/
) else (
    echo Cache already clean
)

echo.
echo [Step 4/5] Clearing webpack cache...
if exist node_modules\.cache\webpack (
    rmdir /s /q node_modules\.cache\webpack
    echo Cleared webpack cache
)

echo.
echo [Step 5/5] Starting fresh dev server...
echo.
echo ========================================
echo  IMPORTANT: After server starts
echo ========================================
echo  1. Go to: http://localhost:8080/upload
echo  2. Press: Ctrl + Shift + R
echo  3. Test the Archive button
echo ========================================
echo.
echo Starting server now...
echo.

npm run serve
