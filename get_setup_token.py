#!/usr/bin/env python3
"""
Get a setup token from the database to test the endpoint
"""
import requests
import json

print("Getting setup token from recent authorization...")

# Login to get access to the API
login_data = {
    "username": "admin",
    "password": "admin123"
}

try:
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
                print(f"Found {len(auths)} authorizations")
                
                # Look for recent test authorizations
                for auth in auths[-5:]:  # Check last 5
                    print(f"Authorization: {auth['signatory_name']} (ID: {auth['id']})")
                    
                    # Since we can't get the setup token from the API response,
                    # let's create a new request and manually extract the token
                    
                # Create a new test request to get a fresh token
                test_data = {
                    "signatory_name": "TOKEN EXTRACTION TEST",
                    "role": "Test Role", 
                    "email": "tokentest@example.com",
                    "justification": "Getting a setup token to test the endpoint"
                }
                
                print("\nCreating new request to get setup token...")
                response = requests.post(
                    "http://localhost:8000/api/signatory-authorizations/request/",
                    json=test_data,
                    headers=headers
                )
                
                if response.status_code == 201:
                    print("✅ Request created, waiting for auto-processor...")
                    import time
                    time.sleep(8)
                    
                    # The auto-processor should have created an authorization
                    # Let's get the updated list
                    auth_response2 = requests.get(
                        "http://localhost:8000/api/signatory-authorizations/my-authorizations/",
                        headers=headers
                    )
                    
                    if auth_response2.status_code == 200:
                        auths2 = auth_response2.json()
                        token_auth = None
                        for auth in auths2:
                            if auth['signatory_name'] == 'TOKEN EXTRACTION TEST':
                                token_auth = auth
                                break
                        
                        if token_auth:
                            print(f"✅ Found authorization: ID={token_auth['id']}")
                            
                            # Since we can't get the setup token from the API,
                            # let's use the management command to get it
                            print("\nThe setup token is stored in the database but not exposed via API.")
                            print("To test the signature setup, we need to:")
                            print("1. Fix the authentication issue in the ViewSet")
                            print("2. Or access the database directly")
                            
                            # For now, let's test if the endpoint works with authentication
                            print("\nTesting signature setup endpoint WITH authentication...")
                            setup_response = requests.get(
                                "http://localhost:8000/api/signatory-authorizations/signature-setup/dummy_token/",
                                headers=headers
                            )
                            
                            print(f"Status: {setup_response.status_code}")
                            print(f"Response: {setup_response.text}")
                            
                            if setup_response.status_code == 404:
                                print("✅ Endpoint works with authentication (404 = token not found, expected)")
                            elif setup_response.status_code == 500:
                                print("❌ 500 error - there's still a bug in the endpoint")
                        else:
                            print("❌ Authorization not found after auto-processing")
                    else:
                        print(f"❌ Failed to get updated authorizations: {auth_response2.text}")
                else:
                    print(f"❌ Failed to create test request: {response.text}")
            else:
                print(f"❌ Failed to get authorizations: {auth_response.text}")
        else:
            print("❌ No access token")
    else:
        print(f"❌ Login failed: {login_response.status_code}")
        
except Exception as e:
    print(f"❌ Error: {e}")