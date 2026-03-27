#!/usr/bin/env python3
"""
Test the specific request endpoint to see if it works
"""
import requests
import json

# Test data
test_data = {
    "signatory_name": "ENDPOINT TEST",
    "role": "Test Role",
    "email": "test@example.com",
    "justification": "Testing the specific request endpoint"
}

# Get auth token first
login_data = {
    "username": "admin",
    "password": "admin123"
}

print("Testing specific request endpoint...")

try:
    # Login to get token
    login_response = requests.post(
        "http://localhost:8000/api/auth/login/",
        json=login_data,
        headers={'Content-Type': 'application/json'}
    )
    
    if login_response.status_code == 200:
        token_data = login_response.json()
        access_token = token_data.get('access')
        
        if access_token:
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {access_token}'
            }
            
            print("Testing different endpoints:")
            
            # Test 1: POST to /request/ (should work)
            print("\n1. Testing POST /signatory-authorizations/request/")
            response1 = requests.post(
                "http://localhost:8000/api/signatory-authorizations/request/",
                json=test_data,
                headers=headers
            )
            print(f"Status: {response1.status_code}")
            if response1.status_code == 201:
                result = response1.json()
                print(f"✅ SUCCESS: Request created with ID {result['id']}")
                print(f"Status: {result['status']}")
            else:
                print(f"❌ FAILED: {response1.text}")
            
            # Test 2: POST to base endpoint (should fail now)
            print("\n2. Testing POST /signatory-authorizations/")
            test_data2 = test_data.copy()
            test_data2["signatory_name"] = "BASE ENDPOINT TEST"
            
            response2 = requests.post(
                "http://localhost:8000/api/signatory-authorizations/",
                json=test_data2,
                headers=headers
            )
            print(f"Status: {response2.status_code}")
            print(f"Response: {response2.text}")
            
        else:
            print("❌ No access token in login response")
    else:
        print(f"❌ Login failed: {login_response.status_code}")
        
except Exception as e:
    print(f"❌ Error: {e}")