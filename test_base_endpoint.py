#!/usr/bin/env python3
"""
Test the base endpoint to see what happens
"""
import requests
import json

# Test data
test_data = {
    "signatory_name": "BASE ENDPOINT TEST",
    "role": "Test Role",
    "email": "basetest@example.com",
    "justification": "Testing the base endpoint"
}

# Get auth token first
login_data = {
    "username": "admin",
    "password": "admin123"
}

print("Testing base endpoint...")

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
            
            print("Testing POST to base endpoint /signatory-authorizations/")
            response = requests.post(
                "http://localhost:8000/api/signatory-authorizations/",
                json=test_data,
                headers=headers
            )
            
            print(f"Status: {response.status_code}")
            print(f"Response: {response.text}")
            
            print("\nTesting POST to /request/ endpoint")
            test_data2 = test_data.copy()
            test_data2["signatory_name"] = "REQUEST ENDPOINT TEST"
            
            response2 = requests.post(
                "http://localhost:8000/api/signatory-authorizations/request/",
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