@echo off
color 0C
title RESTART DEV SERVER

echo.
echo ═══════════════════════════════════════════════════════════
echo   RESTARTING DEV SERVER - THIS WILL FIX THE ERROR
echo ═══════════════════════════════════════════════════════════
echo.
echo Step 1: Killing all Node processes...
echo.

taskkill /F /IM node.exe /T 2>nul
taskkill /F /IM npm.cmd /T 2>nul

timeout /t 3 /nobreak >nul

echo.
echo Step 2: Clearing caches...
echo.

cd npc-reporting-system\frontend

if exist dist rmdir /s /q dist
if exist node_modules\.cache rmdir /s /q node_modules\.cache

echo.
echo Step 3: Starting dev server...
echo.
color 0A
echo ═══════════════════════════════════════════════════════════
echo   WAIT FOR "Compiled successfully" MESSAGE
echo ═══════════════════════════════════════════════════════════
echo.
echo After you see that message:
echo   1. Press Ctrl+Shift+R in your browser
echo   2. Test the Archive button
echo   3. IT WILL WORK!
echo.
echo ═══════════════════════════════════════════════════════════
echo.

npm run serve
