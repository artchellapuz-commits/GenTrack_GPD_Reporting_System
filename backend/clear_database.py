"""
Clear all generation reports and uploaded files from the database
"""
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'npc_reporting.settings')
django.setup()

from reports.models import GenerationReport, UploadedFile

print("Current database status:")
print(f"- Generation Reports: {GenerationReport.objects.count()}")
print(f"- Uploaded Files: {UploadedFile.objects.count()}")
print()

response = input("Do you want to delete all data? (yes/no): ")

if response.lower() == 'yes':
    # Delete all generation reports
    reports_deleted = GenerationReport.objects.all().delete()
    print(f"✓ Deleted {reports_deleted[0]} generation reports")
    
    # Delete all uploaded files
    files_deleted = UploadedFile.objects.all().delete()
    print(f"✓ Deleted {files_deleted[0]} uploaded files")
    
    print("\n✓ Database cleared successfully!")
    print("The dashboard will now show 0 for all statistics.")
else:
    print("Operation cancelled.")
