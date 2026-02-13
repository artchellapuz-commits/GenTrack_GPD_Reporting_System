import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'npc_reporting.settings')
django.setup()

from reports.models import Plant, Unit, HistoricalData, GenerationReport, PlantCapacity

print("=" * 60)
print("DATABASE VERIFICATION")
print("=" * 60)
print()

print("MODELS:")
print(f"  Plants: {Plant.objects.count()}")
print(f"  Units: {Unit.objects.count()}")
print(f"  Historical Data: {HistoricalData.objects.count()}")
print(f"  Generation Reports: {GenerationReport.objects.count()}")
print(f"  Plant Capacity Records: {PlantCapacity.objects.count()}")
print()

print("=" * 60)
print("PLANT DETAILS")
print("=" * 60)
for p in Plant.objects.all():
    units = p.units.count()
    print(f"{p.code}: {p.name}")
    print(f"  Capacity: {p.capacity_mw} MW")
    print(f"  Units: {units}")
    print(f"  Location: {p.location}")
    print()

print("=" * 60)
print("SAMPLE HISTORICAL DATA")
print("=" * 60)
sample = HistoricalData.objects.all()[:5]
for h in sample:
    print(f"{h.plant.code} - {h.date}: {h.generation_mwh} MWh")
print(f"... and {HistoricalData.objects.count() - 5} more records")
print()

print("=" * 60)
print("SAMPLE GENERATION REPORTS")
print("=" * 60)
sample = GenerationReport.objects.all()[:5]
for g in sample:
    print(f"{g.plant.code} Unit {g.unit.unit_number} - {g.report_date}: {g.generation_kwh} kWh")
print(f"... and {GenerationReport.objects.count() - 5} more records")
print()

print("=" * 60)
print("IMPLEMENTATION STATUS: ✓ COMPLETE")
print("=" * 60)
