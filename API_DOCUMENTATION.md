# API Documentation - NPC Reporting System

Base URL: `http://localhost:8000/api`

## Authentication

All endpoints require authentication. Use session-based authentication or token authentication.

```javascript
// Example with session auth
axios.defaults.withCredentials = true;
```

## Endpoints

### 1. Plants

#### List All Plants
```
GET /api/plants/
```

**Response:**
```json
[
  {
    "id": 1,
    "code": "AGUS1",
    "name": "Agus 1 Hydroelectric Plant",
    "capacity_mw": "100.00",
    "location": "Lanao del Sur",
    "commissioned_date": "1990-01-01",
    "is_active": true
  }
]
```

---

### 2. Units

#### List All Units
```
GET /api/units/
```

**Query Parameters:**
- `plant_code` (optional): Filter by plant code (e.g., AGUS1)

**Response:**
```json
[
  {
    "id": 1,
    "plant": 1,
    "plant_name": "Agus 1 Hydroelectric Plant",
    "unit_number": 1,
    "capacity_mw": "25.00",
    "is_active": true
  }
]
```

---

### 3. Upload Excel File

#### Upload File
```
POST /api/uploaded-files/upload/
```

**Request:**
- Content-Type: `multipart/form-data`
- Body:
  - `file`: Excel file (.xlsx)
  - `plant_code`: Plant code (AGUS1-AGUS7)

**Example:**
```javascript
const formData = new FormData();
formData.append('file', fileObject);
formData.append('plant_code', 'AGUS1');

axios.post('/api/uploaded-files/upload/', formData, {
  headers: { 'Content-Type': 'multipart/form-data' }
});
```

**Success Response (201):**
```json
{
  "message": "File uploaded and processed successfully",
  "records_imported": 150,
  "file_id": 42
}
```

**Error Response (400):**
```json
{
  "error": "Validation errors: Missing required columns: generation_kwh"
}
```

---

### 4. Uploaded Files History

#### List Uploaded Files
```
GET /api/uploaded-files/
```

**Response:**
```json
{
  "count": 10,
  "next": "http://localhost:8000/api/uploaded-files/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "original_filename": "agus1_january.xlsx",
      "plant": 1,
      "plant_name": "Agus 1 Hydroelectric Plant",
      "uploaded_by": 1,
      "uploaded_by_username": "admin",
      "uploaded_at": "2024-01-15T10:30:00Z",
      "status": "COMPLETED",
      "records_imported": 150,
      "file_size": 45678
    }
  ]
}
```

---

### 5. Generation Reports

#### List Reports
```
GET /api/generation-reports/
```

**Query Parameters:**
- `plant_code`: Filter by plant (can be multiple: `?plant_code=AGUS1&plant_code=AGUS2`)
- `start_date`: Filter from date (YYYY-MM-DD)
- `end_date`: Filter to date (YYYY-MM-DD)
- `unit_id`: Filter by unit ID
- `page`: Page number for pagination

**Example:**
```
GET /api/generation-reports/?plant_code=AGUS1&start_date=2024-01-01&end_date=2024-01-31&page=1
```

**Response:**
```json
{
  "count": 150,
  "next": "http://localhost:8000/api/generation-reports/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "plant_code": "AGUS1",
      "unit_number": 1,
      "report_date": "2024-01-15",
      "generation_kwh": "500000.00",
      "operating_hours": "23.50",
      "capacity_factor": "85.42",
      "availability_factor": "97.92"
    }
  ]
}
```

#### Get Report Summary
```
GET /api/generation-reports/summary/
```

**Query Parameters:** Same as list reports

**Response:**
```json
{
  "total_generation": "15000000.00",
  "avg_capacity_factor": "82.50",
  "avg_availability_factor": "95.30",
  "total_operating_hours": "3540.00",
  "total_forced_outage_hours": "120.00"
}
```

#### Generate Excel Report
```
POST /api/generation-reports/generate_report/
```

**Request Body:**
```json
{
  "plant_codes": ["AGUS1", "AGUS2"],
  "start_date": "2024-01-01",
  "end_date": "2024-01-31",
  "report_type": "psr"
}
```

**Report Types:**
- `psr`: Plant Status Report (PSR) - Official PSR format for Mindanao plants

**Response:**
- Content-Type: `application/vnd.openxmlformats-officedocument.spreadsheetml.sheet`
- Binary Excel file

**Example:**
```javascript
axios.post('/api/generation-reports/generate_report/', data, {
  responseType: 'blob'
}).then(response => {
  const url = window.URL.createObjectURL(new Blob([response.data]));
  const link = document.createElement('a');
  link.href = url;
  link.setAttribute('download', 'report.xlsx');
  document.body.appendChild(link);
  link.click();
});
```

---

## Error Responses

### 400 Bad Request
```json
{
  "error": "Validation error message",
  "field_errors": {
    "plant_code": ["This field is required."]
  }
}
```

### 401 Unauthorized
```json
{
  "detail": "Authentication credentials were not provided."
}
```

### 404 Not Found
```json
{
  "error": "No data found for the specified criteria"
}
```

### 500 Internal Server Error
```json
{
  "error": "An unexpected error occurred"
}
```

---

## Excel File Format Requirements

### Required Columns
| Column Name | Type | Description | Validation |
|------------|------|-------------|------------|
| date | Date | Report date | YYYY-MM-DD format |
| unit_number | Integer | Unit number | Must exist in database |
| generation_kwh | Decimal | Generation in kWh | Non-negative |
| operating_hours | Decimal | Operating hours | 0-24 |
| availability_hours | Decimal | Availability hours | 0-24 |
| forced_outage_hours | Decimal | Forced outage hours | 0-24 |
| scheduled_outage_hours | Decimal | Scheduled outage hours | 0-24 |
| remarks | Text | Optional remarks | Optional |

### Example Excel Data

| date | unit_number | generation_kwh | operating_hours | availability_hours | forced_outage_hours | scheduled_outage_hours | remarks |
|------|-------------|----------------|-----------------|-------------------|---------------------|----------------------|---------|
| 2024-01-15 | 1 | 500000 | 23.5 | 23.5 | 0.5 | 0 | Normal operation |
| 2024-01-15 | 2 | 480000 | 22.0 | 24.0 | 2.0 | 0 | Minor issue |

---

## Rate Limiting

Currently no rate limiting is implemented. For production, consider:
- 100 requests per minute per user
- 10 file uploads per hour per user

---

## Pagination

All list endpoints use pagination:
- Default page size: 50 items
- Maximum page size: 100 items
- Use `?page=2` to navigate pages

**Response Structure:**
```json
{
  "count": 500,
  "next": "http://localhost:8000/api/endpoint/?page=3",
  "previous": "http://localhost:8000/api/endpoint/?page=1",
  "results": [...]
}
```

---

## CORS Configuration

Allowed origins (development):
- `http://localhost:8080`
- `http://localhost:3000`

For production, update `CORS_ALLOWED_ORIGINS` in settings.py

---

## Testing the API

### Using cURL

```bash
# Login first (if using session auth)
curl -X POST http://localhost:8000/api-auth/login/ \
  -d "username=admin&password=admin123" \
  -c cookies.txt

# List plants
curl -X GET http://localhost:8000/api/plants/ \
  -b cookies.txt

# Upload file
curl -X POST http://localhost:8000/api/uploaded-files/upload/ \
  -F "file=@report.xlsx" \
  -F "plant_code=AGUS1" \
  -b cookies.txt
```

### Using Postman

1. Import collection from `/postman/NPC_API.postman_collection.json`
2. Set environment variables
3. Test endpoints

---

## Versioning

Current version: v1 (implicit)

Future versions will use URL versioning:
- `/api/v1/plants/`
- `/api/v2/plants/`


---

## Historical Data Endpoints

### 1. Historical Data

#### List Historical Data
```
GET /api/historical-data/
```

**Query Parameters:**
- `plant_code` or `plant_code[]` (optional): Filter by plant code(s)
- `start_date` (optional): Filter by start date (YYYY-MM-DD)
- `end_date` (optional): Filter by end date (YYYY-MM-DD)

**Response:**
```json
{
  "count": 100,
  "next": "http://localhost:8000/api/historical-data/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "plant": 1,
      "plant_name": "Agus 1 Hydroelectric Plant",
      "plant_code": "AGUS1",
      "date": "2024-01-01",
      "generation_mwh": "2400.00",
      "availability_percent": "98.50",
      "status": "Operating",
      "remarks": "",
      "sheet_name": "January 2024",
      "created_at": "2026-02-12T09:30:00Z",
      "updated_at": "2026-02-12T09:30:00Z"
    }
  ]
}
```

#### Import Historical Data
```
POST /api/historical-data/import/
```

**Request (multipart/form-data):**
- `capacity_file` (optional): Excel file with plant capacity data
- `historical_file` (optional): Excel file with historical operational data

**Example using cURL:**
```bash
curl -X POST http://localhost:8000/api/historical-data/import/ \
  -F "capacity_file=@0PLANT DEPCAP.xlsx" \
  -F "historical_file=@1DATA APAO.xlsx"
```

**Example using JavaScript:**
```javascript
const formData = new FormData();
formData.append('capacity_file', capacityFile);
formData.append('historical_file', historicalFile);

const response = await axios.post('/api/historical-data/import/', formData, {
  headers: {
    'Content-Type': 'multipart/form-data'
  }
});
```

**Success Response:**
```json
{
  "success": true,
  "total_imported": 150,
  "errors": [],
  "warnings": ["Plant not found: Agus 3"],
  "details": {
    "capacity": {
      "success": true,
      "imported": 6,
      "errors": [],
      "warnings": []
    },
    "historical": {
      "success": true,
      "imported": 144,
      "errors": [],
      "warnings": ["Plant not found: Agus 3"]
    }
  }
}
```

**Error Response:**
```json
{
  "success": false,
  "error": "Invalid file format",
  "imported": 0
}
```

---

### 2. Plant Capacity

#### List Plant Capacity Records
```
GET /api/plant-capacity/
```

**Query Parameters:**
- `plant_code` or `plant_code[]` (optional): Filter by plant code(s)
- `effective_date` (optional): Filter by effective date (YYYY-MM-DD)

**Response:**
```json
{
  "count": 6,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "plant": 1,
      "plant_name": "Agus 1 Hydroelectric Plant",
      "plant_code": "AGUS1",
      "installed_capacity": "100.00",
      "dependable_capacity": "95.00",
      "effective_date": "2024-01-01",
      "remarks": "",
      "created_at": "2026-02-12T09:30:00Z",
      "updated_at": "2026-02-12T09:30:00Z"
    }
  ]
}
```

#### Get Single Capacity Record
```
GET /api/plant-capacity/{id}/
```

**Response:**
```json
{
  "id": 1,
  "plant": 1,
  "plant_name": "Agus 1 Hydroelectric Plant",
  "plant_code": "AGUS1",
  "installed_capacity": "100.00",
  "dependable_capacity": "95.00",
  "effective_date": "2024-01-01",
  "remarks": "",
  "created_at": "2026-02-12T09:30:00Z",
  "updated_at": "2026-02-12T09:30:00Z"
}
```

---

## Excel File Formats

### Plant Capacity File (0PLANT DEPCAP.xlsx)

Expected columns:
- `Plant Name` - Name of the plant
- `Installed Capacity (MW)` - Total installed capacity
- `Dependable Capacity (MW)` - Dependable capacity
- `Type` - Plant type (Hydro/Thermal/etc.)
- `Location` - Plant location (optional)

### Historical Data File (1DATA APAO.xlsx)

Expected columns:
- `Date` or `DATE` - Report date
- `Plant Name` or `PLANT` - Plant name
- `Generation (MWh)` - Generation in MWh
- `Availability (%)` - Availability percentage
- `Status` - Operating status (optional)
- `Remarks` - Additional remarks (optional)

Multiple sheets are supported for different time periods.

---

## Usage Examples

### Fetch Historical Data for a Plant

```javascript
// Get historical data for Agus 1 in 2024
const response = await axios.get('/api/historical-data/', {
  params: {
    plant_code: 'AGUS1',
    start_date: '2024-01-01',
    end_date: '2024-12-31'
  }
});

const historicalData = response.data.results;
```

### Import Historical Data

```javascript
// Import historical data files
const importHistoricalData = async (capacityFile, historicalFile) => {
  const formData = new FormData();
  
  if (capacityFile) {
    formData.append('capacity_file', capacityFile);
  }
  
  if (historicalFile) {
    formData.append('historical_file', historicalFile);
  }
  
  try {
    const response = await axios.post('/api/historical-data/import/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });
    
    console.log(`Imported ${response.data.total_imported} records`);
    
    if (response.data.warnings.length > 0) {
      console.warn('Warnings:', response.data.warnings);
    }
    
    return response.data;
  } catch (error) {
    console.error('Import failed:', error.response.data);
    throw error;
  }
};
```

### Get Plant Capacity History

```javascript
// Get capacity records for all plants
const response = await axios.get('/api/plant-capacity/');
const capacityRecords = response.data.results;

// Group by plant
const capacityByPlant = capacityRecords.reduce((acc, record) => {
  if (!acc[record.plant_code]) {
    acc[record.plant_code] = [];
  }
  acc[record.plant_code].push(record);
  return acc;
}, {});
```

---

## Error Handling

All endpoints return appropriate HTTP status codes:

- `200 OK` - Request successful
- `201 Created` - Resource created successfully
- `400 Bad Request` - Invalid request parameters
- `404 Not Found` - Resource not found
- `500 Internal Server Error` - Server error

Error responses include a message:

```json
{
  "error": "Description of the error"
}
```

For validation errors:

```json
{
  "field_name": ["Error message for this field"]
}
```
