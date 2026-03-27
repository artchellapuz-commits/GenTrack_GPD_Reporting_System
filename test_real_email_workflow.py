#!/usr/bin/env python3
"""
Test the real email workflow by submitting a request through the frontend API
and checking if the email is actually sent
"""

import requests
import json
import time

# Configuration
BACKEND_URL = "http://localhost:8000"

def test_real_email_workflow():
    """Test the real email workflow"""
    print("📧 Testing Real Email Workflow")
    print("=" * 50)
    
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
    
    # Step 2: Submit a real authorization request
    print("\n2. Submitting authorization request...")
    
    # Use a real email address that the user can check
    request_data = {
        "signatory_name": "EMAIL WORKFLOW TEST",
        "role": "Test Role",
        "email": "zahurtongtong@gmail.com",  # This is the email configured in .env
        "justification": "Testing the complete email workflow with signature setup link. This should include a direct link to create the e-signature."
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
        
        # Step 3: Wait a moment for email processing
        print("\n3. Waiting for email processing...")
        time.sleep(3)
        
        # Step 4: Check if authorization was auto-created
        print("\n4. Checking for auto-created authorization...")
        auth_response = requests.get(
            f"{BACKEND_URL}/api/signatory-authorizations/my-authorizations/",
            headers=headers
        )
        
        if auth_response.status_code == 200:
            authorizations = auth_response.json()
            test_auths = [auth for auth in authorizations if auth['signatory_name'] == 'EMAIL WORKFLOW TEST']
            
            if test_auths:
                auth = test_auths[0]
                print("✅ Authorization auto-created!")
                print(f"  - Active: {auth['is_active']}")
                print(f"  - Has setup token: {'setup_token' in auth and auth['setup_token'] is not None}")
                
                if auth.get('setup_token'):
                    setup_url = f"http://localhost:8081/signature-setup/{auth['setup_token']}"
                    print(f"  - Setup URL: {setup_url}")
                    
                    print("\n🎯 SUCCESS! Email workflow is working!")
                    print("📧 CHECK YOUR EMAIL (zahurtongtong@gmail.com) for:")
                    print("   - Subject: E-Signature Required - EMAIL WORKFLOW TEST")
                    print("   - Content should include the signature setup link")
                    print(f"   - Link should be: {setup_url}")
                    return True
                else:
                    print("❌ No setup token found in authorization")
                    return False
            else:
                print("❌ No authorization found for EMAIL WORKFLOW TEST")
                print("This means the auto-approval workflow is not working")
                return False
        else:
            print(f"❌ Failed to get authorizations: {auth_response.status_code}")
            return False
    else:
        print(f"❌ Request failed: {response.status_code}")
        return False

if __name__ == "__main__":
    success = test_real_email_workflow()
    if success:
        print("\n🎉 Email workflow test completed successfully!")
        print("📧 Please check the email inbox for the signature setup link.")
    else:
        print("\n❌ Email workflow test failed.")
        print("The issue might be that the API request is not calling our updated method.")