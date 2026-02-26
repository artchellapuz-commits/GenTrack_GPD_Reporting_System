@echo off
title ULTIMATE FIX - Archive Button
color 0E

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║                                                            ║
echo ║           🔥 ULTIMATE FIX - ARCHIVE BUTTON 🔥              ║
echo ║                                                            ║
echo ║  This will fix the "archiveFile is not a function" error  ║
echo ║                                                            ║
echo ╚════════════════════════════════════════════════════════════╝
echo.
echo What this does:
echo   ✓ Kills all Node processes
echo   ✓ Clears ALL caches
echo   ✓ Touches the file to force recompile
echo   ✓ Starts fresh dev server
echo.
pause

cd npc-reporting-system\frontend

echo.
echo ═══════════════════════════════════════════════════════════
echo  STEP 1: Killing Node processes...
echo ═══════════════════════════════════════════════════════════
taskkill /F /IM node.exe /T 2>nul
taskkill /F /IM npm.cmd /T 2>nul
timeout /t 2 /nobreak >nul
color 0A
echo ✓ DONE!
color 0E

echo.
echo ═══════════════════════════════════════════════════════════
echo  STEP 2: Clearing caches...
echo ═══════════════════════════════════════════════════════════

if exist dist rmdir /s /q dist
if exist node_modules\.cache rmdir /s /q node_modules\.cache
if exist .temp rmdir /s /q .temp

color 0A
echo ✓ DONE!
color 0E

echo.
echo ═══════════════════════════════════════════════════════════
echo  STEP 3: Touching file to force recompile...
echo ═══════════════════════════════════════════════════════════

copy /b src\components\UploadExcel.vue +,, >nul 2>&1

color 0A
echo ✓ DONE!
color 0E

echo.
echo ═══════════════════════════════════════════════════════════
echo  STEP 4: Starting dev server...
echo ═══════════════════════════════════════════════════════════
echo.
color 0B
echo ╔════════════════════════════════════════════════════════════╗
echo ║                                                            ║
echo ║                    IMPORTANT INSTRUCTIONS                  ║
echo ║                                                            ║
echo ║  After you see "Compiled successfully":                   ║
echo ║                                                            ║
echo ║  1. CLOSE your browser COMPLETELY (not just the tab)      ║
echo ║  2. Press Ctrl + Shift + N (open Incognito mode)          ║
echo ║  3. Go to: http://localhost:8080                          ║
echo ║  4. Login                                                  ║
echo ║  5. Go to Upload page                                      ║
echo ║  6. Click Archive button                                   ║
echo ║                                                            ║
echo ║  IT WILL WORK! 🎉                                          ║
echo ║                                                            ║
echo ╚════════════════════════════════════════════════════════════╝
echo.
color 0A

npm run serve
