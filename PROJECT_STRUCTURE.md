# NPC Reporting System - Project Structure

## Overview
Clean, production-ready NPC Generation Reporting System for Agus Hydroelectric Plants.

## Essential Documentation

### Core Documentation
- **README.md** - Project overview, features, and basic information
- **SETUP_GUIDE.md** - Complete step-by-step setup instructions
- **API_DOCUMENTATION.md** - REST API endpoints and usage
- **ARCHITECTURE.md** - System architecture and design
- **DESIGN_CONSIDERATIONS.md** - Design decisions and rationale
- **QUICK_START.md** - Quick start guide for developers

### Startup Scripts
- **AUTOMATED_SETUP.bat** - Automated installation script
- **START_BACKEND.bat** - Start Django backend server
- **START_FRONTEND.bat** - Start Vue.js frontend server
- **START_SYSTEM.bat** - Start both backend and frontend

## Directory Structure

```
npc-reporting-system/
├── backend/                    # Django REST API
│   ├── npc_reporting/         # Django project settings
│   ├── reports/               # Main application
│   │   ├── models.py         # Database models
│   │   ├── views.py          # API views
│   │   ├── serializers.py    # DRF serializers
│   │   ├── services/         # Business logic
│   │   └── management/       # Django commands
│   ├── media/                # Uploaded files
│   ├── logs/                 # Application logs
│   ├── requirements.txt      # Python dependencies
│   └── manage.py            # Django management
│
├── frontend/                  # Vue.js SPA
│   ├── src/
│   │   ├── components/       # Vue components
│   │   ├── router/          # Vue Router
│   │   ├── assets/          # CSS, images
│   │   └── utils/           # Utility functions
│   ├── public/              # Static files
│   └── package.json         # Node dependencies
│
├── database/                 # Database scripts
│   └── schema.sql           # PostgreSQL schema
│
└── sample_data/             # Sample Excel files

```

## Key Features

1. **Excel Import/Export** - Upload and process NPC Excel reports
2. **Data Management** - Store and query generation data
3. **Report Generation** - Generate formatted Excel reports (PSR format)
4. **User Management** - Role-based access control
5. **Audit Logs** - Track all system activities
6. **Historical Data** - Multi-year data storage
7. **Advanced Analytics** - Charts and performance metrics
8. **Scheduled Reports** - Automated report generation
9. **PWA Support** - Progressive Web App capabilities
10. **Responsive Design** - Mobile-friendly interface

## Technology Stack

### Backend
- Django 4.2
- Django REST Framework
- PostgreSQL
- pandas & openpyxl (Excel processing)

### Frontend
- Vue.js 3
- Vue Router
- Axios
- PrimeVue (UI components)
- Chart.js (visualizations)

## Getting Started

1. **Prerequisites**
   - Python 3.9+
   - Node.js 16+
   - PostgreSQL 13+

2. **Quick Setup**
   ```cmd
   # Run automated setup
   AUTOMATED_SETUP.bat
   
   # Start the system
   START_SYSTEM.bat
   ```

3. **Manual Setup**
   - See SETUP_GUIDE.md for detailed instructions

## Plants Supported

- Agus 1 Hydroelectric Plant
- Agus 2 Hydroelectric Plant
- Agus 4 Hydroelectric Plant (Pulangi 4)
- Agus 5 Hydroelectric Plant
- Agus 6 Hydroelectric Plant
- Agus 7 Hydroelectric Plant

Note: Agus 3 does not exist in NPC's plant roster.

## API Endpoints

- `/api/plants/` - Plant management
- `/api/units/` - Unit management
- `/api/uploaded-files/` - File upload history
- `/api/generation-reports/` - Generation data
- `/api/historical-data/` - Historical records
- `/api/scheduled-reports/` - Automated reports
- `/api/analytics/` - Performance analytics

See API_DOCUMENTATION.md for complete details.

## Development

### Backend Development
```cmd
cd backend
venv\Scripts\activate
python manage.py runserver
```

### Frontend Development
```cmd
cd frontend
npm run serve
```

### Database Migrations
```cmd
cd backend
python manage.py makemigrations
python manage.py migrate
```

## Production Deployment

1. **Backend**: Gunicorn + Nginx
2. **Frontend**: Build and serve with Nginx
3. **Database**: PostgreSQL with backups
4. **Static Files**: CDN or Nginx

See SETUP_GUIDE.md for production deployment details.

## Support

For issues or questions:
1. Check documentation files
2. Review error logs in `backend/logs/`
3. Contact system administrator

## License

Internal use only - National Power Corporation

---

Last Updated: February 2026
