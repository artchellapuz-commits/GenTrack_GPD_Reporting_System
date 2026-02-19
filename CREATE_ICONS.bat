@echo off
echo ========================================
echo  Creating Placeholder PWA Icons
echo ========================================
echo.

python CREATE_PLACEHOLDER_ICONS.py

if errorlevel 1 (
    echo.
    echo ERROR: Failed to create icons
    echo.
    echo Manual method:
    echo 1. Create folder: frontend\public\icons
    echo 2. Go to: https://www.pwabuilder.com/imageGenerator
    echo 3. Upload your logo
    echo 4. Download and extract icons
    echo 5. Copy to frontend\public\icons\
    echo.
) else (
    echo.
    echo ✓ Icons created successfully!
    echo.
    echo Now update manifest.json to use these icons:
    echo Edit: frontend\public\manifest.json
    echo Change .png to .svg in icon paths
    echo.
)

pause
