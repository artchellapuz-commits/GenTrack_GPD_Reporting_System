# NPC Reporting System

National Power Corporation - Agus Hydroelectric Plants Generation Reporting System

## Overview

A comprehensive web-based reporting system for managing and analyzing generation data from NPC's Agus Hydroelectric Power Plants (AGUS1, AGUS2, AGUS4, AGUS5, AGUS6, AGUS7).

## Features

- **Excel Upload**: Import generation data from Excel files with validation
- **View Reports**: Browse and filter generation reports with pagination
- **Generate Reports**: Export data to Excel in multiple formats (Daily, Monthly, Consolidated)
- **Summary Statistics**: View aggregated performance metrics
- **Audit Trail**: Track all file uploads and changes

## Technology Stack

### Backend
- Django 6.0.2
- Django REST Framework
- SQLite Database
- Python 3.x
- pandas & openpyxl for Excel processing

### Frontend
- Vue.js 3
- Axios for API calls
- PrimeVue icons
- Modern CSS with responsive design

## Project Structure

```
npc-reporting-system/
├── backend/
│   ├── npc_reporting/          # Django project settings
│   ├── reports/                # Main application
│   │   ├── models.py          # Database models
│   │   ├── views.py           # API endpoints
│   │   ├── serializers.py     # DRF serializers
│   │   ├── services/          # Business logic
│   │   │   ├── excel_importer.py
│   │   │   └── excel_exporter.py
│   │   └── migrations/
│   ├── media/                 # Uploaded files
│   ├── db.sqlite3            # SQLite database
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/       # Vue components
│   │   │   ├── UploadExcel.vue
│   │   │   ├── ViewReports.vue
│   │   │   └── GenerateReport.vue
│   │   ├── services/         # API service
│   │   ├── assets/           # Static assets
│   │   └── App.vue
│   ├── public/
│   └── package.json
└── database/
    └── schema.sql
```

## Installation

### Prerequisites
- Python 3.8+
- Node.js 14+
- npm or yarn

### Backend Setup

1. Navigate to backend directory:
```bash
cd backend
```

2. Create virtual environment:
```bash
python -m venv venv
```

3. Activate virtual environment:
```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Run migrations:
```bash
python manage.py migrate
```

6. Create superuser (optional):
```bash
python manage.py createsuperuser
```

7. Load initial data:
```bash
python manage.py shell < add_initial_data.py
```

8. Start development server:
```bash
python manage.py runserver
```

Backend will run on: http://localhost:8000

### Frontend Setup

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Create .env file:
```bash
cp .env.example .env
```

4. Start development server:
```bash
npm run serve
```

Frontend will run on: http://localhost:8080

## Usage

### Uploading Excel Files

1. Navigate to "Upload Excel Reports"
2. Select the hydroelectric plant
3. Choose an Excel file with the required format
4. Click "Upload File"

**Required Excel Columns:**
- Date
- Unit Number
- Generation kWh
- Operating Hours
- Availability Hours
- Forced Outage Hours
- Scheduled Outage Hours

### Viewing Reports

1. Navigate to "View Reports"
2. Select one or more plants
3. Optionally set date range
4. Click "Apply Filters" for detailed table
5. Click "View Summary" for aggregated statistics

### Generating Reports

1. Navigate to "Generate Report"
2. Select plants to include
3. Set date range
4. Choose report type:
   - **Daily Report**: Detailed daily generation data
   - **Monthly Summary**: Aggregated monthly statistics
   - **Consolidated Report**: Complete overview across plants
5. Click "Generate Report" to download Excel file

## API Endpoints

### Plants
- `GET /api/plants/` - List all plants

### Units
- `GET /api/units/` - List all units
- `GET /api/units/?plant_code=AGUS1` - Filter by plant

### Uploaded Files
- `GET /api/uploaded-files/` - List uploaded files
- `POST /api/uploaded-files/upload/` - Upload Excel file
- `DELETE /api/uploaded-files/{id}/delete_upload/` - Delete upload

### Generation Reports
- `GET /api/generation-reports/` - List reports (with filters)
- `GET /api/generation-reports/summary/` - Get summary statistics
- `POST /api/generation-reports/generate-report/` - Generate Excel report

## Database Models

### Plant
- Agus hydroelectric plants (AGUS1, AGUS2, AGUS4, AGUS5, AGUS6, AGUS7)
- Capacity, location, commissioned date

### Unit
- Generation units within each plant
- Unit number, capacity, status

### UploadedFile
- Audit trail for Excel uploads
- Status tracking, error messages

### GenerationReport
- Daily generation data per unit
- Performance metrics (capacity factor, availability factor)

## Configuration

### Backend (.env)
```
DEBUG=True
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://localhost:8080
```

### Frontend (.env)
```
VUE_APP_API_URL=http://localhost:8000/api
```

## Development

### Running Tests
```bash
# Backend
cd backend
python manage.py test

# Frontend
cd frontend
npm run test
```

### Code Style
- Backend: Follow PEP 8
- Frontend: Follow Vue.js style guide

## Deployment

### Production Checklist
- [ ] Set DEBUG=False in Django settings
- [ ] Configure proper SECRET_KEY
- [ ] Set up production database (PostgreSQL recommended)
- [ ] Configure static files serving
- [ ] Set up HTTPS
- [ ] Configure CORS for production domain
- [ ] Build frontend for production: `npm run build`
- [ ] Use production WSGI server (gunicorn, uwsgi)

## Troubleshooting

### Excel Upload Fails
- Verify column names match exactly (case-sensitive)
- Check date format (YYYY-MM-DD)
- Ensure numeric fields contain valid numbers
- File size must be under 10MB

### CORS Errors
- Check CORS_ALLOWED_ORIGINS in Django settings
- Verify frontend API URL in .env file

### Database Issues
- Run migrations: `python manage.py migrate`
- Check database file permissions

## Contributing

1. Create a feature branch
2. Make your changes
3. Test thoroughly
4. Submit a pull request

## License

Proprietary - National Power Corporation

## Contact

For support or questions, contact the development team.

## Version History

### v1.0.0 (2026-02-11)
- Initial release
- Excel upload and validation
- View reports with filtering
- Generate reports (Daily, Monthly, Consolidated)
- Summary statistics
- Professional UI with PrimeVue icons
