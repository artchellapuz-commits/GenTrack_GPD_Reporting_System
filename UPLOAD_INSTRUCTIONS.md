# Excel Upload Instructions

## ✓ System is Ready!

Both servers are running:
- Backend: http://localhost:8000
- Frontend: http://localhost:8080 or http://192.168.120.87:8080

## Required Excel Format

Your Excel file MUST have these exact columns (case-insensitive):

1. **Date** - Format: YYYY-MM-DD (e.g., 2026-02-01)
2. **Unit Number** - Integer (e.g., 1, 2, 3, 4)
3. **Generation kWh** - Number (e.g., 21000)
4. **Operating Hours** - Number (e.g., 22)
5. **Availability Hours** - Number (e.g., 24)
6. **Forced Outage Hours** - Number (e.g., 0)
7. **Scheduled Outage Hours** - Number (e.g., 0)

## Sample File

A correct sample file has been created: **CORRECT_SAMPLE_AGUS1.xlsx**

This file contains:
- 40 records (10 days × 4 units)
- Correct column names
- Valid data format
- Ready to upload for AGUS1 plant

## How to Upload

1. Open http://192.168.120.87:8080 in your browser
2. Click "Upload" in the navigation
3. Select a plant (e.g., AGUS1)
4. Choose the Excel file (CORRECT_SAMPLE_AGUS1.xlsx)
5. Click "Upload Report"

## Hover Effect

When you click the plant dropdown and move your mouse over any plant option, you will see:
- **Light blue background** (#d4e3f7)
- **Thick blue left border** (5px)
- **Bold plant name** in blue color
- **Subtle shadow effect**

## Troubleshooting

If you get an error about missing columns:
- Check that your Excel file has ALL 7 required columns
- Column names can have spaces or underscores (both work)
- Make sure there's no extra title row at the top
- The system will automatically skip title rows like "National Power Corporation"

## What Happens After Upload

1. File is validated
2. Data is imported into the database
3. Success message shows number of records imported
4. Upload history table is updated
5. You can view the data in "Reports" section
