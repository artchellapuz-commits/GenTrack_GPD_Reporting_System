# Installation Steps for NPC Reporting System

## Current Status
- ❌ Python not accessible from command line
- ❌ Node.js not accessible from command line
- ⚠️ PostgreSQL status unknown

## Step 1: Install Python

### Download and Install
1. Go to https://www.python.org/downloads/
2. Download Python 3.9 or higher (Latest: 3.12.x recommended)
3. **IMPORTANT**: During installation, check "Add Python to PATH"
4. Click "Install Now"

### Verify Installation
Open a NEW PowerShell window and run:
```powershell
python --version
```
Should show: `Python 3.x.x`

If not working, manually add to PATH:
1. Search "Environment Variables" in Windows
2. Click "Environment Variables"
3. Under "System variables", find "Path"
4. Click "Edit"
5. Click "New"
6. Add: `C:\Users\YourUsername\AppData\Local\Programs\Python\Python3xx`
7. Add: `C:\Users\YourUsername\AppData\Local\Programs\Python\Python3xx\Scripts`
8. Click OK
9. Restart PowerShell

---

## Step 2: Install Node.js

### Download and Install
1. Go to https://nodejs.org/
2. Download LTS version (Latest: 20.x.x recommended)
3. Run installer
4. Accept all defaults (it will add to PATH automatically)
5. Click "Install"

### Verify Installation
Open a NEW PowerShell window and run:
```powershell
node --version
npm --version
```
Should show versions for both

---

## Step 3: Install PostgreSQL

### Download and Install
1. Go to https://www.postgresql.org/download/windows/
2. Download PostgreSQL 13 or higher
3. Run installer
4. Remember the password you set for 'postgres' user
5. Default port: 5432 (keep it)
6. Install all components

### Verify Installation
```powershell
psql --version
```

### Create Database
Open SQL Shell (psql) from Start Menu:
```sql
-- Login as postgres user (enter password when prompted)
CREATE DATABASE npc_reporting;
\q
```

---

## Step 4: Setup Backend

### Navigate to Backend
```powershell
cd npc-reporting-system\backend
```

### Create Virtual Environment
```powershell
python -m venv venv
```

### Activate Virtual Environment
```powershell
.\venv\Scripts\Activate.ps1
```

If you get an error about execution policy:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```
Then try activating again.

### Install Dependencies
```powershell
pip install -r requirements.txt
```

This will install:
- Django
- djangorestframework
- psycopg2-binary
- pandas
- openpyxl
- django-cors-headers
- python-dotenv

### Configure Database
Edit `backend\.env` file and update:
```
DB_PASSWORD=your_postgres_password
```

### Run Migrations
```powershell
python manage.py makemigrations
python manage.py migrate
```

### Create Superuser
```powershell
python manage.py createsuperuser
```
Enter:
- Username: admin
- Email: admin@example.com
- Password: (your choice, remember it!)

### Start Backend Server
```powershell
python manage.py runserver
```

Backend should now be running at: http://localhost:8000

---

## Step 5: Setup Frontend

### Open NEW PowerShell Window
Keep backend running, open new window

### Navigate to Frontend
```powershell
cd npc-reporting-system\frontend
```

### Install Dependencies
```powershell
npm install
```

This may take 5-10 minutes

### Start Frontend Server
```powershell
npm run serve
```

Frontend should now be running at: http://localhost:8080

---

## Step 6: Add Initial Data

### Option 1: Using Django Admin
1. Go to http://localhost:8000/admin
2. Login with superuser credentials
3. Add Plants:
   - AGUS1 - Agus 1 Hydroelectric Plant (Capacity: 100 MW, Location: Lanao del Sur)
   - AGUS2 - Agus 2 Hydroelectric Plant (Capacity: 180 MW, Location: Lanao del Sur)
   - AGUS4 - Agus 4 Hydroelectric Plant (Capacity: 200 MW, Location: Lanao del Norte)
   - AGUS5 - Agus 5 Hydroelectric Plant (Capacity: 52 MW, Location: Lanao del Norte)
   - AGUS6 - Agus 6 Hydroelectric Plant (Capacity: 200 MW, Location: Lanao del Norte)
   - AGUS7 - Agus 7 Hydroelectric Plant (Capacity: 200 MW, Location: Lanao del Norte)

4. Add Units for each plant (e.g., Unit 1, 2, 3, 4 for AGUS1)

### Option 2: Using Django Shell
In backend directory with venv activated:
```powershell
python manage.py shell
```

Then paste:
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
    plant, created = Plant.objects.get_or_create(
        code=code,
        defaults={
            'name': name,
            'capacity_mw': capacity,
            'location': location
        }
    )
    if created:
        print(f"Created {code}")

# Create units for AGUS1
agus1 = Plant.objects.get(code='AGUS1')
for i in range(1, 5):
    Unit.objects.get_or_create(
        plant=agus1,
        unit_number=i,
        defaults={'capacity_mw': 25}
    )

print("Initial data created!")
exit()
```

---

## Step 7: Test the System

### Access Application
1. Open browser: http://localhost:8080
2. You should see the NPC Reporting System interface

### Test Upload
1. Click "Upload"
2. Select a plant (AGUS1)
3. Create a test Excel file (see SAMPLE_EXCEL_TEMPLATE.md)
4. Upload the file
5. Verify success message

### Test View Reports
1. Click "View Reports"
2. Apply filters
3. Verify data displays

### Test Generate Report
1. Click "Generate Report"
2. Select plants and date range
3. Click "Generate Report"
4. Verify Excel file downloads

---

## Troubleshooting

### Python not found
- Restart PowerShell after installation
- Check PATH environment variable
- Try `py --version` instead of `python --version`

### Node not found
- Restart PowerShell after installation
- Reinstall Node.js with default options

### Cannot activate virtual environment
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Database connection error
- Verify PostgreSQL is running (check Services)
- Check password in .env file
- Verify database 'npc_reporting' exists

### Port already in use
- Backend (8000): Another Django app is running
- Frontend (8080): Another Vue app is running
- Solution: Stop other apps or change ports

### Module not found errors
- Ensure virtual environment is activated
- Run `pip install -r requirements.txt` again

### npm install fails
- Delete `node_modules` folder
- Delete `package-lock.json`
- Run `npm install` again

---

## Quick Commands Reference

### Backend
```powershell
# Navigate to backend
cd npc-reporting-system\backend

# Activate virtual environment
.\venv\Scripts\Activate.ps1

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
```

### Frontend
```powershell
# Navigate to frontend
cd npc-reporting-system\frontend

# Install dependencies
npm install

# Run server
npm run serve

# Build for production
npm run build
```

### Database
```powershell
# Connect to database
psql -U postgres -d npc_reporting

# Backup
pg_dump -U postgres npc_reporting > backup.sql

# Restore
psql -U postgres -d npc_reporting < backup.sql
```

---

## System URLs

- **Frontend**: http://localhost:8080
- **Backend API**: http://localhost:8000/api
- **Django Admin**: http://localhost:8000/admin

---

## Next Steps After Installation

1. ✅ System is running
2. ✅ Initial data loaded
3. 📝 Create test Excel file
4. 📤 Upload test data
5. 📊 View reports
6. 📥 Generate Excel reports

---

## Need Help?

Check these files:
- **QUICK_START.md** - Quick reference
- **SETUP_GUIDE.md** - Detailed guide
- **SAMPLE_EXCEL_TEMPLATE.md** - Excel format
- **SYSTEM_CHECKLIST.md** - Testing checklist
