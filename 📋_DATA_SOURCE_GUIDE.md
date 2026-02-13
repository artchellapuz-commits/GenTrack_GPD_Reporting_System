# DATA SOURCE GUIDE
## Understanding Where Your Data Comes From

---

## 🔍 THE PROBLEM

You received a **PLANT STATUS** report from your supervisor, but this is a **SUMMARY REPORT**, not the **RAW DATA** your system needs.

### What You Have:
- Plant Status Report (shows current operational status)
- Summary information (MASL levels, gate openings, unit status)
- Snapshot of plant conditions

### What You Need:
- **Daily Generation Records** per unit
- **Hourly operational data**
- **Detailed outage information**
- **Performance metrics**

---

## 📊 DATA FLOW DIAGRAM

```
┌─────────────────────────────────────────────────────────────┐
│                    ACTUAL DATA SOURCE                        │
│  (Plant Operators Record Daily in Logbooks or System)       │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│              DAILY GENERATION DATA (Excel/CSV)               │
│  • Date                                                      │
│  • Unit Number                                               │
│  • Generation kWh                                            │
│  • Operating Hours                                           │
│  • Availability Hours                                        │
│  • Forced Outage Hours                                       │
│  • Scheduled Outage Hours                                    │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│              YOUR NPC REPORTING SYSTEM                       │
│  • Upload Excel files                                        │
│  • Process and validate data                                 │
│  • Store in database                                         │
│  • Generate reports and charts                               │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                   OUTPUT REPORTS                             │
│  • Dashboard with statistics                                 │
│  • Plant performance charts                                  │
│  • Consolidated reports                                      │
│  • Monthly summaries                                         │
└─────────────────────────────────────────────────────────────┘
```

---

## 🎯 WHAT TO ASK YOUR SUPERVISOR

### English Version:
"Sir/Ma'am, I need help understanding where to get the source data for the reporting system. The Plant Status report you provided shows the current operational status, but the system needs detailed daily generation records.

Could you please help me locate:
1. **Daily generation logs** - Where do plant operators record daily kWh generation per unit?
2. **Operating hours records** - Where is the hourly operational data stored?
3. **Outage logs** - Where are forced and scheduled outages documented?
4. **Historical data** - Is there an existing database or Excel files with past records?

The system needs data in this format:
- Date, Unit Number, Generation kWh, Operating Hours, Availability Hours, Forced Outage Hours, Scheduled Outage Hours"

### Cebuano/Bisaya Version:
"Sir/Ma'am, kinahanglan nako og tabang para masabtan asa gikan ang data para sa reporting system. Ang Plant Status report nga gihatag ninyo kay nagpakita ra sa current operational status, pero ang system kinahanglan og detailed daily generation records.

Pwede ba ninyo ko tabangan asa nako makuha ang:
1. **Daily generation logs** - Asa nag-record ang plant operators sa daily kWh generation per unit?
2. **Operating hours records** - Asa naka-store ang hourly operational data?
3. **Outage logs** - Asa naka-document ang forced ug scheduled outages?
4. **Historical data** - Naa bay existing database o Excel files sa past records?

Ang system kinahanglan og data sa ingon ani nga format:
- Date, Unit Number, Generation kWh, Operating Hours, Availability Hours, Forced Outage Hours, Scheduled Outage Hours"

---

## 🔎 POSSIBLE DATA SOURCES

### 1. **SCADA System**
- Most hydroelectric plants use SCADA (Supervisory Control and Data Acquisition)
- Records real-time generation data
- Can export to Excel/CSV
- **Ask:** "Do we have access to SCADA data exports?"

### 2. **Plant Logbooks**
- Operators manually record daily readings
- Usually in physical or digital logbooks
- **Ask:** "Where do operators record daily generation readings?"

### 3. **Existing Database/System**
- May already have a database system
- Could be Access, SQL Server, or other
- **Ask:** "Is there an existing database I can query?"

### 4. **Excel Files/Spreadsheets**
- Operators may maintain Excel files
- Could be on shared network drive
- **Ask:** "Are there Excel files with historical generation data?"

### 5. **Energy Management System (EMS)**
- Some plants have dedicated EMS
- Tracks generation and distribution
- **Ask:** "Do we have an EMS that tracks generation?"

---

## 📝 DATA REQUIREMENTS CHECKLIST

Print this and give to your supervisor:

### Required Data Fields:
- [ ] **Date** - Daily date of operation
- [ ] **Unit Number** - Which generator unit (1, 2, 3, etc.)
- [ ] **Generation kWh** - Total energy generated that day
- [ ] **Operating Hours** - Hours the unit was running
- [ ] **Availability Hours** - Hours the unit was available to run (24 - outages)
- [ ] **Forced Outage Hours** - Unplanned downtime
- [ ] **Scheduled Outage Hours** - Planned maintenance downtime

### Data Format:
- [ ] Excel (.xlsx) format preferred
- [ ] One row per unit per day
- [ ] Date format: YYYY-MM-DD or MM/DD/YYYY
- [ ] Numbers only (no text in number fields)

### Time Period Needed:
- [ ] At least 30 days of historical data for testing
- [ ] Ideally 6-12 months for meaningful reports

---

## 🚀 NEXT STEPS

1. **Schedule a meeting** with your supervisor
2. **Bring this document** to explain what you need
3. **Identify the data source** (SCADA, logbooks, database, etc.)
4. **Get sample data** (even just 1 week to start)
5. **Test the upload** in your system
6. **Verify the reports** look correct
7. **Set up regular data collection** process

---

## 💡 TEMPORARY SOLUTION

While waiting for real data, you can:
1. Use the sample data files already in the system
2. Demonstrate the system functionality to stakeholders
3. Show what reports will look like
4. Get feedback on the dashboard and features

---

## 📞 WHO TO CONTACT

Typical people who might have this data:
- **Plant Manager** - Overall operations
- **Operations Supervisor** - Daily operations
- **Control Room Operators** - Real-time data
- **IT Department** - Database access
- **Engineering Department** - Historical records
- **SCADA Administrator** - System data exports

---

## ⚠️ IMPORTANT NOTES

1. **Plant Status ≠ Generation Data**
   - Plant Status shows current conditions
   - Generation Data shows historical performance

2. **You Need Both**
   - Status reports for context
   - Generation data for your system

3. **Data Quality Matters**
   - Ensure data is accurate
   - Check for missing dates
   - Verify calculations

4. **Regular Updates**
   - Establish how often data will be provided
   - Daily, weekly, or monthly uploads?
   - Who is responsible for providing data?

---

## 📧 EMAIL TEMPLATE

Subject: Request for Daily Generation Data - NPC Reporting System

Dear [Supervisor Name],

I am working on the NPC Reporting System and need clarification on the data source.

The Plant Status report provided shows operational status, but the system requires detailed daily generation records with the following fields:
- Date
- Unit Number  
- Generation kWh
- Operating Hours
- Availability Hours
- Forced Outage Hours
- Scheduled Outage Hours

Could you please help me identify where this data is currently stored or recorded? 

I would appreciate:
1. Access to the data source (SCADA, database, Excel files, etc.)
2. Sample historical data (at least 30 days)
3. Guidance on the regular data collection process

Thank you for your assistance.

Best regards,
[Your Name]

---

**Created:** February 12, 2026
**Purpose:** Guide for identifying and obtaining source data for NPC Reporting System
