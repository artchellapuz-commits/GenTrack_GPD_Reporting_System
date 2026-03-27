# Production Deployment Guide

## You've Built the Production Files! Now What?

After running `npm run build`, your optimized production files are in `frontend/dist/`. Here's how to serve them:

---

## Quick Start Options

### Option 1: Python HTTP Server (Simplest)
```cmd
# Run this batch file
SERVE_PRODUCTION.bat
```

**OR manually:**
```cmd
cd frontend\dist
python -m http.server 8080
```

**Pros:** No installation needed, works immediately
**Cons:** Doesn't handle SPA routing well (404 on refresh)

---

### Option 2: Node.js `serve` Package (Recommended for Testing)
```cmd
# Run this batch file
SERVE_WITH_NODE.bat
```

**OR manually:**
```cmd
# Install serve globally (one time)
npm install -g serve

# Serve the dist folder
cd frontend
serve -s dist -l 8080
```

**Pros:** Handles SPA routing correctly, fast
**Cons:** Requires Node.js

---

### Option 3: Complete Production System (Best for Local Production)
```cmd
# Run this batch file
START_PRODUCTION.bat
```

This starts both:
- Backend on http://localhost:8000
- Frontend on http://localhost:8080

---

### Option 4: Django Serves Everything (All-in-One)

Copy the built files to Django's static folder:

```cmd
# 1. Copy dist files to Django
xcopy /E /I /Y frontend\dist backend\staticfiles\frontend

# 2. Update Django URLs to serve frontend
# (See configuration below)

# 3. Start Django only
cd backend
venv\Scripts\activate
python manage.py runserver
```

Then access everything at http://localhost:8000

---

## Production Server Setup (Real Deployment)

### Using Nginx (Recommended)

1. **Install Nginx** on your server

2. **Configure Nginx** (`/etc/nginx/sites-available/npc-reporting`):

```nginx
server {
    listen 80;
    server_name your-domain.com;

    # Frontend - Serve Vue.js dist files
    location / {
        root /path/to/npc-reporting-system/frontend/dist;
        try_files $uri $uri/ /index.html;
    }

    # Backend API - Proxy to Django
    location /api/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Django Admin
    location /admin/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    # Media files
    location /media/ {
        alias /path/to/npc-reporting-system/backend/media/;
    }

    # Static files
    location /static/ {
        alias /path/to/npc-reporting-system/backend/staticfiles/;
    }
}
```

3. **Run Django with Gunicorn**:

```bash
# Install Gunicorn
pip install gunicorn

# Run Django
cd backend
gunicorn npc_reporting.wsgi:application --bind 127.0.0.1:8000 --workers 4
```

4. **Enable and start Nginx**:

```bash
sudo ln -s /etc/nginx/sites-available/npc-reporting /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

---

## Environment Configuration

### Frontend (.env for production build)

Before building, update `frontend/.env`:

```env
VUE_APP_API_URL=http://your-domain.com/api
```

Then rebuild:
```cmd
cd frontend
npm run build
```

### Backend (settings.py for production)

Update `backend/npc_reporting/settings.py`:

```python
DEBUG = False
ALLOWED_HOSTS = ['your-domain.com', 'www.your-domain.com']

# CORS for production
CORS_ALLOWED_ORIGINS = [
    "http://your-domain.com",
    "https://your-domain.com",
]
```

---

## Testing Your Production Build

1. **Start Backend**:
```cmd
cd backend
venv\Scripts\activate
python manage.py runserver
```

2. **Serve Frontend** (choose one):
```cmd
# Option A: Python
cd frontend\dist
python -m http.server 8080

# Option B: Node serve
cd frontend
serve -s dist -l 8080

# Option C: Use batch file
START_PRODUCTION.bat
```

3. **Test**:
- Open http://localhost:8080
- Login and test features
- Check browser console for errors
- Verify API calls work

---

## Common Issues

### Issue: 404 on Page Refresh

**Problem:** Direct navigation to routes like `/dashboard` returns 404

**Solution:** Use `serve -s` or configure your server for SPA:
```cmd
serve -s dist -l 8080
```

### Issue: API Calls Fail

**Problem:** CORS errors or connection refused

**Solution:** 
1. Ensure backend is running
2. Check `VUE_APP_API_URL` in frontend
3. Verify CORS settings in Django

### Issue: Static Files Not Loading

**Problem:** CSS/JS files return 404

**Solution:**
```cmd
cd backend
python manage.py collectstatic --noinput
```

---

## Performance Optimization

### 1. Enable Gzip Compression (Nginx)

```nginx
gzip on;
gzip_types text/plain text/css application/json application/javascript text/xml application/xml;
gzip_min_length 1000;
```

### 2. Enable Caching (Nginx)

```nginx
location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg)$ {
    expires 1y;
    add_header Cache-Control "public, immutable";
}
```

### 3. Use CDN for Large Files

Move videos and large assets to a CDN:
- AWS S3 + CloudFront
- Azure Blob Storage
- Google Cloud Storage

---

## Security Checklist

- [ ] Set `DEBUG = False` in Django
- [ ] Use strong `SECRET_KEY`
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Enable HTTPS (SSL certificate)
- [ ] Set secure CORS origins
- [ ] Use environment variables for secrets
- [ ] Enable Django security middleware
- [ ] Set up firewall rules
- [ ] Regular security updates

---

## Monitoring

### Application Logs

Django logs: `backend/logs/app.log`

```python
# In settings.py
LOGGING = {
    'version': 1,
    'handlers': {
        'file': {
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'logs' / 'app.log',
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

### Server Monitoring

- Use `htop` or `top` for resource monitoring
- Set up log rotation for Django logs
- Monitor Nginx access/error logs

---

## Backup Strategy

### Database Backup

```bash
# PostgreSQL
pg_dump -U postgres npc_reporting > backup_$(date +%Y%m%d).sql

# Restore
psql -U postgres npc_reporting < backup_20260227.sql
```

### Media Files Backup

```bash
# Backup uploaded files
tar -czf media_backup_$(date +%Y%m%d).tar.gz backend/media/
```

---

## Quick Reference

| Task | Command |
|------|---------|
| Build frontend | `cd frontend && npm run build` |
| Serve with Python | `cd frontend/dist && python -m http.server 8080` |
| Serve with Node | `cd frontend && serve -s dist -l 8080` |
| Start production | `START_PRODUCTION.bat` |
| Collect static files | `cd backend && python manage.py collectstatic` |
| Run with Gunicorn | `cd backend && gunicorn npc_reporting.wsgi:application` |

---

## Need Help?

1. Check logs: `backend/logs/app.log`
2. Browser console: F12 → Console tab
3. Network tab: Check API calls
4. Review Django debug output

---

Last Updated: February 2026
