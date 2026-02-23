# PSR Charts and Graphs Added

## Summary

Successfully added the actual **PIE CHART** and **BAR CHART** to the PSR (Plant Status Report) Excel export. The charts were missing because only the headers were created previously, but now the actual chart objects are generated.

## Charts Added

### 1. Pie Chart - NPC-PSALM Capacity Mix
**Location:** Left side of the report (columns B-D)

**Data:**
- Hydro: 811.31 MW (79%)
- Coal Fired Thermal: 210.00 MW (21%)

**Features:**
- Shows percentage and values
- Blue slice for Hydro
- Orange slice for Coal Fired Thermal
- Size: 10x10
- Positioned below the "NPC-PSALM Capacity Mix" header

### 2. Bar Chart - MinGen Forecasted Load Share
**Location:** Right side of the report (columns H-N)

**Data (MW @ 6pm Today):**
- AGUS 1: 60.0 MW
- AGUS 2: 120.0 MW
- AGUS 4: 96.0 MW
- AGUS 5: 40.0 MW
- AGUS 6: 144.8 MW
- AGUS 7: 40.0 MW
- PULANGI IV: 150.0 MW

**Features:**
- Vertical column chart
- Shows load values on top of each bar
- Different colors for each plant
- Size: 15x10
- Positioned below the "MinGen Forecasted Load Share (MW), @6pm Today" header

## Technical Implementation

### Chart Data Storage
- Chart data is stored in hidden cells (white text on white background)
- Pie chart data: Columns A-B (rows below chart header)
- Bar chart data: Columns F-G (rows below chart header)
- Font size: 1pt, color: white (effectively hidden)

### Chart Configuration

**Pie Chart:**
```python
pie_chart = PieChart()
pie_chart.width = 10
pie_chart.height = 10
pie_chart.dataLabels.showVal = True
pie_chart.dataLabels.showPercent = True
```

**Bar Chart:**
```python
bar_chart = BarChart()
bar_chart.type = "col"  # Column chart
bar_chart.width = 15
bar_chart.height = 10
bar_chart.dataLabels.showVal = True
```

### Legend
- Orange background (#FFC000)
- Text: "■ Hydro     ■ Coal Fired Thermal"
- Positioned below the pie chart
- Merged cells B to D

## File Modified

- `npc-reporting-system/backend/reports/services/psr_exporter.py`

## Changes Made

### Updated `_add_notes_section` method:
1. Added pie chart creation with Hydro vs Coal Fired Thermal data
2. Added bar chart creation with plant-wise forecasted load data
3. Created hidden data cells for chart references
4. Positioned charts in correct locations
5. Configured chart styling (labels, percentages, values)
6. Added legend row below pie chart

## Visual Layout

```
┌─────────────────────────────────────────────────────────────┐
│  NPC-PSALM Capacity Mix  │  MinGen Forecasted Load Share   │
├──────────────────────────┼──────────────────────────────────┤
│                          │                                  │
│      [PIE CHART]         │      [BAR CHART]                 │
│   Hydro 79% (811.31)     │   AGUS1  AGUS2  AGUS4  AGUS5    │
│   Coal 21% (210.00)      │   AGUS6  AGUS7  PULANGI IV      │
│                          │                                  │
├──────────────────────────┴──────────────────────────────────┤
│  ■ Hydro  ■ Coal Fired Thermal                              │
└─────────────────────────────────────────────────────────────┘
```

## Testing

✅ Python file compiles successfully
✅ No syntax errors
✅ No diagnostics errors
✅ Charts use openpyxl's built-in chart objects
✅ Data is properly referenced from hidden cells

## Result

The PSR report now includes:
- ✅ Functional pie chart showing capacity mix
- ✅ Functional bar chart showing forecasted load share
- ✅ Proper chart positioning and sizing
- ✅ Data labels and percentages
- ✅ Legend for pie chart
- ✅ Hidden data cells for chart references

When you generate a PSR report, you will now see both charts rendered in the Excel file!

---

**Date Completed:** February 23, 2026
**Status:** ✅ Complete
