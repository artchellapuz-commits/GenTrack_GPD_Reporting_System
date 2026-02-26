#!/usr/bin/env python
"""
Check if archive fields exist in UploadedFile model
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'npc_reporting.settings')
django.setup()

from reports.models import UploadedFile
from django.db import connection

print("=" * 60)
print("CHECKING ARCHIVE FIELDS IN UPLOADEDFILE MODEL")
print("=" * 60)

# Check model fields
print("\n1. Model Fields:")
print("-" * 60)
model_fields = [f.name for f in UploadedFile._meta.get_fields()]
print(f"All fields: {', '.join(model_fields)}")

archive_fields = ['is_archived', 'archived_at', 'archived_by']
print(f"\nChecking for archive fields: {', '.join(archive_fields)}")
for field in archive_fields:
    if field in model_fields:
        print(f"  ✅ {field} - EXISTS")
    else:
        print(f"  ❌ {field} - MISSING")

# Check database table
print("\n2. Database Table Columns:")
print("-" * 60)
with connection.cursor() as cursor:
    cursor.execute("""
        SELECT column_name, data_type, is_nullable
        FROM information_schema.columns
        WHERE table_name = 'reports_uploadedfile'
        ORDER BY ordinal_position;
    """)
    columns = cursor.fetchall()
    
    if columns:
        print(f"Found {len(columns)} columns in reports_uploadedfile table:")
        for col in columns:
            print(f"  - {col[0]} ({col[1]}) {'NULL' if col[2] == 'YES' else 'NOT NULL'}")
        
        # Check specifically for archive fields
        column_names = [col[0] for col in columns]
        print(f"\nArchive fields in database:")
        for field in archive_fields:
            if field in column_names:
                print(f"  ✅ {field} - EXISTS in database")
            else:
                print(f"  ❌ {field} - MISSING from database")
    else:
        print("  ❌ Table 'reports_uploadedfile' not found!")

# Check migrations
print("\n3. Migration Status:")
print("-" * 60)
from django.db.migrations.recorder import MigrationRecorder
recorder = MigrationRecorder(connection)
migrations = recorder.applied_migrations()
archive_migration = ('reports', '0011_add_archived_field')
if archive_migration in migrations:
    print(f"  ✅ Migration {archive_migration[1]} - APPLIED")
else:
    print(f"  ❌ Migration {archive_migration[1]} - NOT APPLIED")
    print("\n  You need to run: python manage.py migrate")

print("\n" + "=" * 60)
print("DIAGNOSIS:")
print("=" * 60)

# Provide diagnosis
model_has_fields = all(f in model_fields for f in archive_fields)
with connection.cursor() as cursor:
    cursor.execute("""
        SELECT column_name
        FROM information_schema.columns
        WHERE table_name = 'reports_uploadedfile';
    """)
    db_columns = [col[0] for col in cursor.fetchall()]
    db_has_fields = all(f in db_columns for f in archive_fields)

if model_has_fields and db_has_fields:
    print("✅ Everything looks good! Archive feature should work.")
elif model_has_fields and not db_has_fields:
    print("❌ Model has fields but database doesn't!")
    print("   Solution: Run 'python manage.py migrate'")
elif not model_has_fields:
    print("❌ Model is missing archive fields!")
    print("   Solution: Check if models.py has the correct fields")
else:
    print("❌ Unknown issue. Check the details above.")

print("=" * 60)
