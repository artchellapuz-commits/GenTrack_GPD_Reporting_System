@echo off
echo ================================================================
echo   NPC LIVE DATA SETUP
echo ================================================================
echo.

cd backend

echo Step 1: Creating configuration file...
if not exist .env.npc (
    copy .env.npc.example .env.npc
    echo ✓ Created .env.npc
    echo.
    echo IMPORTANT: Edit .env.npc and add your NPC credentials!
    echo.
) else (
    echo ✓ .env.npc already exists
    echo.
)

echo Step 2: Testing connection...
echo.
python manage.py fetch_live_data --test

echo.
echo ================================================================
echo   SETUP COMPLETE
echo ================================================================
echo.
echo Next steps:
echo 1. Edit backend\.env.npc with NPC credentials
echo 2. Run: python manage.py fetch_live_data --test
echo 3. If successful, run: python manage.py fetch_live_data --sync
echo.

pause
