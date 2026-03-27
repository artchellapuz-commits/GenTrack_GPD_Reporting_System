# E-Signature Security Implementation Guide

## ✅ What Has Been Implemented

All critical and enhanced security features have been implemented for the e-signature system:

### 1. Authentication & Authorization ✅
- **Removed AllowAny permissions** - All signature endpoints now require authentication
- **Role-based permissions** - Only Managers and Admins can sign reports
- **Signatory authorizations** - Users must be explicitly authorized to sign as specific signatories
- **Ownership controls** - Users can only modify their own signatures

### 2. Cryptographic Security ✅
- **HMAC-SHA256 verification** - All signatures have cryptographic verification hashes
- **Signature integrity checking** - Tamper detection via hash comparison
- **Encryption at rest** - Signature data encrypted using Fernet symmetric encryption
- **Secure key management** - Separate keys for signing and encryption

### 3. Two-Factor Authentication (2FA) ✅
- **OTP generation** - 6-digit time-based codes
- **Email delivery** - OTP sent to user's email
- **Token management** - Secure token storage with expiration
- **Attempt limiting** - Maximum 3 verification attempts
- **Time-based expiry** - Tokens expire after 5 minutes

### 4. Comprehensive Audit Logging ✅
- **All operations logged** - Create, update, delete, apply, verify, 2FA events
- **Rich metadata** - IP address, user agent, device fingerprint, geolocation
- **Success/failure tracking** - Detailed failure reasons
- **Immutable logs** - Read-only audit trail
- **7-year retention** - Configurable retention period

### 5. Rate Limiting ✅
- **Hourly limits** - Max 10 signatures per hour per user
- **Daily limits** - Max 50 signatures per day per user
- **Bypass for admins** - Superusers exempt from rate limits
- **Configurable thresholds** - Adjustable via settings

### 6. Security Models ✅
- **SignatoryAuthorization** - Manage who can sign as whom
- **SignatureAuditLog** - Complete audit trail
- **SignatureVerificationToken** - 2FA token management
- **SignatureSecuritySettings** - Centralized security configuration

### 7. Admin Interface ✅
- **Full CRUD operations** - Manage all security models
- **Authorization management** - Grant/revoke signatory permissions
- **Audit log viewer** - Browse security events
- **Settings configuration** - Adjust security parameters
- **Token monitoring** - View active 2FA tokens

## 📋 Installation Steps

### Step 1: Install Dependencies

```bash
cd npc-reporting-system/backend
pip install -r requirements.txt
```

New dependencies added:
- `cryptography>=41.0.0` - For encryption and digital signatures
- `pyotp>=2.9.0` - For 2FA/OTP generation

### Step 2: Generate Security Keys

Generate a signature secret key:
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

Generate an encryption key:
```bash
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

### Step 3: Update Environment Variables

Copy the new settings from `.env.example` to your `.env` file:

```bash
# Add to backend/.env
SIGNATURE_SECRET_KEY=<your-generated-secret-key>
SIGNATURE_ENCRYPTION_KEY=<your-generated-fernet-key>
SIGNATURE_2FA_ENABLED=True
SIGNATURE_OTP_VALIDITY_MINUTES=5
SIGNATURE_MAX_OTP_ATTEMPTS=3
SIGNATURE_RATE_LIMIT_HOUR=10
SIGNATURE_RATE_LIMIT_DAY=50
```

### Step 4: Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

This will create:
- `signatory_authorizations` table
- `signature_audit_logs` table
- `signature_verification_tokens` table
- `signature_security_settings` table
- Add `verification_hash` field to `e_signatures` table

### Step 5: Create Security Settings

```bash
python manage.py shell
```

```python
from reports.models import SignatureSecuritySettings
settings = SignatureSecuritySettings.get_settings()
print(f"Security settings created: {settings}")
exit()
```

### Step 6: Configure Email (for 2FA)

Update your `.env` file with SMTP settings:

```bash
# For Gmail
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=noreply@npc-reporting.com
```

For Gmail, you need to:
1. Enable 2-factor authentication
2. Generate an app password: https://myaccount.google.com/apppasswords
3. Use the app password as `EMAIL_HOST_PASSWORD`

### Step 7: Grant Signatory Authorizations

Access Django admin at `http://localhost:8000/admin/`

1. Navigate to **Signatory Authorizations**
2. Click **Add Signatory Authorization**
3. Select:
   - **User**: The user who will sign
   - **Signatory name**: Name they can sign as (e.g., "O.M. LAVA")
   - **Is active**: ✓
   - **Requires 2FA**: ✓ (recommended)
   - **Expiry date**: Optional expiration
4. Click **Save**

### Step 8: Test the Implementation

#### Test 1: Authentication Required
```bash
# This should fail with 401 Unauthorized
curl http://localhost:8000/api/e-signatures/
```

#### Test 2: Create Signature (Authenticated)
```bash
# Login first to get token
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"your-username","password":"your-password"}'

# Use token to create signature
curl -X POST http://localhost:8000/api/e-signatures/create-from-data/ \
  -H "Authorization: Bearer <your-token>" \
  -H "Content-Type: application/json" \
  -d '{
    "signatory_name": "Test User",
    "signatory_title": "Manager",
    "signatory_role": "Prepared by",
    "signature_type": "DRAW",
    "signature_data": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="
  }'
```

#### Test 3: Request 2FA
```bash
curl -X POST http://localhost:8000/api/report-signatures/request-2fa/ \
  -H "Authorization: Bearer <your-token>" \
  -H "Content-Type: application/json" \
  -d '{
    "signatory_name": "O.M. LAVA",
    "signature_intent": {
      "report_date": "2026-03-16",
      "report_type": "PSR"
    }
  }'
```

#### Test 4: Verify 2FA
```bash
curl -X POST http://localhost:8000/api/report-signatures/verify-2fa/ \
  -H "Authorization: Bearer <your-token>" \
  -H "Content-Type: application/json" \
  -d '{
    "token_id": 1,
    "otp_code": "123456"
  }'
```

#### Test 5: Verify Signature Integrity
```bash
curl http://localhost:8000/api/e-signatures/1/verify-integrity/ \
  -H "Authorization: Bearer <your-token>"
```

## 🔐 Security Features in Action

### Feature 1: Authentication Required
- **Before**: Anyone could create/view signatures
- **After**: Must be logged in to access any signature endpoint
- **Impact**: Prevents unauthorized access

### Feature 2: Cryptographic Verification
- **Before**: No way to detect if signature was tampered with
- **After**: HMAC-SHA256 hash verifies signature integrity
- **Impact**: Tamper-proof signatures

### Feature 3: Encryption at Rest
- **Before**: Signature data stored in plain text
- **After**: Encrypted using Fernet symmetric encryption
- **Impact**: Protected even if database is compromised

### Feature 4: Two-Factor Authentication
- **Before**: Single-step signature application
- **After**: Requires OTP verification via email
- **Impact**: Prevents unauthorized signing

### Feature 5: Signatory Authorization
- **Before**: Anyone could sign as anyone
- **After**: Must be explicitly authorized for each signatory
- **Impact**: Controlled delegation of signing authority

### Feature 6: Comprehensive Audit Trail
- **Before**: Limited logging
- **After**: Every action logged with full context
- **Impact**: Complete accountability and forensics

### Feature 7: Rate Limiting
- **Before**: Unlimited signature operations
- **After**: 10/hour, 50/day limits
- **Impact**: Prevents abuse and DoS attacks

## 📊 Admin Dashboard Features

### Signatory Authorizations
- View all authorized signatories
- Grant new authorizations
- Revoke existing authorizations
- Set expiration dates
- Configure 2FA requirements

### Signature Audit Logs
- Browse all signature events
- Filter by user, action, success/failure
- View detailed metadata (IP, device, etc.)
- Export audit reports
- Immutable records

### Verification Tokens
- Monitor active 2FA tokens
- View token usage statistics
- Track failed verification attempts
- Automatic cleanup of expired tokens

### Security Settings
- Enable/disable 2FA globally
- Adjust rate limits
- Configure audit retention
- Toggle encryption features
- Set notification preferences

## 🔄 Migration from Old System

### Existing Signatures
- Old signatures without verification hashes will still work
- They will be marked as "unverified" in the system
- Recommend regenerating signatures with new security features

### Backward Compatibility
- Decryption handles both encrypted and plain text data
- Verification gracefully handles missing hashes
- No breaking changes to existing API endpoints

### Gradual Rollout
1. **Phase 1**: Enable authentication (immediate)
2. **Phase 2**: Grant signatory authorizations (1 week)
3. **Phase 3**: Enable 2FA (2 weeks)
4. **Phase 4**: Enforce encryption (1 month)

## 🚨 Security Best Practices

### 1. Key Management
- **Never commit keys to version control**
- Store keys in environment variables
- Rotate keys periodically (every 6-12 months)
- Use different keys for dev/staging/production

### 2. Email Security
- Use app-specific passwords, not account passwords
- Enable 2FA on email account
- Monitor for suspicious email activity
- Consider dedicated email service for production

### 3. Authorization Management
- Review authorizations quarterly
- Set expiration dates for temporary access
- Revoke immediately when users leave
- Require 2FA for sensitive signatories

### 4. Audit Monitoring
- Review audit logs weekly
- Set up alerts for suspicious activity
- Investigate all failed 2FA attempts
- Monitor rate limit violations

### 5. Regular Updates
- Keep dependencies updated
- Apply security patches promptly
- Review security settings monthly
- Conduct security audits annually

## 📈 Monitoring & Alerts

### Key Metrics to Monitor
- Failed authentication attempts
- Failed 2FA verifications
- Rate limit violations
- Signature verification failures
- Unusual IP addresses
- Off-hours activity

### Recommended Alerts
- 5+ failed 2FA attempts in 1 hour
- 10+ failed authentications from same IP
- Signature verification failure
- Rate limit exceeded
- Authorization granted/revoked
- Security settings changed

## 🆘 Troubleshooting

### Issue: 2FA emails not sending
**Solution**: Check EMAIL_BACKEND and SMTP settings in .env

### Issue: Signature verification fails
**Solution**: Ensure SIGNATURE_SECRET_KEY hasn't changed

### Issue: Encryption errors
**Solution**: Verify SIGNATURE_ENCRYPTION_KEY is valid Fernet key

### Issue: Rate limit too restrictive
**Solution**: Adjust limits in SignatureSecuritySettings admin

### Issue: User can't sign as signatory
**Solution**: Grant SignatoryAuthorization in admin

## 📞 Support

For issues or questions:
1. Check audit logs for error details
2. Review Django logs in `backend/logs/app.log`
3. Verify environment variables are set correctly
4. Ensure migrations have been applied
5. Check user has proper authorizations

## 🎉 Success!

Your e-signature system now has enterprise-grade security with:
- ✅ Authentication & authorization
- ✅ Cryptographic verification
- ✅ Two-factor authentication
- ✅ Comprehensive audit logging
- ✅ Rate limiting
- ✅ Encryption at rest
- ✅ Signatory authorization controls

The system is now production-ready and compliant with security best practices!
