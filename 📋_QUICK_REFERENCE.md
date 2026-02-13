# 📋 NPC Reporting System - Quick Reference

## 🚀 Start System
```batch
START_SYSTEM.bat
```
Then open: http://localhost:8081

---

## 🔗 Important URLs

| Service | URL | Purpose |
|---------|-----|---------|
| Frontend | http://localhost:8081 | Main application |
| Backend API | http://localhost:8000/api/ | REST API |
| Admin Panel | http://localhost:8000/admin | Django admin |
| Network Access | http://192.168.120.87:8081 | Access from other devices |

---

## 📊 System Status

| Component | Status | Count |
|-----------|--------|-------|
| Plants | ✅ | 6 |
| Units | ✅ | 22 |
| Historical Data | ✅ | 9,054 |
| Generation Reports | ✅ | 180 |
| Total Records | ✅ | 9,234 |

---

## 🏭 Plants

| Code | Name | Capacity | Units | Location |
|------|------|----------|-------|----------|
| AGUS1 | Agus 1 Hydroelectric | 100 MW | 4 | Lanao del Sur |
| AGUS2 | Agus 2 Hydroelectric | 180 MW | 4 | Lanao del Sur |
| AGUS4 | Agus 4 Hydroelectric | 200 MW | 4 | Lanao del Norte |
| AGUS5 | Agus 5 Hydroelectric | 52 MW | 2 | Lanao del Norte |
| AGUS6 | Agus 6 Hydroelectric | 200 MW | 4 | Lanao del Norte |
| AGUS7 | Agus 7 Hydroelectric | 200 MW | 4 | Lanao del Norte |

**Total**: 932 MW, 22 Units

---

## 🎯 Common Tasks

### Upload Excel File
1. Open http://localhost:8081
2. Click "Upload Excel"
3. Select plant
4. Choose file
5. Click "Upload"

### View Reports
1. Click "View Reports"
2. Select filters (plant, date range)
3. Click "Search"
4. Browse results

### Generate Report
1. Click "Generate Report"
2. Set date range
3. Select plant(s)
4. Click "Generate"
5. Download Excel

### View Historical Data
1. Click "View Reports"
2. Select plant
3. Set date range (e.g., 2024-01-01 to 2024-12-31)
4. Browse 9,054 records

---

## 📁 Sample Files

Located in `npc-reporting-system/backend/`:

- `CORRECT_SAMPLE_AGUS1.xlsx` - Clean sample
- `SAMPLE_AGUS4_30DAYS.xlsx` - 30 days
- `SAMPLE_AGUS5_45DAYS.xlsx` - 45 days
- `SAMPLE_AGUS6_60DAYS.xlsx` - 60 days
- `SAMPLE_AGUS7_15DAYS.xlsx` - 15 days

---

## 🔧 Useful Commands

### Start Backend
```batch
cd backend
.\venv\Scripts\activate
python manage.py runserver
```

### Start Frontend
```batch
cd frontend
npm run serve
```

### Check Database
```batch
cd backend
.\venv\Scripts\activate
python manage.py shell
```
Then:
```python
from reports.models import Plant, HistoricalData
print(Plant.objects.count())  # 6
print(HistoricalData.objects.count())  # 9054
```

### Verify System
```batch
VERIFY_SYSTEM.bat
```

---

## 🌐 API Endpoints

### Plants
- `GET /api/plants/` - List all plants
- `GET /api/plants/{id}/` - Get plant details

### Units
- `GET /api/units/` - List all units
- `GET /api/units/?plant_code=AGUS1` - Filter by plant

### Historical Data
- `GET /api/historical-data/` - List records
- `GET /api/historical-data/?plant_code=AGUS1&start_date=2024-01-01`

### Generation Reports
- `GET /api/generation-reports/` - List reports
- `GET /api/generation-reports/?plant_code=AGUS1`
- `POST /api/generation-reports/generate_report/` - Generate Excel

### Upload
- `POST /api/uploaded-files/upload/` - Upload Excel file

---

## 📖 Documentation

| File | Purpose |
|------|---------|
| `🎉_SYSTEM_READY.md` | Getting started guide |
| `SYSTEM_STATUS.md` | Current system status |
| `README.md` | Project overview |
| `ARCHITECTURE.md` | System architecture |
| `API_DOCUMENTATION.md` | API reference |
| `SETUP_GUIDE.md` | Setup instructions |
| `EXCEL_FORMAT_GUIDE.md` | Excel format specs |

---

## 🆘 Troubleshooting

### Backend Not Starting
```batch
cd backend
.\venv\Scripts\activate
python manage.py runserver
```

### Frontend Not Starting
```batch
cd frontend
npm run serve
```

### Can't Access Application
- Check both servers are running
- Try http://localhost:8081
- Check firewall settings

### Port Already in Use
- Backend: `python manage.py runserver 8001`
- Frontend: Will auto-use 8082 if 8081 is busy

---

## ✅ System Requirements

- ✅ Python 3.14.3
- ✅ Node.js v25.6.0
- ✅ Django 6.0.2
- ✅ Vue.js 3
- ✅ SQLite database

---

## 🎉 Quick Start

1. Run `START_SYSTEM.bat`
2. Wait 10-15 seconds
3. Open http://localhost:8081
4. Start using the system!

---

**Status**: ✅ Fully Operational  
**Data**: 9,234 records loaded  
**Ready**: YES 🚀

