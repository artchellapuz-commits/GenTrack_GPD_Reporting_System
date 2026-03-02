# Sample Excel Data Files for NPC Reporting System

This directory contains sample Excel files for testing the upload functionality of the NPC Reporting System.

## Generated Files

- `AGUS1_Sample_Report.xlsx` - Agus 1 Hydroelectric Power Plant (4 units, 30 MW each)
- `AGUS2_Sample_Report.xlsx` - Agus 2 Hydroelectric Power Plant (2 units, 25 MW each)
- `AGUS4_Sample_Report.xlsx` - Agus 4 Hydroelectric Power Plant (2 units, 50 MW each)
- `AGUS5_Sample_Report.xlsx` - Agus 5 Hydroelectric Power Plant (2 units, 50 MW each)
- `AGUS6_Sample_Report.xlsx` - Agus 6 Hydroelectric Power Plant (4 units, 50 MW each)
- `AGUS7_Sample_Report.xlsx` - Agus 7 Hydroelectric Power Plant (4 units, 51.3 MW each)
- `PULANGI4_Sample_Report.xlsx` - Pulangi 4 Hydroelectric Power Plant (4 units, 70 MW each)

## File Format

Each Excel file contains the following columns:

| Column Name | Type | Description |
|------------|------|-------------|
| date | Date | Report date (YYYY-MM-DD format) |
| unit_number | Integer | Unit number within the plant |
| generation_kwh | Float | Total generation in kWh |
| operating_hours | Float | Hours the unit was operating (0-24) |
| availability_hours | Float | Hours the unit was available (0-24) |
| forced_outage_hours | Float | Hours of forced outage (0-24) |
| scheduled_outage_hours | Float | Hours of scheduled outage (0-24) |
| remarks | String | Optional remarks or notes |

## How to Use

1. Navigate to the Upload Excel Report page in the web application
2. Select the appropriate plant from the dropdown
3. Upload the corresponding Excel file
4. The system will validate and import the data

## Regenerating Sample Files

To regenerate the sample files with new data, run:

```bash
python generate_sample_excel.py
```

This will create 30 days of sample data for each plant with realistic operational values.
