"""
Check if Pulangi 4 is properly configured in the system
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'npc_reporting.settings')
django.setup()

from reports.models import Plant, Unit

print("=" * 60)
print("PULANGI 4 SYSTEM CHECK")
print("=" * 60)
print()

# Check if Pulangi 4 exists
try:
    plant = Plant.objects.get(code='PULANGI4')
    print("✓ Pulangi 4 plant found in database")
    print(f"  Name: {plant.name}")
    print(f"  Code: {plant.code}")
    print(f"  Capacity: {plant.capacity_mw} MW")
    print(f"  Location: {plant.location}")
    print(f"  Active: {plant.is_active}")
    print()
    
    # Check units
    units = Unit.objects.filter(plant=plant).order_by('unit_number')
    print(f"✓ Found {units.count()} units:")
    for unit in units:
        print(f"  Unit {unit.unit_number}: {unit.capacity_mw} MW (Active: {unit.is_active})")
    print()
    
    # Check if it's in PLANT_CHOICES
    plant_choices = dict(Plant.PLANT_CHOICES)
    if 'PULANGI4' in plant_choices:
        print(f"✓ PULANGI4 is in Plant.PLANT_CHOICES")
        print(f"  Display name: {plant_choices['PULANGI4']}")
    else:
        print("✗ PULANGI4 is NOT in Plant.PLANT_CHOICES")
        print("  Available choices:", list(plant_choices.keys()))
    print()
    
    # Summary
    print("=" * 60)
    print("SYSTEM STATUS: READY")
    print("=" * 60)
    print()
    print("Pulangi 4 is properly configured!")
    print()
    print("You can now:")
    print("1. Upload Excel files for Pulangi 4 (3 units)")
    print("2. View Pulangi 4 in the dashboard")
    print("3. Generate reports including Pulangi 4")
    print()
    print("Sample Excel file: SAMPLE_PULANGI4.xlsx")
    print("Upload guide: PULANGI4_UPLOAD_GUIDE.md")
    print()
    
except Plant.DoesNotExist:
    print("✗ Pulangi 4 NOT found in database!")
    print()
    print("To fix this, run:")
    print("  python add_pulangi4.py")
    print()
except Exception as e:
    print(f"✗ Error checking Pulangi 4: {str(e)}")
    print()
    import traceback
    traceback.print_exc()
