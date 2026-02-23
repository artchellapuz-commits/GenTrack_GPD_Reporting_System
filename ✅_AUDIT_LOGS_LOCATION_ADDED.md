# ✅ Audit Logs Location Feature Added

## What Was Done

Successfully added location tracking to the audit logs system. Now every login, logout, and report generation activity captures the approximate geographic location based on IP address.

## Changes Made

### 1. Database Changes
- Added `location` field to `AuditLog` model
- Created and applied migration `0013_auditlog_location_alter_scheduledreport_report_type.py`
- Location stores approximate geographic information (City, Region, Country)

### 2. Backend Utilities
- Created `backend/reports/utils.py` with two helper functions:
  - `get_location_from_ip(ip_address)`: Fetches location from IP using ip-api.com
  - `get_client_ip(request)`: Extracts client IP from request headers
- Location data is cached for 24 hours to avoid excessive API calls
- Handles local network IPs (127.0.0.1) gracefully

### 3. Updated Views
- **auth_views.py**: Login and logout now capture location
- **views.py**: Report generation captures location
- **views_scheduled.py**: Scheduled report execution captures location
- All views now use the centralized utility functions

### 4. Frontend Updates
- Added "Location" column to audit logs table
- Added map marker icon for visual clarity
- Updated export function to include location in Excel exports

### 5. Dependencies
- Added `requests>=2.31.0` to requirements.txt
- Installed requests library for API calls

## Features

### Location Tracking
- **Login/Logout**: Captures where users log in from
- **Report Generation**: Tracks location of report exports
- **Scheduled Reports**: Logs location of manual executions

### Smart Handling
- Local network IPs show as "Local Network"
- Failed lookups show as "Unknown"
- Results are cached to improve performance
- Non-blocking: Location lookup errors don't break functionality

### Display
- New column in audit logs table with map marker icon
- Shows format: "City, Region, Country"
- Included in Excel exports

## How It Works

1. When a user performs an action (login, logout, generate report)
2. System captures their IP address
3. IP is sent to ip-api.com (free geolocation service)
4. Location is parsed and stored in database
5. Location is cached for 24 hours
6. Displayed in audit logs table and exports

## API Used

**ip-api.com** (Free tier)
- No API key required
- 45 requests per minute limit
- Returns city, region, and country
- Caching prevents hitting rate limits

## Testing

To test the location feature:

1. **Restart Backend Server**:
   ```bash
   cd npc-reporting-system/backend
   python manage.py runserver
   ```

2. **Login to System**:
   - Go to http://localhost:8080
   - Login with your credentials
   - Check Audit Logs - you should see your location

3. **Generate a Report**:
   - Go to Generate Report
   - Create any report
   - Check Audit Logs - location should be captured

4. **Check Location Display**:
   - Navigate to Audit Logs
   - Look for the "Location" column
   - Should show your approximate location

## Notes

- **Local Development**: When testing locally (localhost), location will show as "Local Network"
- **Production**: In production with real external IPs, actual geographic locations will be shown
- **Privacy**: Only approximate location (city/region level) is captured, not precise coordinates
- **Performance**: Caching ensures minimal impact on system performance
- **Reliability**: Location lookup failures don't affect core functionality

## Files Modified

### Backend
- `backend/reports/models.py` - Added location field
- `backend/reports/utils.py` - NEW: Location utilities
- `backend/reports/auth_views.py` - Updated login/logout
- `backend/reports/views.py` - Updated report generation
- `backend/reports/views_scheduled.py` - Updated scheduled reports
- `backend/requirements.txt` - Added requests library

### Frontend
- `frontend/src/components/AuditLogs.vue` - Added location column

### Database
- `backend/reports/migrations/0013_auditlog_location_alter_scheduledreport_report_type.py` - NEW migration

## Status

✅ Database migration applied
✅ Location tracking implemented
✅ Frontend updated with location column
✅ Export includes location
✅ All audit log types capture location
✅ Caching implemented for performance
✅ Error handling in place

## Next Steps

1. Restart the backend server to load the new code
2. Test by logging in and generating reports
3. Verify location appears in audit logs
4. Export audit logs to verify Excel includes location

The system is ready to track user locations for all audit activities!
