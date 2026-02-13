import os
import django
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'npc_reporting.settings')
django.setup()

from django.test import RequestFactory
from reports.views import GenerationReportViewSet
from django.db.models import Sum, Avg

print("=" * 60)
print("TESTING API RESPONSES")
print("=" * 60)

# Test summary endpoint for each plant
factory = RequestFactory()

for plant_code in ['AGUS1', 'AGUS2', 'AGUS4']:
    print(f"\n{plant_code}:")
    print("-" * 40)
    
    # Create a mock request with plant_code parameter
    request = factory.get(f'/api/generation-reports/summary/?plant_code={plant_code}')
    
    # Create viewset instance
    viewset = GenerationReportViewSet()
    viewset.request = request
    viewset.format_kwarg = None
    viewset.action = 'summary'
    
    # Get the filtered queryset
    queryset = viewset.get_queryset()
    count = queryset.count()
    
    print(f"  Queryset count: {count}")
    
    if count > 0:
        # Get summary
        summary = queryset.aggregate(
            total_generation=Sum('generation_kwh'),
            avg_capacity_factor=Avg('capacity_factor'),
            avg_availability_factor=Avg('availability_factor'),
        )
        print(f"  Total Generation: {summary['total_generation']:,.2f} kWh")
        print(f"  Avg Capacity Factor: {summary['avg_capacity_factor']:.2f}%")
        print(f"  Avg Availability: {summary['avg_availability_factor']:.2f}%")
    else:
        print("  NO DATA")

print("\n" + "=" * 60)
