import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'npc_reporting.settings')
django.setup()

from django.contrib.auth.models import User
from reports.serializers import UserProfileSerializer
import json

print('Testing UserProfileSerializer...')
print()

# Test viewer1
try:
    viewer = User.objects.get(username='viewer1')
    serializer = UserProfileSerializer(viewer)
    data = serializer.data
    
    print('✓ viewer1 profile:')
    print(f'  Role: {data["profile"]["role"]}')
    print(f'  Can Upload: {data["profile"]["permissions"]["can_upload_data"]}')
    print(f'  Can Approve: {data["profile"]["permissions"]["can_approve_data"]}')
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
    print(f'  Role: {data["profile"]["role"]}')
    print(f'  Plant: {data["profile"]["plant_name"]}')
    print(f'  Can Upload: {data["profile"]["permissions"]["can_upload_data"]}')
    print(f'  Can Approve: {data["profile"]["permissions"]["can_approve_data"]}')
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
    print(f'  Role: {data["profile"]["role"]}')
    print(f'  Can Upload: {data["profile"]["permissions"]["can_upload_data"]}')
    print(f'  Can Approve: {data["profile"]["permissions"]["can_approve_data"]}')
    print()
except Exception as e:
    print(f'✗ Error with manager1: {e}')
    print()

print('========================================')
print('API test complete!')
print()
print('Expected Results:')
print('  viewer1   - VIEWER role, cannot upload/approve')
print('  operator1 - OPERATOR role, can upload, cannot approve')
print('  manager1  - MANAGER role, can upload and approve')
