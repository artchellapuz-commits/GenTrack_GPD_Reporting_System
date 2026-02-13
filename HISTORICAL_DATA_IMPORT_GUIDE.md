# Historical Data Import Guide

This guide explains how to import historical data into the NPC Reporting System.

## Overview

The system supports importing two types of historical data:

1. **Plant Capacity Data** (`0PLANT DEPCAP.xlsx`)
   - Installed capacity (MW)
   - Dependable capacity (MW)
   - Plant type and location

2. **Historical Operational Data** (`1DATA APAO.xlsx`)
   - Daily generation (MWh)
   - Availability percentages
   - Plant status and remarks
   - Multi-sheet support for different time periods

## Import Methods

### Method 1: Using the Batch Script (Easiest)

1. Place your Excel files in the `backend` folder:
   - `0PLANT DEPCAP.xlsx`
   - `1DATA APAO.xlsx`

2. Run the import script:
   ```
   IMPORT_HISTORICAL_DATA.bat
   ```

3. The script will:
   - Activate the virtual environment
   - Run database migrations
   - Import the data
   - Show import results

### Method 2: Using Django Management Command

```bash
cd backend
venv\Scripts\activate
python manage.py migrate
python manage.py import_historical_data --capacity "path/to/0PLANT DEPCAP.xlsx" --historical "path/to/1DATA APAO.xlsx"
```

You can import files separately:
```bash
# Import only capacity data
python manage.py import_historical_data --capacity "0PLANT DEPCAP.xlsx"

# Import only historical data
python manage.py import_historical_data --historical "1DATA APAO.xlsx"
```

### Method 3: Using the API

Send a POST request to `/api/historical-data/import/`:

```bash
curl -X POST http://localhost:8000/api/historical-data/import/ \
  -F "capacity_file=@0PLANT DEPCAP.xlsx" \
  -F "historical_file=@1DATA APAO.xlsx"
```

Or using Python:
```python
import requests

url = 'http://localhost:8000/api/historical-data/import/'
files = {
    'capacity_file': open('0PLANT DEPCAP.xlsx', 'rb'),
    'historical_file': open('1DATA APAO.xlsx', 'rb')
}
response = requests.post(url, files=files)
print(response.json())
```

## Excel File Format

### Plant Capacity File (0PLANT DEPCAP.xlsx)

Expected columns:
- `Plant Name` - Name of the plant (e.g., "Agus 1")
- `Installed Capacity (MW)` - Total installed capacity
- `Dependable Capacity (MW)` - Dependable capacity
- `Type` - Plant type (Hydro/Thermal/etc.)
- `Location` - Plant location (optional)

Example:
| Plant Name | Installed Capacity (MW) | Dependable Capacity (MW) | Type  | Location |
|------------|------------------------|-------------------------|-------|----------|
| Agus 1     | 100.00                 | 95.00                   | Hydro | Lanao    |
| Agus 2     | 180.00                 | 170.00                  | Hydro | Lanao    |

### Historical Data File (1DATA APAO.xlsx)

Expected columns:
- `Date` or `DATE` - Report date
- `Plant Name` or `PLANT` - Plant name
- `Generation (MWh)` - Generation in MWh
- `Availability (%)` - Availability percentage
- `Status` - Operating status (optional)
- `Remarks` - Additional remarks (optional)

The file can have multiple sheets, each representing different time periods.

Example:
| Date       | Plant Name | Generation (MWh) | Availability (%) | Status    | Remarks |
|------------|------------|------------------|------------------|-----------|---------|
| 2024-01-01 | Agus 1     | 2400.00          | 98.5             | Operating |         |
| 2024-01-02 | Agus 1     | 2350.00          | 97.0             | Operating |         |

## Data Validation

The importer performs the following validations:

1. **File Format**: Only `.xlsx` files are accepted
2. **File Size**: Maximum 50MB per file
3. **Plant Matching**: Plants are matched by name (case-insensitive, partial match)
4. **Date Parsing**: Dates are automatically parsed from various formats
5. **Duplicate Prevention**: Records with the same plant and date are updated, not duplicated

## Viewing Imported Data

### Using the API

1. **List Historical Data**:
   ```
   GET http://localhost:8000/api/historical-data/
   ```

2. **Filter by Plant**:
   ```
   GET http://localhost:8000/api/historical-data/?plant_code=AGUS1
   ```

3. **Filter by Date Range**:
   ```
   GET http://localhost:8000/api/historical-data/?start_date=2024-01-01&end_date=2024-12-31
   ```

4. **View Plant Capacity**:
   ```
   GET http://localhost:8000/api/plant-capacity/
   ```

### Using Python

```python
import requests

# Get historical data for Agus 1
response = requests.get('http://localhost:8000/api/historical-data/', params={
    'plant_code': 'AGUS1',
    'start_date': '2024-01-01',
    'end_date': '2024-12-31'
})
data = response.json()

for record in data['results']:
    print(f"{record['date']}: {record['generation_mwh']} MWh")
```

## Troubleshooting

### Common Issues

1. **"Plant not found" warnings**
   - The plant name in the Excel file doesn't match any existing plant
   - Solution: Ensure plants are created first, or check plant name spelling

2. **"Date parsing error"**
   - The date format is not recognized
   - Solution: Use standard date formats (YYYY-MM-DD, MM/DD/YYYY, etc.)

3. **"Duplicate key error"**
   - Trying to import data that already exists
   - Solution: The system will update existing records automatically

4. **Import fails with no error message**
   - Check the Django logs for detailed error information
   - Ensure the database is accessible and migrations are up to date

### Checking Import Results

After import, check the results:

```bash
cd backend
python manage.py shell
```

```python
from reports.models import HistoricalData, PlantCapacity

# Count imported records
print(f"Historical records: {HistoricalData.objects.count()}")
print(f"Capacity records: {PlantCapacity.objects.count()}")

# View recent imports
for record in HistoricalData.objects.order_by('-created_at')[:5]:
    print(f"{record.plant.code} - {record.date}: {record.generation_mwh} MWh")
```

## Best Practices

1. **Backup First**: Always backup your database before importing large datasets
2. **Test with Small Files**: Test the import with a small sample file first
3. **Check Data Quality**: Review the Excel files for data quality issues before import
4. **Monitor Progress**: Watch the import progress for errors and warnings
5. **Verify Results**: After import, verify a sample of records to ensure accuracy

## API Response Format

### Success Response

```json
{
  "success": true,
  "total_imported": 150,
  "errors": [],
  "warnings": ["Plant not found: Agus 3"],
  "details": {
    "capacity": {
      "success": true,
      "imported": 6,
      "errors": [],
      "warnings": []
    },
    "historical": {
      "success": true,
      "imported": 144,
      "errors": [],
      "warnings": ["Plant not found: Agus 3"]
    }
  }
}
```

### Error Response

```json
{
  "success": false,
  "error": "Failed to read Excel file: Invalid file format",
  "imported": 0
}
```

## Database Schema

### PlantCapacity Table

| Field               | Type          | Description                    |
|---------------------|---------------|--------------------------------|
| id                  | BigInteger    | Primary key                    |
| plant_id            | ForeignKey    | Reference to Plant             |
| installed_capacity  | Decimal(10,2) | Installed capacity in MW       |
| dependable_capacity | Decimal(10,2) | Dependable capacity in MW      |
| effective_date      | Date          | Date when capacity is effective|
| remarks             | Text          | Additional notes               |
| created_at          | DateTime      | Record creation timestamp      |
| updated_at          | DateTime      | Last update timestamp          |

### HistoricalData Table

| Field                | Type          | Description                    |
|----------------------|---------------|--------------------------------|
| id                   | BigInteger    | Primary key                    |
| plant_id             | ForeignKey    | Reference to Plant             |
| date                 | Date          | Report date                    |
| generation_mwh       | Decimal(15,2) | Generation in MWh              |
| availability_percent | Decimal(5,2)  | Availability percentage        |
| status               | String(50)    | Operating status               |
| remarks              | Text          | Additional notes               |
| sheet_name           | String(100)   | Source Excel sheet name        |
| created_at           | DateTime      | Record creation timestamp      |
| updated_at           | DateTime      | Last update timestamp          |

## Support

For issues or questions:
1. Check the error messages in the import output
2. Review the Django logs in `backend/logs/`
3. Verify your Excel file format matches the expected structure
4. Contact the system administrator for database-related issues
