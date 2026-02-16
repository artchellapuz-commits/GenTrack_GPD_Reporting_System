# Export Feature Guide

## Overview
The dashboard now includes comprehensive export functionality that allows users to export plant data, comparison data, and overall dashboard statistics in multiple formats.

## Export Options

### 1. Export Individual Plant Data
Export detailed generation data for a specific plant.

**How to Use:**
1. Navigate to the Dashboard
2. Find the plant card you want to export
3. Click the "Export" button on the plant card
4. The system will attempt to export as Excel (.xlsx) first
5. If Excel export fails, it automatically falls back to CSV format
6. File downloads automatically

**Export Includes:**
- Plant information (name, code, capacity)
- Summary statistics (total generation, avg capacity factor, avg availability)
- Detailed generation data (date, unit, generation, operating hours, capacity factor, availability, remarks)
- Summary by unit (aggregated data per unit)
- Date range of data

**File Naming:**
- Excel: `{PLANT_CODE}_export_{DATE}.xlsx`
- CSV: `{PLANT_CODE}_export_{DATE}.csv`

**Example:** `AGUS1_export_2026-02-16.xlsx`

### 2. Export Plant Comparison
Export comparison data for selected plants.

**How to Use:**
1. Enter comparison mode by clicking "Compare Plants"
2. Select 2-4 plants to compare
3. Click "View Comparison" to open the comparison modal
4. Click "Export Comparison" button in the modal footer
5. CSV file downloads automatically

**Export Includes:**
- Plant codes
- Installed capacity (MW)
- Total generation (kWh)
- Capacity factor (%)
- Availability factor (%)

**File Naming:** `plant-comparison-{DATE}.csv`

**Example:** `plant-comparison-2026-02-16.csv`

### 3. Export Entire Dashboard
Export all dashboard data including overall statistics and all plants.

**How to Use:**
1. Click "Export Dashboard" button in the page header
2. CSV file downloads automatically

**Export Includes:**
- Overall statistics (total generation, avg capacity factor, avg availability, total operating hours)
- All plants summary (name, code, capacity, generation, capacity factor, availability, status)

**File Naming:** `dashboard_export_{DATE}.csv`

**Example:** `dashboard_export_2026-02-16.csv`

## Export Formats

### Excel Format (.xlsx)
- Professional formatting
- Multiple sheets possible
- Compatible with Microsoft Excel, Google Sheets, LibreOffice
- Best for: Detailed analysis, presentations, reports

**When Used:**
- Individual plant exports (primary format)
- Generated using backend API

### CSV Format (.csv)
- Universal compatibility
- Plain text format
- Opens in any spreadsheet software
- Best for: Data import, backup, simple analysis

**When Used:**
- Comparison exports
- Dashboard exports
- Fallback for plant exports if Excel fails

## Data Format Details

### Plant Export CSV Structure

```
Plant Export Report
Generated: [Date and Time]

PLANT INFORMATION
Name,[Plant Name]
Code,[Plant Code]
Capacity,[Capacity] MW

SUMMARY STATISTICS
Total Generation,[Value] kWh
Average Capacity Factor,[Value]%
Average Availability,[Value]%
Total Records,[Count]
Date Range,[Start Date] to [End Date]

DETAILED GENERATION DATA
Date,Unit,Generation (kWh),Operating Hours,Capacity Factor (%),Availability Factor (%),Remarks
[Data rows...]

SUMMARY BY UNIT
Unit,Total Generation (kWh),Total Operating Hours,Number of Records
[Summary rows...]
```

### Comparison Export CSV Structure

```
Metric,Plant 1 Name,Plant 2 Name,...
Code,CODE1,CODE2,...
Capacity (MW),255,200,...
Generation (kWh),1234567.89,987654.32,...
Capacity Factor (%),85.50,78.25,...
Availability (%),92.00,88.50,...
```

### Dashboard Export CSV Structure

```
NPC Reporting System - Dashboard Export
Generated: [Date and Time]

OVERALL STATISTICS
Total Generation,[Value] kWh
Average Capacity Factor,[Value]%
Average Availability,[Value]%
Total Operating Hours,[Value] hrs

PLANTS SUMMARY
Plant Name,Code,Capacity (MW),Generation (kWh),Capacity Factor (%),Availability (%),Status
[Plant rows...]
```

## Features

### Smart Export
- **Automatic Format Selection**: Tries Excel first, falls back to CSV
- **Error Handling**: Graceful fallback if export fails
- **Loading States**: Visual feedback during export
- **Validation**: Checks for data availability before export

### Data Quality
- **Proper CSV Escaping**: Handles commas, quotes, and newlines in data
- **Number Formatting**: Consistent 2 decimal places
- **Date Formatting**: Standard YYYY-MM-DD format
- **Sorted Data**: Reports sorted by date for easy analysis

### User Experience
- **One-Click Export**: Simple button click to export
- **Automatic Download**: No additional steps required
- **Clear Naming**: Descriptive filenames with dates
- **Status Indicators**: Loading spinner during export

## Technical Details

### Export Utilities
Location: `frontend/src/utils/exportUtils.js`

**Functions:**
- `exportPlantToCSV()` - Export plant data to CSV
- `exportComparisonToCSV()` - Export comparison to CSV
- `exportDashboardToCSV()` - Export dashboard to CSV
- `downloadCSV()` - Download CSV file
- `downloadBlob()` - Download blob file (Excel)
- `formatDate()` - Format date to YYYY-MM-DD
- `formatNumber()` - Format number with 2 decimals
- `escapeCSVField()` - Properly escape CSV fields

### API Integration
- Uses existing `generateReport()` API for Excel exports
- Uses `getGenerationReports()` API for fetching plant data
- Automatic date range detection from available data

### Browser Compatibility
- Works in all modern browsers
- Uses standard Blob API for downloads
- No external dependencies required

## Tips & Best Practices

### For Plant Exports
1. **Regular Backups**: Export plant data regularly for backup
2. **Before Analysis**: Export before doing detailed analysis in Excel
3. **Date Range**: Check the date range in the export to ensure completeness
4. **Unit Summary**: Use the unit summary section for quick insights

### For Comparisons
1. **Similar Plants**: Compare plants of similar capacity for meaningful insights
2. **Multiple Comparisons**: Export different combinations for various analyses
3. **Trend Analysis**: Export comparisons at different times to track trends

### For Dashboard Exports
1. **Monthly Reports**: Export dashboard data monthly for records
2. **Management Reports**: Use for executive summaries
3. **Quick Overview**: Good for sharing overall system status

## Troubleshooting

### Export Button Not Working
- Check if plant has data (only plants with data can be exported)
- Ensure you're logged in
- Check browser console for errors
- Try refreshing the page

### Excel Export Fails
- System automatically falls back to CSV
- CSV contains the same data, just different format
- Check backend server is running
- Verify API endpoint is accessible

### CSV Opens Incorrectly in Excel
- Use "Data > From Text/CSV" in Excel instead of double-clicking
- Specify UTF-8 encoding if prompted
- Check delimiter is set to comma

### Missing Data in Export
- Verify data exists in the dashboard view
- Refresh dashboard before exporting
- Check date filters if any are applied

## Future Enhancements

Planned improvements:
- PDF export with charts and graphs
- Custom date range selection for exports
- Scheduled automatic exports
- Email export functionality
- Export templates customization
- Batch export for multiple plants
- Export history and management

## Support

For issues or questions about the export feature:
1. Check this guide first
2. Verify data exists in dashboard
3. Check browser console for errors
4. Contact system administrator if issues persist
