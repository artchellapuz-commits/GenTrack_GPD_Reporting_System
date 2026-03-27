#!/usr/bin/env python3
"""
Test the signature setup endpoint without authentication
"""
import requests
import json

print("Testing signature setup endpoint without authentication...")

try:
    # Test with a dummy token to see if the endpoint is accessible
    setup_response = requests.get(
        "http://localhost:8000/api/signatory-authorizations/signature-setup/dummy_token/"
    )
    
    print(f"Setup endpoint status: {setup_response.status_code}")
    print(f"Setup endpoint response: {setup_response.text}")
    
    if setup_response.status_code == 500:
        print("❌ 500 Internal Server Error - there's still a bug in the endpoint")
    elif setup_response.status_code == 404:
        print("✅ 404 Not Found - endpoint is working but token is invalid (expected)")
    elif setup_response.status_code == 401:
        print("❌ 401 Unauthorized - endpoint still requires authentication")
    else:
        print(f"Status {setup_response.status_code} - endpoint is accessible")
        
    # Now let's get a real token and test it
    print("\nGetting a real setup token...")
    
    # Login to create a test request
    login_data = {
        "username": "admin",
        "password": "admin123"
    }
    
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
            
            # Create a test request
            test_data = {
                "signatory_name": "ENDPOINT FIX TEST",
                "role": "Test Role",
                "email": "endpointfix@example.com",
                "justification": "Testing the fixed signature setup endpoint"
            }
            
            response = requests.post(
                "http://localhost:8000/api/signatory-authorizations/request/",
                json=test_data,
                headers=headers
            )
            
            if response.status_code == 201:
                print("✅ Test request created, waiting for auto-processor...")
                import time
                time.sleep(5)
                
                # Check if we can find the setup token in the success file
                try:
                    with open('npc-reporting-system/backend/email_workflow_success.txt', 'r', encoding='utf-8') as f:
                        success_content = f.read()
                        lines = success_content.split('\n')
                        setup_token = None
                        for line in lines:
                            if line.startswith('Setup Token:'):
                                setup_token = line.split(': ')[1].strip()
                                break
                        
                        if setup_token:
                            print(f"Found setup token: {setup_token[:20]}...")
                            
                            # Test the endpoint with the real token (no auth)
                            real_setup_response = requests.get(
                                f"http://localhost:8000/api/signatory-authorizations/signature-setup/{setup_token}/"
                            )
                            
                            print(f"\nReal token test:")
                            print(f"Status: {real_setup_response.status_code}")
                            print(f"Response: {real_setup_response.text}")
                            
                            if real_setup_response.status_code == 200:
                                print("🎉 SUCCESS! Signature setup endpoint is working without authentication!")
                                setup_data = real_setup_response.json()
                                print(f"Signatory: {setup_data.get('signatory_name')}")
                                print(f"User: {setup_data.get('user_name')}")
                                print(f"2FA Required: {setup_data.get('requires_2fa')}")
                            else:
                                print("❌ Still having issues with the real token")
                        else:
                            print("❌ Could not find setup token in success file")
                            
                except FileNotFoundError:
                    print("❌ No success file found - auto-processor may not have run")
            else:
                print(f"❌ Failed to create test request: {response.text}")
                
except Exception as e:
    print(f"❌ Error: {e}")