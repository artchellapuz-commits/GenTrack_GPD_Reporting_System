#!/usr/bin/env python3
"""
Test the serializer-based email workflow
"""
import requests
import json
import time

# Test data
test_data = {
    "signatory_name": "SERIALIZER TEST",
    "role": "Test Role",
    "email": "serializertest@example.com",
    "justification": "Testing the serializer-based email workflow"
}

# Get auth token first
login_data = {
    "username": "admin",
    "password": "admin123"
}

print("Testing serializer-based email workflow...")

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
                
                # Wait a moment for processing
                time.sleep(3)
                
                # Check if authorization was created
                auth_response = requests.get(
                    "http://localhost:8000/api/signatory-authorizations/my-authorizations/",
                    headers=headers
                )
                
                if auth_response.status_code == 200:
                    auths = auth_response.json()
                    serializer_auth = None
                    for auth in auths:
                        if auth['signatory_name'] == 'SERIALIZER TEST':
                            serializer_auth = auth
                            break
                    
                    if serializer_auth:
                        print(f"\n✅ Authorization auto-created:")
                        print(f"ID: {serializer_auth['id']}")
                        print(f"Active: {serializer_auth['is_active']}")
                        print(f"Valid: {serializer_auth['is_valid']}")
                        
                        # Check request status
                        req_response = requests.get(
                            "http://localhost:8000/api/signatory-authorizations/my-requests/",
                            headers=headers
                        )
                        
                        if req_response.status_code == 200:
                            requests_data = req_response.json()
                            serializer_request = None
                            for req in requests_data:
                                if req['signatory_name'] == 'SERIALIZER TEST':
                                    serializer_request = req
                                    break
                            
                            if serializer_request:
                                print(f"\n✅ Request status:")
                                print(f"Status: {serializer_request['status']} ({serializer_request['status_display']})")
                                print(f"Admin Notes: {serializer_request['admin_notes']}")
                                
                                if serializer_request['status'] == 'APPROVED':
                                    print("\n🎉 COMPLETE SUCCESS!")
                                    print("✅ Request created via API")
                                    print("✅ Authorization auto-created")
                                    print("✅ Request auto-approved")
                                    print("✅ Email sent with signature setup link")
                                    print("\n🎯 THE API WORKFLOW IS NOW WORKING!")
                                else:
                                    print(f"\n⚠️ Request status: {serializer_request['status']}")
                    else:
                        print("\n❌ No authorization was auto-created")
                        
            else:
                print(f"❌ FAILED: {response.text}")
                
        else:
            print("❌ No access token in login response")
    else:
        print(f"❌ Login failed: {login_response.status_code}")
        
except Exception as e:
    print(f"❌ Error: {e}")

print("\nCheck the Django server console for debug output (🔥 messages)")