# Quick Start Guide

## Prerequisites Check

Before running the system, ensure you have:

```bash
# Check Python (should be 3.9 or higher)
python --version

# Check Node.js (should be 16 or higher)
node --version

# Check PostgreSQL (should be 13 or higher)
psql --version
```

If any are missing, install them first:
- **Python**: https://www.python.org/downloads/
- **Node.js**: https://nodejs.org/
- **PostgreSQL**: https://www.postgresql.org/download/

---

## Step 1: Database Setup (5 minutes)

```bash
# Open PostgreSQL command line
psql -U postgres

# Create database
CREATE DATABASE npc_reporting;

# Exit psql
\q
```

---

## Step 2: Backend Setup (10 minutes)

```bash
# Navigate to backend folder
cd npc-reporting-system/backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Verify .env file exists and update database password
# Edit backend/.env and set DB_PASSWORD to your PostgreSQL password

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create admin user
python manage.py createsuperuser
# Enter username, email, and password when prompted

# Start backend server
python manage.py runserver
```

**Backend should now be running at http://localhost:8000**

---

## Step 3: Frontend Setup (5 minutes)

Open a **NEW terminal window** (keep backend running):

```bash
# Navigate to frontend folder
cd npc-reporting-system/frontend

# Install dependencies (this may take a few minutes)
npm install

# Start frontend server
npm run serve
```

**Frontend should now be running at http://localhost:8080**

---

## Step 4: Access the Application

1. **Open browser**: http://localhost:8080
2. **Login**: You'll need to authenticate (use the superuser you created)
3. **Add Plants**: Go to http://localhost:8000/admin and add the 6 Agus plants
4. **Add Units**: Add units for each plant
5. **Upload Excel**: Now you can upload Excel files!

---

## Quick Commands Reference

### Backend Commands
```bash
# Activate virtual environment
cd npc-reporting-system/backend
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

# Run server
python manage.py runserver

# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Access Django shell
python manage.py shell

# Access admin
# http://localhost:8000/admin
```

### Frontend Commands
```bash
# Navigate to frontend
cd npc-reporting-system/frontend

# Install dependencies
npm install

# Run development server
npm run serve

# Build for production
npm run build

# Lint code
npm run lint
```

### Database Commands
```bash
# Connect to database
psql -U postgres -d npc_reporting

# Backup database
pg_dump -U postgres npc_reporting > backup.sql

# Restore database
psql -U postgres -d npc_reporting < backup.sql

# List tables
\dt

# Describe table
\d plants
```

---

## Initial Data Setup

### Option 1: Using Django Admin (Recommended)

1. Go to http://localhost:8000/admin
2. Login with superuser credentials
3. Click "Plants" → "Add Plant"
4. Add each plant:
   - AGUS1 - Agus 1 Hydroelectric Plant
   - AGUS2 - Agus 2 Hydroelectric Plant
   - AGUS4 - Agus 4 Hydroelectric Plant
   - AGUS5 - Agus 5 Hydroelectric Plant
   - AGUS6 - Agus 6 Hydroelectric Plant
   - AGUS7 - Agus 7 Hydroelectric Plant
5. For each plant, add units (e.g., Unit 1, Unit 2, etc.)

### Option 2: Using Django Shell

```bash
python manage.py shell
```

```python
from reports.models import Plant, Unit

# Create plants
plants_data = [
    ('AGUS1', 'Agus 1 Hydroelectric Plant', 100, 'Lanao del Sur'),
    ('AGUS2', 'Agus 2 Hydroelectric Plant', 180, 'Lanao del Sur'),
    ('AGUS4', 'Agus 4 Hydroelectric Plant', 200, 'Lanao del Norte'),
    ('AGUS5', 'Agus 5 Hydroelectric Plant', 52, 'Lanao del Norte'),
    ('AGUS6', 'Agus 6 Hydroelectric Plant', 200, 'Lanao del Norte'),
    ('AGUS7', 'Agus 7 Hydroelectric Plant', 200, 'Lanao del Norte'),
]

for code, name, capacity, location in plants_data:
    Plant.objects.get_or_create(
        code=code,
        defaults={
            'name': name,
            'capacity_mw': capacity,
            'location': location
        }
    )

# Create units for AGUS1 (example)
agus1 = Plant.objects.get(code='AGUS1')
for i in range(1, 5):  # 4 units
    Unit.objects.get_or_create(
        plant=agus1,
        unit_number=i,
        defaults={'capacity_mw': 25}
    )

print("Initial data created!")
```

---

## Troubleshooting

### Backend won't start
- **Check**: Is PostgreSQL running?
- **Check**: Are database credentials correct in .env?
- **Check**: Is virtual environment activated?
- **Try**: `pip install -r requirements.txt` again

### Frontend won't start
- **Check**: Is Node.js installed?
- **Check**: Did `npm install` complete successfully?
- **Try**: Delete `node_modules` folder and run `npm install` again

### Can't connect to database
- **Check**: PostgreSQL service is running
- **Check**: Database 'npc_reporting' exists
- **Check**: Username and password in .env are correct
- **Try**: `psql -U postgres -d npc_reporting` to test connection

### Port already in use
- **Backend (8000)**: Another Django app is running
- **Frontend (8080)**: Another Vue app is running
- **Solution**: Stop other apps or change ports in configuration

---

## System URLs

| Service | URL | Purpose |
|---------|-----|---------|
| Frontend | http://localhost:8080 | Main application |
| Backend API | http://localhost:8000/api | REST API |
| Django Admin | http://localhost:8000/admin | Admin interface |
| API Plants | http://localhost:8000/api/plants/ | Plants endpoint |
| API Reports | http://localhost:8000/api/generation-reports/ | Reports endpoint |

---

## Next Steps

1. ✅ System is running
2. ✅ Initial data is loaded
3. 📝 Create test Excel file with required columns
4. 📤 Upload Excel file via web interface
5. 📊 View imported data
6. 📥 Generate and download reports

---

## Support

For detailed information, see:
- **SETUP_GUIDE.md** - Complete setup instructions
- **API_DOCUMENTATION.md** - API reference
- **ARCHITECTURE.md** - System architecture
- **VALIDATION_REPORT.md** - Code validation results
