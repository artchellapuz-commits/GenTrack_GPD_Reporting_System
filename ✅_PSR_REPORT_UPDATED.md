# ✅ PSR Report Updated to Match Exact Template

## What Was Done

Updated the PSR (Plant Status Report) exporter to match the EXACT format from the provided template file:
`C:\Users\eladiong\Desktop\OJT Intern\REPORTS\8. PSR\PSR REPORT-8AM.xlsx`

## Changes Made

### 1. Analyzed Template Structure
- Ran `analyze_psr.py` to understand the exact Excel structure
- Identified all formatting, merged cells, row heights, column widths
- Mapped plant configurations and data layout

### 2. Complete Rewrite of PSR Exporter
**File**: `backend/reports/services/psr_exporter.py`

**Key Features**:
- Exact column widths matching template (A: 25.86, B: 15.14, etc.)
- Exact row heights matching template
- Proper header section with:
  - "MINDANAO GENERATION"
  - "(PSALM PORTFOLIO)"
  - FOR section with recipients
  - "PLANT STATUS REPORT" title
  - Date formatting: "as of 0800H [Day, Date Month Year]"
- Column headers:
  - PLANT NAME
  - Rated Capacity (MW)
  - Nominated / Capability
  - Available Capacity (MW)
  - Lake Lanao Projected Ave. Outflow
  - Load at 0800H
  - REMARKS
- Plant sections for:
  - AGUS 1 (2 units @ 40 MW each)
  - AGUS 2 (3 units @ 60 MW each)
  - AGUS 4 (3 units @ 52.7 MW each)
  - AGUS 5 (2 units @ 27.5 MW each)
  - AGUS 6 (5 units: 34.5, 34.5, 50, 50, 50 MW)
  - AGUS 7 (2 units @ 27 MW each)
  - TOTAL AGUS summary
  - PULANGI IV (3 units @ 85 MW each)
  - TOTAL HYDRO summary
- Footer section with signatures:
  - Prepared by: DRB CAIRO (Prin. Engr. A, GPD)
  - Checked and Reviewed by: JMM MATA (Manager, GPD)
  - Approved by: DB ESMADE, JR. (Dept. Manager, OPD)

### 3. Data Organization
- Organizes generation data by plant code and unit number
- Calculates totals for each plant
- Generates appropriate remarks based on:
  - Forced outages
  - Scheduled outages
  - Operating status (OPERATIONAL, STANDBY)
  - Custom remarks from database

### 4. Formatting
- Bold fonts for plant names and totals
- Color fills:
  - Green (CCFFCC) for plant headers
  - Yellow (FFFF00) for total rows
  - Gray (CCCCCC) for column headers
- Proper cell alignment and text wrapping
- Merged cells matching template layout

## How to Use

### From Frontend (Generate Report Page)

1. Go to "Generate Report" page
2. Select date range
3. Select plants (AGUS1, AGUS2, etc.)
4. Choose "Plant Status Report (PSR)" from report type dropdown
5. Click "Generate Report"
6. File will download as: `PSR_REPORT_YYYYMMDD.xlsx`

### From API

```bash
POST http://localhost:8000/api/reports/generation-reports/generate-report/

{
  "plant_codes": ["AGUS1", "AGUS2", "AGUS4", "AGUS5", "AGUS6", "AGUS7", "PULANGI4"],
  "start_date": "2026-02-23",
  "end_date": "2026-02-23",
  "report_type": "psr"
}
```

## File Location

Generated PSR reports are saved to:
```
backend/media/exports/PSR_REPORT_YYYYMMDD.xlsx
```

## Template Matching

The generated report matches the template in:
- ✅ Column widths
- ✅ Row heights
- ✅ Header text and formatting
- ✅ Plant names and order
- ✅ Unit configurations
- ✅ Capacity values
- ✅ Column headers
- ✅ Footer signatures
- ✅ Cell merging
- ✅ Font styles and sizes
- ✅ Color fills

## Notes

- The report uses actual generation data from the database
- If no data exists for a unit, it shows "No data" in remarks
- Remarks are automatically generated based on outage hours
- Lake Lanao elevation and reservoir levels are shown as fixed values (can be made dynamic later)
- The report format is specifically for PSALM portfolio plants

## Next Steps (Optional Enhancements)

1. Make lake/reservoir elevations dynamic from database
2. Add forecasted load calculations
3. Include IPP (Independent Power Producer) data if needed
4. Add more detailed outage information
5. Include water flow data if available

---

**Status**: ✅ COMPLETE - PSR Report now matches exact template format
**Date**: February 23, 2026
**Files Modified**: 
- `backend/reports/services/psr_exporter.py` (complete rewrite)
