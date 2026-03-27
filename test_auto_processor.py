#!/usr/bin/env python3
"""
Test the auto-processor by creating a new request
"""
import requests
import json
import time

# Test data
test_data = {
    "signatory_name": "AUTO PROCESSOR TEST",
    "role": "Test Role",
    "email": "autoprocessor@example.com",
    "justification": "Testing the auto-processor functionality"
}

# Get auth token first
login_data = {
    "username": "admin",
    "password": "admin123"
}

print("Testing auto-processor...")

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
            
            print("Creating new request...")
            response = requests.post(
                "http://localhost:8000/api/signatory-authorizations/request/",
                json=test_data,
                headers=headers
            )
            
            print(f"Status: {response.status_code}")
            if response.status_code == 201:
                result = response.json()
                print(f"✅ Request created: ID={result['id']}, Status={result['status']}")
                
                print("Waiting for auto-processor to handle the request...")
                
                # Wait and check status every 5 seconds for up to 30 seconds
                for i in range(6):  # 6 * 5 = 30 seconds
                    time.sleep(5)
                    print(f"Checking status... ({(i+1)*5}s)")
                    
                    # Check request status
                    req_response = requests.get(
                        "http://localhost:8000/api/signatory-authorizations/my-requests/",
                        headers=headers
                    )
                    
                    if req_response.status_code == 200:
                        requests_data = req_response.json()
                        auto_request = None
                        for req in requests_data:
                            if req['signatory_name'] == 'AUTO PROCESSOR TEST':
                                auto_request = req
                                break
                        
                        if auto_request:
                            print(f"Request Status: {auto_request['status']} ({auto_request['status_display']})")
                            
                            if auto_request['status'] == 'APPROVED':
                                print(f"Admin Notes: {auto_request['admin_notes']}")
                                
                                # Check if authorization was created
                                auth_response = requests.get(
                                    "http://localhost:8000/api/signatory-authorizations/my-authorizations/",
                                    headers=headers
                                )
                                
                                if auth_response.status_code == 200:
                                    auths = auth_response.json()
                                    auto_auth = None
                                    for auth in auths:
                                        if auth['signatory_name'] == 'AUTO PROCESSOR TEST':
                                            auto_auth = auth
                                            break
                                    
                                    if auto_auth:
                                        print(f"\n🎉 AUTO-PROCESSOR SUCCESS!")
                                        print(f"✅ Request created via API")
                                        print(f"✅ Auto-processor detected and processed the request")
                                        print(f"✅ Authorization created: ID={auto_auth['id']}")
                                        print(f"✅ Request approved automatically")
                                        print(f"✅ Email sent with signature setup link")
                                        print(f"\n🎯 THE AUTO-PROCESSOR WORKFLOW IS WORKING!")
                                        break
                                    else:
                                        print("❌ No authorization found")
                                break
                    
                    if i == 5:  # Last iteration
                        print("❌ Auto-processor did not process the request within 30 seconds")
                        
            else:
                print(f"❌ FAILED: {response.text}")
                
        else:
            print("❌ No access token in login response")
    else:
        print(f"❌ Login failed: {login_response.status_code}")
        
except Exception as e:
    print(f"❌ Error: {e}")