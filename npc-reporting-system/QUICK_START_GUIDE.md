# Quick Start Guide - NPC Reporting System

## 🚀 System Status
- ✅ Backend: http://127.0.0.1:8000/
- ✅ Frontend: http://localhost:3000/
- ✅ Login: Working
- ✅ User Management: Working

## 🔑 Login Credentials
```
Username: admin
Password: admin123
```

## 📋 Quick Commands

### Start Backend
```bash
cd backend
python manage.py runserver
```

### Start Frontend
```bash
cd frontend
npm run dev
```

### Reset Admin Password
```bash
cd backend
python reset_admin_password.py
```

### Create New Superuser
```bash
cd backend
python manage.py createsuperuser
```

### Test APIs
```bash
cd backend
python test_login.py          # Test login
python test_user_creation.py  # Test user creation
```

## 🌐 Application URLs
- **Home**: http://localhost:3000/
- **Login**: http://localhost:3000/login
- **Dashboard**: http://localhost:3000/ (after login)
- **User Management**: http://localhost:3000/user-management
- **API Docs**: http://localhost:8000/api/

## 📊 Features Available
1. ✅ User Authentication (Login/Logout)
2. ✅ User Management (Create/Edit/Delete users)
3. ✅ Plant Management
4. ✅ Excel File Upload
5. ✅ Report Generation
6. ✅ Monthly Targets
7. ✅ E-Signature Support
8. ✅ Audit Logging

## 🔧 Common Issues & Solutions

### Can't Login
```bash
cd backend
python reset_admin_password.py
```
Then use: admin / admin123

### Backend Not Running
```bash
cd backend
python manage.py runserver
```

### Frontend Not Running
```bash
cd frontend
npm run dev
```

### Port 3000 Already in Use
```powershell
# Find process using port 3000
Get-NetTCPConnection -LocalPort 3000

# Kill the process (replace PID with actual process ID)
Stop-Process -Id <PID> -Force
```

### Port 8000 Already in Use
```powershell
# Find process using port 8000
Get-NetTCPConnection -LocalPort 8000

# Kill the process
Stop-Process -Id <PID> -Force
```

### Database Issues
```bash
cd backend
python manage.py migrate
```

### Clear All Data (Reset Database)
```bash
cd backend
# Delete db.sqlite3 or drop PostgreSQL database
python manage.py migrate
python manage.py createsuperuser
python populate_plants.py
python create_units.py
```

## 📁 Important Files
- `backend/npc_reporting/settings.py` - Django settings
- `backend/reports/auth_views_fixed.py` - Authentication views
- `frontend/src/services/api.js` - API client
- `frontend/.env` - Frontend environment variables
- `backend/.env` - Backend environment variables

## 🗄️ Database Info
- **Type**: PostgreSQL
- **Name**: NPC_REPORTING_SYSTEM
- **User**: postgres
- **Password**: 2002
- **Host**: localhost
- **Port**: 5432

## 👥 User Roles
1. **ADMIN** - Full access to everything
2. **MANAGER** - Can manage reports and users
3. **OPERATOR** - Can create and edit reports
4. **VIEWER** - Read-only access

## 📝 Creating a New User
1. Login as admin
2. Go to User Management
3. Click "Create New User"
4. Fill in the form:
   - Username (required, no spaces)
   - Password (required)
   - Email (optional)
   - Role (ADMIN/MANAGER/OPERATOR/VIEWER)
5. Click "Create User"

## 🔐 Security Notes
⚠️ Current configuration is for **DEVELOPMENT ONLY**

For production:
- Change all default passwords
- Enable CSRF protection
- Enable authentication requirements
- Use HTTPS
- Set DEBUG=False
- Restrict ALLOWED_HOSTS

## 📞 Support
If you encounter issues:
1. Check browser console (F12)
2. Check backend logs
3. Review error messages
4. Restart both servers
5. Clear browser cache

## 🎯 Next Steps
1. ✅ Login to the system
2. ✅ Create additional users
3. ✅ Upload plant data
4. ✅ Generate reports
5. ✅ Configure monthly targets

---

**Last Updated**: May 4, 2026
**System Version**: 1.0.0
**Status**: Development
