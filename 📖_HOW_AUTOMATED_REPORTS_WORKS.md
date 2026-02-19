# 📖 How Automated Reports Works

## Overview

Automated Reports is a scheduling system that automatically generates and distributes reports at specified intervals without manual intervention. It saves time and ensures stakeholders receive timely updates.

---

## 🎯 Key Concepts

### 1. Scheduled Report
A configuration that defines:
- **What** report to generate (type)
- **When** to generate it (frequency + time)
- **How** to deliver it (format)
- **Who** receives it (recipients)

### 2. Report Execution
Each time a scheduled report runs, it creates an execution record tracking:
- When it ran
- Whether it succeeded or failed
- Where the generated file is stored
- Any errors that occurred

---

## 🔄 How It Works (Step-by-Step)

### Step 1: User Creates a Schedule

**Via Frontend** (`/scheduled-reports`):
1. User clicks "Schedule New Report"
2. Fills out the form:
   - **Name**: "Daily Generation Report"
   - **Type**: Generation Summary, Capacity Factor, etc.
   - **Frequency**: Daily, Weekly, Monthly, Quarterly
   - **Time**: "08:00" (when to run)
   - **Format**: PDF, Excel, or Both
   - **Date Range**: Last 30 days of data
3. Clicks "Create Report"

**Backend Processing**:
```python
# Creates ScheduledReport in database
ScheduledReport.objects.create(
    name="Daily Generation Report",
    report_type="GENERATION_SUMMARY",
    frequency="DAILY",
    schedule_time="08:00",
    format="EXCEL",
    date_range_days=30,
    status="ACTIVE",
    next_run=calculate_next_run()  # Tomorrow at 8 AM
)
```

### Step 2: Scheduler Runs (Background Process)

**Management Command** (`run_scheduled_reports.py`):
```bash
# Runs every minute via cron job or task scheduler
python manage.py run_scheduled_reports
```

**What It Does**:
1. Finds all ACTIVE reports where `next_run <= now()`
2. For each report:
   - Generates the report
   - Saves to file system
   - Sends email to recipients
   - Updates `next_run` to next scheduled time
   - Creates execution record

### Step 3: Report Generation

**Automated Reports Service** (`automated_reports.py`):
```python
def generate_report(scheduled_report):
    # 1. Fetch data based on report type
    if report_type == "GENERATION_SUMMARY":
        data = get_generation_data(date_range)
    
    # 2. Generate file(s)
    if format == "EXCEL":
        file = create_excel_report(data)
    elif format == "PDF":
        file = create_pdf_report(data)
    
    # 3. Save to media/automated_reports/
    file_path = save_report_file(file)
    
    # 4. Send email with attachment
    send_email_with_report(recipients, file_path)
    
    # 5. Record execution
    ReportExecution.objects.create(
        scheduled_report=scheduled_report,
        status="SUCCESS",
        file_path=file_path
    )
```

### Step 4: Email Delivery

**Email Service** (`email_service.py`):
```python
def send_report_email(recipients, report_file):
    subject = f"Automated Report: {report_name}"
    body = f"""
    Your scheduled report is ready.
    
    Report: {report_name}
    Generated: {datetime.now()}
    Period: Last {date_range_days} days
    
    Please find the report attached.
    """
    
    # Attach file and send
    send_email_with_attachment(
        to=recipients,
        subject=subject,
        body=body,
        attachment=report_file
    )
```

---

## 📊 Database Structure

### ScheduledReport Model
```python
class ScheduledReport(models.Model):
    name = CharField()                    # "Daily Generation Report"
    report_type = CharField()             # GENERATION_SUMMARY, CAPACITY_FACTOR, etc.
    frequency = CharField()               # DAILY, WEEKLY, MONTHLY, QUARTERLY
    schedule_time = TimeField()           # 08:00
    format = CharField()                  # PDF, EXCEL, BOTH
    date_range_days = IntegerField()      # 30
    status = CharField()                  # ACTIVE, PAUSED, COMPLETED
    next_run = DateTimeField()            # 2026-02-20 08:00:00
    created_by = ForeignKey(User)
    recipients = JSONField()              # ["user1@email.com", "user2@email.com"]
```

### ReportExecution Model
```python
class ReportExecution(models.Model):
    scheduled_report = ForeignKey(ScheduledReport)
    executed_at = DateTimeField()         # When it ran
    status = CharField()                  # SUCCESS, FAILED
    file_path = CharField()               # /media/automated_reports/report_123.xlsx
    error_message = TextField()           # If failed
    execution_time = FloatField()         # How long it took (seconds)
```

---

## 🎨 Frontend Features

### Main Page (`/scheduled-reports`)

**Report Cards Display**:
```
┌─────────────────────────────────────────────┐
│ Daily Generation Report          [ACTIVE]   │
│ Generation Summary                          │
│                                             │
│ 🕐 Daily at 08:00                          │
│ 📅 Next run: Feb 20, 2026 8:00 AM         │
│ 📧 3 recipients                            │
│ ✓ 45 executions                           │
│                                             │
│ [History] [Edit] [Pause] [Run Now]        │
└─────────────────────────────────────────────┘
```

**Actions Available**:
1. **History**: View all past executions
2. **Edit**: Modify schedule settings
3. **Pause/Activate**: Temporarily stop/resume
4. **Run Now**: Execute immediately (don't wait for schedule)

### Create/Edit Dialog

**Form Fields**:
- Report Name (text input)
- Report Type (dropdown)
  - Generation Summary
  - Capacity Factor Analysis
  - Availability Report
  - Performance Metrics
- Frequency (dropdown)
  - Daily
  - Weekly (runs every Monday)
  - Monthly (runs on 1st of month)
  - Quarterly (runs on 1st of quarter)
- Time (time picker) - "08:00"
- Format (dropdown)
  - PDF
  - Excel
  - Both
- Date Range (number) - "30 days"

---

## ⚙️ Backend Components

### 1. Models (`models_scheduled.py`)
Defines database structure for scheduled reports and executions

### 2. Serializers (`serializers_scheduled.py`)
Converts models to/from JSON for API

### 3. Views (`views_scheduled.py`)
API endpoints:
- `GET /api/scheduled-reports/` - List all
- `POST /api/scheduled-reports/` - Create new
- `GET /api/scheduled-reports/{id}/` - Get one
- `PUT /api/scheduled-reports/{id}/` - Update
- `PATCH /api/scheduled-reports/{id}/` - Partial update
- `DELETE /api/scheduled-reports/{id}/` - Delete
- `POST /api/scheduled-reports/{id}/run/` - Run now
- `GET /api/scheduled-reports/{id}/executions/` - Get history

### 4. Service (`automated_reports.py`)
Business logic for generating reports:
- Data fetching
- File generation (Excel/PDF)
- Email sending
- Error handling

### 5. Management Command (`run_scheduled_reports.py`)
Background task that runs periodically:
```bash
python manage.py run_scheduled_reports
```

---

## 🔧 Setup Requirements

### 1. Database Migration
```bash
cd backend
python manage.py migrate
```
This creates the `ScheduledReport` and `ReportExecution` tables.

### 2. Email Configuration
In `settings.py`:
```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'
```

### 3. Scheduler Setup

**Option A: Cron Job (Linux/Mac)**
```bash
# Edit crontab
crontab -e

# Add this line (runs every minute)
* * * * * cd /path/to/backend && python manage.py run_scheduled_reports
```

**Option B: Windows Task Scheduler**
1. Open Task Scheduler
2. Create Basic Task
3. Trigger: Daily, repeat every 1 minute
4. Action: Start a program
   - Program: `python`
   - Arguments: `manage.py run_scheduled_reports`
   - Start in: `C:\path\to\backend`

**Option C: Celery (Production)**
```python
# celery.py
from celery import Celery
from celery.schedules import crontab

app = Celery('npc_reporting')

@app.task
def run_scheduled_reports():
    call_command('run_scheduled_reports')

# Run every minute
app.conf.beat_schedule = {
    'run-reports': {
        'task': 'run_scheduled_reports',
        'schedule': crontab(minute='*'),
    },
}
```

---

## 📈 Report Types Available

### 1. Generation Summary
- Total generation per plant
- Daily/weekly/monthly trends
- Comparison across plants

### 2. Capacity Factor Analysis
- Capacity factor calculations
- Performance vs. capacity
- Efficiency metrics

### 3. Availability Report
- Uptime/downtime statistics
- Forced outages
- Maintenance schedules

### 4. Performance Metrics
- All key performance indicators
- Trends and comparisons
- Anomaly detection

---

## 🎯 Use Cases

### Daily Operations Report
```
Frequency: Daily at 6:00 AM
Recipients: Operations team
Format: Excel
Content: Yesterday's generation data
```

### Weekly Management Summary
```
Frequency: Weekly (Monday) at 8:00 AM
Recipients: Management team
Format: PDF
Content: Last week's performance
```

### Monthly Board Report
```
Frequency: Monthly (1st) at 9:00 AM
Recipients: Board members
Format: Both (PDF + Excel)
Content: Last month's comprehensive data
```

### Quarterly Performance Review
```
Frequency: Quarterly at 10:00 AM
Recipients: All stakeholders
Format: PDF
Content: 90-day performance analysis
```

---

## 🔍 Monitoring & Troubleshooting

### Check Execution History
1. Go to `/scheduled-reports`
2. Click "History" on any report
3. View all past executions with status

### Common Issues

**Report Not Running**:
- Check if status is ACTIVE
- Verify `next_run` time is in the past
- Ensure scheduler is running
- Check backend logs

**Email Not Sending**:
- Verify email settings in `settings.py`
- Check recipient email addresses
- Look for errors in execution history

**Report Generation Fails**:
- Check if data exists for date range
- Verify file permissions for media folder
- Review error message in execution record

---

## 🚀 Benefits

1. **Time Savings**: No manual report generation
2. **Consistency**: Reports always generated on time
3. **Reliability**: Automatic retry on failure
4. **Audit Trail**: Complete execution history
5. **Flexibility**: Easy to modify schedules
6. **Scalability**: Handle multiple reports simultaneously

---

## 📝 Summary

**Automated Reports** = Set it and forget it!

1. Create a schedule once
2. System runs automatically
3. Reports generated on time
4. Emails sent to recipients
5. History tracked for audit

No more manual work, no more missed deadlines!

---

**Need Help?**
- Check execution history for errors
- Review backend logs
- Verify email configuration
- Ensure scheduler is running
