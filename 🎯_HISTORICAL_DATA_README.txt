========================================
📊 HISTORICAL DATA IMPORT - README
========================================

WHAT IS THIS?
-------------
This feature allows you to import historical plant data from Excel files into the NPC Reporting System.

Two types of data can be imported:
  1. Plant Capacity Data (installed/dependable capacity)
  2. Historical Operational Data (generation, availability, status)

QUICK START (3 STEPS)
----------------------

STEP 1: Setup Database
  Run: SETUP_HISTORICAL_DATA.bat
  
  This creates the necessary database tables.

STEP 2: Prepare Excel Files
  Place these files in the 'backend' folder:
    • 0PLANT DEPCAP.xlsx (Plant capacity data)
    • 1DATA APAO.xlsx (Historical operational data)
  
  Don't have data yet? Generate sample files:
    python CREATE_SAMPLE_HISTORICAL_DATA.py

STEP 3: Import Data
  Run: IMPORT_HISTORICAL_DATA.bat
  
  This imports the data and shows you the results.

THAT'S IT! ✅

VERIFY IMPORT
-------------
After import, check these URLs in your browser:
  • http://localhost:8000/api/historical-data/
  • http://localhost:8000/api/plant-capacity/

You should see your imported data in JSON format.

EXCEL FILE FORMAT
-----------------

Plant Capacity File (0PLANT DEPCAP.xlsx):
  Required Columns:
    - Plant Name
    - Installed Capacity (MW)
    - Dependable Capacity (MW)
  
  Optional Columns:
    - Type
    - Location

Historical Data File (1DATA APAO.xlsx):
  Required Columns:
    - Date (or DATE)
    - Plant Name (or PLANT)
    - Generation (MWh)
    - Availability (%)
  
  Optional Columns:
    - Status
    - Remarks
  
  Note: Can have multiple sheets for different time periods

IMPORT METHODS
--------------

Method 1: Batch Script (Easiest)
  IMPORT_HISTORICAL_DATA.bat

Method 2: Command Line
  cd backend
  venv\Scripts\activate
  python manage.py import_historical_data --capacity "0PLANT DEPCAP.xlsx" --historical "1DATA APAO.xlsx"

Method 3: API (for developers)
  POST http://localhost:8000/api/historical-data/import/
  (Send files as multipart/form-data)

TROUBLESHOOTING
---------------

Problem: "Plant not found" warnings
Solution: Ensure plant names in Excel match existing plants
          Check spelling and capitalization

Problem: Import fails with error
Solution: 1. Check file format is .xlsx
          2. Verify column names match expected format
          3. Run: python manage.py migrate
          4. Check Django logs for details

Problem: "Django not found" error
Solution: Activate virtual environment first:
          cd backend
          venv\Scripts\activate

Problem: Database errors
Solution: Run migrations:
          cd backend
          venv\Scripts\activate
          python manage.py migrate

FEATURES
--------
✅ Import plant capacity data
✅ Import historical operational data
✅ Multi-sheet Excel support
✅ Automatic plant name matching
✅ Multiple date format support
✅ Duplicate prevention (updates existing records)
✅ Error and warning tracking
✅ Progress reporting
✅ API access to imported data

API ENDPOINTS
-------------
GET  /api/historical-data/          List historical data
POST /api/historical-data/import/   Import from Excel
GET  /api/plant-capacity/           List capacity records

Query Parameters:
  ?plant_code=AGUS1              Filter by plant
  ?start_date=2024-01-01         Filter by start date
  ?end_date=2024-12-31           Filter by end date

DOCUMENTATION
-------------
📖 Detailed Guide:    HISTORICAL_DATA_IMPORT_GUIDE.md
📋 Quick Reference:   QUICK_IMPORT_GUIDE.txt
🔌 API Docs:          API_DOCUMENTATION.md
📊 Solution Summary:  📊_HISTORICAL_DATA_SOLUTION.md

FILES INCLUDED
--------------
Backend:
  • historical_data_importer.py      Import service
  • import_historical_data.py        Management command
  • 0002_plantcapacity_historicaldata.py  Database migration

Scripts:
  • SETUP_HISTORICAL_DATA.bat        Setup database
  • IMPORT_HISTORICAL_DATA.bat       Import data
  • CREATE_SAMPLE_HISTORICAL_DATA.py Generate test files

Documentation:
  • HISTORICAL_DATA_IMPORT_GUIDE.md  Complete guide
  • QUICK_IMPORT_GUIDE.txt           Quick reference
  • 📊_HISTORICAL_DATA_SOLUTION.md   Technical summary
  • 🎯_HISTORICAL_DATA_README.txt    This file

EXAMPLE WORKFLOW
----------------
1. Run SETUP_HISTORICAL_DATA.bat
2. Run CREATE_SAMPLE_HISTORICAL_DATA.py
3. Move generated files to backend folder
4. Run IMPORT_HISTORICAL_DATA.bat
5. Open http://localhost:8000/api/historical-data/
6. See your imported data!

TIPS
----
💡 Always backup your database before importing large datasets
💡 Test with small sample files first
💡 Review import results for errors and warnings
💡 Use API filters when querying large datasets
💡 Check the documentation for advanced usage

SUPPORT
-------
For issues or questions:
  1. Check the error messages in the import output
  2. Review the documentation files
  3. Check Django logs in backend/logs/
  4. Verify your Excel file format

========================================
Status: ✅ Ready to Use
Last Updated: February 12, 2026
========================================
