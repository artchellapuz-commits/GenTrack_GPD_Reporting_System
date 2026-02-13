import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'npc_reporting.settings')
django.setup()

from reports.models import GenerationReport
from django.db.models import Count

print("Records per plant:")
plants = GenerationReport.objects.values('plant__code').annotate(count=Count('id'))
for p in plants:
    print(f"{p['plant__code']}: {p['count']} records")

print(f"\nTotal records: {GenerationReport.objects.count()}")
