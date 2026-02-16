# Plant Comparison Feature Guide

## Overview
The dashboard now includes a fully functional plant comparison feature that allows users to compare performance metrics across multiple plants side-by-side.

## Features

### 1. Comparison Mode
- Click "Compare Plants" button in the filter controls to enter comparison mode
- Select 2-4 plants by clicking on their cards
- Selected plants are highlighted with a blue border and checkmark
- A comparison bar shows how many plants are selected

### 2. Visual Comparison Modal
Once you've selected plants, click "View Comparison" to see:

**Comparison Grid:**
- Side-by-side metrics table
- Plant name, code, capacity
- Generation, capacity factor, availability
- Color-coded progress bars
- Status indicators

**Comparison Charts:**
- Generation comparison bar chart
- Capacity factor comparison bar chart
- Color-coded bars based on performance levels
- Visual representation of relative performance

### 3. Export Functionality
- Export comparison data to CSV format
- Includes all metrics for selected plants
- Filename includes date stamp
- Easy to share and analyze in Excel

## How to Use

### Step 1: Enter Comparison Mode
1. Navigate to the Dashboard
2. Click the "Compare Plants" button in the filter controls
3. The button will turn blue and plant cards become selectable

### Step 2: Select Plants
1. Click on 2-4 plant cards that have data
2. Selected plants show a blue border and checkmark icon
3. The comparison bar shows your selection count

### Step 3: View Comparison
1. Click "View Comparison" button (enabled when 2+ plants selected)
2. A modal opens with detailed comparison
3. Review metrics in table and chart format

### Step 4: Export (Optional)
1. Click "Export Comparison" in the modal footer
2. CSV file downloads automatically
3. Open in Excel or other spreadsheet software

### Step 5: Exit Comparison Mode
- Click "Cancel" in the comparison bar, or
- Click "Cancel Compare" button in filter controls
- Selection is cleared and normal mode resumes

## Visual Indicators

### Progress Bar Colors
- **Green** (≥80%): Excellent performance
- **Blue** (≥60%): Good performance
- **Yellow** (≥40%): Fair performance
- **Red** (<40%): Needs attention

### Status Badges
- **Active** (Green): Plant has data and is operational
- **No Data** (Gray): No data uploaded for this plant

## Tips

1. **Compare Similar Plants**: Compare plants of similar capacity for meaningful insights
2. **Use Filters**: Use search and sort before entering comparison mode
3. **Export for Reports**: Export comparison data for presentations and reports
4. **Multiple Comparisons**: Exit and re-enter comparison mode to compare different sets

## Technical Details

### Data Included in Comparison
- Plant name and code
- Installed capacity (MW)
- Total generation (kWh)
- Average capacity factor (%)
- Average availability factor (%)
- Operational status

### Export Format
CSV file with columns:
- Metric name
- Values for each selected plant
- Includes all comparison metrics

## Limitations
- Maximum 4 plants can be compared at once
- Only plants with uploaded data can be compared
- Comparison uses current dashboard data (refresh for latest)

## Future Enhancements
- Historical trend comparison
- Custom date range selection
- PDF export with charts
- Save comparison presets
- Email comparison reports
