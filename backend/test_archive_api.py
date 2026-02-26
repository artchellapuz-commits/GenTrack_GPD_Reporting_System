#!/usr/bin/env python
"""
Test archive API endpoints
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'npc_reporting.settings')
django.setup()

from reports.models import UploadedFile
from django.contrib.auth import get_user_model

User = get_user_model()

print("=" * 60)
print("TESTING ARCHIVE API")
print("=" * 60)

# Get all uploaded files
print("\n📁 All Uploaded Files:")
files = UploadedFile.objects.all().order_by('-id')[:10]
for f in files:
    archived_status = "📥 ARCHIVED" if f.is_archived else "📤 ACTIVE"
    print(f"   ID: {f.id} | {archived_status} | {f.original_filename}")

# Check file ID 49
print("\n🔍 Checking File ID 49:")
try:
    file_49 = UploadedFile.objects.get(id=49)
    print(f"   ✅ File exists: {file_49.original_filename}")
    print(f"   Status: {'ARCHIVED' if file_49.is_archived else 'ACTIVE'}")
    print(f"   Plant: {file_49.plant.name if file_49.plant else 'None'}")
    print(f"   Uploaded: {file_49.uploaded_at}")
    
    if file_49.is_archived:
        print(f"   Archived at: {file_49.archived_at}")
        print(f"   Archived by: {file_49.archived_by}")
        print("\n   ⚠️  File is already archived!")
        print("   Cannot archive again (will get 400 error)")
        print("   Can restore it though!")
    else:
        print("\n   ✅ File can be archived")
        
except UploadedFile.DoesNotExist:
    print(f"   ❌ File ID 49 does not exist!")
    print("   This is why you're getting 404/400 errors")

# Show archived files
print("\n📥 Currently Archived Files:")
archived = UploadedFile.objects.filter(is_archived=True)
if archived.exists():
    for f in archived:
        print(f"   ID: {f.id} | {f.original_filename}")
else:
    print("   No archived files")

# Show active files
print("\n📤 Currently Active Files:")
active = UploadedFile.objects.filter(is_archived=False)
if active.exists():
    for f in active[:5]:
        print(f"   ID: {f.id} | {f.original_filename}")
else:
    print("   No active files")

print("\n" + "=" * 60)
print("DIAGNOSIS:")
print("=" * 60)

try:
    file_49 = UploadedFile.objects.get(id=49)
    if file_49.is_archived:
        print("❌ File 49 is ALREADY ARCHIVED")
        print("   - Archive endpoint will return 400 (already archived)")
        print("   - Restore endpoint should work")
        print("   - Delete endpoint should work")
    else:
        print("✅ File 49 is ACTIVE")
        print("   - Archive endpoint should work")
        print("   - Restore endpoint will return 400 (not archived)")
except UploadedFile.DoesNotExist:
    print("❌ File 49 DOES NOT EXIST")
    print("   - All endpoints will return 404")
    print("   - The file was probably deleted")
    print("   - Frontend is trying to operate on a non-existent file")

print("=" * 60)
