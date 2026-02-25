# ✅ Plant Status Excel Template Added

## What Was Added

Successfully added a new "Plant Status" Excel template to the download templates section. This template allows users to upload daily operational status for all power plants.

## Changes Made

### 1. Backend - Template Generator ✅
**File**: `backend/reports/services/template_generator.py`

Added `generate_plant_status_template()` method that creates an Excel file with:

**Data Sheet Columns:**
- Date (YYYY-MM-DD)
- Plant Code
- Plant Name
- Status (Operating, Maintenance, Shutdown, Standby)
- Installed Capacity (MW)
- Available Capacity (MW)
- Generation (MWh)
- Capacity Factor (%)
- Availability (%)
- Operating Units
- Total Units
- Remarks

**Sample Data:**
- Includes 3 sample rows for AGUS1, AGUS2, and PULANGI4
- Shows realistic operational data
- First row has gray background (to be deleted before upload)

**Instructions Sheet:**
- Comprehensive guide on how to fill the template
- Column descriptions
- Valid status values
- Important notes and validation rules
- Example use cases
- Professional formatting with colors

### 2. Backend - API Endpoint ✅
**File**: `backend/reports/views.py`

Added new endpoint:
```python
@action(detail=False, methods=['get'], url_path='download-template/plant-status')
def download_plant_status_template(self, request):
    """Download Plant Status template"""
    wb = TemplateGenerator.generate_plant_status_template()
    return TemplateGenerator.create_http_response(wb, 'Plant_Status_Template.xlsx')
```

**API URL**: `GET /api/uploaded-files/download-template/plant-status/`

### 3. Frontend - UI Button ✅
**File**: `frontend/src/components/UploadExcel.vue`

Added new template button in the template grid:
```vue
<button @click="downloadTemplate('plant-status')" class="template-btn glass-button">
  <i class="pi pi-file-excel"></i>
  <div class="template-info">
    <span class="template-name">Plant Status</span>
    <span class="template-desc">For daily plant operational status</span>
  </div>
</button>
```

## Template Features

### Professional Design
- Blue header row with white text
- Gray sample data row (easy to identify and delete)
- Yellow highlighted sections in instructions
- Auto-sized columns for readability
- Borders on all cells

### Comprehensive Instructions
The template includes detailed instructions covering:
- Purpose of the template
- Column descriptions
- Valid status values
- Important validation rules
- Example use cases
- Support contact information

### Sample Data
Includes realistic sample data for:
- **AGUS1**: 50 MW, 100% operational
- **AGUS2**: 100 MW, 95% available (Unit 1 under maintenance)
- **PULANGI4**: 255 MW, 98% capacity factor, all units operational

### Validation Rules
- Date must be in YYYY-MM-DD format
- Plant Code must match existing plants
- Available Capacity ≤ Installed Capacity
- Operating Units ≤ Total Units
- Percentages between 0-100
- Status must be valid value

## Use Cases

1. **Daily Status Reporting**
   - Upload daily operational status for all plants
   - Track availability and generation
   - Monitor unit operations

2. **Historical Data Import**
   - Bulk import past operational data
   - Compile monthly/annual status reports
   - Historical performance analysis

3. **Maintenance Tracking**
   - Record scheduled maintenance periods
   - Track unit availability during maintenance
   - Document operational remarks

## How to Use

### For Users:
1. Go to "Upload Excel" page
2. Click "Plant Status" template button
3. Download the template
4. Fill in the data (delete sample rows)
5. Upload the completed file

### Template Structure:
```
Sheet 1: Plant Status (Data Entry)
├── Headers (Blue background)
├── Sample Data (Gray background - DELETE THIS)
└── Empty rows for data entry

Sheet 2: Instructions
├── Purpose
├── Column Descriptions
├── Valid Status Values
├── Important Notes
└── Example Use Cases
```

## Files Modified

### Backend
- `backend/reports/services/template_generator.py` - Added generate_plant_status_template()
- `backend/reports/views.py` - Added download_plant_status_template() endpoint

### Frontend
- `frontend/src/components/UploadExcel.vue` - Added Plant Status button

## Testing

To test the new template:

1. **Download Template**:
   ```
   Navigate to: Upload Excel page
   Click: "Plant Status" button
   Result: Plant_Status_Template.xlsx downloads
   ```

2. **Verify Template**:
   - Open the downloaded file
   - Check "Plant Status" sheet has correct columns
   - Check "Instructions" sheet has detailed guide
   - Verify sample data is present

3. **Test Upload** (Optional):
   - Fill in the template with real data
   - Delete sample rows
   - Upload through the system
   - Verify data is imported correctly

## Template Columns Explained

| Column | Description | Example |
|--------|-------------|---------|
| Date | Report date | 2026-02-23 |
| Plant Code | Official code | AGUS1 |
| Plant Name | Full name | Agus 1 Hydroelectric Power Plant |
| Status | Operational status | Operating |
| Installed Capacity (MW) | Total capacity | 50.0 |
| Available Capacity (MW) | Currently available | 50.0 |
| Generation (MWh) | Daily generation | 1200.0 |
| Capacity Factor (%) | Performance | 100.0 |
| Availability (%) | Availability | 100.0 |
| Operating Units | Units running | 1 |
| Total Units | Total units | 1 |
| Remarks | Notes | Normal operation |

## Status Values

Valid status values for the Status column:
- **Operating** - Plant is generating power
- **Maintenance** - Plant is under scheduled maintenance
- **Shutdown** - Plant is temporarily shut down
- **Standby** - Plant is ready but not generating

## Benefits

1. **Standardized Format** - Ensures consistent data entry
2. **Clear Instructions** - Reduces upload errors
3. **Sample Data** - Shows users exactly what to enter
4. **Validation Rules** - Prevents invalid data
5. **Professional Design** - Easy to read and use
6. **Comprehensive** - Covers all operational aspects

## Summary

The Plant Status template is now available for download! Users can:
- Download a professionally formatted Excel template
- See sample data for guidance
- Read comprehensive instructions
- Upload daily operational status for all plants
- Track plant performance and availability

The template is ready for immediate use and follows the same design patterns as the other templates in the system. 🎉
