@echo off
echo ========================================
echo  CLEAN RESTART FRONTEND DEV SERVER
echo ========================================
echo.
echo This will:
echo 1. Stop any running dev server
echo 2. Clear webpack cache
echo 3. Clear node_modules cache
echo 4. Restart dev server fresh
echo.
pause

cd frontend

echo.
echo [1/4] Stopping any running processes...
taskkill /F /IM node.exe 2>nul
timeout /t 2 >nul

echo.
echo [2/4] Clearing webpack cache...
if exist node_modules\.cache (
    rmdir /s /q node_modules\.cache
    echo Cache cleared!
) else (
    echo No cache found.
)

echo.
echo [3/4] Clearing dist folder...
if exist dist (
    rmdir /s /q dist
    echo Dist cleared!
) else (
    echo No dist found.
)

echo.
echo [4/4] Starting dev server...
echo.
echo ========================================
echo  DEV SERVER STARTING
echo ========================================
echo.
echo Wait for "Compiled successfully" message
echo Then open: http://localhost:8080/upload
echo.
echo Press Ctrl+Shift+R in browser to hard refresh!
echo.

npm run serve

pause
