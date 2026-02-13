# 📊 PSR Report Import - Complete Solution

## 🎯 What This Does

This solution allows you to import historical plant generation data from PSR (Plant Status Report) Excel files into your NPC Reporting System.

## ✅ What's Included

### 1. **Historical Data Importer Service**
   - File: `backend/reports/services/historical_data_importer.py`
   - Automatically detects PSR Report format
   - Supports multiple Excel formats
   - Handles date parsing and data validation

### 2. **Import Scripts**
   - `IMPORT_PSR_REPORT.bat` - One-click import for PSR reports
   - `ANALYZE_PSR_REPORT.py` - Analyze Excel file structure before import

### 3. **Documentation**
   - `PSR_REPORT_IMPORT_GUIDE.md` - Complete import guide
   - This README file

## 🚀 Quick Start (3 Steps)

### Step 1: Place Your Excel File
```
npc-reporting-system/
├── REPORTS/
│   └── 8. PSR/
│       └── PSR REPORT-8AM.xlsx  ← Put your file here
```

### Step 2: Analyze the File (Optional but Recommended)
```bash
python ANALYZE_PSR_REPORT.py
```

This will show you:
- File structure
- Detected plant codes
- Date columns
- Sample data values
- Format type

### Step 3: Import the Data
**Option A: Double-click the batch file**
```
IMPORT_PSR_REPORT.bat
```

**Option B: Use command line**
```bash
cd backend
venv\Scripts\activate
python manage.py import_historical_data --historical "..\REPORTS\8. PSR\PSR REPORT-8AM.xlsx"
```

## 📋 Supported File Formats

### Format 1: PSR Report
```
| Plant Code | 2024-01-01 | 2024-01-02 | 2024-01-03 | ...
|------------|------------|------------|------------|----
| AGUS1      | 150.5      | 148.2      | 152.0      | ...
| AGUS2      | 200.3      | 198.5      | 201.2      | ...
```

### Format 2: Daily Data (1DATA APAO style)
```
Month: JANUARY 2024

| Plant Code | 1   | 2   | 3   | 4   | ... | 31  |
|------------|-----|-----|-----|-----|-----|-----|
| AGUS1      | 150 | 148 | 152 | 149 | ... | 151 |
| AGUS2      | 200 | 198 | 201 | 199 | ... | 202 |
```

### Format 3: Plant Capacity (0PLANT DEPCAP)
```
| Plant Code | Plant Name | Dependable (MW) | Installed (MW) |
|------------|------------|-----------------|----------------|
| AGUS1      | Agus 1     | 200.0           | 250.0          |
| AGUS2      | Agus 2     | 180.0           | 220.0          |
```

## 🔧 How It Works

### 1. Format Detection
The importer automatically detects the file format by:
- Looking for "PSR" or "PLANT STATUS REPORT" keywords
- Checking for date columns vs. day number columns
- Identifying plant code patterns

### 2. Data Extraction
- **Plant Codes**: Extracted from the first column
- **Dates**: Parsed from column headers or calculated from day numbers
- **Generation Values**: Numeric values in data cells (in MW)

### 3. Database Storage
```python
# Creates or updates records
HistoricalData.objects.update_or_create(
    plant=plant,
    date=report_date,
    defaults={
        'actual_generation': generation_value,
        'remarks': 'Imported from PSR Report'
    }
)
```

## 📊 Example Usage

### Import PSR Report
```bash
python manage.py import_historical_data --historical "REPORTS\8. PSR\PSR REPORT-8AM.xlsx"
```

**Output:**
```
Starting import...
Importing historical data from: REPORTS\8. PSR\PSR REPORT-8AM.xlsx
✓ Imported 1,250 historical records

✓ Import complete! Total records imported: 1,250
```

### Import Plant Capacity
```bash
python manage.py import_historical_data --capacity "REPORTS\8. PSR\0PLANT DEPCAP.xlsx"
```

### Import Both
```bash
python manage.py import_historical_data \
    --capacity "REPORTS\8. PSR\0PLANT DEPCAP.xlsx" \
    --historical "REPORTS\8. PSR\PSR REPORT-8AM.xlsx"
```

## 🔍 Verify Import

### Check Record Count
```bash
python manage.py shell
```

```python
from reports.models import HistoricalData, PlantCapacity, Plant

# Check counts
print(f"Plants: {Plant.objects.count()}")
print(f"Historical records: {HistoricalData.objects.count()}")
print(f"Capacity records: {PlantCapacity.objects.count()}")

# Check date range
from django.db.models import Min, Max
date_range = HistoricalData.objects.aggregate(
    min_date=Min('date'),
    max_date=Max('date')
)
print(f"Data from {date_range['min_date']} to {date_range['max_date']}")

# Check specific plant
agus1_data = HistoricalData.objects.filter(plant__code='AGUS1').count()
print(f"AGUS1 has {agus1_data} historical records")
```

### View Sample Data
```python
# Get recent data
recent = HistoricalData.objects.order_by('-date')[:10]
for record in recent:
    print(f"{record.date} - {record.plant.code}: {record.actual_generation} MW")
```

## ⚠️ Troubleshooting

### Problem: "Could not find header row"
**Cause**: The Excel file doesn't have recognizable headers

**Solution**:
1. Run `ANALYZE_PSR_REPORT.py` to see the file structure
2. Ensure the file has a row with plant codes or dates
3. Check if the file is corrupted

### Problem: "Unknown file format"
**Cause**: The file doesn't match PSR or Daily format

**Solution**:
1. Check the file structure matches one of the supported formats
2. Ensure date columns or day numbers are present
3. Verify plant codes are in the first column

### Problem: Import shows warnings
**Cause**: Some cells have invalid data

**Solution**:
- Warnings are non-critical - the import continues
- Review the warnings to identify problematic cells
- Check the Excel file for merged cells, formulas, or text in numeric columns

### Problem: No data imported
**Cause**: Various reasons

**Solution**:
1. Check if plants exist in the database
2. Verify the date format is recognized
3. Ensure numeric values are in the data cells
4. Run `ANALYZE_PSR_REPORT.py` to diagnose

## 🎓 Advanced Features

### Re-import (Update Existing Data)
The importer uses `update_or_create`, so you can safely re-import:
```bash
python manage.py import_historical_data --historical "PSR REPORT-8AM.xlsx"
```

Existing records will be updated, new records will be created.

### Import Multiple Files
```bash
# Windows
for %f in (REPORTS\8. PSR\*.xlsx) do python manage.py import_historical_data --historical "%f"

# Linux/Mac
for file in REPORTS/8.\ PSR/*.xlsx; do
    python manage.py import_historical_data --historical "$file"
done
```

### Custom Date Range
Modify the importer to filter by date:
```python
# In historical_data_importer.py
if report_date < date(2024, 1, 1):
    continue  # Skip dates before 2024
```

### Export After Import
```python
from reports.models import HistoricalData
import csv

# Export to CSV
with open('exported_data.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Date', 'Plant Code', 'Generation (MW)'])
    
    for record in HistoricalData.objects.all():
        writer.writerow([
            record.date,
            record.plant.code,
            record.actual_generation
        ])
```

## 📈 Data Quality Checks

### Check for Gaps
```python
from reports.models import HistoricalData
from datetime import timedelta

# Find date gaps for a plant
plant_code = 'AGUS1'
records = HistoricalData.objects.filter(
    plant__code=plant_code
).order_by('date')

prev_date = None
for record in records:
    if prev_date:
        gap = (record.date - prev_date).days
        if gap > 1:
            print(f"Gap of {gap} days between {prev_date} and {record.date}")
    prev_date = record.date
```

### Check for Outliers
```python
from reports.models import HistoricalData
from django.db.models import Avg, StdDev

# Find outliers (values > 3 standard deviations from mean)
plant_code = 'AGUS1'
stats = HistoricalData.objects.filter(
    plant__code=plant_code
).aggregate(
    avg=Avg('actual_generation'),
    stddev=StdDev('actual_generation')
)

threshold = stats['avg'] + (3 * stats['stddev'])
outliers = HistoricalData.objects.filter(
    plant__code=plant_code,
    actual_generation__gt=threshold
)

for record in outliers:
    print(f"{record.date}: {record.actual_generation} MW (avg: {stats['avg']:.2f})")
```

## 🔐 Best Practices

1. **Backup First**: Always backup your database before importing
   ```bash
   python manage.py dumpdata > backup.json
   ```

2. **Test with Small File**: Test the import with a small sample first

3. **Review Warnings**: Always check warnings for data quality issues

4. **Verify Results**: Query the database after import to verify

5. **Document Sources**: Keep track of which files you've imported

## 📞 Support

If you need help:
1. Run `ANALYZE_PSR_REPORT.py` to diagnose file issues
2. Check the error messages carefully
3. Review the `PSR_REPORT_IMPORT_GUIDE.md` for detailed instructions
4. Check Django logs for detailed error information

## 📝 Summary

You now have a complete solution for importing PSR Report data:

✅ Automatic format detection  
✅ Support for multiple Excel formats  
✅ Data validation and error handling  
✅ Easy-to-use batch scripts  
✅ Comprehensive documentation  
✅ Analysis tools for troubleshooting  

**Next Steps:**
1. Place your PSR REPORT-8AM.xlsx in `REPORTS/8. PSR/`
2. Run `ANALYZE_PSR_REPORT.py` to preview
3. Run `IMPORT_PSR_REPORT.bat` to import
4. Verify the data in your dashboard

Happy importing! 🚀
