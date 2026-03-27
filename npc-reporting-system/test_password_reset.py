"""
Quick test script for password reset request endpoint
Run this after starting the backend server
"""

import requests
import json

API_URL = "http://localhost:8000/api"

def test_password_reset_request():
    """Test the password reset request endpoint"""
    
    print("Testing Password Reset Request Endpoint")
    print("=" * 50)
    
    # Test 1: Valid username
    print("\nTest 1: Valid username with reason")
    data = {
        "username": "admin",  # Assuming admin user exists
        "reason": "Testing password reset functionality"
    }
    
    try:
        response = requests.post(
            f"{API_URL}/auth/password-reset-request/",
            json=data,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 201:
            print("✓ Test 1 PASSED: Request created successfully")
        else:
            print("✗ Test 1 FAILED: Unexpected status code")
    except Exception as e:
        print(f"✗ Test 1 ERROR: {str(e)}")
    
    # Test 2: Invalid username
    print("\n" + "=" * 50)
    print("\nTest 2: Invalid username")
    data = {
        "username": "nonexistent_user_12345",
        "reason": "Testing with invalid username"
    }
    
    try:
        response = requests.post(
            f"{API_URL}/auth/password-reset-request/",
            json=data,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 404:
            print("✓ Test 2 PASSED: Invalid username rejected correctly")
        else:
            print("✗ Test 2 FAILED: Should return 404 for invalid username")
    except Exception as e:
        print(f"✗ Test 2 ERROR: {str(e)}")
    
    # Test 3: Without reason (optional field)
    print("\n" + "=" * 50)
    print("\nTest 3: Valid username without reason")
    data = {
        "username": "admin"
    }
    
    try:
        response = requests.post(
            f"{API_URL}/auth/password-reset-request/",
            json=data,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 201:
            print("✓ Test 3 PASSED: Request created without reason")
        else:
            print("✗ Test 3 FAILED: Should accept request without reason")
    except Exception as e:
        print(f"✗ Test 3 ERROR: {str(e)}")
    
    print("\n" + "=" * 50)
    print("\nAll tests completed!")
    print("\nNext steps:")
    print("1. Check Django admin panel at http://localhost:8000/admin/")
    print("2. Navigate to 'Password Reset Requests' section")
    print("3. Verify the test requests appear in the list")
    print("4. Check email inbox for admin notifications (if SMTP configured)")

if __name__ == "__main__":
    test_password_reset_request()
