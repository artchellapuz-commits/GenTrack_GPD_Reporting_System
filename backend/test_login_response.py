"""
Test script to verify login response includes role and permissions
"""
import requests
import json

API_URL = "http://localhost:8000/api"

def test_login(username, password):
    """Test login and check response structure"""
    print(f"\n{'='*60}")
    print(f"Testing login for: {username}")
    print(f"{'='*60}")
    
    try:
        response = requests.post(
            f"{API_URL}/auth/login/",
            json={"username": username, "password": password}
        )
        
        if response.status_code == 200:
            data = response.json()
            print("\n✅ Login successful!")
            print(f"\nAccess Token: {data.get('access', 'N/A')[:50]}...")
            print(f"Refresh Token: {data.get('refresh', 'N/A')[:50]}...")
            
            # Check user data
            user = data.get('user', {})
            print(f"\n📋 User Data:")
            print(f"  Username: {user.get('username')}")
            print(f"  Email: {user.get('email')}")
            print(f"  Is Staff: {user.get('is_staff')}")
            
            # Check profile data
            profile = user.get('profile')
            if profile:
                print(f"\n👤 Profile Data:")
                print(f"  Role: {profile.get('role')}")
                print(f"  Role Display: {profile.get('role_display')}")
                print(f"  Plant: {profile.get('plant_name', 'N/A')}")
                print(f"  Department: {profile.get('department', 'N/A')}")
                print(f"  Position: {profile.get('position', 'N/A')}")
                
                # Check permissions
                permissions = profile.get('permissions', {})
                print(f"\n🔐 Permissions:")
                print(f"  Can Upload Data: {permissions.get('can_upload_data')}")
                print(f"  Can Approve Data: {permissions.get('can_approve_data')}")
                print(f"  Can Manage Users: {permissions.get('can_manage_users')}")
                print(f"  Can Export Data: {permissions.get('can_export_data')}")
            else:
                print("\n❌ No profile data found in response!")
                print("\nFull response:")
                print(json.dumps(data, indent=2))
        else:
            print(f"\n❌ Login failed with status {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    # Test all user roles
    test_users = [
        ("viewer1", "test123"),
        ("operator1", "test123"),
        ("manager1", "test123"),
    ]
    
    for username, password in test_users:
        test_login(username, password)
    
    print(f"\n{'='*60}")
    print("Testing complete!")
    print(f"{'='*60}\n")
