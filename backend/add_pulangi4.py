"""
Add Pulangi 4 Hydro-electric Power Plant to the NPC Reporting System
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'npc_reporting.settings')
django.setup()

from reports.models import Plant, Unit

print("=" * 60)
print("Adding Pulangi 4 Hydro-electric Power Plant")
print("=" * 60)
print()

# Pulangi 4 Plant Data
# Based on typical Mindanao hydroelectric plant specifications
plant_data = {
    'code': 'PULANGI4',
    'name': 'Pulangi 4 Hydroelectric Power Plant',
    'capacity_mw': 255,  # Total installed capacity
    'location': 'Bukidnon',
    'num_units': 3,
    'unit_capacity': 85  # Each unit capacity
}

try:
    # Create or get plant
    plant, created = Plant.objects.get_or_create(
        code=plant_data['code'],
        defaults={
            'name': plant_data['name'],
            'capacity_mw': plant_data['capacity_mw'],
            'location': plant_data['location'],
            'is_active': True
        }
    )
    
    if created:
        print(f"✓ Created plant: {plant_data['code']}")
        print(f"  Name: {plant_data['name']}")
        print(f"  Capacity: {plant_data['capacity_mw']} MW")
        print(f"  Location: {plant_data['location']}")
    else:
        print(f"○ Plant already exists: {plant_data['code']}")
        print(f"  Updating plant information...")
        plant.name = plant_data['name']
        plant.capacity_mw = plant_data['capacity_mw']
        plant.location = plant_data['location']
        plant.is_active = True
        plant.save()
        print(f"  ✓ Plant information updated")
    
    print()
    print("Creating units...")
    
    # Create units
    units_created = 0
    units_existing = 0
    
    for i in range(1, plant_data['num_units'] + 1):
        unit, created = Unit.objects.get_or_create(
            plant=plant,
            unit_number=i,
            defaults={
                'capacity_mw': plant_data['unit_capacity'],
                'is_active': True
            }
        )
        
        if created:
            print(f"  ✓ Created unit: {plant_data['code']} Unit {i} ({plant_data['unit_capacity']} MW)")
            units_created += 1
        else:
            print(f"  ○ Unit already exists: {plant_data['code']} Unit {i}")
            units_existing += 1
    
    print()
    print("=" * 60)
    print("Summary:")
    print("=" * 60)
    print(f"Plant: {plant_data['name']}")
    print(f"Code: {plant_data['code']}")
    print(f"Total Capacity: {plant_data['capacity_mw']} MW")
    print(f"Number of Units: {plant_data['num_units']}")
    print(f"Units Created: {units_created}")
    print(f"Units Already Existing: {units_existing}")
    print()
    print("✓ Pulangi 4 has been successfully added to the system!")
    print()
    print("You can now:")
    print("1. Upload daily generation data for Pulangi 4")
    print("2. View Pulangi 4 in the dashboard")
    print("3. Generate reports including Pulangi 4 data")
    print()
    
except Exception as e:
    print()
    print("✗ Error adding Pulangi 4:")
    print(f"  {str(e)}")
    print()
    import traceback
    traceback.print_exc()
