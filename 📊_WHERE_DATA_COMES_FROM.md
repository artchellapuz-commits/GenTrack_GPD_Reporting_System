# 📊 Where Automated Reports Data Comes From

## Quick Answer

**Automated reports pull data from the `GenerationReport` table in your database.**

This is the same data you see in:
- Dashboard
- View Reports page
- Generate Reports page
- Charts and analytics

---

## Data Flow Diagram

```
┌─────────────────────────────────────────────────────────┐
│                    DATA SOURCE                          │
└─────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────┐
│  1. Upload Excel Files (Upload Excel page)             │
│     - User uploads daily generation data                │
│     - System parses Excel file                          │
│     - Data saved to database                            │
└─────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────┐
│  2. Database (SQLite/PostgreSQL)                        │
│     Table: GenerationReport                             │
│     - report_date                                       │
│     - plant (AGUS1, AGUS2, etc.)                       │
│     - unit (Unit 1, Unit 2, etc.)                      │
│     - generation_kwh                                    │
│     - operating_hours                                   │
│     - capacity_factor                                   │
│     - availability_factor                               │
│     - forced_outage_hours                               │
│     - scheduled_outage_hours                            │
└─────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────┐
│  3. Automated Reports Service                           │
│     When "Run Now" clicked:                             │
│     - Queries last 30 days of data                      │
│     - Filters by selected plants                        │
│     - Aggregates based on report type                   │
│     - Creates Excel file                                │
└─────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────┐
│  4. Excel Report Output                                 │
│     - GENERATION_SUMMARY_*.xlsx                         │
│     - CAPACITY_FACTOR_*.xlsx                            │
│     - AVAILABILITY_*.xlsx                               │
│     - PERFORMANCE_METRICS_*.xlsx                        │
└─────────────────────────────────────────────────────────┘
```

---

## Detailed Explanation

### 1. Data Entry

Data enters the system through:

**A. Upload Excel Feature**
- Go to: http://localhost:8080/upload
- Upload Excel files with generation data
- System parses and saves to database

**B. Manual Entry** (if implemented)
- Direct data entry forms
- API imports
- Bulk imports

**C. Historical Data Import**
- Import past data from Excel files
- Use `IMPORT_HISTORICAL_DATA.bat`
- Loads years of historical data

### 2. Database Storage

Data is stored in the `GenerationReport` model:

```python
class GenerationReport(models.Model):
    report_date = models.DateField()
    plant = models.ForeignKey(Plant)
    unit = models.ForeignKey(Unit)
    generation_kwh = models.DecimalField()
    operating_hours = models.DecimalField()
    capacity_factor = models.DecimalField()
    availability_factor = models.DecimalField()
    forced_outage_hours = models.DecimalField()
    scheduled_outage_hours = models.DecimalField()
    # ... more fields
```

### 3. Report Generation

When you click "Run Now", the system:

**Step 1: Query Database**
```python
# Get last 30 days of data
end_date = timezone.now().date()
start_date = end_date - timedelta(days=30)

reports = GenerationReport.objects.filter(
    plant__in=selected_plants,
    report_date__range=[start_date, end_date]
)
```

**Step 2: Process Data**
- Filters by date range (default: last 30 days)
- Filters by selected plants (or all plants)
- Aggregates based on report type
- Calculates totals and averages

**Step 3: Create Excel File**
- Formats data into Excel
- Adds headers and styling
- Saves to `media/automated_reports/`

---

## Report Types & Data Sources

### 1. Generation Summary
**Data Source:** `GenerationReport` table

**Queries:**
```python
GenerationReport.objects.filter(
    plant__in=plants,
    report_date__range=[start_date, end_date]
).select_related('plant', 'unit')
```

**Output Columns:**
- Date
- Plant
- Unit
- Generation (kWh)
- Operating Hours
- Capacity Factor (%)
- Availability Factor (%)

### 2. Capacity Factor Analysis
**Data Source:** `GenerationReport` table (aggregated)

**Queries:**
```python
GenerationReport.objects.filter(
    plant=plant,
    report_date__range=[start_date, end_date]
).aggregate(
    avg_capacity_factor=Avg('capacity_factor'),
    total_generation=Sum('generation_kwh'),
    avg_operating_hours=Avg('operating_hours')
)
```

**Output Columns:**
- Plant
- Average Capacity Factor (%)
- Total Generation (MWh)
- Average Operating Hours

### 3. Availability Report
**Data Source:** `GenerationReport` table (aggregated)

**Queries:**
```python
GenerationReport.objects.filter(
    plant=plant,
    report_date__range=[start_date, end_date]
).aggregate(
    avg_availability=Avg('availability_factor'),
    total_forced_outage=Sum('forced_outage_hours'),
    total_scheduled_outage=Sum('scheduled_outage_hours')
)
```

**Output Columns:**
- Plant
- Average Availability (%)
- Total Forced Outage Hours
- Total Scheduled Outage Hours

### 4. Performance Metrics
**Data Source:** `GenerationReport` table (comprehensive aggregation)

**Queries:**
```python
GenerationReport.objects.filter(
    plant=plant,
    report_date__range=[start_date, end_date]
).aggregate(
    avg_capacity_factor=Avg('capacity_factor'),
    avg_availability=Avg('availability_factor'),
    total_generation=Sum('generation_kwh'),
    total_operating_hours=Sum('operating_hours'),
    report_count=Count('id')
)
```

**Output Columns:**
- Plant
- Capacity (MW)
- Average Capacity Factor (%)
- Average Availability (%)
- Total Generation (MWh)
- Total Operating Hours
- Days Reported

---

## Date Range

**Default:** Last 30 days from today

**Configurable:** When creating scheduled report, you can set:
- `date_range_days` = 7 (last week)
- `date_range_days` = 30 (last month)
- `date_range_days` = 90 (last quarter)
- `date_range_days` = 365 (last year)

**Example:**
```
Today: February 20, 2026
Date Range: 30 days
Start Date: January 21, 2026
End Date: February 20, 2026

Report includes all data from Jan 21 to Feb 20
```

---

## Plant Selection

**Default:** All active plants

**Configurable:** When creating scheduled report, you can select specific plants:
- AGUS1
- AGUS2
- AGUS3
- AGUS4
- AGUS5
- AGUS6
- AGUS7
- PULANGI4

**Example:**
```python
# All plants
plants = Plant.objects.filter(is_active=True)

# Specific plants
plants = scheduled_report.plants.all()
```

---

## Data Requirements

For reports to have data, you need:

1. **Plants in Database**
   - At least one active plant
   - Check: Dashboard shows plants

2. **Generation Data**
   - Upload Excel files with generation data
   - Or import historical data
   - Check: View Reports page shows data

3. **Date Range with Data**
   - Data must exist within the date range
   - Default is last 30 days
   - Check: Dashboard shows recent data

---

## How to Check Your Data

### Method 1: Dashboard
- Go to: http://localhost:8080/dashboard
- See current generation data
- Check if plants are showing

### Method 2: View Reports
- Go to: http://localhost:8080/reports
- Filter by date range
- See all generation reports

### Method 3: Database Query
```bash
cd backend
python manage.py shell

from reports.models import GenerationReport
print(f"Total reports: {GenerationReport.objects.count()}")
print(f"Date range: {GenerationReport.objects.earliest('report_date').report_date} to {GenerationReport.objects.latest('report_date').report_date}")
```

### Method 4: Backend Console
When you click "Run Now", check backend console:
```
[INFO] Starting report execution: Daily Generation Summary Report
[INFO] Generated 120 records  ← This shows how many records found
[INFO] Created report file: ...
```

---

## If No Data Shows in Reports

### Problem: "0 records processed"

**Cause:** No data in database for the date range

**Solutions:**

1. **Upload Data**
   - Go to: http://localhost:8080/upload
   - Upload Excel files with generation data
   - Try "Run Now" again

2. **Import Historical Data**
   - Run: `IMPORT_HISTORICAL_DATA.bat`
   - Loads sample data for testing
   - Try "Run Now" again

3. **Check Date Range**
   - Default is last 30 days
   - Your data might be older
   - Increase `date_range_days` to 90 or 365

4. **Check Plants**
   - Make sure plants are active
   - Check plant selection in scheduled report
   - Try "All plants" option

---

## Data Freshness

**Real-time:** Reports use current database data

**When you upload new data:**
1. Upload Excel file
2. Data saved to database immediately
3. Next "Run Now" includes new data
4. No cache or delay

**Example:**
```
9:00 AM - Upload today's data
9:01 AM - Click "Run Now"
9:01 AM - Report includes today's data ✅
```

---

## Summary

| Question | Answer |
|----------|--------|
| Where does data come from? | `GenerationReport` table in database |
| How does data get there? | Upload Excel files or import historical data |
| What date range? | Last 30 days (configurable) |
| Which plants? | All active plants (configurable) |
| How fresh is data? | Real-time from database |
| What if no data? | Upload data first, then run report |

**The automated reports use the exact same data you see everywhere else in the system!**
