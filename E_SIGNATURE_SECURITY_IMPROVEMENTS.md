# E-Signature Security Improvements

## Current Security Issues

Based on the analysis of your e-signature implementation, here are the identified security vulnerabilities:

### 1. **No Authentication Required**
- `permission_classes = [AllowAny]` allows unauthenticated access
- Anyone can create, view, or modify signatures without logging in
- No user verification before signature application

### 2. **Weak Signature Verification**
- `verification_hash` field exists but is not implemented
- No cryptographic signing of signature data
- No tamper detection mechanism
- No signature integrity validation

### 3. **Missing Audit Trail**
- No comprehensive logging of signature operations
- IP address captured but not validated
- No device fingerprinting
- No session tracking for signature events

### 4. **Insecure Storage**
- Signatures stored as plain images without encryption
- Base64 data stored in plain text
- No secure key management
- Media files accessible without authentication

### 5. **No Multi-Factor Authentication**
- Single-step signature application
- No secondary verification (email, SMS, OTP)
- No biometric validation option

### 6. **Insufficient Access Control**
- No role-based signature permissions
- Anyone can sign on behalf of others
- No approval workflow for sensitive signatures
- No signature delegation controls

### 7. **Missing Non-Repudiation**
- No cryptographic proof of signature
- Signatures can be disputed
- No timestamp authority integration
- No digital certificate chain

## Recommended Security Enhancements

### Priority 1: Critical Security (Implement Immediately)

#### 1.1 Enable Authentication & Authorization
```python
# backend/reports/views.py
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes

class ESignatureViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]  # Require authentication
    
    def get_permissions(self):
        """Custom permissions based on action"""
        if self.action in ['create', 'update', 'destroy']:
            return [IsAuthenticated(), IsSignatureOwner()]
        return [IsAuthenticated()]
```

#### 1.2 Implement Cryptographic Signature Verification
```python
# backend/reports/utils/signature_crypto.py
import hashlib
import hmac
from datetime import datetime
from django.conf import settings

class SignatureVerifier:
    """Cryptographic signature verification"""
    
    @staticmethod
    def generate_signature_hash(signature_data, signatory_name, timestamp):
        """Generate HMAC-SHA256 hash for signature verification"""
        secret_key = settings.SIGNATURE_SECRET_KEY
        message = f"{signature_data}|{signatory_name}|{timestamp}"
        return hmac.new(
            secret_key.encode(),
            message.encode(),
            hashlib.sha256
        ).hexdigest()
    
    @staticmethod
    def verify_signature(signature_obj):
        """Verify signature integrity"""
        computed_hash = SignatureVerifier.generate_signature_hash(
            signature_obj.signature_data,
            signature_obj.signatory_name,
            signature_obj.created_at.isoformat()
        )
        return hmac.compare_digest(computed_hash, signature_obj.verification_hash)
```

#### 1.3 Add Comprehensive Audit Logging
```python
# backend/reports/middleware/signature_audit.py
import logging
from .models import SignatureAuditLog

class SignatureAuditMiddleware:
    """Middleware to log all signature operations"""
    
    def __init__(self, get_response):
        self.get_response = get_response
        self.logger = logging.getLogger('signature_audit')
    
    def __call__(self, request):
        if 'e-signatures' in request.path or 'report-signatures' in request.path:
            self.log_signature_operation(request)
        return self.get_response(request)
    
    def log_signature_operation(self, request):
        SignatureAuditLog.objects.create(
            user=request.user if request.user.is_authenticated else None,
            action=request.method,
            endpoint=request.path,
            ip_address=self.get_client_ip(request),
            user_agent=request.META.get('HTTP_USER_AGENT', ''),
            device_fingerprint=self.get_device_fingerprint(request),
            timestamp=timezone.now()
        )
```

### Priority 2: Enhanced Security (Implement Within 1 Month)

#### 2.1 Two-Factor Authentication for Signatures
```python
# backend/reports/services/signature_2fa.py
import pyotp
from django.core.mail import send_mail

class Signature2FA:
    """Two-factor authentication for signature operations"""
    
    @staticmethod
    def generate_otp(user):
        """Generate time-based OTP"""
        secret = pyotp.random_base32()
        totp = pyotp.TOTP(secret)
        return totp.now(), secret
    
    @staticmethod
    def send_otp_email(user, otp_code):
        """Send OTP via email"""
        send_mail(
            'E-Signature Verification Code',
            f'Your verification code is: {otp_code}\nValid for 5 minutes.',
            'noreply@npc-reporting.com',
            [user.email],
            fail_silently=False,
        )
    
    @staticmethod
    def verify_otp(secret, user_input):
        """Verify OTP code"""
        totp = pyotp.TOTP(secret)
        return totp.verify(user_input, valid_window=1)
```

#### 2.2 Role-Based Signature Permissions
```python
# backend/reports/permissions.py
from rest_framework import permissions

class CanSignReports(permissions.BasePermission):
    """Permission to sign reports based on user role"""
    
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        # Check user profile role
        profile = getattr(request.user, 'profile', None)
        if not profile:
            return False
        
        # Only managers and admins can sign reports
        return profile.role in ['MANAGER', 'ADMIN']

class CanSignAsSignatory(permissions.BasePermission):
    """Verify user can sign as specific signatory"""
    
    def has_object_permission(self, request, view, obj):
        # Verify user is authorized to sign as this signatory
        return SignatoryAuthorization.objects.filter(
            user=request.user,
            signatory_name=obj.signatory_name,
            is_active=True
        ).exists()
```

#### 2.3 Signature Encryption at Rest
```python
# backend/reports/utils/signature_encryption.py
from cryptography.fernet import Fernet
from django.conf import settings
import base64

class SignatureEncryption:
    """Encrypt signature data at rest"""
    
    def __init__(self):
        self.cipher = Fernet(settings.SIGNATURE_ENCRYPTION_KEY)
    
    def encrypt_signature_data(self, signature_data):
        """Encrypt signature base64 data"""
        return self.cipher.encrypt(signature_data.encode()).decode()
    
    def decrypt_signature_data(self, encrypted_data):
        """Decrypt signature data"""
        return self.cipher.decrypt(encrypted_data.encode()).decode()
```

### Priority 3: Advanced Security (Implement Within 3 Months)

#### 3.1 Digital Certificate Integration
```python
# backend/reports/services/digital_certificate.py
from cryptography import x509
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding

class DigitalCertificateService:
    """PKI-based digital signature service"""
    
    @staticmethod
    def sign_with_certificate(data, private_key):
        """Sign data using private key"""
        signature = private_key.sign(
            data.encode(),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return base64.b64encode(signature).decode()
    
    @staticmethod
    def verify_certificate_signature(data, signature, public_key):
        """Verify signature using public key"""
        try:
            public_key.verify(
                base64.b64decode(signature),
                data.encode(),
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            return True
        except Exception:
            return False
```

#### 3.2 Blockchain-Based Signature Registry
```python
# backend/reports/services/blockchain_registry.py
import hashlib
from datetime import datetime

class BlockchainSignatureRegistry:
    """Immutable signature registry using blockchain concepts"""
    
    def __init__(self):
        self.chain = []
        self.create_genesis_block()
    
    def create_genesis_block(self):
        """Create the first block"""
        genesis_block = {
            'index': 0,
            'timestamp': datetime.now().isoformat(),
            'signatures': [],
            'previous_hash': '0',
            'hash': self.calculate_hash(0, '0', [])
        }
        self.chain.append(genesis_block)
    
    def add_signature_block(self, signature_data):
        """Add signature to blockchain"""
        previous_block = self.chain[-1]
        new_block = {
            'index': len(self.chain),
            'timestamp': datetime.now().isoformat(),
            'signatures': [signature_data],
            'previous_hash': previous_block['hash'],
        }
        new_block['hash'] = self.calculate_hash(
            new_block['index'],
            new_block['previous_hash'],
            new_block['signatures']
        )
        self.chain.append(new_block)
        return new_block
    
    def calculate_hash(self, index, previous_hash, signatures):
        """Calculate block hash"""
        value = f"{index}{previous_hash}{signatures}"
        return hashlib.sha256(value.encode()).hexdigest()
    
    def verify_chain(self):
        """Verify blockchain integrity"""
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i-1]
            
            if current['previous_hash'] != previous['hash']:
                return False
            
            if current['hash'] != self.calculate_hash(
                current['index'],
                current['previous_hash'],
                current['signatures']
            ):
                return False
        return True
```

#### 3.3 Biometric Signature Verification
```python
# backend/reports/services/biometric_verification.py
class BiometricSignatureVerification:
    """Biometric verification for signatures"""
    
    @staticmethod
    def verify_signature_dynamics(signature_data):
        """Verify signature based on drawing dynamics"""
        # Analyze:
        # - Stroke speed
        # - Pressure points
        # - Drawing patterns
        # - Time intervals
        dynamics = {
            'speed_variance': calculate_speed_variance(signature_data),
            'pressure_points': extract_pressure_points(signature_data),
            'stroke_pattern': analyze_stroke_pattern(signature_data)
        }
        return verify_against_baseline(dynamics)
```

## New Database Models

```python
# backend/reports/models.py

class SignatoryAuthorization(models.Model):
    """Authorization for users to sign as specific signatories"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    signatory_name = models.CharField(max_length=100)
    authorized_by = models.ForeignKey(User, on_delete=models.SET_NULL, 
                                     null=True, related_name='granted_authorizations')
    authorization_date = models.DateTimeField(auto_now_add=True)
    expiry_date = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    requires_2fa = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'signatory_authorizations'
        unique_together = ['user', 'signatory_name']


class SignatureAuditLog(models.Model):
    """Comprehensive audit log for signature operations"""
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    action = models.CharField(max_length=50)
    signature = models.ForeignKey(ESignature, on_delete=models.SET_NULL, null=True)
    report_signature = models.ForeignKey(ReportSignature, on_delete=models.SET_NULL, null=True)
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField()
    device_fingerprint = models.CharField(max_length=255)
    geolocation = models.JSONField(null=True, blank=True)
    success = models.BooleanField(default=True)
    failure_reason = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'signature_audit_logs'
        indexes = [
            models.Index(fields=['user', 'timestamp']),
            models.Index(fields=['signature', 'timestamp']),
            models.Index(fields=['ip_address']),
        ]


class SignatureVerificationToken(models.Model):
    """2FA tokens for signature verification"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=6)
    secret = models.CharField(max_length=32)
    signature_intent = models.JSONField()  # Store what they're trying to sign
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)
    verified_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'signature_verification_tokens'


class SignatureCertificate(models.Model):
    """Digital certificates for PKI-based signatures"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    certificate_data = models.TextField()  # PEM format
    public_key = models.TextField()
    private_key_encrypted = models.TextField()  # Encrypted private key
    issuer = models.CharField(max_length=255)
    subject = models.CharField(max_length=255)
    serial_number = models.CharField(max_length=100, unique=True)
    valid_from = models.DateTimeField()
    valid_until = models.DateTimeField()
    is_revoked = models.BooleanField(default=False)
    revocation_date = models.DateTimeField(null=True, blank=True)
    revocation_reason = models.TextField(blank=True)
    
    class Meta:
        db_table = 'signature_certificates'
```

## Configuration Changes

```python
# backend/npc_reporting/settings.py

# Signature Security Settings
SIGNATURE_SECRET_KEY = env('SIGNATURE_SECRET_KEY', default='change-this-in-production')
SIGNATURE_ENCRYPTION_KEY = env('SIGNATURE_ENCRYPTION_KEY')  # Fernet key

# 2FA Settings
SIGNATURE_2FA_ENABLED = True
SIGNATURE_OTP_VALIDITY_MINUTES = 5
SIGNATURE_MAX_OTP_ATTEMPTS = 3

# Audit Settings
SIGNATURE_AUDIT_RETENTION_DAYS = 2555  # 7 years
SIGNATURE_LOG_GEOLOCATION = True

# Certificate Settings
SIGNATURE_CERTIFICATE_AUTHORITY = 'NPC Internal CA'
SIGNATURE_CERTIFICATE_VALIDITY_YEARS = 2

# Rate Limiting
SIGNATURE_RATE_LIMIT = '10/hour'  # Max 10 signatures per hour per user
```

## Frontend Security Enhancements

```javascript
// frontend/src/services/signatureService.js

class SignatureService {
  // Add device fingerprinting
  async getDeviceFingerprint() {
    const canvas = document.createElement('canvas');
    const ctx = canvas.getContext('2d');
    ctx.textBaseline = 'top';
    ctx.font = '14px Arial';
    ctx.fillText('Device Fingerprint', 2, 2);
    
    return {
      canvas: canvas.toDataURL(),
      userAgent: navigator.userAgent,
      language: navigator.language,
      platform: navigator.platform,
      screenResolution: `${screen.width}x${screen.height}`,
      timezone: Intl.DateTimeFormat().resolvedOptions().timeZone
    };
  }
  
  // Implement signature with 2FA
  async signWithVerification(signatureData, otpCode) {
    const fingerprint = await this.getDeviceFingerprint();
    
    return api.post('/api/report-signatures/sign-with-2fa/', {
      ...signatureData,
      otp_code: otpCode,
      device_fingerprint: fingerprint
    });
  }
  
  // Verify signature integrity before display
  async verifySignatureIntegrity(signatureId) {
    return api.get(`/api/e-signatures/${signatureId}/verify-integrity/`);
  }
}
```

## Implementation Roadmap

### Week 1-2: Critical Security
- [ ] Enable authentication on all signature endpoints
- [ ] Implement HMAC signature verification
- [ ] Add comprehensive audit logging
- [ ] Secure media file access

### Week 3-4: Enhanced Security
- [ ] Implement 2FA for signatures
- [ ] Add role-based permissions
- [ ] Encrypt signatures at rest
- [ ] Add device fingerprinting

### Month 2: Advanced Features
- [ ] Digital certificate integration
- [ ] Blockchain registry (optional)
- [ ] Enhanced audit dashboard
- [ ] Signature analytics

### Month 3: Compliance & Testing
- [ ] Security audit
- [ ] Penetration testing
- [ ] Compliance documentation
- [ ] User training materials

## Compliance Considerations

### Legal Requirements
- **E-SIGN Act (US)**: Ensure consent and record retention
- **eIDAS (EU)**: Qualified electronic signatures if applicable
- **Local Regulations**: Check Philippine e-signature laws

### Industry Standards
- **ISO 27001**: Information security management
- **NIST SP 800-63**: Digital identity guidelines
- **PCI DSS**: If handling payment-related signatures

## Testing Checklist

- [ ] Signature cannot be created without authentication
- [ ] Signature verification detects tampering
- [ ] 2FA required for sensitive signatures
- [ ] Audit logs capture all operations
- [ ] Encrypted signatures cannot be read directly
- [ ] Role-based access enforced
- [ ] Rate limiting prevents abuse
- [ ] Certificate validation works correctly
- [ ] Blockchain integrity maintained
- [ ] Biometric verification accurate

## Monitoring & Alerts

```python
# backend/reports/monitoring/signature_monitor.py

class SignatureSecurityMonitor:
    """Monitor signature security events"""
    
    @staticmethod
    def check_suspicious_activity():
        """Detect suspicious signature patterns"""
        alerts = []
        
        # Multiple failed signature attempts
        failed_attempts = SignatureAuditLog.objects.filter(
            success=False,
            timestamp__gte=timezone.now() - timedelta(hours=1)
        ).values('user').annotate(count=Count('id'))
        
        for attempt in failed_attempts:
            if attempt['count'] > 5:
                alerts.append({
                    'type': 'MULTIPLE_FAILURES',
                    'user_id': attempt['user'],
                    'count': attempt['count']
                })
        
        # Signature from unusual location
        # Signature at unusual time
        # Multiple signatures in short time
        
        return alerts
```

## Conclusion

Implementing these security improvements will transform your e-signature system from a basic image storage solution to a robust, legally-defensible digital signature platform with:

- Strong authentication and authorization
- Cryptographic integrity verification
- Comprehensive audit trails
- Non-repudiation guarantees
- Compliance with legal standards

Start with Priority 1 items immediately, as they address critical security vulnerabilities that could compromise the entire reporting system.
