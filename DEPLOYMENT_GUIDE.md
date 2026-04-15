# NPC Reporting System - Production Deployment

## Overview
This system can be deployed for FREE using the following services:
- **Frontend**: Netlify (free tier - 100GB bandwidth/month)
- **Backend**: Render.com (free tier - 750 hours/month)
- **Database**: Neon PostgreSQL (free tier - 0.5GB storage)

## Quick Start Deployment

### Step 1: Create Free Accounts
1. Sign up for [Netlify](https://netlify.com) - use Bitbucket
2. Sign up for [Render](https://render.com) - use Bitbucket
3. Sign up for [Neon](https://neon.tech) - PostgreSQL database

### Step 2: Set Up Neon Database
1. Go to https://neon.tech and create a free account
2. Create a new project with PostgreSQL
3. Copy the connection string (DATABASE_URL)

### Step 3: Deploy Backend to Render
1. Go to https://render.com and connect your Bitbucket
2. Click "New +" → "Blueprint"
3. Select your repository
4. Render will auto-detect `render.yaml` - just configure:
   - Add `DATABASE_URL` from Neon
   - Add `SECRET_KEY` (generate a secure random key)
   - Set `DEBUG=False`

### Step 4: Deploy Frontend to Netlify
1. Go to https://netlify.com and connect your Bitbucket
2. Click "Add new site" → "Import an existing project"
3. Select your repository
4. Configure build settings:
   - Build command: `npm run build`
   - Publish directory: `frontend/dist`
5. Add environment variable:
   - `VUE_APP_API_URL` = your Render backend URL (e.g., `https://npc-reporting-backend.onrender.com/api`)

### Step 5: Configure CORS
Update your Django `settings.py` to allow your Netlify URL:
```python
CORS_ALLOWED_ORIGINS = [
    "https://npc-reporting-frontend.netlify.app",
]
```

## Alternative: All-in-One with Vercel

If you want simpler deployment, consider using **Vercel** for frontend and **Railway** for backend:
1. Frontend: Deploy `frontend/` to Vercel
2. Backend: Deploy `backend/` to Railway

## Important Notes

### Security
- Change `SECRET_KEY` in production!
- Use environment variables for all sensitive data
- Enable HTTPS (automatic on Netlify/Render)

### Database
- SQLite works for small projects but PostgreSQL is recommended
- Neon free tier provides 0.5GB storage
- Render provides free PostgreSQL with paid plans

### Performance
- Free tier services may sleep after inactivity
- First request after sleep may take 30-60 seconds
- Consider upgrading for production use

## Troubleshooting

### CORS Errors
- Make sure your backend ALLOWED_HOSTS includes your frontend URL
- Check CORS_ALLOWED_ORIGINS in settings

### Database Connection
- Verify DATABASE_URL is correctly set
- Check Neon dashboard for connection issues

### Build Failures
- Check package.json scripts are correct
- Ensure all dependencies are in requirements.txt
