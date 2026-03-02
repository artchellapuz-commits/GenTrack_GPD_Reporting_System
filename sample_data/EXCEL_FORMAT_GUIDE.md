# Excel File Format Guide

## Required Columns (in any order)

The Excel file MUST contain these exact column names (case-insensitive):

1. **date** - Report date in YYYY-MM-DD format (e.g., 2026-02-20)
2. **unit_number** - Integer unit number (e.g., 1, 2, 3, 4)
3. **generation_kwh** - Generation in kilowatt-hours (numeric, >= 0)
4. **operating_hours** - Hours unit was operating (0-24)
5. **availability_hours** - Hours unit was available (0-24)
6. **forced_outage_hours** - Hours of forced outage (0-24)
7. **scheduled_outage_hours** - Hours of scheduled outage (0-24)
8. **remarks** - Optional text notes

## Example Data

```
date        | unit_number | generation_kwh | operating_hours | availability_hours | forced_outage_hours | scheduled_outage_hours | remarks
2026-02-20  | 1          | 540000.50      | 22.5           | 23.0              | 0.5                | 0.0                   | Normal operation
2026-02-20  | 2          | 520000.00      | 21.0           | 22.0              | 2.0                | 0.0                   | Minor maintenance
```

## Validation Rules

- All numeric values must be >= 0
- Hour values must be between 0 and 24
- Date must be valid date format
- Unit number must exist for the selected plant
- No null/empty values in required columns

## Plant Units

- AGUS1: Units 1, 2, 3, 4
- AGUS2: Units 1, 2
- AGUS4: Units 1, 2
- AGUS5: Units 1, 2
- AGUS6: Units 1, 2, 3, 4
- AGUS7: Units 1, 2, 3, 4
- PULANGI4: Units 1, 2, 3, 4
