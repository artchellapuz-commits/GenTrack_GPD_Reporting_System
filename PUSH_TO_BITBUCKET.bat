@echo off
echo ========================================
echo  NPC Reporting System - Push to Bitbucket
echo ========================================
echo.

REM Check if git is installed
where git >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Git is not installed!
    echo.
    echo Please install Git first:
    echo 1. Go to: https://git-scm.com/download/win
    echo 2. Download and install Git for Windows
    echo 3. Run this script again
    echo.
    pause
    exit /b 1
)

echo Git is installed. Version:
git --version
echo.

REM Check if git is initialized
if not exist ".git" (
    echo Initializing Git repository...
    git init
    echo.
)

REM Check if remote exists
git remote get-url origin >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo Adding Bitbucket remote...
    git remote add origin https://artchelintern-admin@bitbucket.org/ojtinternprogram/npc.git
    echo.
)

echo Current status:
git status
echo.

echo ========================================
echo  Ready to commit and push!
echo ========================================
echo.

set /p commit_msg="Enter commit message (or press Enter for default): "
if "%commit_msg%"=="" set commit_msg=Update NPC Reporting System

echo.
echo Adding all files...
git add .

echo.
echo Committing with message: "%commit_msg%"
git commit -m "%commit_msg%"

echo.
echo Pushing to Bitbucket...
git branch -M main
git push -u origin main

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================
    echo  SUCCESS! Code pushed to Bitbucket
    echo ========================================
    echo.
    echo Repository: https://bitbucket.org/ojtinternprogram/npc
    echo.
) else (
    echo.
    echo ========================================
    echo  PUSH FAILED!
    echo ========================================
    echo.
    echo Possible reasons:
    echo 1. Authentication failed - check username/password
    echo 2. No write access to repository
    echo 3. Network connection issue
    echo.
    echo If you have 2FA enabled, use an App Password:
    echo https://bitbucket.org/account/settings/app-passwords/
    echo.
)

pause
