@echo off
echo ========================================
echo Complete Rebuild to Fix PDF Export
echo ========================================
echo.
echo This will:
echo 1. Stop any running servers
echo 2. Clear webpack cache
echo 3. Reinstall packages
echo 4. Restart dev server
echo.
pause

cd frontend

echo.
echo Step 1: Clearing webpack cache...
if exist node_modules\.cache (
    rmdir /s /q node_modules\.cache
    echo Cache cleared!
) else (
    echo No cache to clear.
)

echo.
echo Step 2: Verifying jspdf packages...
call npm list jspdf jspdf-autotable

echo.
echo Step 3: Reinstalling jspdf packages...
call npm uninstall jspdf jspdf-autotable
call npm install jspdf@2.5.1 jspdf-autotable@3.8.2 --save

echo.
echo ========================================
echo Rebuild Complete!
echo ========================================
echo.
echo Now start your dev server:
echo   npm run serve
echo.
echo Then:
echo 1. Open browser in incognito mode
echo 2. Go to Dashboard
echo 3. Try Export PDF
echo.
pause
