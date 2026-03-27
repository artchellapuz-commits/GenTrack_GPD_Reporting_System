# NPC Agus Hydroelectric Plants Reporting System

## System Architecture

```
┌─────────────────┐         ┌──────────────────┐         ┌─────────────────┐
│   Vue.js UI     │────────▶│  Django REST API │────────▶│   PostgreSQL    │
│  (Frontend)     │◀────────│    (Backend)     │◀────────│   (Database)    │
└─────────────────┘         └──────────────────┘         └─────────────────┘
       │                            │
       │                            │
       ▼                            ▼
  User Actions              Excel Processing
  - Upload Excel            - pandas (read)
  - View Data               - openpyxl (write)
  - Generate Reports        - Validation
  - Download Reports        - Data transformation
```

## Project Structure

```
npc-reporting-system/
├── backend/                    # Django project
│   ├── config/                 # Django settings
│   │   ├── __init__.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── apps/
│   │   ├── plants/            # Plant management
│   │   │   ├── models.py
│   │   │   ├── serializers.py
│   │   │   ├── views.py
│   │   │   └── urls.py
│   │   ├── reports/           # Generation reports
│   │   │   ├── models.py
│   │   │   ├── serializers.py
│   │   │   ├── views.py
│   │   │   └── urls.py
│   │   ├── imports/           # Excel import handling
│   │   │   ├── models.py
│   │   │   ├── serializers.py
│   │   │   ├── views.py
│   │   │   ├── validators.py
│   │   │   └── excel_processor.py
│   │   └── exports/           # Report generation
│   │       ├── views.py
│   │       ├── generators.py
│   │       └── formatters.py
│   ├── media/                 # Uploaded files
│   ├── requirements.txt
│   └── manage.py
│
└── frontend/                  # Vue.js project
    ├── src/
    │   ├── components/
    │   │   ├── UploadExcel.vue
    │   │   ├── DataTable.vue
    │   │   ├── ReportGenerator.vue
    │   │   └── PlantSelector.vue
    │   ├── views/
    │   │   ├── Dashboard.vue
    │   │   ├── ImportData.vue
    │   │   ├── ViewData.vue
    │   │   └── GenerateReports.vue
    │   ├── services/
    │   │   └── api.js
    │   ├── router/
    │   │   └── index.js
    │   ├── App.vue
    │   └── main.js
    ├── package.json
    └── vite.config.js
```
