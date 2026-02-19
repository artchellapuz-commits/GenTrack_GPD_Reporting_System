"""
Test script for User Management API
Run this after starting the backend server to verify the API endpoints
"""

import requests
import json

BASE_URL = "http://localhost:8000/api"

def test_user_api():
    print("=" * 60)
    print("Testing User Management API")
    print("=" * 60)
    
    # Step 1: Login as admin
    print("\n1. Logging in as admin...")
    login_data = {
        "username": "admin",
        "password": "admin123"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/token/", json=login_data)
        if response.status_code == 200:
            token = response.json()['access']
            print("✓ Login successful")
            print(f"  Token: {token[:20]}...")
        else:
            print(f"✗ Login failed: {response.status_code}")
            print(f"  Response: {response.text}")
            return
    except Exception as e:
        print(f"✗ Error: {e}")
        return
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # Step 2: Get all users
    print("\n2. Fetching all users...")
    try:
        response = requests.get(f"{BASE_URL}/users/", headers=headers)
        if response.status_code == 200:
            users = response.json()
            if isinstance(users, dict) and 'results' in users:
                users = users['results']
            print(f"✓ Found {len(users)} users")
            for user in users:
                role = user.get('profile', {}).get('role', 'N/A')
                status = "Active" if user.get('is_active') else "Inactive"
                print(f"  - {user['username']} ({role}) - {status}")
        else:
            print(f"✗ Failed to fetch users: {response.status_code}")
            print(f"  Response: {response.text}")
    except Exception as e:
        print(f"✗ Error: {e}")
    
    # Step 3: Create a test user
    print("\n3. Creating a test user...")
    test_user_data = {
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "testpass123",
        "role": "OPERATOR",
        "is_active": True
    }
    
    try:
        response = requests.post(f"{BASE_URL}/users/", json=test_user_data, headers=headers)
        if response.status_code == 201:
            new_user = response.json()
            print(f"✓ User created successfully")
            print(f"  ID: {new_user['id']}")
            print(f"  Username: {new_user['username']}")
            print(f"  Role: {new_user.get('profile', {}).get('role', 'N/A')}")
            test_user_id = new_user['id']
        elif response.status_code == 400 and 'username' in response.text:
            print("✓ User already exists (this is okay)")
            # Get the existing user
            response = requests.get(f"{BASE_URL}/users/", headers=headers)
            users = response.json()
            if isinstance(users, dict) and 'results' in users:
                users = users['results']
            for user in users:
                if user['username'] == 'testuser':
                    test_user_id = user['id']
                    print(f"  Using existing user ID: {test_user_id}")
                    break
        else:
            print(f"✗ Failed to create user: {response.status_code}")
            print(f"  Response: {response.text}")
            test_user_id = None
    except Exception as e:
        print(f"✗ Error: {e}")
        test_user_id = None
    
    # Step 4: Update user
    if test_user_id:
        print(f"\n4. Updating user {test_user_id}...")
        update_data = {
            "email": "updated@example.com",
            "role": "MANAGER",
            "is_active": True
        }
        
        try:
            response = requests.patch(f"{BASE_URL}/users/{test_user_id}/", 
                                     json=update_data, headers=headers)
            if response.status_code == 200:
                updated_user = response.json()
                print(f"✓ User updated successfully")
                print(f"  Email: {updated_user.get('email')}")
                print(f"  Role: {updated_user.get('profile', {}).get('role', 'N/A')}")
            else:
                print(f"✗ Failed to update user: {response.status_code}")
                print(f"  Response: {response.text}")
        except Exception as e:
            print(f"✗ Error: {e}")
        
        # Step 5: Deactivate user
        print(f"\n5. Deactivating user {test_user_id}...")
        try:
            response = requests.patch(f"{BASE_URL}/users/{test_user_id}/", 
                                     json={"is_active": False}, headers=headers)
            if response.status_code == 200:
                print(f"✓ User deactivated successfully")
            else:
                print(f"✗ Failed to deactivate user: {response.status_code}")
        except Exception as e:
            print(f"✗ Error: {e}")
        
        # Step 6: Delete user
        print(f"\n6. Deleting user {test_user_id}...")
        try:
            response = requests.delete(f"{BASE_URL}/users/{test_user_id}/", headers=headers)
            if response.status_code == 204:
                print(f"✓ User deleted successfully")
            else:
                print(f"✗ Failed to delete user: {response.status_code}")
                print(f"  Response: {response.text}")
        except Exception as e:
            print(f"✗ Error: {e}")
    
    print("\n" + "=" * 60)
    print("Test completed!")
    print("=" * 60)

if __name__ == "__main__":
    test_user_api()
