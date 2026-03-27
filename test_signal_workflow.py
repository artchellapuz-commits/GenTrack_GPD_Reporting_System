#!/usr/bin/env python3
"""
Test the signal-based email workflow
"""
import requests
import json
import time

# Test data
test_data = {
    "signatory_name": "SIGNAL TEST",
    "role": "Test Role",
    "email": "signaltest@example.com",
    "justification": "Testing the signal-based email workflow"
}

# Get auth token first
login_data = {
    "username": "admin",
    "password": "admin123"
}

print("Testing signal-based email workflow...")

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
            
            print("Making request...")
            response = requests.post(
                "http://localhost:8000/api/signatory-authorizations/request/",
                json=test_data,
                headers=headers
            )
            
            print(f"Status: {response.status_code}")
            if response.status_code == 201:
                result = response.json()
                print(f"✅ Request created: ID={result['id']}, Status={result['status']}")
                
                # Wait a moment for signal processing
                time.sleep(5)
                
                # Check for success/error files
                try:
                    with open('npc-reporting-system/backend/email_workflow_success.txt', 'r', encoding='utf-8') as f:
                        success_content = f.read()
                        print(f"\n✅ EMAIL WORKFLOW SUCCESS!")
                        print(success_content)
                        
                        # If we have success, check the results
                        auth_response = requests.get(
                            "http://localhost:8000/api/signatory-authorizations/my-authorizations/",
                            headers=headers
                        )
                        
                        if auth_response.status_code == 200:
                            auths = auth_response.json()
                            signal_auth = None
                            for auth in auths:
                                if auth['signatory_name'] == 'SIGNAL TEST':
                                    signal_auth = auth
                                    break
                            
                            if signal_auth:
                                print(f"\n✅ Authorization auto-created:")
                                print(f"ID: {signal_auth['id']}")
                                print(f"Active: {signal_auth['is_active']}")
                                print(f"Valid: {signal_auth['is_valid']}")
                                
                                # Check request status
                                req_response = requests.get(
                                    "http://localhost:8000/api/signatory-authorizations/my-requests/",
                                    headers=headers
                                )
                                
                                if req_response.status_code == 200:
                                    requests_data = req_response.json()
                                    signal_request = None
                                    for req in requests_data:
                                        if req['signatory_name'] == 'SIGNAL TEST':
                                            signal_request = req
                                            break
                                    
                                    if signal_request and signal_request['status'] == 'APPROVED':
                                        print("\n🎉 COMPLETE SUCCESS!")
                                        print("✅ Request created via API")
                                        print("✅ Signal triggered email workflow")
                                        print("✅ Authorization auto-created")
                                        print("✅ Request auto-approved")
                                        print("✅ Email sent with signature setup link")
                                        print("\n🎯 THE SIGNAL-BASED WORKFLOW IS WORKING!")
                                        
                                        # Extract setup URL from success file
                                        lines = success_content.split('\n')
                                        for line in lines:
                                            if line.startswith('Setup Token:'):
                                                token = line.split(': ')[1]
                                                setup_url = f"http://localhost:8081/signature-setup/{token}"
                                                print(f"\n🔗 Signature Setup URL: {setup_url}")
                                                break
                        
                except FileNotFoundError:
                    print("\n❌ No success file found")
                
                try:
                    with open('npc-reporting-system/backend/email_workflow_error.txt', 'r', encoding='utf-8') as f:
                        error_content = f.read()
                        print(f"\n❌ EMAIL WORKFLOW ERROR!")
                        print(error_content)
                except FileNotFoundError:
                    print("No error file found - signal may not have been triggered")
                        
            else:
                print(f"❌ FAILED: {response.text}")
                
        else:
            print("❌ No access token in login response")
    else:
        print(f"❌ Login failed: {login_response.status_code}")
        
except Exception as e:
    print(f"❌ Error: {e}")

print("\nIf no success/error files were found, the Django server may need to be restarted to load the new signal.")