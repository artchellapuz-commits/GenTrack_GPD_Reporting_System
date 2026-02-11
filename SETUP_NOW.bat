@echo off
color 0A
echo.
echo ========================================
echo   NPC REPORTING SYSTEM
echo   COMPLETE AUTOMATED SETUP
echo ========================================
echo.
echo This will set up everything automatically!
echo.
echo What will happen:
echo   1. Create Python virtual environment
echo   2. Install all Python packages
echo   3. Setup SQLite database
echo   4. Create admin user
echo   5. Install Node.js packages
echo   6. Add 6 Agus plants with units
echo.
echo Time required: 10-15 minutes
echo.
pause
echo.

:: Run main setup
call AUTOMATED_SETUP.bat

:: Add initial data
echo.
echo ========================================
echo Adding Initial Plant Data...
echo ========================================
echo.
call ADD_INITIAL_DATA.bat

echo.
echo ========================================
echo   SETUP COMPLETE!
echo ========================================
echo.
echo Your system is ready to use!
echo.
echo To start the system:
echo   1. Run: START_BACKEND.bat
echo   2. Run: START_FRONTEND.bat (in new terminal)
echo   3. Open: http://localhost:8080
echo.
echo Admin login: Use credentials you created
echo.
pause
