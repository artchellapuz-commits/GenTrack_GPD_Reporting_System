#!/usr/bin/env python3
"""
Test if the API workflow is now working automatically
"""

import requests
import json
import time

# Configuration
BACKEND_URL = "http://localhost:8000"

def test_api_workflow():
    """Test the API workflow"""
    print("🔧 Testing API Workflow Fix")
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
    
    # Step 2: Submit a new request to test the API workflow
    print("\n2. Testing API workflow...")
    
    request_data = {
        "signatory_name": "API WORKFLOW TEST",
        "role": "Test Role",
        "email": "zahurtongtong@gmail.com",
        "justification": "Testing if the API workflow now automatically includes signature setup links"
    }
    
    print(f"Submitting request: {request_data['signatory_name']}")
    
    response = requests.post(
        f"{BACKEND_URL}/api/signatory-authorizations/request/",
        json=request_data,
        headers=headers
    )
    
    print(f"Response Status: {response.status_code}")
    
    if response.status_code == 201:
        response_data = response.json()
        request_id = response_data['id']
        print(f"✅ Request created with ID: {request_id}")
        
        # Step 3: Wait for processing
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
            test_auths = [auth for auth in authorizations if auth['signatory_name'] == 'API WORKFLOW TEST']
            
            if test_auths:
                auth = test_auths[0]
                print("✅ Authorization auto-created by API!")
                print(f"  - Active: {auth['is_active']}")
                print(f"  - Has setup token: {'setup_token' in auth and auth['setup_token'] is not None}")
                
                if auth.get('setup_token'):
                    setup_url = f"http://localhost:8081/signature-setup/{auth['setup_token']}"
                    print(f"  - Setup URL: {setup_url}")
                    
                    print("\n🎯 SUCCESS! API workflow is now working automatically!")
                    print("📧 Check email for: E-Signature Required - API WORKFLOW TEST")
                    print("🔗 The email should contain the signature setup link")
                    return True
                else:
                    print("❌ Authorization created but no setup token")
                    return False
            else:
                print("❌ No authorization auto-created")
                print("API workflow still not working - will need manual fix")
                
                # Manually fix this request
                print(f"\n🔧 Manually fixing request ID {request_id}...")
                import subprocess
                result = subprocess.run([
                    'python', 'manage.py', 'fix_email_workflow', '--request-id', str(request_id)
                ], cwd='npc-reporting-system/backend', capture_output=True, text=True)
                
                if result.returncode == 0:
                    print("✅ Manual fix applied successfully")
                    print("📧 Check email for the corrected version")
                else:
                    print(f"❌ Manual fix failed: {result.stderr}")
                
                return False
        else:
            print(f"❌ Failed to get authorizations: {auth_response.status_code}")
            return False
    else:
        print(f"❌ Request failed: {response.status_code}")
        return False

if __name__ == "__main__":
    success = test_api_workflow()
    if success:
        print("\n🎉 API workflow is now working automatically!")
        print("Future requests will include signature setup links automatically.")
    else:
        print("\n⚠️ API workflow still needs manual intervention.")
        print("Use the management command to fix requests as needed.")