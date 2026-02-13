# UNDERSTANDING THE PLANT STATUS REPORT

## What is a Plant Status Report?

The Plant Status report you received is a **SNAPSHOT** document that shows the **CURRENT OPERATIONAL STATUS** of the hydroelectric plants at a specific point in time.

---

## 🔍 WHAT THE PLANT STATUS REPORT SHOWS

### 1. **Water Levels (MASL - Meters Above Sea Level)**
- Shows reservoir water levels
- Example: "701.9 MASL" means water is at 701.9 meters above sea level
- Important for determining generation capacity

### 2. **Gate Openings**
- Gate #1, Gate #2, etc.
- Measured in meters (m)
- Example: "0.90 m" means gate is open 0.90 meters
- Controls water flow to turbines

### 3. **Unit Status**
- **OPERATIONAL** - Unit is running normally
- **Extended GOMP** - Extended Generator Out of Merit (long-term outage)
- **Limited to XX MW** - Operating but at reduced capacity
- Shows reasons for limitations (cooling issues, maintenance, etc.)

### 4. **Total MinGen Output**
- Minimum generation output across all plants
- Example: "636.49 MW" total output

---

## ❌ WHAT THE PLANT STATUS REPORT DOES NOT SHOW

### Missing Information:
1. **Historical generation data** - Only shows current status, not past performance
2. **Daily kWh generation** - No energy totals per day
3. **Operating hours** - No time-based metrics
4. **Detailed outage hours** - Just status, not duration
5. **Unit-by-unit daily records** - No per-unit breakdown over time
6. **Capacity factors** - No performance calculations
7. **Availability factors** - No availability metrics

---

## 🔄 THE RELATIONSHIP BETWEEN REPORTS

```
┌──────────────────────────────────────────────────────────────┐
│                    DAILY OPERATIONS                           │
│  Plant operators record:                                      │
│  • Hourly generation readings                                 │
│  • Unit start/stop times                                      │
│  • Outage events and durations                                │
│  • Performance issues                                          │
└────────────────┬─────────────────────────────────────────────┘
                 │
                 ├─────────────────┬─────────────────────────────┐
                 ▼                 ▼                             ▼
    ┌────────────────────┐  ┌──────────────────┐  ┌────────────────────┐
    │  PLANT STATUS      │  │  DAILY GENERATION│  │  MONTHLY SUMMARY   │
    │  REPORT            │  │  DATA (Excel)    │  │  REPORT            │
    │                    │  │                  │  │                    │
    │  • Current status  │  │  • Date          │  │  • Total MWh       │
    │  • Water levels    │  │  • Unit #        │  │  • Avg capacity    │
    │  • Gate positions  │  │  • Generation    │  │  • Outage summary  │
    │  • Unit conditions │  │  • Hours         │  │  • Performance     │
    └────────────────────┘  │  • Outages       │  └────────────────────┘
                            └──────────────────┘
                                     │
                                     ▼
                            ┌──────────────────┐
                            │  YOUR NPC        │
                            │  REPORTING       │
                            │  SYSTEM          │
                            └──────────────────┘
```

---

## 📊 EXAMPLE: HOW DATA FLOWS

### Scenario: January 15, 2026 - AGUS1 Unit 1

#### What Operators Record (Source Data):
```
Date: 2026-01-15
Unit: 1
Start Time: 00:00
Stop Time: 22:30
Generation: 45,250 kWh
Operating Hours: 22.5
Forced Outage: 1.5 hours (cooling issue)
Scheduled Outage: 0 hours
```

#### What Goes in Plant Status Report:
```
Agus 1 HEP: 701.9 MASL
Unit 1: 45.0 OPERATIONAL. Maximized with respect to ave. outflow.
```

#### What Goes in Your System (Excel Upload):
```
Date          | Unit | Gen kWh | Op Hrs | Avail Hrs | Forced Out | Sched Out
2026-01-15    | 1    | 45250   | 22.5   | 22.5      | 1.5        | 0.0
```

#### What Your System Generates (Dashboard):
```
AGUS1 - Unit 1
• Total Generation: 45,250 kWh
• Capacity Factor: 78.5%
• Availability Factor: 93.8%
• Operating Hours: 22.5
• Outage Hours: 1.5 (forced)
```

---

## 🎯 WHY YOU NEED BOTH TYPES OF DATA

### Plant Status Report:
- **Purpose:** Real-time operational awareness
- **Audience:** Operations managers, dispatchers
- **Frequency:** Daily or shift-based
- **Use:** Immediate decision-making

### Daily Generation Data:
- **Purpose:** Historical performance tracking
- **Audience:** Management, planning, reporting
- **Frequency:** Daily collection, periodic reporting
- **Use:** Analysis, trends, compliance

---

## 💡 HOW TO GET THE DATA YOU NEED

### Step 1: Identify the Source System
Ask your supervisor:
- "Where do operators record daily generation readings?"
- "Is there a SCADA system that logs this data?"
- "Do we have a database or Excel files with historical records?"

### Step 2: Understand the Data Collection Process
- Who records the data? (Operators, SCADA, automated system)
- When is it recorded? (Hourly, end of shift, end of day)
- Where is it stored? (Database, Excel, paper logbooks)
- How can you access it? (Export, query, manual entry)

### Step 3: Request Sample Data
- Ask for 1 week of data to start
- Verify it has all required fields
- Test upload in your system
- Confirm reports look correct

### Step 4: Establish Regular Process
- How often will data be provided? (Daily, weekly, monthly)
- Who will prepare the Excel files?
- What is the deadline for submission?
- Who reviews for accuracy?

---

## 📋 CHECKLIST: QUESTIONS TO ASK

Print this and bring to your meeting:

### About the Data Source:
- [ ] Where is daily generation data currently recorded?
- [ ] Is there a SCADA or EMS system?
- [ ] Can we export data to Excel?
- [ ] Who has access to this data?

### About Historical Data:
- [ ] Do we have historical records?
- [ ] How far back does the data go?
- [ ] Is it in digital format?
- [ ] Can I get a sample?

### About Data Quality:
- [ ] How accurate is the recorded data?
- [ ] Are there any known gaps or issues?
- [ ] Who validates the data?
- [ ] What is the quality control process?

### About the Process:
- [ ] Who will provide data for the system?
- [ ] How often will updates be provided?
- [ ] What format should data be in?
- [ ] Who do I contact if there are issues?

---

## 🚨 COMMON MISUNDERSTANDINGS

### ❌ WRONG: "The Plant Status report has all the data I need"
**✅ CORRECT:** Plant Status shows current conditions, not historical performance data

### ❌ WRONG: "I can manually type data from the Plant Status report"
**✅ CORRECT:** You need the underlying daily generation records, not the summary

### ❌ WRONG: "The system can calculate everything from status reports"
**✅ CORRECT:** The system needs raw operational data (kWh, hours, outages)

### ❌ WRONG: "I should create fake data to test the system"
**✅ CORRECT:** Use sample data for testing, but get real data for production

---

## 📞 SAMPLE CONVERSATION WITH SUPERVISOR

**You:** "Sir/Ma'am, thank you for the Plant Status report. I can see it shows the current operational status of the plants. However, for the reporting system to work, I need the underlying daily generation data."

**Supervisor:** "What do you mean by daily generation data?"

**You:** "The system needs detailed records for each unit, each day, including:
- How many kWh were generated
- How many hours the unit operated
- Any outage hours (forced or scheduled)

The Plant Status report shows current conditions, but I need the historical performance data that operators record daily."

**Supervisor:** "Where would that data be?"

**You:** "That's what I'm trying to find out. It could be in:
- SCADA system exports
- Operator logbooks
- An existing database
- Excel files maintained by operations

Could you help me identify where this data is stored and how I can access it?"

---

## 📧 FOLLOW-UP EMAIL TEMPLATE

Subject: Clarification on Data Requirements - NPC Reporting System

Dear [Supervisor Name],

Thank you for providing the Plant Status report dated [date]. This helps me understand the current operational status of the plants.

However, I need clarification on the data source for the NPC Reporting System. The Plant Status report shows current conditions, but the system requires historical daily generation records.

**What I Need:**
For each plant unit, for each day:
- Date
- Unit Number
- Generation (kWh)
- Operating Hours
- Availability Hours
- Forced Outage Hours
- Scheduled Outage Hours

**Questions:**
1. Where is this daily operational data currently recorded?
2. Is there a SCADA system or database I can access?
3. Can you provide a sample of historical data (even just 1 week)?
4. Who should I coordinate with to get regular data updates?

I've created a template file (attached) that shows exactly what format the system needs. This might help identify the right data source.

Please let me know when we can discuss this further.

Thank you for your guidance.

Best regards,
[Your Name]

---

**Created:** February 12, 2026
**Purpose:** Help understand the difference between Plant Status reports and required generation data
