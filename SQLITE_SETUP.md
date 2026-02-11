# NPC Reporting System - SQLite Setup (EASIEST!)

## ✅ Why SQLite?

**No database installation needed!**
- ✅ Built into Python
- ✅ No configuration required
- ✅ Perfect for development and small deployments
- ✅ Single file database (db.sqlite3)
- ✅ Zero setup time

---

## 🚀 Super Simple Setup (2 Steps!)

### Step 1: Run Complete Setup (10 minutes)

Just double-click:
```
SETUP_NOW.bat
```

This does EVERYTHING:
- ✅ Creates Python virtual environment
- ✅ Installs all packages
- ✅ Creates SQLite database
- ✅ Creates admin user (you'll be prompted)
- ✅ Installs Node.js packages
- ✅ Adds 6 Agus plants automatically

### Step 2: Start the System (20 seconds)

**Terminal 1:**
```
START_BACKEND.bat
```

**Terminal 2:**
```
START_FRONTEND.bat
```

**Browser:**
```
http://localhost:8080
```

**That's it!** 🎉

---

## ⚡ One-Command Setup

```cmd
cd npc-reporting-system
SETUP_NOW.bat
```

Then start with:
```cmd
START_BACKEND.bat    (Terminal 1)
START_FRONTEND.bat   (Terminal 2)
```

---

## 📊 What You Get

### 6 Agus Plants (Pre-loaded)
- AGUS1 - 4 units (25 MW each)
- AGUS2 - 4 units (45 MW each)
- AGUS4 - 4 units (50 MW each)
- AGUS5 - 2 units (26 MW each)
- AGUS6 - 4 units (50 MW each)
- AGUS7 - 4 units (50 MW each)

### Features
- ✅ Upload Excel files
- ✅ View and filter reports
- ✅ Generate Excel reports
- ✅ Admin panel
- ✅ Audit trail

---

## 🗄️ Database Location

Your data is stored in:
```
backend/db.sqlite3
```

### Backup
Just copy this file:
```cmd
copy backend\db.sqlite3 backup\db_backup_2024-01-15.sqlite3
```

### Restore
Replace the file:
```cmd
copy backup\db_backup_2024-01-15.sqlite3 backend\db.sqlite3
```

---

## 🔄 Switching to PostgreSQL Later

If you need PostgreSQL later (for production):

1. Install PostgreSQL
2. Edit `backend/npc_reporting/settings.py`
3. Uncomment PostgreSQL configuration
4. Comment out SQLite configuration
5. Run migrations again

---

## 📋 Daily Usage

### Start System
```cmd
START_BACKEND.bat    (Terminal 1)
START_FRONTEND.bat   (Terminal 2)
```

### Stop System
Press `Ctrl+C` in both terminals

### Access
- Frontend: http://localhost:8080
- Admin: http://localhost:8000/admin
- API: http://localhost:8000/api

---

## 🎯 Advantages of SQLite

### For Development
- ✅ Zero configuration
- ✅ No separate database server
- ✅ Easy backup (just copy file)
- ✅ Perfect for testing

### For Small Deployments
- ✅ Handles thousands of records easily
- ✅ Fast for single-user scenarios
- ✅ No maintenance required
- ✅ Portable (move file = move database)

### Limitations
- ⚠️ Not ideal for multiple concurrent writers
- ⚠️ No network access (local only)
- ⚠️ For production with many users, use PostgreSQL

---

## 🔧 Troubleshooting

### "Database is locked"
- Only one process can write at a time
- Close any other connections to db.sqlite3
- Restart the backend server

### "No such table"
- Run migrations: `python manage.py migrate`
- Or run AUTOMATED_SETUP.bat again

### "Permission denied"
- Close any programs accessing db.sqlite3
- Check file permissions

---

## ✨ Summary

**With SQLite:**
- ✅ No PostgreSQL installation needed
- ✅ No database configuration
- ✅ No password setup
- ✅ Just run SETUP_NOW.bat and you're done!

**Perfect for:**
- Development
- Testing
- Small deployments
- Single-user scenarios
- Quick demos

**Time to running system:** 10-15 minutes total!

---

## 🚀 Ready?

```cmd
cd npc-reporting-system
SETUP_NOW.bat
```

That's all you need! 🎉
