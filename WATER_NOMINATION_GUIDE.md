# 💧 Water Nomination Module - User Guide

## Overview
The Water Nomination module allows you to manage hourly water dispatch nominations for hydroelectric plants. This feature helps plan and track water release schedules for power generation.

## Features

### 1. Create Nominations
- Create day-ahead, hour-ahead, or real-time nominations
- Input hourly MW values for 24-hour periods
- Automatic calculation of total nominated MWh
- Add water parameters (reservoir levels, flow rates)
- Save as draft for later editing

### 2. Nomination Workflow
```
DRAFT → SUBMITTED → APPROVED/REJECTED → COMPLETED
```

- **Draft**: Initial creation, can be edited
- **Submitted**: Sent for approval, no longer editable
- **Approved**: Approved by authorized personnel
- **Rejected**: Rejected with remarks
- **Completed**: Actual generation data recorded

### 3. View & Filter
- Filter by plant, status, date range
- View nomination details with hourly breakdown
- Visual hourly profile chart
- Track submission and approval history

### 4. Variance Analysis
- Compare nominated vs actual generation
- Hourly variance breakdown
- Percentage deviation calculation
- Identify over/under generation patterns

## How to Use

### Creating a New Nomination

1. Click **"New Nomination"** button
2. Select the plant
3. Choose nomination date
4. Select nomination type (Day-Ahead, Hour-Ahead, Real-Time)
5. Enter hourly MW values for each hour (00:00 to 23:00)
6. Add optional water parameters:
   - Reservoir level (start/end)
   - Water flow rate
   - Inflow rate
7. Add remarks if needed
8. Click **"Create"** to save as draft

### Submitting for Approval

1. Find your draft nomination in the list
2. Click **"Submit"** button
3. Confirm submission
4. Status changes to "SUBMITTED"

### Approving Nominations

1. Filter by status "SUBMITTED"
2. Click **"View"** to review details
3. Click **"Approve"** to approve
4. Or reject with remarks if needed

### Recording Actual Generation

Use the API endpoint to record actual hourly generation:
```
POST /api/actual-generations/
```

### Viewing Variance Analysis

1. Navigate to variance analysis section
2. Select plant and date range
3. View comparison charts
4. Export variance reports

## API Endpoints

### Water Nominations
- `GET /api/water-nominations/` - List all nominations
- `POST /api/water-nominations/` - Create new nomination
- `GET /api/water-nominations/{id}/` - Get nomination details
- `PUT /api/water-nominations/{id}/` - Update nomination (draft only)
- `DELETE /api/water-nominations/{id}/` - Delete nomination
- `POST /api/water-nominations/{id}/submit/` - Submit for approval
- `POST /api/water-nominations/{id}/approve/` - Approve nomination
- `POST /api/water-nominations/{id}/reject/` - Reject nomination

### Actual Generation
- `GET /api/actual-generations/` - List actual generation data
- `POST /api/actual-generations/` - Record actual generation
- `GET /api/actual-generations/{id}/` - Get actual generation details
- `PUT /api/actual-generations/{id}/` - Update actual generation
- `GET /api/actual-generations/variance_analysis/` - Get variance analysis

## Data Model

### WaterNomination Fields
- **plant**: Plant reference
- **nomination_date**: Date for nomination
- **nomination_type**: DAY_AHEAD, HOUR_AHEAD, REAL_TIME
- **status**: DRAFT, SUBMITTED, APPROVED, REJECTED, COMPLETED
- **hour_00 to hour_23**: Hourly MW values
- **total_nominated_mw**: Sum of hourly values
- **total_nominated_mwh**: Total energy (MWh)
- **reservoir_level_start/end**: Water levels (meters)
- **water_flow_rate**: Average flow (m³/s)
- **inflow_rate**: Inflow rate (m³/s)
- **submitted_by/at**: Submission tracking
- **approved_by/at**: Approval tracking
- **remarks**: Additional notes

### ActualGeneration Fields
- **plant**: Plant reference
- **generation_date**: Date of generation
- **hour_00 to hour_23**: Actual hourly MW values
- **total_actual_mw**: Sum of actual values
- **total_actual_mwh**: Total actual energy
- **actual_water_flow**: Actual water flow
- **reservoir_level**: Actual reservoir level
- **remarks**: Notes

## Example API Usage

### Create Nomination
```javascript
const nomination = {
  plant: 1,  // Plant ID
  nomination_date: "2026-02-19",
  nomination_type: "DAY_AHEAD",
  hour_00: 50.5,
  hour_01: 48.2,
  // ... other hours
  hour_23: 52.0,
  reservoir_level_start: 125.5,
  reservoir_level_end: 124.8,
  water_flow_rate: 150.0,
  remarks: "Normal operation expected"
};

const response = await axios.post(
  'http://localhost:8000/api/water-nominations/',
  nomination
);
```

### Record Actual Generation
```javascript
const actual = {
  plant: 1,
  generation_date: "2026-02-19",
  hour_00: 51.2,
  hour_01: 47.8,
  // ... other hours
  hour_23: 51.5,
  actual_water_flow: 148.5,
  reservoir_level: 124.9
};

const response = await axios.post(
  'http://localhost:8000/api/actual-generations/',
  actual
);
```

### Get Variance Analysis
```javascript
const response = await axios.get(
  'http://localhost:8000/api/actual-generations/variance_analysis/',
  {
    params: {
      plant_code: 'AGUS1',
      start_date: '2026-02-01',
      end_date: '2026-02-28'
    }
  }
);

// Response includes:
// - total_nominated_mwh
// - total_actual_mwh
// - variance_mwh
// - variance_percent
// - hourly_comparison array
```

## Tips & Best Practices

1. **Create nominations in advance**: Use day-ahead nominations for better planning
2. **Review before submitting**: Double-check hourly values before submission
3. **Track variances**: Regular variance analysis helps improve forecasting
4. **Document deviations**: Use remarks to explain significant variances
5. **Update water parameters**: Keep reservoir and flow data current
6. **Archive old nominations**: Export historical data for analysis

## Customization

The module is designed to be flexible. You can customize:
- Nomination types (add more types in models.py)
- Water parameters (add plant-specific fields)
- Approval workflow (add multiple approval levels)
- Validation rules (add business logic)
- Export formats (customize reports)

## Troubleshooting

### Cannot submit nomination
- Ensure all required fields are filled
- Check that status is "DRAFT"
- Verify you have permission

### Variance analysis shows no data
- Ensure actual generation data is recorded
- Check date range filters
- Verify plant code matches

### Hourly values not saving
- Check that values are numeric
- Ensure values are within valid range
- Verify network connection

## Support

For issues or questions:
1. Check this guide first
2. Review API documentation
3. Check backend logs for errors
4. Contact system administrator

---

**Module Status**: ✅ Fully Implemented
**Last Updated**: February 18, 2026
**Version**: 1.0.0
