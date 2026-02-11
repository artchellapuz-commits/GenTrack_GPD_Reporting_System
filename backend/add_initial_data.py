import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'npc_reporting.settings')
django.setup()

from reports.models import Plant, Unit

print("Creating plants...")

# Plant data: (code, name, capacity_mw, location, num_units, unit_capacity)
plants_data = [
    ('AGUS1', 'Agus 1 Hydroelectric Plant', 100, 'Lanao del Sur', 4, 25),
    ('AGUS2', 'Agus 2 Hydroelectric Plant', 180, 'Lanao del Sur', 4, 45),
    ('AGUS4', 'Agus 4 Hydroelectric Plant', 200, 'Lanao del Norte', 4, 50),
    ('AGUS5', 'Agus 5 Hydroelectric Plant', 52, 'Lanao del Norte', 2, 26),
    ('AGUS6', 'Agus 6 Hydroelectric Plant', 200, 'Lanao del Norte', 4, 50),
    ('AGUS7', 'Agus 7 Hydroelectric Plant', 200, 'Lanao del Norte', 4, 50),
]

for code, name, capacity, location, num_units, unit_capacity in plants_data:
    # Create or get plant
    plant, created = Plant.objects.get_or_create(
        code=code,
        defaults={
            'name': name,
            'capacity_mw': capacity,
            'location': location
        }
    )
    
    if created:
        print(f"✓ Created plant: {code}")
    else:
        print(f"○ Plant already exists: {code}")
    
    # Create units
    for i in range(1, num_units + 1):
        unit, created = Unit.objects.get_or_create(
            plant=plant,
            unit_number=i,
            defaults={'capacity_mw': unit_capacity}
        )
        
        if created:
            print(f"  ✓ Created unit: {code} Unit {i}")

print("\n✓ All plants and units created successfully!")
print("\nPlants in database:")
for plant in Plant.objects.all():
    units_count = plant.units.count()
    print(f"  - {plant.code}: {plant.name} ({units_count} units)")
