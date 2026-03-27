import os
import sys
import django

# Setup Django
sys.path.insert(0, 'npc-reporting-system/backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'npc_reporting.settings')
django.setup()

from django.db import connection

# Check signature tables
cursor = connection.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE '%signature%'")
tables = cursor.fetchall()

print("Signature-related tables:")
for table in tables:
    print(f"  - {table[0]}")

# Check if e_signatures table exists and has data
from reports.models import ESignature, ReportSignature

print(f"\nESignature records: {ESignature.objects.count()}")
print(f"ReportSignature records: {ReportSignature.objects.count()}")

# Show recent e-signatures
print("\nRecent E-Signatures:")
for sig in ESignature.objects.all()[:5]:
    print(f"  - {sig.signatory_name} ({sig.signatory_role}) - Created by: {sig.created_by.username if sig.created_by else 'N/A'}")

# Show recent report signatures
print("\nRecent Report Signatures:")
for sig in ReportSignature.objects.all()[:5]:
    print(f"  - {sig.signatory_name} ({sig.signatory_role}) - Report: {sig.report_date} - Signed by: {sig.signed_by.username if sig.signed_by else 'N/A'}")
