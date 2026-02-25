# ✅ PSR Report Now Uses Real Database Data

## Summary

The PSR (Plant Status Report) has been updated to use **real data from the database** instead of hardcoded sample values.

## What Was Changed

### 1. Generation Data (`_calculate_generation_data` method)
**Before:** Hardcoded sample values
```python
gen_data = [
    ['AGUS1', '1,920', '57,600', '115,200'],
    ['AGUS2', '4,320', '129,600', '259,200'],
    ...
]
```

**After:** Real database queries
```python
# Query actual generation from GenerationReport model
today_gen = GenerationReport.objects.filter(
    plant=plant,
    report_date=today_start
).aggregate(total=Sum('generation_kwh'))['total'] or 0
```

### 2. Capacity Factor Data (`_calculate_capacity_factor` method)
**Before:** Hardcoded percentages
```python
cf_data = [
    ['AGUS1', '100.0', '100.0', '100.0'],
    ['AGUS2', '100.0', '100.0', '100.0'],
    ...
]
```

**After:** Calculated from database
```python
# Calculate average capacity factor from actual data
today_cf = GenerationReport.objects.filter(
    plant=plant,
    report_date=today_start
).aggregate(avg_cf=Avg('capacity_factor'))['avg_cf'] or 0
```

## Data Sources

### From Database (Real Data)
✅ **Generation Data**
- Today's generation (MWh)
- Month-to-date generation (MWh)
- Year-to-date generation (MWh)

✅ **Capacity Factors**
- Today's capacity factor (%)
- Month-to-date average (%)
- Year-to-date average (%)

✅ **Plant Information**
- Unit-level generation data
- Operating hours
- Outage hours
- Remarks

### Template Values (Operator Input)
📝 **Operational Parameters** (would be updated by operators in real-time)
- Gate openings (GATE#1-6)
- Reservoir elevations
- Lake Lanao elevation
- Forebay elevations
- Spillage data (MCM)
- Water flow rates (CMS)
- MLRD gates status

## Verification Results

Run `python verify_psr_real_data.py` to see real data:

```
📅 Checking data for: February 13, 2026

🔍 GENERATION DATA FROM DATABASE:
----------------------------------------------------------------------
  PULANGI4   -   5,700.00 MWh  |  CF:  93.1%  |  ✓ HAS DATA
----------------------------------------------------------------------
  TOTAL      -   5,700.00 MWh

📊 MONTH-TO-DATE DATA:
----------------------------------------------------------------------
  AGUS1      -     990.00 MWh  |  10 days of data
  AGUS2      -     990.00 MWh  |  10 days of data
  PULANGI4   -  61,650.00 MWh  |  11 days of data
----------------------------------------------------------------------
  TOTAL      -  63,630.00 MWh
```

## How It Works

1. **Data Upload**: Users upload Excel files with generation data
2. **Database Storage**: Data is stored in `GenerationReport` model
3. **PSR Generation**: When generating PSR report, system queries database
4. **Calculations**: 
   - Today: Single day data
   - MTD: From 1st of month to report date
   - YTD: From January 1 to report date
5. **Aggregations**: Sum for generation, Average for capacity factors

## Benefits

✅ **Accurate**: Data comes directly from uploaded generation reports
✅ **Dynamic**: Updates automatically as new data is uploaded
✅ **Traceable**: All data linked to source files and upload records
✅ **Auditable**: Complete audit trail of data sources
✅ **Flexible**: Easy to add more calculations or metrics

## Testing

### Test PSR Generation
```bash
python test_psr_generation.py
```

### Verify Real Data
```bash
python verify_psr_real_data.py
```

### Check Database
```bash
cd backend
python manage.py shell
```
```python
from reports.models import GenerationReport
from datetime import date

# Check data for a specific date
reports = GenerationReport.objects.filter(report_date=date(2026, 2, 13))
for r in reports:
    print(f"{r.plant.code} Unit {r.unit.unit_number}: {r.generation_kwh} kWh")
```

## Next Steps

To add more real-time operational data:

1. **Gate Openings**: Create `GateOperation` model to store gate positions
2. **Reservoir Levels**: Create `ReservoirLevel` model for elevation data
3. **Spillage Data**: Create `SpillageRecord` model for water spillage
4. **SCADA Integration**: Connect to SCADA systems for real-time data

## Files Modified

- `backend/reports/services/psr_exporter.py`
  - Updated `_calculate_generation_data()` method
  - Updated `_calculate_capacity_factor()` method
  - Added database queries with proper aggregations

## Database Models Used

- `Plant`: Plant information (AGUS1-7, PULANGI4)
- `Unit`: Generation units within each plant
- `GenerationReport`: Daily generation data per unit
- `PlantCapacity`: Historical capacity information

---

**Status**: ✅ Complete and Tested
**Date**: February 24, 2026
**Impact**: PSR reports now show actual operational data from the system
