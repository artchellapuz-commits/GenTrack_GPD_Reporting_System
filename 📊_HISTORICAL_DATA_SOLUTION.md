# 📊 Historical Data Import Solution

## Overview

Complete implementation for importing historical data into the NPC Reporting System from Excel files.

## ✅ What's Been Implemented

### 1. Database Models
- **PlantCapacity**: Stores historical capacity data (installed/dependable capacity)
- **HistoricalData**: Stores historical operational data (generation, availability, status)

### 2. Import Service
- **File**: `backend/reports/services/historical_data_importer.py`
- **Features**:
  - Import plant capacity from Excel
  - Import historical operational data from Excel
  - Multi-sheet support for historical data
  - Automatic plant matching (fuzzy matching by name)
  - Date parsing from various formats
  - Duplicate prevention (update existing records)
  - Error and warning tracking

### 3. API Endpoints

#### Historical Data
- `GET /api/historical-data/` - List historical data with filters
- `POST /api/historical-data/import/` - Import historical data from Excel files

#### Plant Capacity
- `GET /api/plant-capacity/` - List plant capacity records
- `GET /api/plant-capacity/{id}/` - Get specific capacity record

### 4. Management Command
- **Command**: `python manage.py import_historical_data`
- **Options**:
  - `--capacity` - Path to plant capacity Excel file
  - `--historical` - Path to historical data Excel file

### 5. Batch Script
- **File**: `IMPORT_HISTORICAL_DATA.bat`
- **Purpose**: Easy one-click import for Windows users

### 6. Documentation
- **HISTORICAL_DATA_IMPORT_GUIDE.md** - Comprehensive import guide
- **QUICK_IMPORT_GUIDE.txt** - Quick reference
- **API_DOCUMENTATION.md** - Updated with new endpoints

### 7. Sample Data Generator
- **File**: `CREATE_SAMPLE_HISTORICAL_DATA.py`
- **Purpose**: Generate sample Excel files for testing

## 📁 Files Created/Modified

### New Files
```
backend/reports/services/historical_data_importer.py
backend/reports/management/commands/import_historical_data.py
backend/reports/migrations/0002_plantcapacity_historicaldata.py
IMPORT_HISTORICAL_DATA.bat
HISTORICAL_DATA_IMPORT_GUIDE.md
QUICK_IMPORT_GUIDE.txt
CREATE_SAMPLE_HISTORICAL_DATA.py
📊_HISTORICAL_DATA_SOLUTION.md
```

### Modified Files
```
backend/reports/models.py (added PlantCapacity, HistoricalData)
backend/reports/serializers.py (added serializers)
backend/reports/views.py (added viewsets)
backend/reports/urls.py (added routes)
API_DOCUMENTATION.md (added endpoints documentation)
```

## 🚀 Quick Start

### Method 1: Using Batch Script (Easiest)

1. Place Excel files in `backend` folder:
   - `0PLANT DEPCAP.xlsx`
   - `1DATA APAO.xlsx`

2. Run:
   ```
   IMPORT_HISTORICAL_DATA.bat
   ```

### Method 2: Using Management Command

```bash
cd backend
venv\Scripts\activate
python manage.py migrate
python manage.py import_historical_data --capacity "0PLANT DEPCAP.xlsx" --historical "1DATA APAO.xlsx"
```

### Method 3: Using API

```bash
curl -X POST http://localhost:8000/api/historical-data/import/ \
  -F "capacity_file=@0PLANT DEPCAP.xlsx" \
  -F "historical_file=@1DATA APAO.xlsx"
```

## 📋 Excel File Format

### Plant Capacity File (0PLANT DEPCAP.xlsx)

| Column | Description | Required |
|--------|-------------|----------|
| Plant Name | Name of the plant | Yes |
| Installed Capacity (MW) | Total installed capacity | Yes |
| Dependable Capacity (MW) | Dependable capacity | Yes |
| Type | Plant type (Hydro/Thermal) | No |
| Location | Plant location | No |

### Historical Data File (1DATA APAO.xlsx)

| Column | Description | Required |
|--------|-------------|----------|
| Date or DATE | Report date | Yes |
| Plant Name or PLANT | Plant name | Yes |
| Generation (MWh) | Generation in MWh | Yes |
| Availability (%) | Availability percentage | Yes |
| Status | Operating status | No |
| Remarks | Additional notes | No |

**Note**: Multiple sheets are supported for different time periods.

## 🔍 Testing the Import

### 1. Generate Sample Data

```bash
python CREATE_SAMPLE_HISTORICAL_DATA.py
```

This creates:
- `0PLANT DEPCAP.xlsx` - Sample capacity data for 6 plants
- `1DATA APAO.xlsx` - Sample operational data for 60 days

### 2. Move Files to Backend

```bash
move 0PLANT*.xlsx backend\
move 1DATA*.xlsx backend\
```

### 3. Run Import

```bash
IMPORT_HISTORICAL_DATA.bat
```

### 4. Verify Import

Visit these URLs:
- http://localhost:8000/api/historical-data/
- http://localhost:8000/api/plant-capacity/

## 📊 API Usage Examples

### Fetch Historical Data

```javascript
// Get historical data for Agus 1 in 2024
const response = await axios.get('/api/historical-data/', {
  params: {
    plant_code: 'AGUS1',
    start_date: '2024-01-01',
    end_date: '2024-12-31'
  }
});
```

### Import Data via API

```javascript
const formData = new FormData();
formData.append('capacity_file', capacityFile);
formData.append('historical_file', historicalFile);

const response = await axios.post('/api/historical-data/import/', formData, {
  headers: { 'Content-Type': 'multipart/form-data' }
});

console.log(`Imported ${response.data.total_imported} records`);
```

### Get Plant Capacity

```javascript
const response = await axios.get('/api/plant-capacity/', {
  params: { plant_code: 'AGUS1' }
});
```

## 🔧 Database Migration

Run migrations to create the new tables:

```bash
cd backend
venv\Scripts\activate
python manage.py migrate
```

This creates:
- `plant_capacity` table
- `historical_data` table

## ⚠️ Important Notes

1. **Plant Matching**: Plants are matched by name (case-insensitive, partial match)
2. **Duplicate Handling**: Records with same plant+date are updated, not duplicated
3. **File Size Limit**: Maximum 50MB per file
4. **Supported Format**: Only `.xlsx` files
5. **Date Formats**: Automatically parses various date formats

## 🐛 Troubleshooting

### "Plant not found" warnings
- Ensure plant names in Excel match existing plants
- Check plant name spelling
- Plants must exist in the database before import

### Import fails
- Verify file format is `.xlsx`
- Check column names match expected format
- Review Django logs for detailed errors

### Database errors
- Run `python manage.py migrate`
- Ensure database is accessible
- Check database permissions

## 📈 Performance

- **Batch Processing**: Uses Django's `bulk_create` for efficiency
- **Transaction Safety**: All imports wrapped in database transactions
- **Error Recovery**: Continues processing even if some records fail
- **Progress Tracking**: Shows import progress and statistics

## 🔐 Security

- **File Validation**: Validates file type and size
- **SQL Injection Protection**: Uses Django ORM (parameterized queries)
- **Error Handling**: Graceful error handling with detailed messages
- **Transaction Rollback**: Failed imports don't leave partial data

## 📚 Additional Resources

- **Detailed Guide**: See `HISTORICAL_DATA_IMPORT_GUIDE.md`
- **Quick Reference**: See `QUICK_IMPORT_GUIDE.txt`
- **API Docs**: See `API_DOCUMENTATION.md`

## ✨ Features

✅ Import plant capacity data
✅ Import historical operational data
✅ Multi-sheet Excel support
✅ Automatic plant matching
✅ Date format auto-detection
✅ Duplicate prevention
✅ Error and warning tracking
✅ API endpoints for data access
✅ Management command for CLI import
✅ Batch script for easy import
✅ Comprehensive documentation
✅ Sample data generator

## 🎯 Next Steps

1. **Run Migrations**: `python manage.py migrate`
2. **Test with Sample Data**: Run `CREATE_SAMPLE_HISTORICAL_DATA.py`
3. **Import Sample Data**: Run `IMPORT_HISTORICAL_DATA.bat`
4. **Verify Import**: Check API endpoints
5. **Import Real Data**: Replace sample files with actual data

## 💡 Tips

- Always backup your database before importing large datasets
- Test with small sample files first
- Review import results for errors and warnings
- Use filters when querying large datasets
- Monitor database size as historical data grows

---

**Status**: ✅ Complete and Ready to Use

**Last Updated**: February 12, 2026
