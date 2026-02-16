# Pulangi 4 Upload Guide

## Excel File Format for Pulangi 4

Pulangi 4 has **3 units** (not 4 like most Agus plants), so your Excel file must have data for exactly 3 units.

### Required Columns

Your Excel file MUST have these columns (exact names, case-insensitive):

1. **Date** - Format: YYYY-MM-DD (e.g., 2026-02-13)
2. **Unit Number** - Values: 1, 2, or 3
3. **Generation kWh** - Numeric value (e.g., 1800000)
4. **Operating Hours** - Numeric value 0-24 (e.g., 22.5)
5. **Availability Hours** - Numeric value 0-24 (e.g., 23.0)
6. **Forced Outage Hours** - Numeric value 0-24 (e.g., 0.5)
7. **Scheduled Outage Hours** - Numeric value 0-24 (e.g., 0.5)
8. **Remarks** (Optional) - Text

### Sample Data Structure

```
| Date       | Unit Number | Generation kWh | Operating Hours | Availability Hours | Forced Outage Hours | Scheduled Outage Hours | Remarks          |
|------------|-------------|----------------|-----------------|--------------------|--------------------|------------------------|------------------|
| 2026-02-13 | 1           | 1800000        | 22.5            | 23.0               | 0.5                | 0.5                    | Normal operation |
| 2026-02-13 | 2           | 1850000        | 23.0            | 23.5               | 0.5                | 0.0                    | Normal operation |
| 2026-02-13 | 3           | 1900000        | 23.5            | 24.0               | 0.0                | 0.0                    | Normal operation |
```

### Unit Specifications

- **Unit 1**: 85 MW capacity
- **Unit 2**: 85 MW capacity
- **Unit 3**: 85 MW capacity
- **Total Plant Capacity**: 255 MW

### Common Errors and Solutions

#### Error: "Upload failed"

**Possible Causes:**

1. **Wrong number of units**
   - ❌ Your file has 4 units (like Agus plants)
   - ✅ Pulangi 4 needs exactly 3 units
   - **Solution**: Remove Unit 4 data from your Excel file

2. **Missing required columns**
   - Check that all 7 required columns are present
   - Column names must match exactly (case-insensitive)
   - **Solution**: Use the sample file `SAMPLE_PULANGI4.xlsx` as a template

3. **Invalid date format**
   - ❌ Wrong: 02/13/2026, 13-Feb-2026
   - ✅ Correct: 2026-02-13
   - **Solution**: Format dates as YYYY-MM-DD

4. **Invalid numeric values**
   - Hours must be between 0 and 24
   - Generation must be positive numbers
   - **Solution**: Check all numeric values are valid

5. **Unit numbers out of range**
   - ❌ Wrong: Unit 0, Unit 4, Unit 5
   - ✅ Correct: Unit 1, 2, or 3 only
   - **Solution**: Ensure unit numbers are 1, 2, or 3

#### Error: "Unit X not found for plant PULANGI4"

**Cause**: Your Excel file references a unit that doesn't exist

**Solution**: 
- Pulangi 4 only has 3 units
- Check your Excel file only has Unit 1, 2, and 3
- Remove any references to Unit 4 or higher

#### Error: "Missing required columns"

**Cause**: Excel file is missing one or more required columns

**Solution**:
1. Open `SAMPLE_PULANGI4.xlsx` to see the correct format
2. Ensure your file has all 7 required columns
3. Check column names match exactly (spaces, hyphens, etc.)

### Using the Sample File

A sample Excel file has been created for you: `SAMPLE_PULANGI4.xlsx`

**To use it:**
1. Open `SAMPLE_PULANGI4.xlsx`
2. Replace the sample data with your actual data
3. Keep the same column structure
4. Save the file
5. Upload to the system

**Or create your own:**
1. Run `python CREATE_PULANGI4_SAMPLE.py` to generate a new sample
2. Modify the generated file with your data
3. Upload to the system

### Step-by-Step Upload Process

1. **Prepare Your Excel File**
   - Ensure it has 3 units only
   - Check all required columns are present
   - Verify date format is YYYY-MM-DD
   - Confirm all numeric values are valid

2. **Upload to System**
   - Go to "Upload Excel" page
   - Select "Pulangi 4 Hydroelectric Plant" from dropdown
   - Choose your Excel file
   - Click "Upload Report"

3. **Verify Upload**
   - Check for success message
   - Go to Dashboard to see Pulangi 4 data
   - Go to "View Reports" and filter by Pulangi 4

### Troubleshooting Checklist

Before uploading, verify:

- [ ] Excel file has exactly 3 units (not 4)
- [ ] All 7 required columns are present
- [ ] Column names match the required format
- [ ] Dates are in YYYY-MM-DD format
- [ ] All hours are between 0 and 24
- [ ] All generation values are positive
- [ ] Unit numbers are 1, 2, or 3 only
- [ ] No empty cells in required columns
- [ ] File is saved as .xlsx format

### Getting Help

If you still encounter errors:

1. **Check Backend Logs**
   - Look at the terminal where backend is running
   - Error messages will show the specific problem

2. **Use Sample File**
   - Start with `SAMPLE_PULANGI4.xlsx`
   - If sample works, compare with your file

3. **Verify Plant Installation**
   - Run: `python backend/add_pulangi4.py`
   - Ensure Pulangi 4 has 3 units created

4. **Check Browser Console**
   - Open Developer Tools (F12)
   - Look for error messages in Console tab

### Example: Converting Agus Format to Pulangi 4

If you have an Agus plant Excel file (4 units), convert it for Pulangi 4:

**Agus Format (4 units):**
```
Date       | Unit 1 | Unit 2 | Unit 3 | Unit 4
2026-02-13 | ...    | ...    | ...    | ...
```

**Pulangi 4 Format (3 units):**
```
Date       | Unit 1 | Unit 2 | Unit 3
2026-02-13 | ...    | ...    | ...
```

**Steps:**
1. Remove all Unit 4 columns/data
2. Keep only Unit 1, 2, and 3
3. Adjust capacity calculations if needed (85 MW per unit)
4. Save and upload

---

**Need the sample file?** Run: `python CREATE_PULANGI4_SAMPLE.py`

**Questions?** Check the backend terminal for detailed error messages.
