@echo off
echo Cleaning node_modules...
rmdir /s /q node_modules 2>nul
del package-lock.json 2>nul
echo.
echo Installing fresh dependencies...
call npm install --legacy-peer-deps
echo.
echo Done! Press any key to exit...
pause >nul
