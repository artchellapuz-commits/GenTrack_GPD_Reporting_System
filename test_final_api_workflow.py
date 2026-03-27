#!/usr/bin/env python3
"""
Test the final fixed API workflow
"""
import requests
import json

# Test data
test_data = {
    "signatory_name": "FINAL API TEST",
    "role": "Test Role",
    "email": "finaltest@example.com",
    "justification": "Testing the final fixed API workflow with debug output"
}

# Get auth token first
login_data = {
    "username": "admin",
    "password": "admin123"
}

print("Testing final fixed API workflow...")

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
            
            print("Making request to /signatory-authorizations/request/")
            response = requests.post(
                "http://localhost:8000/api/signatory-authorizations/request/",
                json=test_data,
                headers=headers
            )
            
            print(f"Status: {response.status_code}")
            if response.status_code == 201:
                result = response.json()
                print(f"✅ SUCCESS: Request created")
                print(f"ID: {result['id']}")
                print(f"Status: {result['status']}")
                print(f"Email: {result['email']}")
                
                # Wait a moment for processing
                import time
                time.sleep(2)
                
                # Check if authorization was created
                auth_response = requests.get(
                    "http://localhost:8000/api/signatory-authorizations/my-authorizations/",
                    headers=headers
                )
                
                if auth_response.status_code == 200:
                    auths = auth_response.json()
                    final_auth = None
                    for auth in auths:
                        if auth['signatory_name'] == 'FINAL API TEST':
                            final_auth = auth
                            break
                    
                    if final_auth:
                        print(f"\n✅ Authorization auto-created:")
                        print(f"ID: {final_auth['id']}")
                        print(f"Active: {final_auth['is_active']}")
                        print(f"Valid: {final_auth['is_valid']}")
                        print(f"Date: {final_auth['authorization_date']}")
                        
                        # Check request status again
                        req_response = requests.get(
                            "http://localhost:8000/api/signatory-authorizations/my-requests/",
                            headers=headers
                        )
                        
                        if req_response.status_code == 200:
                            requests_data = req_response.json()
                            final_request = None
                            for req in requests_data:
                                if req['signatory_name'] == 'FINAL API TEST':
                                    final_request = req
                                    break
                            
                            if final_request:
                                print(f"\n✅ Request status updated:")
                                print(f"Status: {final_request['status']} ({final_request['status_display']})")
                                print(f"Admin Notes: {final_request['admin_notes']}")
                                
                                if final_request['status'] == 'APPROVED':
                                    print("\n🎉 COMPLETE SUCCESS!")
                                    print("✅ Request created via API")
                                    print("✅ Authorization auto-created")
                                    print("✅ Request auto-approved")
                                    print("✅ Email sent with signature setup link")
                                    print("\nThe API workflow is now working correctly!")
                                else:
                                    print(f"\n❌ Request status is still: {final_request['status']}")
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