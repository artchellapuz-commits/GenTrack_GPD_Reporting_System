# Design Considerations and Best Practices

## Database Design

### Normalization
The database follows Third Normal Form (3NF):
- **Plants table**: Master data for Agus plants (1, 2, 4, 5, 6, 7)
- **Units table**: One-to-many with Plants
- **GenerationReports**: References both Plant and Unit
- **UploadedFiles**: Audit trail with foreign key to Plant

### Why This Design?
1. **Eliminates redundancy**: Plant/unit info stored once
2. **Data integrity**: Foreign keys enforce relationships
3. **Flexibility**: Easy to add new plants or units
4. **Query efficiency**: Indexes on foreign keys
5. **Audit capability**: Complete upload history

### Indexes Strategy
```sql
-- Frequently queried fields
CREATE INDEX idx_generation_reports_plant_date ON generation_reports(plant_id, report_date);
CREATE INDEX idx_generation_reports_date ON generation_reports(report_date);

-- Foreign key indexes (automatic in PostgreSQL)
-- Composite unique constraint
UNIQUE(plant_id, unit_id, report_date)
```

### Calculated Fields
- `capacity_factor` and `availability_factor` calculated on save
- Stored in database for query performance
- Recalculated on update

## Backend Architecture

### Service Layer Pattern
Separates business logic from views:

```python
# Good: Business logic in service
class ExcelImporter:
    def process(self):
        df = self._read_excel()
        self._validate_columns(df)
        self._validate_data(df)
        return self._import_data(df)

# View only handles HTTP
def upload(self, request):
    importer = ExcelImporter(uploaded_file)
    records = importer.process()
    return Response({'records': records})
```

**Benefits**:
- Testable business logic
- Reusable across views
- Clear separation of concerns
- Easier maintenance

### Transaction Management
```python
@transaction.atomic
def _import_data(self, df):
    # All inserts succeed or all fail
    for row in df.iterrows():
        GenerationReport.objects.create(...)
```

**Why?**:
- Data consistency
- Rollback on errors
- No partial imports

### Error Handling Strategy
```python
try:
    importer.process()
    uploaded_file.status = 'COMPLETED'
except ValueError as e:
    uploaded_file.status = 'FAILED'
    uploaded_file.error_message = str(e)
    return Response({'error': str(e)}, status=400)
```

**Levels**:
1. **Validation errors**: Return 400 with details
2. **Not found**: Return 404
3. **Server errors**: Return 500, log details
4. **Business logic errors**: Custom exceptions

## Frontend Architecture

### Component Structure
```
App.vue (Shell)
├── UploadExcel.vue (Upload page)
├── ViewReports.vue (Data viewing)
└── GenerateReport.vue (Report generation)
```

**Principles**:
- Single responsibility per component
- Reusable where possible
- Props down, events up
- API calls in methods, not computed

### State Management
Currently using component state:
```javascript
data() {
  return {
    reports: [],
    filters: {},
    loading: false
  }
}
```

**Future**: Consider Vuex/Pinia for:
- Shared state across components
- User authentication state
- Global configuration

### API Service Pattern
Centralized API calls:
```javascript
// services/api.js
export default {
  getReports(params) {
    return apiClient.get('/generation-reports/', { params });
  }
}

// Component
import api from '@/services/api';
const response = await api.getReports(filters);
```

**Benefits**:
- Single source of truth for endpoints
- Easy to mock for testing
- Consistent error handling
- Interceptors for auth tokens

## Excel Processing

### Import Strategy
1. **Read with pandas**: Fast, handles large files
2. **Validate early**: Fail fast on errors
3. **Normalize data**: Clean column names
4. **Batch insert**: Use transactions
5. **Update on duplicate**: Upsert logic

### Export Strategy
1. **Query efficiently**: Use select_related
2. **Format with openpyxl**: Professional output
3. **Add calculations**: Totals, averages
4. **Style appropriately**: Headers, borders
5. **Stream large files**: Memory efficient

### Validation Rules
```python
REQUIRED_COLUMNS = [
    'date', 'unit_number', 'generation_kwh',
    'operating_hours', 'availability_hours'
]

# Validate data types
df['date'] = pd.to_datetime(df['date'])
df['generation_kwh'] = pd.to_numeric(df['generation_kwh'])

# Validate ranges
assert (df['operating_hours'] >= 0).all()
assert (df['operating_hours'] <= 24).all()
```

## Security Best Practices

### File Upload Security
```python
# 1. Validate file type
if not file.name.endswith('.xlsx'):
    raise ValidationError("Only .xlsx files allowed")

# 2. Limit file size
if file.size > 10485760:  # 10MB
    raise ValidationError("File too large")

# 3. Calculate checksum
checksum = hashlib.sha256(file.read()).hexdigest()

# 4. Check for duplicates
if UploadedFile.objects.filter(checksum=checksum).exists():
    raise ValidationError("File already uploaded")

# 5. Sanitize filename
safe_filename = secure_filename(file.name)
```

### API Security
```python
# settings.py
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}

CORS_ALLOWED_ORIGINS = [
    "http://localhost:8080",  # Development only
]
```

### SQL Injection Prevention
Django ORM automatically escapes queries:
```python
# Safe - parameterized
GenerationReport.objects.filter(plant__code=user_input)

# Unsafe - never do this
GenerationReport.objects.raw(f"SELECT * FROM reports WHERE plant='{user_input}'")
```

## Performance Optimization

### Database Queries
```python
# Bad: N+1 queries
for report in GenerationReport.objects.all():
    print(report.plant.name)  # Query per iteration

# Good: Single query with join
reports = GenerationReport.objects.select_related('plant', 'unit')
for report in reports:
    print(report.plant.name)  # No additional query
```

### Pagination
```python
# settings.py
REST_FRAMEWORK = {
    'PAGE_SIZE': 50,  # Limit results
}

# Returns: {results: [...], next: url, previous: url}
```

### Serializer Optimization
```python
# List view: Minimal fields
class GenerationReportListSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['id', 'date', 'plant_code', 'generation_kwh']

# Detail view: All fields
class GenerationReportSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
```

## Testing Strategy

### Backend Tests
```python
# Unit tests
class ExcelImporterTest(TestCase):
    def test_validate_columns(self):
        # Test validation logic
        
# Integration tests
class UploadAPITest(APITestCase):
    def test_upload_valid_file(self):
        # Test full upload flow
```

### Frontend Tests
```javascript
// Component tests
describe('UploadExcel', () => {
  it('validates file type', () => {
    // Test validation
  });
});

// E2E tests (Cypress)
describe('Upload Flow', () => {
  it('uploads file successfully', () => {
    cy.visit('/upload');
    cy.get('input[type=file]').attachFile('test.xlsx');
    cy.get('button').click();
    cy.contains('Success');
  });
});
```

## Deployment Considerations

### Environment Variables
```bash
# .env
SECRET_KEY=random-secret-key
DEBUG=False
ALLOWED_HOSTS=yourdomain.com
DB_PASSWORD=secure-password
```

### Static Files
```python
# Production settings
STATIC_ROOT = '/var/www/static/'
MEDIA_ROOT = '/var/www/media/'

# Collect static files
python manage.py collectstatic
```

### Database Migrations
```bash
# Always backup before migrating
pg_dump npc_reporting > backup.sql

# Run migrations
python manage.py migrate

# Verify
python manage.py showmigrations
```

### Monitoring
```python
# settings.py
LOGGING = {
    'version': 1,
    'handlers': {
        'file': {
            'class': 'logging.FileHandler',
            'filename': '/var/log/django/npc.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'INFO',
        },
    },
}
```

## Future Enhancements

### 1. Async Processing
```python
# tasks.py
@celery_task
def process_excel_file(uploaded_file_id):
    uploaded_file = UploadedFile.objects.get(id=uploaded_file_id)
    importer = ExcelImporter(uploaded_file)
    importer.process()

# views.py
def upload(self, request):
    uploaded_file = UploadedFile.objects.create(...)
    process_excel_file.delay(uploaded_file.id)
    return Response({'status': 'processing'})
```

### 2. Real-time Updates
```javascript
// WebSocket connection
const ws = new WebSocket('ws://localhost:8000/ws/uploads/');
ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  if (data.status === 'completed') {
    this.loadUploadHistory();
  }
};
```

### 3. Advanced Reporting
- PDF generation with ReportLab
- Charts with Chart.js
- Dashboard with aggregated metrics
- Scheduled reports via Celery Beat

### 4. Data Validation Rules
- Custom validation per plant
- Configurable thresholds
- Anomaly detection
- Data quality scoring

## Maintenance Guidelines

### Code Quality
- Follow PEP 8 (Python)
- Use ESLint (JavaScript)
- Write docstrings
- Keep functions small
- DRY principle

### Documentation
- Update README on changes
- Document API endpoints
- Comment complex logic
- Maintain changelog

### Version Control
- Feature branches
- Pull request reviews
- Semantic versioning
- Tag releases

### Backup Strategy
- Daily database backups
- Backup uploaded files
- Test restore procedures
- Off-site storage
