#!/usr/bin/env python3
"""
Test the signature setup endpoint to identify the NameError
"""
import requests
import json

# Get a recent authorization with setup token
def get_recent_authorization():
    login_data = {
        "username": "admin",
        "password": "admin123"
    }
    
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
                
                # Get recent authorizations
                auth_response = requests.get(
                    "http://localhost:8000/api/signatory-authorizations/my-authorizations/",
                    headers=headers
                )
                
                if auth_response.status_code == 200:
                    auths = auth_response.json()
                    # Find one that was created recently
                    for auth in auths:
                        if 'FINAL REAL EMAIL TEST' in auth['signatory_name'] or 'AUTO PROCESSOR TEST' in auth['signatory_name']:
                            return auth
                            
    except Exception as e:
        print(f"Error getting authorization: {e}")
    
    return None

def test_signature_setup():
    print("Testing signature setup endpoint...")
    
    # First, let's get the setup token from the database directly
    # We'll use a known token from our recent tests
    
    # Let's try with a test token to see the error
    test_token = "test_token_to_see_error"
    
    try:
        # Test the signature setup endpoint
        response = requests.get(f"http://localhost:8000/api/signatory-authorizations/signature-setup/{test_token}/")
        
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 500:
            print("\n❌ 500 Internal Server Error detected!")
            print("This confirms there's a server-side error in the signature setup endpoint.")
            
    except Exception as e:
        print(f"❌ Error testing endpoint: {e}")

if __name__ == "__main__":
    test_signature_setup()