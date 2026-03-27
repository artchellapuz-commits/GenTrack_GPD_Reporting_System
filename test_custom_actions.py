#!/usr/bin/env python3
"""
Test if custom actions are working at all
"""

import requests

# Configuration
BACKEND_URL = "http://localhost:8000"

def test_custom_actions():
    """Test custom actions"""
    print("🧪 Testing Custom Actions")
    print("=" * 50)
    
    # Login
    login_data = {"username": "testuser", "password": "testpass123"}
    login_response = requests.post(f"{BACKEND_URL}/api/auth/login/", json=login_data)
    token = login_response.json()['access']
    headers = {'Authorization': f'Bearer {token}'}
    
    # Test 1: my-authorizations (GET action)
    print("\n1. Testing my-authorizations action...")
    response = requests.get(f"{BACKEND_URL}/api/signatory-authorizations/my-authorizations/", headers=headers)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print("✅ my-authorizations action works")
    else:
        print(f"❌ my-authorizations action failed: {response.text}")
    
    # Test 2: my-requests (GET action)
    print("\n2. Testing my-requests action...")
    response = requests.get(f"{BACKEND_URL}/api/signatory-authorizations/my-requests/", headers=headers)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print("✅ my-requests action works")
        print(f"Number of requests: {len(response.json())}")
    else:
        print(f"❌ my-requests action failed: {response.text}")
    
    # Test 3: Try to call request action with GET (should fail)
    print("\n3. Testing request action with GET (should fail)...")
    response = requests.get(f"{BACKEND_URL}/api/signatory-authorizations/request/", headers=headers)
    print(f"Status: {response.status_code}")
    if response.status_code == 405:  # Method not allowed
        print("✅ GET to request action properly rejected (method not allowed)")
    else:
        print(f"❌ Unexpected response: {response.text}")
    
    # Test 4: Try to call a non-existent action
    print("\n4. Testing non-existent action...")
    response = requests.get(f"{BACKEND_URL}/api/signatory-authorizations/nonexistent/", headers=headers)
    print(f"Status: {response.status_code}")
    if response.status_code == 404:
        print("✅ Non-existent action properly returns 404")
    else:
        print(f"❌ Unexpected response: {response.text}")

if __name__ == "__main__":
    test_custom_actions()