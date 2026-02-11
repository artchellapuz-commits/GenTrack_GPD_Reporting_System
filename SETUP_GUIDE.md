# Setup Guide - NPC Reporting System

Complete step-by-step guide to set up the NPC Reporting System on Windows.

## Prerequisites

### Required Software
1. **Python 3.9+** - [Download](https://www.python.org/downloads/)
2. **Node.js 16+** - [Download](https://nodejs.org/)
3. **PostgreSQL 13+** - [Download](https://www.postgresql.org/download/windows/)
4. **Git** (optional) - [Download](https://git-scm.com/download/win)

### Verify Installations
```cmd
python --version
node --version
npm --version
psql --version
```

---

## Part 1: Database Setup

### Step 1: Create Database

Open PostgreSQL command line (psql):

```sql
-- Create database
CREATE DATABASE npc_reporting;

-- Create user (optional, or use postgres user)
CREATE USER npc_user WITH PASSWORD 'your_password';

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE npc_reporting TO npc_user;

-- Connect to database
\c npc_reporting

-- Verify connection
SELECT current_database();
```

### Step 2: Verify Database
```cmd
psql -U postgres -d npc_reporting -c "SELECT version();"
```

---

## Part 2: Backend Setup

### Step 1: Navigate to Backend Directory
```cmd
cd npc-reporting-system\backend
```

### Step 2: Create Virtual Environment
```cmd
python -m venv venv
```

### Step 3: Activate Virtual Environment
```cmd
venv\Scripts\activate
```

You should see `(venv)` in your command prompt.

### Step 4: Install Dependencies
```cmd
pip install -r requirements.txt
```

### Step 5: Configure Environment Variables
```cmd
copy .env.example .env
```

Edit `.env` file with your settings:
```env
SECRET_KEY=your-random-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

DB_NAME=npc_reporting
DB_USER=postgres
DB_PASSWORD=your_postgres_password
DB_HOST=localhost
DB_PORT=5432
```

### Step 6: Run Migrations
```cmd
python manage.py makemigrations
python manage.py migrate
```

Expected output:
```
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, reports, sessions
Running migrations:
  Applying reports.0001_initial... OK
  ...
```

### Step 7: Create Superuser
```cmd
python manage.py createsuperuser
```

Follow prompts to create admin account.

### Step 8: Load Initial Data

Create a file `backend/initial_data.json`:
```json
[
  {
    "model": "reports.plant",
    "pk": 1,
    "fields": {
      "code": "AGUS1",
      "name": "Agus 1 Hydroelectric Plant",
      "capacity_mw": "100.00",
      "location": "Lanao del Sur",
      "is_active": true
    }
  },
  {
    "model": "reports.plant",
    "pk": 2,
    "fields": {
      "code": "AGUS2",
      "name": "Agus 2 Hydroelectric Plant",
      "capacity_mw": "180.00",
      "location": "Lanao del Sur",
      "is_active": true
    }
  }
]
```

Load data:
```cmd
python manage.py loaddata initial_data.json
```

### Step 9: Test Backend
```cmd
python manage.py runserver
```

Visit: http://localhost:8000/admin

Login with superuser credentials.

---

## Part 3: Frontend Setup

### Step 1: Open New Terminal

Keep backend running, open new command prompt.

Note: The system supports Agus plants 1, 2, 4, 5, 6, 7 (Agus 3 does not exist in NPC).

### Step 2: Navigate to Frontend Directory
```cmd
cd npc-reporting-system\frontend
```

### Step 3: Install Dependencies
```cmd
npm install
```

This may take a few minutes.

### Step 4: Configure Environment
```cmd
copy .env.example .env
```

Edit `.env`:
```env
VUE_APP_API_URL=http://localhost:8000/api
```

### Step 5: Start Development Server
```cmd
npm run serve
```

Expected output:
```
  App running at:
  - Local:   http://localhost:8080/
  - Network: http://192.168.x.x:8080/
```

### Step 6: Access Application

Open browser: http://localhost:8080

---

## Part 4: Verification

### Test Upload Functionality

1. Navigate to Upload page
2. Select a plant (AGUS1)
3. Upload a test Excel file
4. Verify success message

### Test View Reports

1. Navigate to View Reports
2. Apply filters
3. Verify data displays

### Test Generate Report

1. Navigate to Generate Report
2. Select plants and date range
3. Click Generate
4. Verify Excel file downloads

---

## Part 5: Create Test Data

### Option 1: Using Django Admin

1. Go to http://localhost:8000/admin
2. Add Plants (Agus 1, 2, 4, 5, 6, 7)
3. Add Units for each plant
4. Manually add some generation reports

### Option 2: Using Django Shell

```cmd
python manage.py shell
```

```python
from reports.models import Plant, Unit, GenerationReport
from datetime import date

# Create plant
plant = Plant.objects.create(
    code='AGUS1',
    name='Agus 1 Hydroelectric Plant',
    capacity_mw=100,
    location='Lanao del Sur'
)

# Create units
for i in range(1, 5):
    Unit.objects.create(
        plant=plant,
        unit_number=i,
        capacity_mw=25
    )

print("Test data created!")
```

### Option 3: Create Sample Excel File

Create `test_data.xlsx` with columns:
- date
- unit_number
- generation_kwh
- operating_hours
- availability_hours
- forced_outage_hours
- scheduled_outage_hours

Upload via the web interface.

---

## Troubleshooting

### Issue: Database Connection Error

**Error:** `could not connect to server`

**Solution:**
1. Verify PostgreSQL is running:
   ```cmd
   sc query postgresql-x64-13
   ```
2. Check credentials in `.env`
3. Test connection:
   ```cmd
   psql -U postgres -d npc_reporting
   ```

### Issue: Module Not Found

**Error:** `ModuleNotFoundError: No module named 'django'`

**Solution:**
1. Ensure virtual environment is activated
2. Reinstall requirements:
   ```cmd
   pip install -r requirements.txt
   ```

### Issue: Port Already in Use

**Error:** `Error: That port is already in use`

**Solution:**
1. Find process using port:
   ```cmd
   netstat -ano | findstr :8000
   ```
2. Kill process:
   ```cmd
   taskkill /PID <process_id> /F
   ```

### Issue: CORS Error in Browser

**Error:** `Access to XMLHttpRequest blocked by CORS policy`

**Solution:**
1. Verify backend CORS settings in `settings.py`
2. Ensure frontend URL is in `CORS_ALLOWED_ORIGINS`
3. Restart backend server

### Issue: Excel Upload Fails

**Error:** `Validation errors: Missing required columns`

**Solution:**
1. Check Excel file has all required columns
2. Verify column names match exactly (lowercase, underscores)
3. Check data types are correct

---

## Production Deployment

### Backend (Gunicorn + Nginx)

1. Install Gunicorn:
```cmd
pip install gunicorn
```

2. Run with Gunicorn:
```cmd
gunicorn npc_reporting.wsgi:application --bind 0.0.0.0:8000
```

3. Configure Nginx as reverse proxy

### Frontend (Build for Production)

1. Build Vue.js app:
```cmd
npm run build
```

2. Serve `dist` folder with Nginx or Apache

### Environment Variables

Update `.env` for production:
```env
DEBUG=False
ALLOWED_HOSTS=yourdomain.com
SECRET_KEY=generate-new-secret-key
```

### Database

1. Backup regularly:
```cmd
pg_dump -U postgres npc_reporting > backup.sql
```

2. Use connection pooling (pgBouncer)

---

## Next Steps

1. **Add More Plants**: Use Django admin to add Agus 2-7
2. **Configure Units**: Add units for each plant
3. **Upload Historical Data**: Import past reports
4. **Set Up Backups**: Schedule database backups
5. **Configure Monitoring**: Set up logging and monitoring
6. **User Management**: Create user accounts for staff

---

## Useful Commands

### Backend
```cmd
# Activate virtual environment
venv\Scripts\activate

# Run server
python manage.py runserver

# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Django shell
python manage.py shell

# Collect static files
python manage.py collectstatic
```

### Frontend
```cmd
# Install dependencies
npm install

# Run dev server
npm run serve

# Build for production
npm run build

# Lint code
npm run lint
```

### Database
```cmd
# Connect to database
psql -U postgres -d npc_reporting

# Backup database
pg_dump -U postgres npc_reporting > backup.sql

# Restore database
psql -U postgres -d npc_reporting < backup.sql
```

---

## Support

For issues or questions:
1. Check troubleshooting section
2. Review error logs
3. Consult documentation files
4. Contact system administrator
