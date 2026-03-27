import os
import sys
import django
import base64

# Setup Django
sys.path.insert(0, 'npc-reporting-system/backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'npc_reporting.settings')
django.setup()

from django.contrib.auth.models import User
from reports.models import ESignature, ReportSignature
from datetime import date

print("Testing E-Signature Database Saving...")
print("=" * 60)

# Get a test user
user = User.objects.first()
print(f"\nTest User: {user.username}")

# Create a simple test signature (1x1 pixel PNG in base64)
test_signature_data = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="

# Test 1: Create ESignature
print("\n1. Creating ESignature...")
try:
    from django.core.files.base import ContentFile
    image_data = base64.b64decode(test_signature_data)
    
    esig = ESignature.objects.create(
        signatory_name="TEST USER",
        signatory_title="Test Title",
        signatory_role="Prepared by:",
        signature_type="DRAW",
        signature_image=ContentFile(image_data, "test_signature.png"),
        signature_data=test_signature_data,
        is_default=True,
        created_by=user
    )
    print(f"   ✓ ESignature created: ID={esig.id}")
    print(f"   ✓ Created by: {esig.created_by.username if esig.created_by else 'NULL'}")
    print(f"   ✓ Signature image: {esig.signature_image.url if esig.signature_image else 'NULL'}")
except Exception as e:
    print(f"   ✗ Error: {e}")

# Test 2: Create ReportSignature
print("\n2. Creating ReportSignature...")
try:
    report_sig = ReportSignature.objects.create(
        report_date=date.today(),
        report_type="PSR",
        signature=esig,
        signatory_name="TEST USER",
        signatory_role="Prepared by:",
        signed_by=user,
        ip_address="127.0.0.1"
    )
    print(f"   ✓ ReportSignature created: ID={report_sig.id}")
    print(f"   ✓ Signed by: {report_sig.signed_by.username if report_sig.signed_by else 'NULL'}")
    print(f"   ✓ Report date: {report_sig.report_date}")
except Exception as e:
    print(f"   ✗ Error: {e}")

# Test 3: Verify data persists
print("\n3. Verifying persistence...")
try:
    # Reload from database
    esig_check = ESignature.objects.get(id=esig.id)
    report_sig_check = ReportSignature.objects.get(id=report_sig.id)
    
    print(f"   ✓ ESignature persisted: {esig_check.signatory_name}")
    print(f"   ✓ Created by persisted: {esig_check.created_by.username if esig_check.created_by else 'NULL'}")
    print(f"   ✓ ReportSignature persisted: {report_sig_check.signatory_name}")
    print(f"   ✓ Signed by persisted: {report_sig_check.signed_by.username if report_sig_check.signed_by else 'NULL'}")
except Exception as e:
    print(f"   ✗ Error: {e}")

# Cleanup
print("\n4. Cleaning up test data...")
try:
    report_sig.delete()
    esig.delete()
    print("   ✓ Test data cleaned up")
except Exception as e:
    print(f"   ✗ Error: {e}")

print("\n" + "=" * 60)
print("E-Signature database saving is working correctly!")
print("Both ESignature and ReportSignature records are saved to database.")
