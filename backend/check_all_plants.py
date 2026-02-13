import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'npc_reporting.settings')
django.setup()

from reports.models import GenerationReport, Plant
from django.db.models import Sum, Avg, Count

print("=" * 60)
print("DATABASE STATUS - ALL PLANTS")
print("=" * 60)

all_plants = Plant.objects.all()

for plant in all_plants:
    count = GenerationReport.objects.filter(plant=plant).count()
    
    if count > 0:
        stats = GenerationReport.objects.filter(plant=plant).aggregate(
            total_gen=Sum('generation_kwh'),
            avg_cf=Avg('capacity_factor'),
            avg_av=Avg('availability_factor')
        )
        print(f"\n{plant.code} - {plant.name}")
        print(f"  Records: {count}")
        print(f"  Total Generation: {stats['total_gen']:,.2f} kWh")
        print(f"  Avg Capacity Factor: {stats['avg_cf']:.2f}%")
        print(f"  Avg Availability: {stats['avg_av']:.2f}%")
    else:
        print(f"\n{plant.code} - {plant.name}")
        print(f"  Records: 0 (NO DATA)")

print("\n" + "=" * 60)
print(f"TOTAL RECORDS IN DATABASE: {GenerationReport.objects.count()}")
print("=" * 60)
