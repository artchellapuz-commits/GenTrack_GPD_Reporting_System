# E-Signature Security - Quick Reference Card

## 🚀 Quick Start (5 Minutes)

```bash
# 1. Install dependencies
cd npc-reporting-system/backend
pip install cryptography pyotp

# 2. Generate keys
python -c "import secrets; print(secrets.token_urlsafe(32))"
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"

# 3. Add to .env
# SIGNATURE_SECRET_KEY=<output-from-step-2-first-command>
# SIGNATURE_ENCRYPTION_KEY=<output-from-step-2-second-command>

# 4. Migrations already applied ✅
# python manage.py migrate

# 5. Start server
python manage.py runserver
```

## 🔑 Key Features

| Feature | Status | Description |
|---------|--------|-------------|
| Authentication | ✅ | Login required for all operations |
| Encryption | ✅ | Fernet symmetric encryption |
| Verification | ✅ | HMAC-SHA256 hash checking |
| 2FA | ✅ | OTP via email |
| Audit Logs | ✅ | Complete activity tracking |
| Rate Limiting | ✅ | 10/hour, 50/day per user |
| Authorizations | ✅ | Control who signs as whom |

## 📡 API Endpoints

### Authentication Required for All

```bash
# Get token
POST /api/auth/login/
Body: {"username": "user", "password": "pass"}
Response: {"access": "token", "refresh": "token"}

# Use token in headers
Authorization: Bearer <access-token>
```

### E-Signatures

```bash
# List signatures (your own)
GET /api/e-signatures/

# Create signature
POST /api/e-signatures/create-from-data/
Body: {
  "signatory_name": "John Doe",
  "signatory_title": "Manager",
  "signatory_role": "Approved by",
  "signature_type": "DRAW",
  "signature_data": "data:image/png;base64,..."
}

# Verify integrity
GET /api/e-signatures/{id}/verify-integrity/
Response: {"is_valid": true, "message": "Signature is valid"}
```

### 2FA Flow

```bash
# Step 1: Request OTP
POST /api/report-signatures/request-2fa/
Body: {
  "signatory_name": "O.M. LAVA",
  "signature_intent": {
    "report_date": "2026-03-16",
    "report_type": "PSR"
  }
}
Response: {"token_id": 1, "message": "Code sent to email"}

# Step 2: Verify OTP (check email)
POST /api/report-signatures/verify-2fa/
Body: {
  "token_id": 1,
  "otp_code": "123456"
}
Response: {"verified": true, "message": "Success"}

# Step 3: Sign with 2FA
POST /api/report-signatures/sign-with-2fa/
Body: {
  "token_id": 1,
  "otp_code": "123456",
  "report_date": "2026-03-16",
  "report_type": "PSR",
  "signature": 5,
  "signatory_name": "O.M. LAVA",
  "signatory_role": "Approved by"
}
```

## 🔐 Admin Tasks

### Grant Signatory Authorization

1. Go to: http://localhost:8000/admin/
2. Navigate to: **Signatory Authorizations**
3. Click: **Add Signatory Authorization**
4. Fill in:
   - User: Select user
   - Signatory name: "O.M. LAVA" (exact match)
   - Is active: ✓
   - Requires 2FA: ✓
5. Save

### View Audit Logs

1. Admin → **Signature Audit Logs**
2. Filter by: User, Action, Success/Failure
3. View details: IP, Device, Timestamp

### Configure Security Settings

1. Admin → **Signature Security Settings**
2. Adjust:
   - 2FA requirements
   - Rate limits
   - Encryption settings
   - Notification preferences

## ⚙️ Configuration

### Environment Variables (.env)

```bash
# Required
SIGNATURE_SECRET_KEY=your-secret-key-here
SIGNATURE_ENCRYPTION_KEY=your-fernet-key-here

# Email (for 2FA)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# Optional (defaults shown)
SIGNATURE_2FA_ENABLED=True
SIGNATURE_OTP_VALIDITY_MINUTES=5
SIGNATURE_MAX_OTP_ATTEMPTS=3
SIGNATURE_RATE_LIMIT_HOUR=10
SIGNATURE_RATE_LIMIT_DAY=50
```

### Gmail Setup for 2FA

1. Enable 2FA: https://myaccount.google.com/security
2. Generate app password: https://myaccount.google.com/apppasswords
3. Use app password in EMAIL_HOST_PASSWORD

## 🐛 Troubleshooting

### Issue: "Authentication credentials were not provided"
**Solution**: Include `Authorization: Bearer <token>` header

### Issue: "You are not authorized to sign as this signatory"
**Solution**: Admin must grant SignatoryAuthorization

### Issue: "Token has expired or maximum attempts reached"
**Solution**: Request new 2FA code

### Issue: "Rate limit exceeded"
**Solution**: Wait or adjust limits in Security Settings

### Issue: 2FA emails not sending
**Solution**: Check EMAIL_* settings in .env

### Issue: Signature verification failed
**Solution**: Ensure SIGNATURE_SECRET_KEY hasn't changed

## 📊 Monitoring

### Key Metrics

```python
# In Django shell
from reports.models import SignatureAuditLog
from datetime import timedelta
from django.utils import timezone

# Failed 2FA attempts (last hour)
hour_ago = timezone.now() - timedelta(hours=1)
failed_2fa = SignatureAuditLog.objects.filter(
    action='2FA_FAILURE',
    timestamp__gte=hour_ago
).count()

# Signatures created today
today = timezone.now().date()
sigs_today = SignatureAuditLog.objects.filter(
    action='CREATE',
    success=True,
    timestamp__date=today
).count()

# Rate limit violations
rate_limit_hits = SignatureAuditLog.objects.filter(
    success=False,
    failure_reason__icontains='rate limit'
).count()
```

## 🔍 Common Commands

```bash
# Check migrations
python manage.py showmigrations reports

# Create superuser
python manage.py createsuperuser

# Django shell
python manage.py shell

# View logs
tail -f logs/app.log

# Test email
python manage.py shell
>>> from django.core.mail import send_mail
>>> send_mail('Test', 'Message', 'from@example.com', ['to@example.com'])
```

## 📱 Frontend Integration

```javascript
// Device fingerprinting
function getDeviceFingerprint() {
  const canvas = document.createElement('canvas');
  const ctx = canvas.getContext('2d');
  ctx.textBaseline = 'top';
  ctx.font = '14px Arial';
  ctx.fillText('Fingerprint', 2, 2);
  
  return {
    canvas: canvas.toDataURL(),
    userAgent: navigator.userAgent,
    language: navigator.language,
    platform: navigator.platform,
    screenResolution: `${screen.width}x${screen.height}`,
    timezone: Intl.DateTimeFormat().resolvedOptions().timeZone
  };
}

// Include in API calls
const response = await fetch('/api/e-signatures/create-from-data/', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    ...signatureData,
    device_fingerprint: JSON.stringify(getDeviceFingerprint())
  })
});
```

## 📋 Security Checklist

- [ ] Generated unique SIGNATURE_SECRET_KEY
- [ ] Generated unique SIGNATURE_ENCRYPTION_KEY
- [ ] Configured email for 2FA
- [ ] Granted signatory authorizations
- [ ] Tested authentication requirement
- [ ] Tested 2FA flow
- [ ] Verified signature integrity check
- [ ] Reviewed audit logs
- [ ] Configured rate limits
- [ ] Set up monitoring
- [ ] Trained users
- [ ] Updated documentation

## 🆘 Emergency Contacts

- **Documentation**: See `SIGNATURE_SECURITY_IMPLEMENTATION_GUIDE.md`
- **Logs**: `backend/logs/app.log`
- **Admin**: http://localhost:8000/admin/
- **API Docs**: http://localhost:8000/api/

## 🎯 Quick Tests

```bash
# Test 1: Auth required
curl http://localhost:8000/api/e-signatures/
# Expected: 401 Unauthorized

# Test 2: Login
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin"}'
# Expected: {"access": "...", "refresh": "..."}

# Test 3: Access with token
curl http://localhost:8000/api/e-signatures/ \
  -H "Authorization: Bearer YOUR_TOKEN"
# Expected: 200 OK with signature list
```

## 📚 Full Documentation

- **E_SIGNATURE_SECURITY_IMPROVEMENTS.md** - Detailed analysis
- **SIGNATURE_SECURITY_IMPLEMENTATION_GUIDE.md** - Full guide
- **SIGNATURE_SECURITY_SUMMARY.md** - Feature summary
- **IMPLEMENTATION_COMPLETE.md** - Completion status
- **QUICK_REFERENCE_SIGNATURE_SECURITY.md** - This file

---

**Quick Reference v1.0** | Last Updated: March 16, 2026
