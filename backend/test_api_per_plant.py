import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'npc_reporting.settings')
django.setup()

from reports.models import Plant, GenerationReport
from django.db.models import Sum, Avg

print("=" * 60)
print("TESTING API RESPONSES PER PLANT")
print("=" * 60)

plants = Plant.objects.filter(is_active=True)

for plant in plants:
    print(f"\n{plant.code} - {plant.name}")
    
    # Get reports for this plant
    reports = GenerationReport.objects.filter(plant=plant)
    count = reports.count()
    
    print(f"  Reports Count: {count}")
    
    if count > 0:
        # Get summary stats
        stats = reports.aggregate(
            total_generation=Sum('generation_kwh'),
            avg_capacity_factor=Avg('capacity_factor'),
            avg_availability_factor=Avg('availability_factor'),
            total_operating_hours=Sum('operating_hours')
        )
        
        print(f"  Total Generation: {stats['total_generation']:,.2f} kWh")
        print(f"  Avg Capacity Factor: {stats['avg_capacity_factor']:.2f}%")
        print(f"  Avg Availability: {stats['avg_availability_factor']:.2f}%")
        print(f"  Total Operating Hours: {stats['total_operating_hours']:,.2f} hrs")
    else:
        print("  NO DATA - Should show zeros in dashboard")

print("\n" + "=" * 60)
print("OVERALL STATS (All Plants Combined)")
print("=" * 60)

all_reports = GenerationReport.objects.all()
overall = all_reports.aggregate(
    total_generation=Sum('generation_kwh'),
    avg_capacity_factor=Avg('capacity_factor'),
    avg_availability_factor=Avg('availability_factor'),
    total_operating_hours=Sum('operating_hours')
)

print(f"Total Generation: {overall['total_generation']:,.2f} kWh")
print(f"Avg Capacity Factor: {overall['avg_capacity_factor']:.2f}%")
print(f"Avg Availability: {overall['avg_availability_factor']:.2f}%")
print(f"Total Operating Hours: {overall['total_operating_hours']:,.2f} hrs")
print("=" * 60)
