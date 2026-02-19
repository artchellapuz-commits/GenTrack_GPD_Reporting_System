import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'npc_reporting.settings')
django.setup()

from django.contrib.auth.models import User
from reports.models import UserProfile, Plant

print("Creating test users...")
print()

# Create viewer
try:
    viewer = User.objects.create_user('viewer1', 'viewer@test.com', 'test123')
    viewer.profile.role = 'VIEWER'
    viewer.profile.save()
    print('✓ Created viewer1 (password: test123)')
except Exception as e:
    print(f'✗ viewer1: {e}')

# Create operator
try:
    operator = User.objects.create_user('operator1', 'operator@test.com', 'test123')
    operator.profile.role = 'OPERATOR'
    plant = Plant.objects.first()
    if plant:
        operator.profile.plant = plant
        print(f'✓ Created operator1 (password: test123) - Assigned to {plant.name}')
    else:
        operator.profile.save()
        print('✓ Created operator1 (password: test123) - No plant assigned')
except Exception as e:
    print(f'✗ operator1: {e}')

# Create manager
try:
    manager = User.objects.create_user('manager1', 'manager@test.com', 'test123')
    manager.profile.role = 'MANAGER'
    manager.profile.save()
    print('✓ Created manager1 (password: test123)')
except Exception as e:
    print(f'✗ manager1: {e}')

print()
print("Test users created successfully!")
print()
print("Login credentials:")
print("  viewer1    / test123  (VIEWER role)")
print("  operator1  / test123  (OPERATOR role)")
print("  manager1   / test123  (MANAGER role)")
