#!/usr/bin/env python3
"""
Test the real API request to see if the fixed workflow works
"""
import requests
import json

# Test data
test_data = {
    "signatory_name": "REAL API TEST",
    "role": "Test Role",
    "email": "test@example.com",
    "justification": "Testing the real API workflow after fixes"
}

# Get auth token first (you'll need to replace with actual credentials)
login_data = {
    "username": "admin",  # Replace with actual username
    "password": "admin123"  # Replace with actual password
}

print("Testing real API workflow...")

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
            print("✅ Login successful, got access token")
            
            # Make the authorization request
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {access_token}'
            }
            
            response = requests.post(
                "http://localhost:8000/api/signatory-authorizations/request/",
                json=test_data,
                headers=headers
            )
            
            print(f"\nAuthorization Request:")
            print(f"Status: {response.status_code}")
            print(f"Response: {json.dumps(response.json(), indent=2)}")
            
            if response.status_code == 201:
                print("\n✅ SUCCESS: Authorization request created!")
                print("Check your email for the signature setup link.")
                
                # Also check the debug log
                try:
                    with open('npc-reporting-system/backend/debug_log.txt', 'r') as f:
                        log_content = f.read()
                        if log_content:
                            print(f"\nDebug Log:\n{log_content}")
                except FileNotFoundError:
                    print("No debug log found")
            else:
                print(f"❌ Request failed: {response.text}")
        else:
            print("❌ No access token in login response")
    else:
        print(f"❌ Login failed: {login_response.status_code}")
        print(f"Response: {login_response.text}")
        
except Exception as e:
    print(f"❌ Error: {e}")