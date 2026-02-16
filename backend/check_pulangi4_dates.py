"""
Check what dates exist for Pulangi 4 in the database
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'npc_reporting.settings')
django.setup()

from reports.models import GenerationReport

# Get all Pulangi 4 reports
reports = GenerationReport.objects.filter(plant__code='PULANGI4').order_by('report_date', 'unit__unit_number')

print(f"\n{'='*60}")
print(f"PULANGI 4 DATA IN DATABASE")
print(f"{'='*60}")
print(f"\nTotal reports: {reports.count()}")

if reports.exists():
    earliest = reports.earliest('report_date')
    latest = reports.latest('report_date')
    print(f"Date range: {earliest.report_date} to {latest.report_date}")
    
    print(f"\nAll records:")
    print(f"{'Date':<12} {'Unit':<6} {'Generation (kWh)':<20} {'Operating Hours':<15}")
    print(f"{'-'*60}")
    
    for r in reports:
        print(f"{r.report_date} Unit {r.unit.unit_number:<4} {r.generation_kwh:>18,.0f} {r.operating_hours:>14.1f}")
    
    # Calculate totals
    from django.db.models import Sum
    totals = reports.aggregate(
        total_gen=Sum('generation_kwh'),
        total_hours=Sum('operating_hours')
    )
    print(f"\n{'='*60}")
    print(f"TOTALS:")
    print(f"  Total Generation: {totals['total_gen']:,.0f} kWh")
    print(f"  Total Operating Hours: {totals['total_hours']:,.1f}")
    print(f"{'='*60}\n")
else:
    print("\nNo Pulangi 4 data found in database!")
    print("Please upload the SAMPLE_PULANGI4.xlsx file first.\n")
