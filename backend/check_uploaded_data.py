import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'npc_reporting.settings')
django.setup()

from reports.models import GenerationReport, UploadedFile, Plant
from datetime import datetime, timedelta

print("=" * 80)
print("CHECKING UPLOADED DATA")
print("=" * 80)

# Check uploaded files
print("\n1. UPLOADED FILES:")
files = UploadedFile.objects.all().order_by('-uploaded_at')[:5]
for f in files:
    print(f"   - {f.original_filename}")
    print(f"     Plant: {f.plant.name} ({f.plant.code})")
    print(f"     Uploaded: {f.uploaded_at}")
    print(f"     Status: {f.status}")
    print(f"     Records: {f.records_imported}")
    print()

# Check generation reports
print("\n2. GENERATION REPORTS:")
reports = GenerationReport.objects.all().order_by('-report_date')[:10]
print(f"   Total reports: {GenerationReport.objects.count()}")
print(f"   Recent reports:")
for r in reports:
    print(f"   - {r.report_date} | {r.plant.code} Unit {r.unit.unit_number} | {r.generation_kwh} kWh")

# Check today's data
print("\n3. TODAY'S DATA (2026-02-19):")
today = datetime(2026, 2, 19).date()
today_reports = GenerationReport.objects.filter(report_date=today)
print(f"   Reports for today: {today_reports.count()}")
for r in today_reports:
    print(f"   - {r.plant.code} Unit {r.unit.unit_number} | {r.generation_kwh} kWh")

# Check Pulangi 4 data
print("\n4. PULANGI 4 DATA:")
try:
    pulangi4 = Plant.objects.get(code='PULANGI4')
    pulangi4_reports = GenerationReport.objects.filter(plant=pulangi4).order_by('-report_date')[:5]
    print(f"   Total Pulangi 4 reports: {GenerationReport.objects.filter(plant=pulangi4).count()}")
    print(f"   Recent Pulangi 4 reports:")
    for r in pulangi4_reports:
        print(f"   - {r.report_date} | Unit {r.unit.unit_number} | {r.generation_kwh} kWh")
except Plant.DoesNotExist:
    print("   Pulangi 4 plant not found!")

print("\n" + "=" * 80)
