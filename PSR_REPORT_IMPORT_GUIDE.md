# PSR Report Import Guide

## Overview
This guide explains how to import historical data from PSR (Plant Status Report) Excel files into the NPC Reporting System.

## Supported File Formats

### 1. PSR Report Format
- **File Example**: `PSR REPORT-8AM.xlsx`
- **Structure**:
  - Plant codes in the first column
  - Date columns across the top
  - Generation values in the data cells
  - Multiple sheets supported

### 2. Daily Data Format
- **File Example**: `1DATA APAO.xlsx`
- **Structure**:
  - Plant codes in the first column
  - Day numbers (1-31) as column headers
  - Month/Year in the header section
  - Generation values in the data cells

### 3. Plant Capacity Format
- **File Example**: `0PLANT DEPCAP.xlsx`
- **Structure**:
  - Plant Code column
  - Plant Name column
  - Dependable Capacity (MW) column
  - Installed Capacity (MW) column

## Quick Import Methods

### Method 1: Using the Batch File (Easiest)
```batch
# Double-click this file:
IMPORT_PSR_REPORT.bat
```

### Method 2: Using Django Management Command
```bash
# Activate virtual environment
cd backend
venv\Scripts\activate

# Import PSR report
python manage.py import_historical_data --historical "path\to\PSR REPORT-8AM.xlsx"

# Import plant capacity
python manage.py import_historical_data --capacity "path\to\0PLANT DEPCAP.xlsx"

# Import both
python manage.py import_historical_data --capacity "path\to\0PLANT DEPCAP.xlsx" --historical "path\to\1DATA APAO.xlsx"
```

### Method 3: Using Python Script
```python
from reports.services.historical_data_importer import HistoricalDataImporter

importer = HistoricalDataImporter()

# Import PSR report
result = importer.import_historical_data('path/to/PSR REPORT-8AM.xlsx')
print(f"Imported {result['imported']} records")

# Import capacity data
result = importer.import_plant_capacity('path/to/0PLANT DEPCAP.xlsx')
print(f"Imported {result['imported']} capacity records")
```

## File Location
Place your Excel files in the `REPORTS/8. PSR/` directory:
```
npc-reporting-system/
├── REPORTS/
│   └── 8. PSR/
│       ├── PSR REPORT-8AM.xlsx
│       ├── 0PLANT DEPCAP.xlsx
│       └── 1DATA APAO.xlsx
```

## Import Process

### Step 1: Prepare Your Files
1. Ensure Excel files are in the correct format
2. Close the Excel files (they must not be open)
3. Place files in the `REPORTS/8. PSR/` directory

### Step 2: Run the Import
Choose one of the methods above to import your data.

### Step 3: Verify the Import
The import process will show:
- ✓ Number of records imported
- ⚠ Any warnings (non-critical issues)
- ✗ Any errors (critical issues)

### Step 4: Check the Database
After import, you can verify the data:
```bash
python manage.py shell

from reports.models import HistoricalData, PlantCapacity
print(f"Historical records: {HistoricalData.objects.count()}")
print(f"Plant capacity records: {PlantCapacity.objects.count()}")
```

## Data Mapping

### PSR Report → Database
| Excel Column | Database Field | Notes |
|--------------|----------------|-------|
| Plant Code | Plant.code | Auto-creates plant if not exists |
| Date Columns | HistoricalData.date | Parsed from column headers |
| Generation Values | HistoricalData.actual_generation | In MW |

### Plant Capacity → Database
| Excel Column | Database Field | Notes |
|--------------|----------------|-------|
| Plant Code | Plant.code | Auto-creates plant if not exists |
| Plant Name | Plant.name | Updates existing plant name |
| Dependable Capacity | PlantCapacity.dependable_capacity | In MW |
| Installed Capacity | PlantCapacity.installed_capacity | In MW |

## Troubleshooting

### Error: "Could not find header row"
**Solution**: The importer looks for rows containing "PLANT" or date information. Ensure your Excel file has proper headers.

### Error: "Unknown file format"
**Solution**: The file doesn't match PSR or Daily format. Check the file structure matches one of the supported formats.

### Warning: "Row X, Col Y: Invalid value"
**Solution**: Some cells contain invalid data. The import continues but skips those cells. Review the warnings to identify problematic data.

### Error: "File not found"
**Solution**: Check the file path is correct and the file exists.

## Advanced Usage

### Import Multiple Files
```bash
# Import all files in a directory
for file in REPORTS/8. PSR/*.xlsx; do
    python manage.py import_historical_data --historical "$file"
done
```

### Re-import Data (Update Existing)
The importer uses `update_or_create`, so re-importing will update existing records:
```bash
python manage.py import_historical_data --historical "path\to\PSR REPORT-8AM.xlsx"
```

### Clear Existing Data Before Import
```bash
python manage.py shell

from reports.models import HistoricalData, PlantCapacity

# Clear historical data
HistoricalData.objects.all().delete()

# Clear capacity data
PlantCapacity.objects.all().delete()
```

## Data Validation

After import, validate your data:

### Check Date Range
```python
from reports.models import HistoricalData
from django.db.models import Min, Max

date_range = HistoricalData.objects.aggregate(
    min_date=Min('date'),
    max_date=Max('date')
)
print(f"Data from {date_range['min_date']} to {date_range['max_date']}")
```

### Check Plant Coverage
```python
from reports.models import Plant, HistoricalData

plants_with_data = HistoricalData.objects.values('plant__code').distinct().count()
total_plants = Plant.objects.count()
print(f"{plants_with_data} out of {total_plants} plants have historical data")
```

### Check Data Completeness
```python
from reports.models import HistoricalData
from django.db.models import Count

# Plants with most data
top_plants = HistoricalData.objects.values('plant__code').annotate(
    count=Count('id')
).order_by('-count')[:10]

for plant in top_plants:
    print(f"{plant['plant__code']}: {plant['count']} records")
```

## Best Practices

1. **Backup First**: Always backup your database before importing large datasets
2. **Test Import**: Test with a small file first to verify the format
3. **Review Warnings**: Check warnings for data quality issues
4. **Verify Results**: Always verify the import results in the database
5. **Document Sources**: Keep track of which files you've imported and when

## Support

If you encounter issues:
1. Check the error messages carefully
2. Verify your Excel file format matches the expected structure
3. Review the troubleshooting section above
4. Check the Django logs for detailed error information

## Example Output

Successful import:
```
Starting import...
Importing historical data from: REPORTS/8. PSR/PSR REPORT-8AM.xlsx
✓ Imported 1,250 historical records

✓ Import complete! Total records imported: 1,250
```

Import with warnings:
```
Starting import...
Importing historical data from: REPORTS/8. PSR/PSR REPORT-8AM.xlsx
⚠ Warnings:
  - Row 15, Col 5: Invalid value
  - Row 23, Col 8: Could not parse date
✓ Imported 1,248 historical records

✓ Import complete! Total records imported: 1,248
```
