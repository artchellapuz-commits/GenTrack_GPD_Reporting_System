@echo off
echo Killing all Node processes...
taskkill /F /IM node.exe 2>nul
timeout /t 3 /nobreak >nul

echo Removing node_modules completely...
if exist node_modules (
    rd /s /q node_modules 2>nul
    if exist node_modules (
        echo Retrying with force...
        rmdir /s /q node_modules
    )
)

echo Removing package-lock.json...
if exist package-lock.json del /f package-lock.json

echo Clearing npm cache...
npm cache clean --force

echo Installing with force and legacy peer deps...
npm install --force --legacy-peer-deps

echo.
echo Installation complete! Now starting server...
echo.
npm run serve
