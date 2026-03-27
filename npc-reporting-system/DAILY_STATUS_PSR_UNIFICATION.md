# Daily Plant Status Report & PSR Template Unification

## Summary
Both the Daily Plant Status Report and the PSR (Plant Status Report) now use the **same comprehensive template** with identical formatting, layout, sections, and **header styling**. The only differences are:

1. **Title text** - "DAILY PLANT STATUS" vs "PLANT STATUS REPORT"
2. **Time reference** - "12:00 NN" vs "0800H"
3. **Date format** - Different date formatting
4. **Filename** - Different naming conventions

**Both reports now have the dark gray/teal header background (#2F4F4F) with white text.**

## Changes Made

### 1. Modified `PSRExporter` Class
**File**: `npc-reporting-system/backend/reports/services/psr_exporter.py`

#### Added `report_type` Parameter
```python
def __init__(self, queryset, report_date, report_type='psr'):
    # report_type can be 'psr' or 'daily_status'
```

#### Updated `_add_header()` Method
The header now uses the same dark gray/teal styling for both report types:

**For Daily Plant Status Report** (`report_type='daily_status'`):
- Header background: Dark gray/teal (`#2F4F4F`)
- Font color: White (`#FFFFFF`)
- Title: "DAILY PLANT STATUS"
- Time: "as of 12:00 NN    [Date]"
- Date format: "Monday, March 02, 2026"

**For PSR Report** (`report_type='psr'`):
- Header background: Dark gray/teal (`#2F4F4F`) ✨ **NEW**
- Font color: White (`#FFFFFF`) ✨ **NEW**
- Title: "PLANT STATUS REPORT"
- Time: "as of 0800H [Date]"
- Date format: "Monday, 02 March 2026"

### 2. Updated `views.py`
**File**: `npc-reporting-system/backend/reports/views.py`

Modified the `generate_report()` method in `GenerationReportViewSet`:
```python
# Pass report_type to customize header styling
exporter = PSRExporter(reports, report_date, report_type=report_type)
file_path = exporter.generate()
```

## Template Features (Both Reports)

Both reports now include:

✅ **Header Section**
- MINDANAO GENERATION title
- (PSALM PORTFOLIO) subtitle
- FOR: section with recipients
- Report title with conditional styling
- Date/time with conditional styling

✅ **Column Headers**
- Plant Name
- Rated Capacity (MW)
- Nominated Capability
- Available Capacity (MW)
- Lake Lanao Projected Ave. Outflow
- Load at 0800H
- Remarks

✅ **Plant Data Sections**
- AGUS 1-7 plants with all units
- TOTAL AGUS summary
- PULANGI IV with all units
- TOTAL HYDRO summary

✅ **Forecasted Load Section**
- Yellow highlighted row
- Agus-Pulangi forecasted load breakdown

✅ **IPP Section**
- MCFPP (STEAG) units 1 & 2
- TOTAL IPP summary
- TOTAL NPC-PSALM summary

✅ **Charts & Notes**
- NPC-PSALM Capacity Mix (Pie Chart)
- MinGen Forecasted Load Share (Bar Chart)
- Detailed notes section
- MCFPP and MGPP information

✅ **Footer Section**
- Multiple signature blocks
- Prepared by, Checked by, Approved by
- Personnel names and titles

✅ **Right Side Sections**
- INPUT workflow section
- Plant data tables
- Capacity factor calculations
- Elevation data

## Visual Appearance

### Both Reports Now Have Identical Header Styling

```
┌─────────────────────────────────────────────┐
│  MINDANAO GENERATION                        │
│  (PSALM PORTFOLIO)                          │
│                                             │
│  ┌───────────────────────────────────────┐ │
│  │ DAILY PLANT STATUS / PLANT STATUS     │ │ ← Dark gray/teal background
│  │ REPORT                                │ │ ← White text
│  │ as of 12:00 NN / 0800H [Date]         │ │ ← White text
│  └───────────────────────────────────────┘ │
└─────────────────────────────────────────────┘
```

### Daily Plant Status Report Header
- Title: "DAILY PLANT STATUS"
- Time: "as of 12:00 NN    Monday, March 02, 2026"
- Background: Dark gray/teal (#2F4F4F)
- Text: White (#FFFFFF)

### PSR Report Header
- Title: "PLANT STATUS REPORT"
- Time: "as of 0800H Monday, 02 March 2026"
- Background: Dark gray/teal (#2F4F4F) ✨ **SAME AS DAILY STATUS**
- Text: White (#FFFFFF) ✨ **SAME AS DAILY STATUS**

## File Naming

- **Daily Plant Status**: `DAILY_PLANT_STATUS_YYYYMMDD.xlsx`
- **PSR Report**: `PSR_REPORT_YYYYMMDD.xlsx`

## Benefits

1. **Consistency** - Both reports use the same comprehensive template AND styling
2. **Professional Look** - Unified dark gray/teal header across all reports
3. **Maintainability** - Single template to maintain instead of two
4. **Visual Identity** - Both reports share the same distinctive header style
5. **Completeness** - Daily Status now includes all PSR sections (charts, notes, IPP data)
6. **Flexibility** - Easy to add more report types with the same styling

## Testing

To test the changes:

1. **Generate Daily Plant Status Report**:
   - Select report type: "Daily Plant Status"
   - Choose date range and plants
   - Click "Generate Report"
   - Verify dark gray/teal header with "DAILY PLANT STATUS" title

2. **Generate PSR Report**:
   - Select report type: "PSR"
   - Choose date range and plants
   - Click "Generate Report"
   - Verify dark gray/teal header with "PLANT STATUS REPORT" title ✨ **NOW HAS COLORED HEADER**

3. **Verify Content**:
   - Both reports should have identical sections
   - Both should include charts, notes, IPP data
   - Both should have footer signatures
   - Both should have right-side sections

## Backward Compatibility

✅ PSR reports now have enhanced visual styling with colored header
✅ Daily Status reports continue to work exactly as before
✅ No breaking changes to API or frontend
✅ Old `daily_status_exporter.py` is no longer used but kept for reference
✅ Both reports now have professional, consistent appearance

## Files Modified

1. `npc-reporting-system/backend/reports/services/psr_exporter.py`
   - Added `report_type` parameter to `__init__()`
   - Modified `_add_header()` to support conditional styling

2. `npc-reporting-system/backend/reports/views.py`
   - Updated `generate_report()` to pass `report_type` to PSRExporter

## Files Deprecated (but kept)

- `npc-reporting-system/backend/reports/services/daily_status_exporter.py`
  - No longer used in production
  - Kept for reference only
