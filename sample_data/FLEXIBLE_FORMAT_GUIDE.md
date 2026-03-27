# Flexible Excel Format Support

The NPC Reporting System now accepts Excel files in various formats and layouts!

## Supported File Types

- **.xlsx** (Excel 2007 and later)
- **.xls** (Excel 97-2003)
- **Maximum file size:** 25MB

## Flexible Column Names

The system recognizes multiple variations of column names. You can use ANY of these alternatives:

### Date Column
- `date`, `report_date`, `reportdate`, `day`, `datetime`, `timestamp`

### Unit Number Column
- `unit_number`, `unitnumber`, `unit`, `unit_no`, `unitno`, `unit_id`, `unitid`

### Generation Column
- `generation_kwh`, `generation`, `gen_kwh`, `kwh`, `energy`, `energy_kwh`

### Operating Hours Column
- `operating_hours`, `operatinghours`, `op_hours`, `ophours`, `run_hours`, `runtime`

### Availability Hours Column
- `availability_hours`, `availabilityhours`, `avail_hours`, `available_hours`

### Forced Outage Hours Column
- `forced_outage_hours`, `forcedoutagehours`, `forced_outage`, `fo_hours`, `foh`

### Scheduled Outage Hours Column
- `scheduled_outage_hours`, `scheduledoutagehours`, `scheduled_outage`, `so_hours`, `soh`, `maintenance_hours`

## Flexible Layout Support

### Multiple Sheets
- The system will automatically search all sheets in your Excel file
- It will use the first sheet that contains valid data

### Header Row Detection
- The system automatically detects where your header row is
- You can have title rows, logos, or other content above your data
- The system looks for keywords like "date", "unit", "generation" to find headers

### Column Order
- Columns can be in ANY order
- The system maps columns by name, not position

### Extra Columns
- You can have additional columns in your file
- They will be ignored if not required

## Data Flexibility

### Date Formats
The system accepts various date formats:
- `2026-02-20` (YYYY-MM-DD)
- `02/20/2026` (MM/DD/YYYY)
- `20/02/2026` (DD/MM/YYYY)
- `Feb 20, 2026`
- Excel date numbers

### Numeric Formats
- Numbers with commas: `1,234.56`
- Numbers with currency symbols: `$1234.56`
- Plain numbers: `1234.56`

### Missing Data Handling
- Empty cells in outage columns default to 0
- Rows with missing dates are skipped
- Rows with missing unit numbers are skipped
- Invalid data is automatically cleaned

### Data Validation
- Negative values are automatically set to 0
- Hours outside 0-24 range are capped
- Invalid dates are reported but don't stop the import

## Example Layouts

### Layout 1: Standard Format
```
date        | unit | generation_kwh | operating_hours | ...
2026-02-20  | 1    | 540000        | 22.5           | ...
```

### Layout 2: With Title Row
```
National Power Corporation - Generation Report

date        | unit_number | gen_kwh | op_hours | ...
2026-02-20  | 1          | 540000  | 22.5     | ...
```

### Layout 3: Different Column Names
```
report_date | unitno | energy | runtime | avail_hours | ...
02/20/2026  | 1      | 540000 | 22.5    | 23.0       | ...
```

All three layouts above will work!

## Tips for Best Results

1. **Use clear column headers** - Include at least the required column names
2. **Keep data together** - Don't have large gaps between rows
3. **One plant per file** - Each file should contain data for one plant only
4. **Consistent units** - Use the correct unit numbers for your plant
5. **Valid dates** - Use recognizable date formats

## What Gets Imported

For each row, the system imports:
- Report date
- Unit number
- Generation in kWh
- Operating hours
- Availability hours
- Forced outage hours (optional, defaults to 0)
- Scheduled outage hours (optional, defaults to 0)
- Remarks (optional)

## Error Handling

The system is forgiving:
- Skips invalid rows instead of failing completely
- Shows warnings for data issues
- Imports all valid rows even if some rows have errors
- Provides detailed error messages for troubleshooting

## Need Help?

If your file isn't importing:
1. Check that you have the required columns (date, unit_number, generation_kwh, operating_hours, availability_hours)
2. Verify your unit numbers match the plant's units
3. Ensure dates are in a recognizable format
4. Check the error messages for specific issues
