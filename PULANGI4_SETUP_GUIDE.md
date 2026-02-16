# Pulangi 4 Hydro-electric Power Plant Setup Guide

## Overview
This guide explains how to add Pulangi 4 Hydro-electric Power Plant to the NPC Reporting System.

## Plant Information
- **Plant Name**: Pulangi 4 Hydroelectric Plant
- **Plant Code**: PULANGI4
- **Location**: Bukidnon
- **Total Capacity**: 255 MW
- **Number of Units**: 3
- **Unit Capacity**: 85 MW each

## Installation Steps

### Method 1: Using the Batch File (Easiest)
1. Double-click `ADD_PULANGI4.bat`
2. Wait for the script to complete
3. Press any key to close

### Method 2: Manual Installation
1. Open Command Prompt
2. Navigate to the backend folder:
   ```
   cd backend
   ```
3. Activate virtual environment:
   ```
   venv\Scripts\activate
   ```
4. Run the migration:
   ```
   python manage.py migrate
   ```
5. Add the plant:
   ```
   python add_pulangi4.py
   ```

## Verification

After installation, verify that Pulangi 4 was added successfully:

1. Start the backend server:
   ```
   cd backend
   venv\Scripts\activate
   python manage.py runserver
   ```

2. Open Django Admin:
   - Go to http://localhost:8000/admin
   - Login with your admin credentials
   - Navigate to "Plants"
   - You should see "Pulangi 4 Hydroelectric Plant" in the list

3. Check the frontend:
   - Start the frontend server
   - Go to http://localhost:8080
   - Login to the dashboard
   - Pulangi 4 should appear in the plant list

## Using Pulangi 4

### Upload Daily Generation Data
1. Go to "Upload Excel" page
2. Select "Pulangi 4" from the plant dropdown
3. Upload the Excel file with daily generation data
4. The system will process data for all 3 units

### View Reports
1. Go to "View Reports" page
2. Select "Pulangi 4" to filter reports
3. View generation data, capacity factor, and availability

### Generate Reports
1. Go to "Generate Report" page
2. Select date range
3. Include "Pulangi 4" in the report
4. Download the consolidated report

## Excel File Format for Pulangi 4

The Excel file should follow the same format as other plants:

| Date       | Unit 1 Gen (kWh) | Unit 1 Hours | Unit 2 Gen (kWh) | Unit 2 Hours | Unit 3 Gen (kWh) | Unit 3 Hours |
|------------|------------------|--------------|------------------|--------------|------------------|--------------|
| 2026-02-13 | 1,800,000        | 22.5         | 1,850,000        | 23.0         | 1,900,000        | 24.0         |

## Troubleshooting

### Plant Not Showing in Dropdown
- Make sure you ran the migration: `python manage.py migrate`
- Restart the backend server
- Clear browser cache

### Units Not Created
- Run the add_pulangi4.py script again
- Check the console output for errors

### Data Upload Fails
- Verify the Excel file format matches the template
- Check that all 3 units are included in the file
- Ensure date format is correct (YYYY-MM-DD)

## Technical Details

### Database Changes
- Added 'PULANGI4' to Plant.PLANT_CHOICES
- Created migration file: 0004_add_pulangi4_plant.py
- Plant record with 3 units will be created

### API Endpoints
All existing API endpoints now support Pulangi 4:
- GET /api/plants/ - Lists all plants including Pulangi 4
- POST /api/upload/ - Upload data for Pulangi 4
- GET /api/reports/ - Filter reports by Pulangi 4
- GET /api/export/ - Include Pulangi 4 in exports

## Support

If you encounter any issues:
1. Check the console output for error messages
2. Verify database connection
3. Ensure all migrations are applied
4. Contact system administrator

---

**Note**: After adding Pulangi 4, you can start uploading daily generation data immediately. The system will automatically calculate capacity factors and availability metrics for all 3 units.
