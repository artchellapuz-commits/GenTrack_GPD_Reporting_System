# System Architecture - NPC Reporting System

## Overview

The NPC Reporting System is a three-tier web application designed to manage generation reports for Agus Hydroelectric Plants (1, 2, 4, 5, 6, 7).

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                     Presentation Layer                       │
│                                                               │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              Vue.js Frontend (SPA)                   │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────────────┐  │   │
│  │  │  Upload  │  │   View   │  │     Generate     │  │   │
│  │  │Component │  │ Reports  │  │  Report Component│  │   │
│  │  └──────────┘  └──────────┘  └──────────────────┘  │   │
│  │                                                       │   │
│  │              API Service (Axios)                     │   │
│  └─────────────────────────────────────────────────────┘   │
└───────────────────────────┬─────────────────────────────────┘
                            │ HTTP/REST API
                            │ (JSON)
┌───────────────────────────▼─────────────────────────────────┐
│                     Application Layer                        │
│                                                               │
│  ┌─────────────────────────────────────────────────────┐   │
│  │         Django REST Framework Backend               │   │
│  │                                                       │   │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────┐  │   │
│  │  │   ViewSets   │  │ Serializers  │  │  Models  │  │   │
│  │  └──────────────┘  └──────────────┘  └──────────┘  │   │
│  │                                                       │   │
│  │  ┌──────────────────────────────────────────────┐  │   │
│  │  │          Service Layer                       │  │   │
│  │  │  ┌──────────────┐  ┌──────────────────────┐ │  │   │
│  │  │  │ExcelImporter │  │   ExcelExporter      │ │  │   │
│  │  │  └──────────────┘  └──────────────────────┘ │  │   │
│  │  └──────────────────────────────────────────────┘  │   │
│  └─────────────────────────────────────────────────────┘   │
└───────────────────────────┬─────────────────────────────────┘
                            │ Django ORM
                            │ (SQL)
┌───────────────────────────▼─────────────────────────────────┐
│                       Data Layer                             │
│                                                               │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              PostgreSQL Database                     │   │
│  │                                                       │   │
│  │  ┌────────┐  ┌────────┐  ┌──────────────┐  ┌─────┐│   │
│  │  │ Plants │  │ Units  │  │ Uploaded     │  │Gen. ││   │
│  │  │        │  │        │  │ Files        │  │Rpts ││   │
│  │  └────────┘  └────────┘  └──────────────┘  └─────┘│   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

## Component Details

### 1. Frontend Layer (Vue.js)

**Technology**: Vue.js 3 with Vue Router

**Components**:
- `UploadExcel.vue` - File upload interface
- `ViewReports.vue` - Data viewing and filtering
- `GenerateReport.vue` - Report generation interface
- `App.vue` - Main application shell

**Responsibilities**:
- User interface rendering
- Form validation
- API communication via Axios
- File upload/download handling
- Client-side routing

**Communication**: REST API calls to Django backend

### 2. Backend Layer (Django)

**Technology**: Django 4.2 + Django REST Framework

**Components**:

#### ViewSets
- `PlantViewSet` - Plant CRUD operations
- `UnitViewSet` - Unit CRUD operations
- `UploadedFileViewSet` - File upload handling
- `GenerationReportViewSet` - Report data operations

#### Serializers
- Data validation
- JSON serialization/deserialization
- Nested relationships

#### Models
- `Plant` - Plant master data
- `Unit` - Unit master data
- `UploadedFile` - Upload audit trail
- `GenerationReport` - Generation data records

#### Service Layer
- `ExcelImporter` - Excel file processing and validation
- `ExcelExporter` - Report generation logic

**Responsibilities**:
- Business logic execution
- Data validation
- Excel file processing
- API endpoint exposure
- Authentication/authorization
- Error handling

### 3. Database Layer (PostgreSQL)

**Technology**: PostgreSQL 13+

**Schema Design**:

```sql
plants (1) ──< (M) units
   │                  │
   │                  │
   ├──< uploaded_files
   │         │
   │         │
   └──< generation_reports >──┘
```

**Key Features**:
- Normalized schema (3NF)
- Foreign key constraints
- Unique constraints
- Indexes for performance
- Audit timestamps

## Data Flow

### Excel Upload Flow

```
1. User selects file + plant → Vue Component
2. FormData created → API Service
3. POST /api/uploaded-files/upload/ → Django View
4. File saved to media folder → UploadedFile model
5. ExcelImporter.process() → Service Layer
   - Read Excel with pandas
   - Validate columns and data
   - Check for duplicates
   - Calculate checksums
6. Bulk insert → GenerationReport model
7. Update UploadedFile status → Database
8. Return success response → Frontend
9. Display confirmation → User
```

### Report Generation Flow

```
1. User selects filters → GenerateReport Component
2. POST /api/generation-reports/generate_report/ → Django View
3. Query database with filters → ORM
4. ExcelExporter.generate() → Service Layer
   - Create workbook with openpyxl
   - Format headers and data
   - Add calculations/totals
   - Apply styling
5. Save to media/exports/ → File System
6. Return file as blob → HTTP Response
7. Browser downloads file → User
```

### Data Query Flow

```
1. User applies filters → ViewReports Component
2. GET /api/generation-reports/?params → Django View
3. Apply filters to queryset → ORM
4. Serialize data → Serializer
5. Paginate results → DRF Pagination
6. Return JSON → Frontend
7. Render table → Component
```

## Security Considerations

### Authentication
- Session-based authentication
- CSRF protection enabled
- User authentication required for all operations

### File Upload Security
- File type validation (.xlsx only)
- File size limits (10MB)
- SHA-256 checksum for duplicate detection
- Secure file storage in media folder
- Filename sanitization

### API Security
- CORS configuration for frontend origin
- Input validation via serializers
- SQL injection prevention (ORM)
- XSS prevention (Vue.js escaping)

## Performance Optimizations

### Database
- Indexes on frequently queried fields
- `select_related()` for foreign keys
- Pagination for large datasets
- Unique constraints prevent duplicates

### Backend
- Transaction management for bulk imports
- Efficient pandas operations
- Lazy evaluation of querysets
- Optimized serializers for list views

### Frontend
- Component-based architecture
- Lazy loading of routes
- Efficient re-rendering
- API response caching (future)

## Scalability Considerations

### Current Design
- Handles moderate file sizes (<10MB)
- Synchronous processing
- Single server deployment

### Future Enhancements
1. **Async Processing**: Celery + Redis for large files
2. **Caching**: Redis for frequently accessed data
3. **Load Balancing**: Multiple Django instances
4. **Database**: Read replicas for reporting
5. **File Storage**: S3 or cloud storage
6. **CDN**: Static asset delivery

## Deployment Architecture

### Development
```
Frontend: npm run serve (localhost:8080)
Backend: python manage.py runserver (localhost:8000)
Database: PostgreSQL (localhost:5432)
```

### Production (Recommended)
```
Frontend: Nginx serving built Vue.js app
Backend: Gunicorn + Nginx reverse proxy
Database: PostgreSQL with connection pooling
Static Files: Nginx or CDN
Media Files: S3 or local storage with backup
```

## Error Handling Strategy

### Frontend
- Try-catch blocks for API calls
- User-friendly error messages
- Loading states during operations
- Form validation before submission

### Backend
- Exception handling in views
- Validation errors in serializers
- Transaction rollback on failures
- Detailed error logging
- Status-appropriate HTTP responses

### Database
- Constraint violations caught
- Transaction management
- Connection error handling
- Backup and recovery procedures

## Monitoring and Logging

### Application Logs
- Django logging configuration
- Request/response logging
- Error tracking
- Performance metrics

### Database Logs
- Query performance
- Slow query identification
- Connection pool monitoring

### Audit Trail
- All file uploads logged
- User actions tracked
- Data modifications recorded
- Timestamp on all records

## Technology Justification

### Django + DRF
- Rapid development
- Built-in ORM
- Excellent REST API support
- Strong security features
- Large ecosystem

### Vue.js
- Reactive UI updates
- Component reusability
- Easy learning curve
- Good documentation
- Active community

### PostgreSQL
- ACID compliance
- Complex query support
- JSON support (future use)
- Excellent performance
- Reliable and mature

### pandas + openpyxl
- Industry standard for Excel
- Powerful data manipulation
- Easy validation
- Format preservation
- Good performance
