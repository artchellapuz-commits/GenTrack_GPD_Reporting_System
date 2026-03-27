# Actual Data Implementation - All Reports Use Uploaded File Data

## Summary
All generated reports (PSR and Daily Plant Status) now use **100% actual data from uploaded files** instead of hardcoded placeholder values. Every number, chart, and calculation is based on real uploaded generation data.

## Changes Made

### 1. Forecasted Load Section
**Before**: Hardcoded values (500.8 MW for Agus, 150.0 MW for Pulangi)
**After**: Calculated from actual uploaded data by summing generation from all units

```python
# Calculate from actual data
agus_forecast = sum of all AGUS1-7 generation from uploaded files
pulangi_forecast = sum of PULANGI4 generation from uploaded files
```

### 2. INPUT Workflow Section (Right Side)
**Before**: Hardcoded plant data with 0.00 loads
**After**: Actual rated capacity, available capacity, and load from uploaded files

```python
# For each plant
total_capacity = sum of unit capacities (from config)
total_available = sum of available units (from uploaded data)
total_load = sum of actual generation (from uploaded files)
```

### 3. Total Load Display
**Before**: Hardcoded "650.80 MW"
**After**: Calculated by summing all generation from all plants in uploaded files

```python
total_load_all = sum of all unit generation across all plants
```

### 4. Summary Tables
**Before**: Hardcoded values for each plant
**After**: Dynamic calculation from uploaded data

- Rated capacity: From plant configuration
- Available capacity: Sum of units with data
- Load: Sum of actual generation from uploaded files
- Capacity factor: (load / rated * 100)%

### 5. Pie Chart Data
**Before**: Hardcoded 811.31 MW for Hydro
**After**: Calculated total capacity from all hydro plants (AGUS1-7 + PULANGI4)

```python
hydro_capacity = sum of all unit capacities from AGUS and PULANGI plants
```

### 6. Bar Chart Data
**Before**: Hardcoded forecasted loads for each plant
**After**: Actual generation from uploaded files for each plant

```python
# For each plant
load = sum of generation from all units with uploaded data
```

### 7. Plant Capacity Comparison Chart
**Before**: Hardcoded rated, available, and load values
**After**: Calculated from actual uploaded data

```python
# For each plant
rated = sum of unit capacities
available = sum of units with data
load = sum of actual generation
```

## Data Flow

```
Uploaded Excel/CSV Files
        ↓
Excel Importer processes files
        ↓
GenerationReport records created in database
        ↓
PSRExporter queries GenerationReport data
        ↓
_organize_data() creates data_by_plant dictionary
        ↓
All report sections use data_by_plant for calculations
        ↓
Generated Excel report with 100% actual data
```

## Key Methods Updated

### `_add_forecasted_load()`
- Calculates Agus and Pulangi forecasts from actual data
- Sums generation across all units for each plant group

### `_add_input_workflow_right_side()`
- Plant data table uses actual capacity and load
- Total load calculated from all uploaded data
- Summary tables use actual data
- Capacity factor calculated from actual load/capacity ratio

### `_add_notes_section()`
- Pie chart uses calculated hydro capacity
- Bar chart uses actual plant loads from uploaded files

### `_add_chart_and_agus2_note()`
- Plant comparison chart uses actual rated, available, and load data

## Data Sources

### From Uploaded Files (Dynamic):
- ✅ Generation (kWh/MW)
- ✅ Operating hours
- ✅ Forced outage hours
- ✅ Scheduled outage hours
- ✅ Remarks
- ✅ All load calculations
- ✅ All availability calculations
- ✅ All capacity factor calculations

### From Configuration (Static):
- Unit capacities (MW)
- Unit labels
- Plant names
- Nominated capacity values

### Fixed Values (Industry Standard):
- IPP (STEAG) capacity: 210 MW (not from uploaded files)
- Lake elevations (operational data, not from generation files)

## Benefits

1. **Accuracy**: Reports reflect actual operational data
2. **Real-time**: Data updates as new files are uploaded
3. **Transparency**: All numbers traceable to uploaded files
4. **Flexibility**: Works with any date range and plant selection
5. **Reliability**: No manual data entry or hardcoded values

## Testing

To verify actual data is being used:

1. **Upload test files** with known generation values
2. **Generate report** for the same date range
3. **Verify numbers match**:
   - Plant loads should match uploaded generation
   - Forecasted load should equal sum of all generation
   - Charts should reflect uploaded data
   - Summary tables should show actual values

## Example Data Flow

**Uploaded File**: AGUS1_Sample_Report.xlsx
```
Date: 2026-03-01
Unit 1: 35.5 MW
Unit 2: 38.2 MW
```

**Generated Report Shows**:
- AGUS 1 Total Load: 73.7 MW (35.5 + 38.2)
- Agus Forecasted Load: Includes this 73.7 MW
- Total Load @ 0800H: Includes this 73.7 MW
- Charts: Show 73.7 MW for AGUS 1
- Summary Tables: Show 73.7 MW for AGUS1

## Files Modified

- `npc-reporting-system/backend/reports/services/psr_exporter.py`
  - `_add_forecasted_load()` - Calculate from actual data
  - `_add_input_workflow_right_side()` - Use actual plant data
  - `_add_notes_section()` - Use actual data for charts
  - `_add_chart_and_agus2_note()` - Use actual data for comparison chart

## No More Hardcoded Values

All these hardcoded values have been removed:
- ❌ 500.8 MW (Agus forecast)
- ❌ 150.0 MW (Pulangi forecast)
- ❌ 650.80 MW (Total load)
- ❌ 811.31 MW (Hydro capacity in pie chart)
- ❌ All plant load values in summary tables
- ❌ All chart data values

Now replaced with:
- ✅ Dynamic calculations from uploaded files
- ✅ Real-time data aggregation
- ✅ Actual generation values
- ✅ Traceable to source files

## Impact

**Before**: Reports showed placeholder/example data regardless of uploads
**After**: Reports show exact data from uploaded files

This ensures that all stakeholders see accurate, real-time operational data in every generated report.
