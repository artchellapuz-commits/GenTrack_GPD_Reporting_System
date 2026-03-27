@echo off
echo ========================================
echo  NPC Frontend Fix and Run Script
echo ========================================
echo.

echo Step 1: Stopping any running Node processes...
taskkill /F /IM node.exe 2>nul
timeout /t 2 /nobreak >nul

echo Step 2: Removing corrupted node_modules...
if exist node_modules (
    echo This may take a moment...
    rmdir /s /q node_modules
)
if exist package-lock.json del package-lock.json

echo Step 3: Clearing npm cache...
call npm cache clean --force

echo Step 4: Installing dependencies (this will take a few minutes)...
call npm install

echo.
echo Step 5: Starting development server...
echo.
echo ========================================
echo  Server will start at http://localhost:8080
echo  Press Ctrl+C to stop the server
echo ========================================
echo.

call npm run serve
