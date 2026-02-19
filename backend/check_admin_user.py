"""
Check Admin User Configuration
Run this to verify your admin user is properly configured
"""

import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'npc_reporting.settings')
django.setup()

from django.contrib.auth.models import User
from reports.models import UserProfile

def check_admin_user():
    print("=" * 60)
    print("CHECKING ADMIN USER CONFIGURATION")
    print("=" * 60)
    
    # Find admin user
    try:
        admin = User.objects.get(username='admin')
        print(f"\n✓ Found user: {admin.username}")
        print(f"  ID: {admin.id}")
        print(f"  Email: {admin.email or 'Not set'}")
        print(f"  is_staff: {admin.is_staff}")
        print(f"  is_superuser: {admin.is_superuser}")
        print(f"  is_active: {admin.is_active}")
        
        # Check if user has profile
        try:
            profile = admin.profile
            print(f"\n✓ User has profile:")
            print(f"  Role: {profile.role}")
            print(f"  Department: {profile.department or 'Not set'}")
            print(f"  Phone: {profile.phone or 'Not set'}")
            print(f"\n✓ Permissions:")
            print(f"  Can upload data: {profile.can_upload_data()}")
            print(f"  Can approve data: {profile.can_approve_data()}")
            print(f"  Can manage users: {profile.can_manage_users()}")
            print(f"  Can export data: {profile.can_export_data()}")
        except UserProfile.DoesNotExist:
            print("\n✗ User has NO profile!")
            print("  Creating profile now...")
            profile = UserProfile.objects.create(
                user=admin,
                role='ADMIN'
            )
            print(f"✓ Profile created with role: {profile.role}")
        
        # Check what needs to be fixed
        print("\n" + "=" * 60)
        print("DIAGNOSIS")
        print("=" * 60)
        
        issues = []
        fixes = []
        
        if not admin.is_staff:
            issues.append("✗ is_staff is False")
            fixes.append("Set is_staff = True")
            admin.is_staff = True
            admin.save()
            print("✓ Fixed: Set is_staff = True")
        
        if not admin.is_active:
            issues.append("✗ is_active is False")
            fixes.append("Set is_active = True")
            admin.is_active = True
            admin.save()
            print("✓ Fixed: Set is_active = True")
        
        try:
            profile = admin.profile
            if profile.role != 'ADMIN':
                issues.append(f"✗ Profile role is {profile.role}, not ADMIN")
                fixes.append("Set profile.role = 'ADMIN'")
                profile.role = 'ADMIN'
                profile.save()
                print("✓ Fixed: Set profile.role = 'ADMIN'")
        except UserProfile.DoesNotExist:
            issues.append("✗ No UserProfile exists")
            fixes.append("Create UserProfile with role='ADMIN'")
        
        if not issues:
            print("\n✓ Everything is configured correctly!")
            print("\nUser Management should be visible in the sidebar.")
            print("\nIf it's still not showing:")
            print("1. Logout and login again")
            print("2. Or clear browser cache and localStorage")
        else:
            print("\n✓ All issues have been fixed!")
            print("\nNow:")
            print("1. Restart the backend server")
            print("2. Logout and login again in the frontend")
            print("3. User Management should now appear")
        
        # Show what the API will return
        print("\n" + "=" * 60)
        print("API RESPONSE PREVIEW")
        print("=" * 60)
        print("\nWhen you login, the API will return:")
        print(f"""
{{
  "id": {admin.id},
  "username": "{admin.username}",
  "email": "{admin.email or ''}",
  "is_staff": {str(admin.is_staff).lower()},
  "is_active": {str(admin.is_active).lower()},
  "profile": {{
    "role": "{admin.profile.role}",
    "role_display": "{admin.profile.get_role_display()}",
    "permissions": {{
      "can_upload_data": {str(admin.profile.can_upload_data()).lower()},
      "can_approve_data": {str(admin.profile.can_approve_data()).lower()},
      "can_manage_users": {str(admin.profile.can_manage_users()).lower()},
      "can_export_data": {str(admin.profile.can_export_data()).lower()}
    }}
  }}
}}
""")
        
    except User.DoesNotExist:
        print("\n✗ Admin user does not exist!")
        print("\nCreating admin user now...")
        admin = User.objects.create_superuser(
            username='admin',
            email='admin@npc.com',
            password='admin123'
        )
        print(f"✓ Admin user created: {admin.username}")
        
        # Create profile
        profile = UserProfile.objects.create(
            user=admin,
            role='ADMIN'
        )
        print(f"✓ Profile created with role: {profile.role}")
        print("\nYou can now login with:")
        print("  Username: admin")
        print("  Password: admin123")
    
    print("\n" + "=" * 60)
    print("CHECK COMPLETE")
    print("=" * 60)

if __name__ == "__main__":
    check_admin_user()
