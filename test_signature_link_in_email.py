#!/usr/bin/env python3
"""
Test script to verify that signature setup links are included in confirmation emails
"""

import requests
import json
import time

# Configuration
BACKEND_URL = "http://localhost:8000"
FRONTEND_URL = "http://localhost:8081"

def test_signature_link_workflow():
    """Test the complete signature link workflow"""
    print("🧪 Testing Signature Link in Email Workflow")
    print("=" * 50)
    
    # Step 1: Login as a test user
    print("\n1. Logging in as test user...")
    login_data = {
        "username": "testuser",
        "password": "testpass123"
    }
    
    try:
        login_response = requests.post(f"{BACKEND_URL}/api/auth/login/", json=login_data)
        if login_response.status_code == 200:
            token = login_response.json()['access']
            headers = {'Authorization': f'Bearer {token}'}
            print("✅ Login successful")
        else:
            print(f"❌ Login failed: {login_response.status_code}")
            print(f"Response: {login_response.text}")
            return
    except Exception as e:
        print(f"❌ Login error: {e}")
        return
    
    # Step 2: Submit an e-signature authorization request
    print("\n2. Submitting e-signature authorization request...")
    request_data = {
        "signatory_name": "TEST SIGNATORY",
        "role": "Test Role",
        "email": "test@example.com",
        "justification": "Testing the new signature link workflow - this should include a direct link to signature setup"
    }
    
    try:
        request_response = requests.post(
            f"{BACKEND_URL}/api/signatory-authorizations/request/",
            json=request_data,
            headers=headers
        )
        
        if request_response.status_code == 201:
            print("✅ Authorization request submitted successfully")
            request_id = request_response.json()['id']
            print(f"Request ID: {request_id}")
        else:
            print(f"❌ Request failed: {request_response.status_code}")
            print(f"Response: {request_response.text}")
            return
    except Exception as e:
        print(f"❌ Request error: {e}")
        return
    
    # Step 3: Check if authorization was auto-created
    print("\n3. Checking if authorization was auto-created...")
    try:
        auth_response = requests.get(
            f"{BACKEND_URL}/api/signatory-authorizations/my-authorizations/",
            headers=headers
        )
        
        if auth_response.status_code == 200:
            authorizations = auth_response.json()
            if authorizations:
                latest_auth = authorizations[0]
                print("✅ Authorization auto-created successfully")
                print(f"Signatory: {latest_auth['signatory_name']}")
                print(f"Active: {latest_auth['is_active']}")
                print(f"Setup Token Present: {'setup_token' in latest_auth and latest_auth['setup_token'] is not None}")
                
                if latest_auth.get('setup_token'):
                    setup_token = latest_auth['setup_token']
                    setup_url = f"{FRONTEND_URL}/signature-setup/{setup_token}"
                    print(f"🔗 Signature Setup URL: {setup_url}")
                    
                    # Step 4: Test the signature setup endpoint
                    print("\n4. Testing signature setup endpoint...")
                    try:
                        setup_response = requests.get(f"{BACKEND_URL}/api/signatory-authorizations/signature-setup/{setup_token}/")
                        if setup_response.status_code == 200:
                            setup_data = setup_response.json()
                            print("✅ Signature setup endpoint working")
                            print(f"Signatory Name: {setup_data['signatory_name']}")
                            print(f"User Name: {setup_data['user_name']}")
                            print(f"Requires 2FA: {setup_data['requires_2fa']}")
                        else:
                            print(f"❌ Setup endpoint failed: {setup_response.status_code}")
                            print(f"Response: {setup_response.text}")
                    except Exception as e:
                        print(f"❌ Setup endpoint error: {e}")
                else:
                    print("❌ No setup token found in authorization")
            else:
                print("❌ No authorizations found")
        else:
            print(f"❌ Failed to get authorizations: {auth_response.status_code}")
    except Exception as e:
        print(f"❌ Authorization check error: {e}")
    
    print("\n" + "=" * 50)
    print("🎯 EXPECTED BEHAVIOR:")
    print("1. User submits e-signature request")
    print("2. System auto-approves and creates authorization")
    print("3. Confirmation email contains signature setup link")
    print("4. Link format: http://localhost:8081/signature-setup/{token}")
    print("5. User clicks link and can draw signature immediately")
    print("\n📧 CHECK YOUR EMAIL for the confirmation message with the signature setup link!")

if __name__ == "__main__":
    test_signature_link_workflow()