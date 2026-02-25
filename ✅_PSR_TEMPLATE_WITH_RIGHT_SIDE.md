# ✅ PSR Template with Right Side Section - COMPLETE

## What Was Added

Successfully added a comprehensive PSR (Plant Status Report) Excel template with the right side section containing additional operational data.

## Template Features

### Main Table (Left Side)
- Unit identification
- Rated Capacity (MW)
- Dependable Capacity (MW)
- GENFCST columns for generation forecast
- Remarks column

### Right Side Sections

#### 1. PRIMARY STORAGE OF HYDRO HEPs
- Lake/Dam levels in meters above sea level
- Current status and remarks
- Includes:
  - Lake Lanao (701.20 m)
  - Agus 2 Forebay (637.30 m)
  - Agus 4 Forebay (358.50 m)
  - Agus 5 Forebay (242.80 m)
  - Agus 6 Forebay (199.80 m)

#### 2. HYDRO INFLOW/OUTFLOW
- Inflow and outflow rates in cubic meters per second (cms)
- Data for each plant and reservoir
- Includes Lake Lanao, Agus 1, Agus 2, Agus 4, Agus 5

#### 3. GENERATION DATA (MWh)
- Today - Current day generation
- MTD - Month-to-date generation
- YTD - Year-to-date generation
- Data for AGUS1, AGUS2, PULANGI4
- Total NPC row with calculations

#### 4. CAPACITY FACTOR (%)
- Percentage of maximum possible generation
- Today, MTD, and YTD values
- Plant-wise breakdown
- Average capacity factor

## Files Modified

### Backend
1. `backend/reports/services/template_generator.py`
   - Added `generate_psr_template()` method
   - Creates comprehensive PSR template with all sections
   - Includes proper styling, borders, and formatting
   - Sample data for all sections

2. `backend/reports/views.py`
   - Added `download_psr_template()` endpoint
   - URL: `/api/uploaded-files/download-template/psr/`

### Frontend
3. `frontend/src/components/UploadExcel.vue`
   - Added "PSR Template" button in template grid
   - Button description: "Plant Status Report with right side data"
   - Uses existing downloadTemplate method

## How to Use

### Download the Template
1. Go to "Upload Excel Report" page
2. Look for "Download Excel Templates" section
3. Click the "PSR Template" button
4. File will download as `psr_template.xlsx`

### Template Structure
- **Data Sheet**: Main PSR template with all sections
- **Instructions Sheet**: Comprehensive guide with:
  - Purpose and overview
  - Column descriptions for main table
  - Detailed explanation of each right side section
  - Important notes and guidelines

### Filling the Template
1. Enter date in the header section
2. Fill main table with unit data
3. Update PRIMARY STORAGE levels
4. Enter HYDRO INFLOW/OUTFLOW data
5. Fill GENERATION DATA (Today, MTD, YTD)
6. Update CAPACITY FACTOR percentages
7. Review all sections before finalizing

## Template Styling

### Colors
- **Header Fill**: Dark blue (#2F5496) with white text
- **Yellow Fill**: Bright yellow (#FFFF00) for sub-headers
- **Light Blue Fill**: Light blue (#B4C7E7) for certain sections
- **Light Gray Fill**: Gray (#D9D9D9) for totals and averages

### Formatting
- All cells have thin borders
- Headers are bold with centered alignment
- Numeric values are right-aligned
- Text values are left-aligned
- Proper column widths for readability

## API Endpoint

```
GET /api/uploaded-files/download-template/psr/
```

**Response**: Excel file download
**Filename**: `PSR_Template.xlsx`

## Sample Data Included

The template includes sample data for:
- AGUS1 (1 unit, 50 MW)
- AGUS2 (2 units, 100 MW)
- Lake levels and forebay elevations
- Inflow/outflow rates
- Generation data (Today: 9,600 MWh, MTD: 288,000 MWh, YTD: 576,000 MWh)
- Capacity factors (ranging from 98% to 100%)

## Important Notes

- All sample data should be deleted before entering actual data
- Numeric values should be entered without commas
- Dates should be in YYYY-MM-DD format
- Ensure all calculations are accurate
- Review all sections before finalizing the report

## Status

✅ Backend implementation complete
✅ Frontend button added
✅ API endpoint working
✅ Template includes all right side sections
✅ Instructions sheet included
✅ Server restarted and changes applied

The PSR template with comprehensive right side section is now ready to use!
