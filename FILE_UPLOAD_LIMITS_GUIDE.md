# File Upload Limits Guide

## Current Configuration

**Maximum Upload Size: 25MB**

This limit is configured in both frontend and backend:
- Frontend: `frontend/src/components/UploadExcel.vue`
- Backend: `backend/npc_reporting/settings.py`

## Why File Size Limits Matter

### 1. Memory Usage
**Impact:** Each uploaded file is loaded into server memory for processing.

**Considerations:**
- 25MB file = ~25MB RAM usage during upload
- Multiple simultaneous uploads multiply memory usage
- Example: 4 users uploading 25MB files = 100MB RAM

**Recommendation:**
- For 25MB limit: Ensure server has at least 2GB RAM
- For 50MB limit: Ensure server has at least 4GB RAM
- For 100MB limit: Ensure server has at least 8GB RAM

### 2. Processing Time
**Impact:** Larger files take longer to process.

**Typical Processing Times:**
- 1MB Excel file: 1-3 seconds
- 10MB Excel file: 5-15 seconds
- 25MB Excel file: 15-45 seconds
- 50MB Excel file: 30-90 seconds
- 100MB Excel file: 60-180 seconds

**Factors Affecting Speed:**
- Number of rows in Excel
- Number of columns
- Formula complexity
- Server CPU speed
- Database write speed

### 3. Network Transfer
**Impact:** Upload time depends on network speed.

**Upload Times (approximate):**

**Fast Connection (10 Mbps):**
- 10MB: 8 seconds
- 25MB: 20 seconds
- 50MB: 40 seconds
- 100MB: 80 seconds

**Moderate Connection (5 Mbps):**
- 10MB: 16 seconds
- 25MB: 40 seconds
- 50MB: 80 seconds
- 100MB: 160 seconds

**Slow Connection (1 Mbps):**
- 10MB: 80 seconds
- 25MB: 200 seconds (3.3 minutes)
- 50MB: 400 seconds (6.7 minutes)
- 100MB: 800 seconds (13.3 minutes)

### 4. Database Impact
**Impact:** More data = more database operations.

**Considerations:**
- Each row in Excel = 1 database INSERT
- 1,000 rows = 1,000 database operations
- 10,000 rows = 10,000 database operations
- Large batches can slow down database

**Database Performance:**
- SQLite (development): Good up to 10,000 records/upload
- PostgreSQL (production): Good up to 100,000+ records/upload
- MySQL (production): Good up to 50,000+ records/upload

### 5. User Experience
**Impact:** Long uploads can frustrate users.

**Best Practices:**
- Show progress bar (implemented ✓)
- Display status messages (implemented ✓)
- Allow cancellation (not implemented)
- Provide time estimates (not implemented)

## How to Increase Upload Limit

### Option 1: Increase to 50MB

**Frontend Changes:**
```javascript
// In UploadExcel.vue
const maxSize = 50 * 1024 * 1024; // 50MB
```

**Backend Changes:**
```python
# In settings.py
DATA_UPLOAD_MAX_MEMORY_SIZE = 52428800  # 50MB
FILE_UPLOAD_MAX_MEMORY_SIZE = 52428800  # 50MB
```

**Server Requirements:**
- Minimum 4GB RAM
- Good CPU (2+ cores)
- Fast disk I/O

### Option 2: Increase to 100MB

**Frontend Changes:**
```javascript
// In UploadExcel.vue
const maxSize = 100 * 1024 * 1024; // 100MB
```

**Backend Changes:**
```python
# In settings.py
DATA_UPLOAD_MAX_MEMORY_SIZE = 104857600  # 100MB
FILE_UPLOAD_MAX_MEMORY_SIZE = 104857600  # 100MB
```

**Server Requirements:**
- Minimum 8GB RAM
- Good CPU (4+ cores)
- SSD storage recommended
- Consider PostgreSQL instead of SQLite

### Option 3: No Limit (Not Recommended)

**Frontend Changes:**
```javascript
// In UploadExcel.vue
// Remove or comment out size check
// if (file.size > maxSize) { ... }
```

**Backend Changes:**
```python
# In settings.py
DATA_UPLOAD_MAX_MEMORY_SIZE = None  # No limit
FILE_UPLOAD_MAX_MEMORY_SIZE = None  # No limit
```

**⚠️ Risks:**
- Server can run out of memory
- Very slow processing
- Potential crashes
- Poor user experience

## Recommended Limits by Use Case

### Small Organization (1-10 users)
**Recommended: 25MB**
- Handles typical monthly reports
- Good balance of size and performance
- Works on modest hardware

### Medium Organization (10-50 users)
**Recommended: 50MB**
- Handles larger datasets
- Supports annual reports
- Requires better hardware

### Large Organization (50+ users)
**Recommended: 100MB with optimization**
- Implement chunked uploads
- Use background processing (Celery)
- Upgrade to PostgreSQL
- Use dedicated server

## Performance Optimization Tips

### 1. Batch Processing
Instead of processing all rows at once, process in batches:
```python
# Process 1000 rows at a time
batch_size = 1000
for i in range(0, len(rows), batch_size):
    batch = rows[i:i+batch_size]
    process_batch(batch)
```

### 2. Background Processing
Use Celery for async processing:
- Upload file immediately
- Process in background
- Notify user when complete
- User can continue working

### 3. Database Optimization
- Use bulk_create() instead of individual saves
- Add database indexes
- Use database transactions
- Optimize queries

### 4. File Validation
Validate before processing:
- Check file format
- Check column headers
- Check data types
- Reject invalid files early

## Monitoring and Alerts

### What to Monitor
1. **Upload Success Rate**
   - Track failed uploads
   - Identify common errors
   - Fix issues proactively

2. **Processing Time**
   - Average time per file
   - Identify slow uploads
   - Optimize bottlenecks

3. **Server Resources**
   - Memory usage
   - CPU usage
   - Disk space
   - Network bandwidth

4. **Database Performance**
   - Query execution time
   - Connection pool usage
   - Lock contention

### Alert Thresholds
- Memory usage > 80%
- Processing time > 2 minutes
- Upload failure rate > 5%
- Database response time > 1 second

## Troubleshooting

### Problem: Upload Fails with Large Files
**Solutions:**
1. Increase server memory
2. Increase upload limits
3. Optimize processing code
4. Use background processing

### Problem: Slow Upload Speed
**Solutions:**
1. Check network connection
2. Reduce file size
3. Compress data
4. Use faster server

### Problem: Server Crashes During Upload
**Solutions:**
1. Increase server memory
2. Reduce upload limit
3. Implement rate limiting
4. Add error handling

### Problem: Database Timeout
**Solutions:**
1. Increase database timeout
2. Use batch processing
3. Optimize database queries
4. Add database indexes

## Best Practices

### For Users
1. **Prepare Files Properly**
   - Remove unnecessary columns
   - Remove empty rows
   - Use correct format
   - Compress if possible

2. **Upload During Off-Peak Hours**
   - Less server load
   - Faster processing
   - Better experience

3. **Split Large Files**
   - Upload in smaller chunks
   - Easier to manage
   - Faster processing

### For Administrators
1. **Regular Monitoring**
   - Check server resources
   - Review error logs
   - Monitor performance

2. **Regular Maintenance**
   - Clean old uploads
   - Optimize database
   - Update software

3. **Capacity Planning**
   - Estimate growth
   - Plan upgrades
   - Budget for hardware

## Conclusion

**Current 25MB limit is appropriate for:**
- Typical monthly reports (500-5,000 rows)
- Small to medium organizations
- Standard server hardware
- Good balance of functionality and performance

**Consider increasing to 50MB if:**
- Users regularly upload large datasets
- Server has adequate resources (4GB+ RAM)
- Processing time is acceptable
- Network speed is good

**Consider 100MB+ only if:**
- Dedicated high-performance server
- Background processing implemented
- PostgreSQL database
- Professional monitoring in place

## Support

For questions or issues with file uploads:
1. Check this guide first
2. Review error messages
3. Check server logs
4. Contact system administrator
