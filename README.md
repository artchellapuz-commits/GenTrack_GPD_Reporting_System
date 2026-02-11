# NPC Generation Reporting System

Database-driven reporting system for National Power Corporation (NPC) Agus Hydroelectric Plants (1, 2, 4, 5, 6, 7).

## Tech Stack

- **Backend**: Django + Django REST Framework
- **Frontend**: Vue.js 3
- **Database**: PostgreSQL
- **File Processing**: pandas, openpyxl

## System Architecture

```
Vue.js Frontend (Port 8080)
    ↓ HTTP/REST API
Django Backend (Port 8000)
    ↓ ORM
PostgreSQL Database (Port 5432)
```

## Features

1. **Excel Import**: Upload and validate Excel reports from NPC
2. **Data Storage**: Store generation data in normalized PostgreSQL tables
3. **Query & Filter**: View reports by plant, date range, unit
4. **Report Generation**: Export data to formatted Excel files
5. **Audit Trail**: Track all file uploads and changes
6. **Historical Data**: Multi-year data storage

## Database Schema

### Tables
- `plants` - Agus plants (1, 2, 4, 5, 6, 7) information
- `units` - Generation units per plant
- `uploaded_files` - Audit trail of Excel uploads
- `generation_reports` - Daily generation data

### Key Features
- Foreign key relationships
- Unique constraints (plant + unit + date)
- Indexes for performance
- Automatic capacity/availability factor calculation

## Setup Instructions

### Backend Setup

1. Create virtual environment:
```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure database:
```bash
copy .env.example .env
# Edit .env with your PostgreSQL credentials
```

4. Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

5. Create superuser:
```bash
python manage.py createsuperuser
```

6. Load initial data (plants and units):
```bash
python manage.py loaddata initial_data.json
```

7. Run development server:
```bash
python manage.py runserver
```

### Frontend Setup

1. Install dependencies:
```bash
cd frontend
npm install
```

2. Configure API URL:
```bash
copy .env.example .env
# Edit .env if needed
```

3. Run development server:
```bash
npm run serve
```

4. Access application at http://localhost:8080

## API Endpoints

### Plants
- `GET /api/plants/` - List all plants

### Units
- `GET /api/units/` - List all units
- `GET /api/units/?plant_code=AGUS1` - Filter by plant

### Upload
- `POST /api/uploaded-files/upload/` - Upload Excel file
  - Form data: `file`, `plant_code`

### Reports
- `GET /api/generation-reports/` - List reports (paginated)
- `GET /api/generation-reports/?plant_code=AGUS1&start_date=2024-01-01&end_date=2024-12-31`
- `GET /api/generation-reports/summary/` - Get aggregated statistics
- `POST /api/generation-reports/generate_report/` - Generate Excel report

## Excel File Format

### Required Columns
- `date` - Report date (YYYY-MM-DD)
- `unit_number` - Unit number (integer)
- `generation_kwh` - Generation in kWh
- `operating_hours` - Operating hours (0-24)
- `availability_hours` - Availability hours (0-24)
- `forced_outage_hours` - Forced outage hours
- `scheduled_outage_hours` - Scheduled outage hours
- `remarks` - Optional remarks

### Validation Rules
- All required columns must be present
- Dates must be valid
- Numeric values must be non-negative
- Hours must be between 0-24
- No duplicate entries (same plant, unit, date)

## Best Practices

### Security
- File size limit: 10MB
- Only .xlsx files allowed
- SHA-256 checksum for duplicate detection
- User authentication required
- CSRF protection enabled

### Performance
- Database indexes on frequently queried fields
- Pagination for large result sets
- Efficient bulk imports using transactions
- Optimized serializers for list views

### Maintainability
- Service layer for business logic
- Separate Excel import/export services
- Clear separation of concerns
- Comprehensive error handling
- Audit trail for all operations

## Future Enhancements

1. **Authentication**: JWT token-based auth
2. **Async Processing**: Celery for large file imports
3. **Data Validation**: Advanced validation rules
4. **Reporting**: More report types and formats
5. **Dashboard**: Real-time analytics and charts
6. **Export**: PDF report generation
7. **Notifications**: Email alerts for failed imports
8. **API Documentation**: Swagger/OpenAPI integration

## Troubleshooting

### Database Connection Error
- Verify PostgreSQL is running
- Check credentials in .env file
- Ensure database exists

### File Upload Fails
- Check file size (max 10MB)
- Verify file format (.xlsx only)
- Check column names match requirements

### Import Validation Errors
- Review error message for specific issues
- Check Excel file format
- Verify data types and ranges

## License

Internal use only - National Power Corporation
