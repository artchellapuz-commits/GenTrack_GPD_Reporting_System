# How to Run the NPC Reporting System

## ✅ Prerequisites Verified
- ✅ Python 3.14.3 installed
- ✅ Node.js v25.6.0 installed
- ❌ PostgreSQL NOT installed (required!)

---

## Step 1: Install PostgreSQL (REQUIRED)

### Download and Install
1. Go to: https://www.postgresql.org/download/windows/
2. Download PostgreSQL 13 or higher
3. Run the installer
4. **Remember the password** you set for 'postgres' user
5. Keep default port: 5432
6. Install all components

### Create Database
After installation, open **SQL Shell (psql)** from Start Menu:

```sql
-- Enter password when prompted
CREATE DATABASE npc_reporting;

-- Verify
\l

-- Exit
\q
```

---

## Step 2: Setup Backend

### Option A: Using Batch Script (Easiest)
```cmd
cd npc-reporting-system
setup_backend.bat
```

### Option B: Manual Setup
```cmd
cd npc-reporting-system\backend

:: Create virtual environment
python -m venv venv

:: Activate it
venv\Scripts\activate

:: Install dependencies
pip install -r requirements.txt
```

### Configure Database
Edit `backend\.env` file:
```
DB_PASSWORD=your_postgres_password_here
```

### Run Migrations
```cmd
:: Make sure venv is activated
python manage.py makemigrations
python manage.py migrate
```

### Create Admin User
```cmd
python manage.py createsuperuser
```
Enter:
- Username: admin
- Email: admin@example.com  
- Password: (your choice)

### Start Backend Server
```cmd
python manage.py runserver
```

Backend will run at: **http://localhost:8000**

---

## Step 3: Setup Frontend

### Option A: Using Batch Script (Easiest)
Open **NEW** command prompt:
```cmd
cd npc-reporting-system
setup_frontend.bat
```

### Option B: Manual Setup
```cmd
cd npc-reporting-system\frontend

:: Install dependencies (takes 5-10 minutes)
npm install

:: Start server
npm run serve
```

Frontend will run at: **http://localhost:8080**

---

## Step 4: Add Initial Data

### Using Django Admin (Recommended)
1. Go to: http://localhost:8000/admin
2. Login with admin credentials
3. Click "Plants" → "Add Plant"
4. Add these 6 plants:

| Code | Name | Capacity (MW) | Location |
|------|------|---------------|----------|
| AGUS1 | Agus 1 Hydroelectric Plant | 100 | Lanao del Sur |
| AGUS2 | Agus 2 Hydroelectric Plant | 180 | Lanao del Sur |
| AGUS4 | Agus 4 Hydroelectric Plant | 200 | Lanao del Norte |
| AGUS5 | Agus 5 Hydroelectric Plant | 52 | Lanao del Norte |
| AGUS6 | Agus 6 Hydroelectric Plant | 200 | Lanao del Norte |
| AGUS7 | Agus 7 Hydroelectric Plant | 200 | Lanao del Norte |

5. For each plant, add units (e.g., Unit 1, 2, 3, 4)

### Using Django Shell (Alternative)
```cmd
cd npc-reporting-system\backend
venv\Scripts\activate
python manage.py shell
```

Then paste this code:
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
        defaults={'name': name, 'capacity_mw': capacity, 'location': location}
    )
    print(f"{'Created' if created else 'Already exists'}: {code}")

# Create units for AGUS1 (example)
agus1 = Plant.objects.get(code='AGUS1')
for i in range(1, 5):
    unit, created = Unit.objects.get_or_create(
        plant=agus1, unit_number=i, defaults={'capacity_mw': 25}
    )
    print(f"{'Created' if created else 'Already exists'}: AGUS1 Unit {i}")

print("\nDone! Add units for other plants as needed.")
exit()
```

---

## Step 5: Access the System

### URLs
- **Frontend**: http://localhost:8080
- **Backend API**: http://localhost:8000/api
- **Admin Panel**: http://localhost:8000/admin

### Test the System
1. Open http://localhost:8080
2. Click "Upload" → Select plant → Upload Excel file
3. Click "View Reports" → See imported data
4. Click "Generate Report" → Download Excel report

---

## Quick Reference

### Start Backend
```cmd
cd npc-reporting-system\backend
venv\Scripts\activate
python manage.py runserver
```

### Start Frontend
```cmd
cd npc-reporting-system\frontend
npm run serve
```

### Both Must Be Running
- Keep backend running in one terminal
- Keep frontend running in another terminal
- Access application at http://localhost:8080

---

## Troubleshooting

### "psycopg2" error
PostgreSQL is not installed. Install it first.

### "Database connection error"
- Check PostgreSQL is running
- Verify password in backend\.env
- Verify database 'npc_reporting' exists

### "Port 8000 already in use"
Another Django app is running. Stop it or use different port.

### "Port 8080 already in use"
Another Vue app is running. Stop it or use different port.

### Virtual environment activation fails
```cmd
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

## Summary

**Current Status:**
- ✅ Python installed and working
- ✅ Node.js installed and working
- ❌ PostgreSQL needs to be installed

**Next Action:**
1. Install PostgreSQL
2. Run `setup_backend.bat`
3. Run `setup_frontend.bat`
4. Add initial data
5. Start using the system!

**Estimated Time:** 30-40 minutes total
