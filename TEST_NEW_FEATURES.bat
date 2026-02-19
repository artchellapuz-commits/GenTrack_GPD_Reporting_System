@echo off
echo ========================================
echo  Testing Week 1-2 Features
echo ========================================
echo.

cd backend

echo Creating test users with different roles...
python -c "
from django.contrib.auth.models import User
from reports.models import UserProfile, Plant

# Create viewer
try:
    viewer = User.objects.create_user('viewer1', 'viewer@test.com', 'test123')
    viewer.profile.role = 'VIEWER'
    viewer.profile.save()
    print('✓ Created viewer1 (password: test123)')
except:
    print('✗ viewer1 already exists')

# Create operator
try:
    operator = User.objects.create_user('operator1', 'operator@test.com', 'test123')
    operator.profile.role = 'OPERATOR'
    plant = Plant.objects.first()
    if plant:
        operator.profile.plant = plant
    operator.profile.save()
    print('✓ Created operator1 (password: test123)')
except:
    print('✗ operator1 already exists')

# Create manager
try:
    manager = User.objects.create_user('manager1', 'manager@test.com', 'test123')
    manager.profile.role = 'MANAGER'
    manager.profile.save()
    print('✓ Created manager1 (password: test123)')
except:
    print('✗ manager1 already exists')

print('\nTest users created successfully!')
print('Login with: username/password = viewer1/test123, operator1/test123, or manager1/test123')
"

echo.
echo ========================================
echo  Test Users Created:
echo ========================================
echo  viewer1    / test123  (VIEWER role)
echo  operator1  / test123  (OPERATOR role)
echo  manager1   / test123  (MANAGER role)
echo.
echo  Test these features:
echo  1. Login with different users
echo  2. Check permissions in profile
echo  3. Try uploading (operator/manager only)
echo  4. Check console for email notifications
echo  5. View audit logs (admin only)
echo.
pause
