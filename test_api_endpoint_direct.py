#!/usr/bin/env python3
"""
Test the API endpoint directly to see if it's using the updated code
"""

import requests
import json

# Configuration
BACKEND_URL = "http://localhost:8000"

def test_api_endpoint():
    """Test the API endpoint directly"""
    print("🧪 Testing API Endpoint Directly")
    print("=" * 50)
    
    # Login
    print("1. Logging in...")
    login_data = {"username": "testuser", "password": "testpass123"}
    login_response = requests.post(f"{BACKEND_URL}/api/auth/login/", json=login_data)
    
    if login_response.status_code != 200:
        print(f"❌ Login failed: {login_response.status_code}")
        return False
    
    token = login_response.json()['access']
    headers = {'Authorization': f'Bearer {token}'}
    print("✅ Login successful")
    
    # Submit request with unique name
    print("\n2. Submitting authorization request...")
    request_data = {
        "signatory_name": "MINIMAL TEST",
        "role": "Test Role",
        "email": "apitest@example.com",
        "justification": "Testing API endpoint directly to see if debug messages appear"
    }
    
    print(f"Calling URL: {BACKEND_URL}/api/signatory-authorizations/request/")
    response = requests.post(
        f"{BACKEND_URL}/api/signatory-authorizations/request/",
        json=request_data,
        headers=headers
    )
    
    print(f"Response Status: {response.status_code}")
    print(f"Response: {response.text}")
    
    if response.status_code == 201:
        response_data = response.json()
        request_id = response_data['id']
        print(f"✅ Request created with ID: {request_id}")
        
        # Check if authorization was auto-created
        print("\n3. Checking for auto-created authorization...")
        auth_response = requests.get(
            f"{BACKEND_URL}/api/signatory-authorizations/my-authorizations/",
            headers=headers
        )
        
        if auth_response.status_code == 200:
            authorizations = auth_response.json()
            fresh_test_auths = [auth for auth in authorizations if auth['signatory_name'] == 'FRESH SERVER TEST']
            
            if fresh_test_auths:
                auth = fresh_test_auths[0]
                print("✅ Authorization auto-created!")
                print(f"  - Active: {auth['is_active']}")
                print(f"  - Has setup token: {'setup_token' in auth and auth['setup_token'] is not None}")
                
                if auth.get('setup_token'):
                    setup_url = f"http://localhost:8081/signature-setup/{auth['setup_token']}"
                    print(f"  - Setup URL: {setup_url}")
                    print("\n🎯 SUCCESS! The API endpoint is working with the new code!")
                    return True
                else:
                    print("❌ No setup token found")
                    return False
            else:
                print("❌ No authorization found for FRESH SERVER TEST")
                return False
        else:
            print(f"❌ Failed to get authorizations: {auth_response.status_code}")
            return False
    else:
        print(f"❌ Request failed: {response.status_code}")
        return False

if __name__ == "__main__":
    success = test_api_endpoint()
    if success:
        print("\n🎉 API endpoint is working with the updated code!")
        print("📧 Check your email for the confirmation message with signature setup link!")
    else:
        print("\n❌ API endpoint is not working as expected.")