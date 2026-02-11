# 🚀 START HERE - Complete Automated Setup

## What I've Done For You

✅ **Created complete system** with backend, frontend, and database  
✅ **Validated all code** - no errors  
✅ **Created automated setup scripts** - just run them!  
✅ **Removed AGUS3** - only 6 plants (1, 2, 4, 5, 6, 7)

---

## 🎯 One-Command Setup (Almost!)

### Step 1: Install PostgreSQL (Manual - 15 minutes)

**Why manual?** PostgreSQL requires interactive installation with password setup.

1. **Download**: https://www.postgresql.org/download/windows/
2. **Install**: Run installer, remember the password!
3. **Create database**: Open SQL Shell (psql) from Start Menu
   ```sql
   CREATE DATABASE npc_reporting;
   \q
   ```

### Step 2: Update Database Password (30 seconds)

Edit `backend\.env` file:
```
DB_PASSWORD=your_postgres_password_here
```

### Step 3: Run Automated Setup (10-15 minutes)

```cmd
cd npc-reporting-system
AUTOMATED_SETUP.bat
```

This will:
- ✅ Create Python virtual environment
- ✅ Install all Python packages
- ✅ Run database migrations
- ✅ Create admin user (you'll be prompted)
- ✅ Install all Node.js packages
- ✅ Everything ready to run!

### Step 4: Add Initial Data (1 minute)

```cmd
ADD_INITIAL_DATA.bat
```

This adds all 6 Agus plants with units automatically!

### Step 5: Start the System (2 terminals)

**Terminal 1 - Backend:**
```cmd
START_BACKEND.bat
```

**Terminal 2 - Frontend:**
```cmd
START_FRONTEND.bat
```

### Step 6: Access the System

Open browser: **http://localhost:8080**

---

## 📁 All Scripts Created For You

| Script | Purpose | When to Use |
|--------|---------|-------------|
| **AUTOMATED_SETUP.bat** | Complete setup | First time only |
| **ADD_INITIAL_DATA.bat** | Add 6 plants | After setup |
| **START_BACKEND.bat** | Start Django server | Every time |
| **START_FRONTEND.bat** | Start Vue server | Every time |
| **check_prerequisites.bat** | Check installations | Troubleshooting |

---

## ⚡ Quick Start (Copy-Paste)

```cmd
:: 1. Install PostgreSQL first (manual)
:: 2. Create database in SQL Shell:
::    CREATE DATABASE npc_reporting;

:: 3. Update password in backend\.env

:: 4. Run automated setup
cd npc-reporting-system
AUTOMATED_SETUP.bat

:: 5. Add initial data
ADD_INITIAL_DATA.bat

:: 6. Start backend (keep this running)
START_BACKEND.bat

:: 7. In NEW terminal, start frontend
START_FRONTEND.bat

:: 8. Open browser: http://localhost:8080
```

---

## 🎓 What Each Script Does

### AUTOMATED_SETUP.bat
- Checks PostgreSQL is installed
- Creates Python virtual environment
- Installs Django, pandas, openpyxl, etc.
- Runs database migrations
- Prompts for admin user creation
- Installs Vue.js dependencies
- **Run once** at the beginning

### ADD_INITIAL_DATA.bat
- Adds 6 Agus plants (AGUS1, 2, 4, 5, 6, 7)
- Adds sample units for each plant
- **Run once** after setup

### START_BACKEND.bat
- Activates Python virtual environment
- Starts Django server on port 8000
- **Run every time** you want to use the system
- Keep this terminal open

### START_FRONTEND.bat
- Starts Vue.js development server on port 8080
- **Run every time** you want to use the system
- Keep this terminal open

---

## 🔧 Troubleshooting

### "PostgreSQL NOT found"
- Install PostgreSQL first
- Restart terminal after installation
- Run `psql --version` to verify

### "Database migration failed"
- Check PostgreSQL is running (Services)
- Verify database 'npc_reporting' exists
- Check password in backend\.env

### "Port already in use"
- Backend (8000): Stop other Django apps
- Frontend (8080): Stop other Vue apps
- Or change ports in configuration

### "Module not found"
- Run AUTOMATED_SETUP.bat again
- Ensure virtual environment is activated

---

## 📊 System Features

Once running, you can:

1. **Upload Excel Files**
   - Select plant (AGUS1-7)
   - Upload .xlsx file
   - Data imported automatically

2. **View Reports**
   - Filter by plant, date, unit
   - See summary statistics
   - Paginated results

3. **Generate Reports**
   - Daily, monthly, or consolidated
   - Multiple plants
   - Download formatted Excel

4. **Admin Panel**
   - Manage plants and units
   - View upload history
   - User management

---

## 📝 Excel File Format

Your Excel files must have these columns:

| Column | Type | Example |
|--------|------|---------|
| date | Date | 2024-01-15 |
| unit_number | Integer | 1 |
| generation_kwh | Decimal | 500000 |
| operating_hours | Decimal | 23.5 |
| availability_hours | Decimal | 24.0 |
| forced_outage_hours | Decimal | 0.5 |
| scheduled_outage_hours | Decimal | 0.0 |
| remarks | Text | Normal operation |

See **SAMPLE_EXCEL_TEMPLATE.md** for details.

---

## 🎯 Daily Usage

### Starting the System
```cmd
:: Terminal 1
cd npc-reporting-system
START_BACKEND.bat

:: Terminal 2 (new window)
cd npc-reporting-system
START_FRONTEND.bat

:: Browser
http://localhost:8080
```

### Stopping the System
- Press `Ctrl+C` in both terminals
- Or just close the terminal windows

---

## 📞 Need Help?

### Documentation Files
- **START_HERE.md** - This file (start here!)
- **RUN_SYSTEM.md** - Detailed running guide
- **SAMPLE_EXCEL_TEMPLATE.md** - Excel format
- **API_DOCUMENTATION.md** - API reference
- **SYSTEM_CHECKLIST.md** - Testing checklist

### Common Questions

**Q: Do I need to run AUTOMATED_SETUP.bat every time?**  
A: No, only once. After that, just use START_BACKEND.bat and START_FRONTEND.bat

**Q: Can I stop and restart the servers?**  
A: Yes! Just close the terminals and run the START scripts again

**Q: Where is the data stored?**  
A: In PostgreSQL database 'npc_reporting'

**Q: How do I backup data?**  
A: Use `pg_dump -U postgres npc_reporting > backup.sql`

**Q: Can I access from another computer?**  
A: Yes, but you need to configure ALLOWED_HOSTS in settings.py

---

## ✨ Summary

**What you need to do:**
1. ✅ Install PostgreSQL (15 min)
2. ✅ Run AUTOMATED_SETUP.bat (10 min)
3. ✅ Run ADD_INITIAL_DATA.bat (1 min)
4. ✅ Run START_BACKEND.bat (always)
5. ✅ Run START_FRONTEND.bat (always)

**Total time:** ~30 minutes first time, then 1 minute to start daily

**Everything else is automated!** 🎉

---

## 🚀 Ready? Let's Go!

```cmd
cd npc-reporting-system
AUTOMATED_SETUP.bat
```

Follow the prompts, and you'll be up and running in no time!

---

**Last Updated**: February 10, 2026  
**Status**: Ready for automated setup  
**Estimated Time**: 30 minutes total
