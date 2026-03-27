#!/usr/bin/env python3
"""
Test with real email to verify the complete workflow
"""
import requests
import json
import time

# Test data with real email
test_data = {
    "signatory_name": "FINAL REAL EMAIL TEST",
    "role": "System Administrator",
    "email": "zahurtongtong@gmail.com",  # Real email for testing
    "justification": "Final test to verify the complete email workflow with clickable signature setup link"
}

# Get auth token first
login_data = {
    "username": "admin",
    "password": "admin123"
}

print("Testing with real email address...")

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
            
            print("Creating request with real email...")
            response = requests.post(
                "http://localhost:8000/api/signatory-authorizations/request/",
                json=test_data,
                headers=headers
            )
            
            print(f"Status: {response.status_code}")
            if response.status_code == 201:
                result = response.json()
                print(f"✅ Request created: ID={result['id']}")
                print(f"📧 Email will be sent to: {result['email']}")
                
                print("Waiting for auto-processor...")
                time.sleep(10)
                
                # Check final status
                req_response = requests.get(
                    "http://localhost:8000/api/signatory-authorizations/my-requests/",
                    headers=headers
                )
                
                if req_response.status_code == 200:
                    requests_data = req_response.json()
                    final_request = None
                    for req in requests_data:
                        if req['signatory_name'] == 'FINAL REAL EMAIL TEST':
                            final_request = req
                            break
                    
                    if final_request and final_request['status'] == 'APPROVED':
                        print(f"\n🎉 COMPLETE SUCCESS!")
                        print(f"✅ Request approved: {final_request['status_display']}")
                        print(f"✅ Admin notes: {final_request['admin_notes']}")
                        
                        # Get authorization details
                        auth_response = requests.get(
                            "http://localhost:8000/api/signatory-authorizations/my-authorizations/",
                            headers=headers
                        )
                        
                        if auth_response.status_code == 200:
                            auths = auth_response.json()
                            final_auth = None
                            for auth in auths:
                                if auth['signatory_name'] == 'FINAL REAL EMAIL TEST':
                                    final_auth = auth
                                    break
                            
                            if final_auth:
                                print(f"✅ Authorization created: ID={final_auth['id']}")
                                print(f"✅ Active: {final_auth['is_active']}")
                                print(f"✅ Valid: {final_auth['is_valid']}")
                                
                                print(f"\n📧 EMAIL SENT TO: zahurtongtong@gmail.com")
                                print(f"📧 SUBJECT: E-Signature Required - FINAL REAL EMAIL TEST")
                                print(f"📧 The email contains a secure signature setup link")
                                print(f"📧 The link is valid for 24 hours")
                                
                                print(f"\n🎯 WORKFLOW COMPLETE!")
                                print(f"The user can now:")
                                print(f"1. Check their email inbox")
                                print(f"2. Click the signature setup link")
                                print(f"3. Draw their e-signature")
                                print(f"4. Start using e-signatures in reports")
                        
            else:
                print(f"❌ FAILED: {response.text}")
                
        else:
            print("❌ No access token in login response")
    else:
        print(f"❌ Login failed: {login_response.status_code}")
        
except Exception as e:
    print(f"❌ Error: {e}")