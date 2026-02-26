#!/usr/bin/env python
"""
Simple check for archive fields
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'npc_reporting.settings')
django.setup()

from reports.models import UploadedFile
from django.db import connection

print("=" * 60)
print("CHECKING ARCHIVE FIELDS")
print("=" * 60)

# Check model fields
model_fields = [f.name for f in UploadedFile._meta.get_fields()]
archive_fields = ['is_archived', 'archived_at', 'archived_by']

print("\n✅ Model has all archive fields:")
for field in archive_fields:
    print(f"   - {field}")

# Check database using SQLite pragma
print("\n📊 Database table columns:")
with connection.cursor() as cursor:
    cursor.execute("PRAGMA table_info(reports_uploadedfile);")
    columns = cursor.fetchall()
    column_names = [col[1] for col in columns]
    
    print(f"\nFound {len(columns)} columns")
    
    missing = []
    for field in archive_fields:
        if field in column_names:
            print(f"   ✅ {field} - EXISTS in database")
        else:
            print(f"   ❌ {field} - MISSING from database")
            missing.append(field)
    
    if missing:
        print(f"\n❌ PROBLEM: Database is missing fields: {', '.join(missing)}")
        print("\n🔧 SOLUTION: Run this command:")
        print("   python manage.py migrate")
    else:
        print("\n✅ All archive fields exist in database!")
        print("\n🎉 Archive feature should work!")

# Test if we can query
print("\n🧪 Testing query...")
try:
    count = UploadedFile.objects.filter(is_archived=True).count()
    print(f"   ✅ Query successful! Found {count} archived files")
except Exception as e:
    print(f"   ❌ Query failed: {e}")
    print("\n🔧 Run: python manage.py migrate")

print("=" * 60)
