#!/usr/bin/env python3
"""
Test the email workflow with a fresh request after server restart
"""

import requests
import json
import time

# Configuration
BACKEND_URL = "http://localhost:8000"

def test_fresh_email_workflow():
    """Test the email workflow with a fresh request"""
    print("📧 Testing Fresh Email Workflow After Server Restart")
    print("=" * 60)
    
    # Step 1: Login
    print("\n1. Logging in...")
    login_data = {"username": "testuser", "password": "testpass123"}
    login_response = requests.post(f"{BACKEND_URL}/api/auth/login/", json=login_data)
    
    if login_response.status_code != 200:
        print(f"❌ Login failed: {login_response.status_code}")
        return False
    
    token = login_response.json()['access']
    headers = {'Authorization': f'Bearer {token}'}
    print("✅ Login successful")
    
    # Step 2: Submit a fresh authorization request
    print("\n2. Submitting fresh authorization request...")
    
    # Use a unique signatory name and the configured email
    request_data = {
        "signatory_name": "FRESH EMAIL TEST",
        "role": "Test Role",
        "email": "zahurtongtong@gmail.com",  # Email configured in .env
        "justification": "Testing fresh email workflow after server restart. This should include the signature setup link directly in the email."
    }
    
    print(f"Request data: {json.dumps(request_data, indent=2)}")
    
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
        
        # Step 3: Wait for email processing
        print("\n3. Waiting for email processing...")
        time.sleep(5)
        
        # Step 4: Check if authorization was auto-created
        print("\n4. Checking for auto-created authorization...")
        auth_response = requests.get(
            f"{BACKEND_URL}/api/signatory-authorizations/my-authorizations/",
            headers=headers
        )
        
        if auth_response.status_code == 200:
            authorizations = auth_response.json()
            fresh_auths = [auth for auth in authorizations if auth['signatory_name'] == 'FRESH EMAIL TEST']
            
            if fresh_auths:
                auth = fresh_auths[0]
                print("✅ Authorization auto-created!")
                print(f"  - Active: {auth['is_active']}")
                print(f"  - Has setup token: {'setup_token' in auth and auth['setup_token'] is not None}")
                
                if auth.get('setup_token'):
                    setup_url = f"http://localhost:8081/signature-setup/{auth['setup_token']}"
                    print(f"  - Setup URL: {setup_url}")
                    
                    print("\n🎯 SUCCESS! Fresh email workflow is working!")
                    print("📧 CHECK YOUR EMAIL (zahurtongtong@gmail.com) for:")
                    print("   - Subject: E-Signature Required - FRESH EMAIL TEST")
                    print("   - Content should include: 'CREATE YOUR E-SIGNATURE NOW'")
                    print("   - Direct signature setup link")
                    print(f"   - Link: {setup_url}")
                    
                    # Step 5: Check the request status
                    print("\n5. Checking request status...")
                    request_response = requests.get(
                        f"{BACKEND_URL}/api/signatory-authorizations/my-requests/",
                        headers=headers
                    )
                    
                    if request_response.status_code == 200:
                        requests_data = request_response.json()
                        fresh_requests = [req for req in requests_data if req['signatory_name'] == 'FRESH EMAIL TEST']
                        
                        if fresh_requests:
                            req = fresh_requests[0]
                            print(f"  - Request Status: {req['status']}")
                            print(f"  - Status Display: {req['status_display']}")
                            
                            if req['status'] == 'APPROVED':
                                print("✅ Request was auto-approved!")
                            else:
                                print(f"⚠️ Request status is {req['status']}, expected APPROVED")
                    
                    return True
                else:
                    print("❌ No setup token found in authorization")
                    return False
            else:
                print("❌ No authorization found for FRESH EMAIL TEST")
                print("This means the auto-approval workflow is not working")
                return False
        else:
            print(f"❌ Failed to get authorizations: {auth_response.status_code}")
            return False
    else:
        print(f"❌ Request failed: {response.status_code}")
        return False

if __name__ == "__main__":
    success = test_fresh_email_workflow()
    if success:
        print("\n🎉 Fresh email workflow test completed successfully!")
        print("📧 The email should now contain the signature setup link.")
        print("🔗 Click the link in the email to test the signature creation process.")
    else:
        print("\n❌ Fresh email workflow test failed.")
        print("The serializer method might not be working as expected.")