@echo off
echo ========================================
echo  Testing Role-Based API
echo ========================================
echo.

cd backend

echo Testing API endpoints...
echo.

python -c "
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'npc_reporting.settings')
django.setup()

from django.contrib.auth.models import User
from reports.serializers import UserProfileSerializer

print('Testing UserProfileSerializer...')
print()

# Test viewer1
try:
    viewer = User.objects.get(username='viewer1')
    serializer = UserProfileSerializer(viewer)
    data = serializer.data
    
    print('✓ viewer1 profile:')
    print(f'  Role: {data[\"profile\"][\"role\"]}')
    print(f'  Can Upload: {data[\"profile\"][\"permissions\"][\"can_upload_data\"]}')
    print(f'  Can Approve: {data[\"profile\"][\"permissions\"][\"can_approve_data\"]}')
    print()
except Exception as e:
    print(f'✗ Error with viewer1: {e}')
    print()

# Test operator1
try:
    operator = User.objects.get(username='operator1')
    serializer = UserProfileSerializer(operator)
    data = serializer.data
    
    print('✓ operator1 profile:')
    print(f'  Role: {data[\"profile\"][\"role\"]}')
    print(f'  Plant: {data[\"profile\"][\"plant_name\"]}')
    print(f'  Can Upload: {data[\"profile\"][\"permissions\"][\"can_upload_data\"]}')
    print(f'  Can Approve: {data[\"profile\"][\"permissions\"][\"can_approve_data\"]}')
    print()
except Exception as e:
    print(f'✗ Error with operator1: {e}')
    print()

# Test manager1
try:
    manager = User.objects.get(username='manager1')
    serializer = UserProfileSerializer(manager)
    data = serializer.data
    
    print('✓ manager1 profile:')
    print(f'  Role: {data[\"profile\"][\"role\"]}')
    print(f'  Can Upload: {data[\"profile\"][\"permissions\"][\"can_upload_data\"]}')
    print(f'  Can Approve: {data[\"profile\"][\"permissions\"][\"can_approve_data\"]}')
    print()
except Exception as e:
    print(f'✗ Error with manager1: {e}')
    print()

print('API test complete!')
"

echo.
echo ========================================
echo  Next Steps:
echo ========================================
echo  1. Start backend: python manage.py runserver
echo  2. Start frontend: npm run serve
echo  3. Login with test users to see differences
echo.
pause
