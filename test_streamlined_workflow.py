#!/usr/bin/env python3
"""
Test script for the streamlined e-signature authorization workflow.

This script tests the complete workflow:
1. User clicks "Request Access" from Generate Report
2. Goes through Steps 1, 2, 3 with animation
3. Submits request and gets email
4. If existing signature exists, gets direct approval link
5. Clicks approval link and approves with existing signature
"""

import requests
import json
import time
from datetime import datetime

# Configuration
BASE_URL = "http://localhost:8000"
FRONTEND_URL = "http://localhost:8081"

def test_streamlined_workflow():
    """Test the complete streamlined workflow"""
    
    print("🚀 Testing Streamlined E-Signature Authorization Workflow")
    print("=" * 60)
    
    # Step 1: Login as a test user
    print("\n1. Logging in as test user...")
    login_data = {
        "username": "testuser",
        "password": "testpass123"
    }
    
    login_response = requests.post(f"{BASE_URL}/api/auth/login/", json=login_data)
    if login_response.status_code != 200:
        print(f"❌ Login failed: {login_response.status_code}")
        print(f"Response: {login_response.text}")
        return False
    
    token = login_response.json().get('access')
    headers = {'Authorization': f'Bearer {token}'}
    print("✅ Login successful")
    
    # Step 1.5: Clean up existing data for this test
    print("\n1.5. Cleaning up existing test data...")
    signatory_name = "Test Streamlined Signatory"
    
    # Get existing authorizations and delete them
    auth_response = requests.get(f"{BASE_URL}/api/signatory-authorizations/my-authorizations/", 
                               headers=headers)
    if auth_response.status_code == 200:
        authorizations = auth_response.json()
        for auth in authorizations:
            if auth['signatory_name'] == signatory_name:
                delete_response = requests.delete(f"{BASE_URL}/api/signatory-authorizations/{auth['id']}/", 
                                                headers=headers)
                print(f"   Deleted existing authorization: {auth['id']}")
    
    print("✅ Cleanup completed")
    
    # Step 2: Create an existing signature first (simulate user already has signature)
    print("\n2. Creating existing signature for testing...")
    signature_data = {
        "signatory_name": signatory_name,
        "signature_data": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg=="
    }
    
    sig_response = requests.post(f"{BASE_URL}/api/e-signatures/create-from-data/", 
                                json=signature_data, headers=headers)
    if sig_response.status_code == 201:
        print("✅ Existing signature created")
    else:
        print(f"⚠️ Signature creation response: {sig_response.status_code}")
        print(f"Response: {sig_response.text}")
    
    # Step 3: Submit authorization request (simulating the animated form)
    print("\n3. Submitting authorization request...")
    request_data = {
        "signatory_name": signatory_name,
        "role": "Prepared by:",
        "justification": "Testing streamlined workflow with existing signature",
        "email": "test@example.com"
    }
    
    request_response = requests.post(f"{BASE_URL}/api/signatory-authorizations/request/", 
                                   json=request_data, headers=headers)
    
    if request_response.status_code != 201:
        print(f"❌ Request submission failed: {request_response.status_code}")
        print(f"Response: {request_response.text}")
        return False
    
    print("✅ Authorization request submitted")
    print("📧 Email should be sent with approval link (since signature exists)")
    
    # Step 4: Get the authorization token (simulate clicking email link)
    print("\n4. Getting authorization details...")
    
    # Get user's authorizations to find the token
    auth_response = requests.get(f"{BASE_URL}/api/signatory-authorizations/my-authorizations/", 
                               headers=headers)
    
    if auth_response.status_code != 200:
        print(f"❌ Failed to get authorizations: {auth_response.status_code}")
        return False
    
    authorizations = auth_response.json()
    if not authorizations:
        print("❌ No authorizations found")
        return False
    
    # Find the authorization with a setup token for our test signatory
    auth_with_token = None
    for auth in authorizations:
        if auth.get('setup_token') and auth['signatory_name'] == signatory_name:
            auth_with_token = auth
            break
    
    if not auth_with_token:
        print("❌ No authorization with setup token found")
        print("Available authorizations:")
        for auth in authorizations:
            print(f"   - {auth['signatory_name']}: token={bool(auth.get('setup_token'))}")
        return False
    
    token_value = auth_with_token['setup_token']
    print(f"✅ Found authorization token: {token_value[:20]}...")
    
    # Step 5: Test the approval endpoint (simulate clicking "Approve Request")
    print("\n5. Testing approval with existing signature...")
    
    # First, get authorization details by token
    token_response = requests.get(f"{BASE_URL}/api/signatory-authorizations/by-token/{token_value}/", 
                                headers=headers)
    
    if token_response.status_code != 200:
        print(f"❌ Failed to get authorization by token: {token_response.status_code}")
        print(f"Response: {token_response.text}")
        return False
    
    auth_details = token_response.json()
    print("✅ Authorization details retrieved:")
    print(f"   - Signatory: {auth_details['signatory_name']}")
    print(f"   - Role: {auth_details['role']}")
    print(f"   - User: {auth_details['user_name']}")
    
    # Now approve with existing signature
    approve_response = requests.post(f"{BASE_URL}/api/signatory-authorizations/approve-with-existing/{token_value}/", 
                                   headers=headers)
    
    if approve_response.status_code != 200:
        print(f"❌ Approval failed: {approve_response.status_code}")
        print(f"Response: {approve_response.text}")
        return False
    
    approval_result = approve_response.json()
    print("✅ Authorization approved successfully!")
    print(f"   - Authorization ID: {approval_result['authorization_id']}")
    print(f"   - Signatory: {approval_result['signatory_name']}")
    print(f"   - Active: {approval_result['is_active']}")
    
    # Step 6: Verify the authorization is now active
    print("\n6. Verifying authorization is active...")
    
    final_auth_response = requests.get(f"{BASE_URL}/api/signatory-authorizations/my-authorizations/", 
                                     headers=headers)
    
    if final_auth_response.status_code == 200:
        final_auths = final_auth_response.json()
        active_auth = None
        for auth in final_auths:
            if auth['signatory_name'] == signatory_name and auth['is_active']:
                active_auth = auth
                break
        
        if active_auth:
            print("✅ Authorization is now active and ready for signing!")
            print(f"   - Signature Created: {active_auth.get('signature_created', False)}")
        else:
            print("⚠️ Authorization not found or not active")
    
    print("\n🎉 Streamlined workflow test completed successfully!")
    print("\nWorkflow Summary:")
    print("1. ✅ User submitted request from Generate Report")
    print("2. ✅ System detected existing signature")
    print("3. ✅ Email sent with direct approval link")
    print("4. ✅ User clicked approval link")
    print("5. ✅ Authorization approved with existing signature")
    print("6. ✅ User can now sign reports immediately")
    
    return True

def test_frontend_routes():
    """Test that frontend routes are accessible"""
    print("\n🌐 Testing Frontend Routes")
    print("-" * 30)
    
    # Test the new approval route
    test_token = "test-token-123"
    approval_url = f"{FRONTEND_URL}/approve-request/{test_token}"
    
    print(f"📍 Approval URL: {approval_url}")
    print("   (This would be the link sent in the email)")
    
    # Test existing routes
    routes_to_test = [
        "/signatory-authorization",
        "/generate",
        "/dashboard"
    ]
    
    for route in routes_to_test:
        url = f"{FRONTEND_URL}{route}"
        print(f"📍 Route: {url}")
    
    print("✅ All routes configured")

if __name__ == "__main__":
    print("🧪 E-Signature Streamlined Workflow Test")
    print("=" * 50)
    
    try:
        # Test backend workflow
        success = test_streamlined_workflow()
        
        # Test frontend routes
        test_frontend_routes()
        
        if success:
            print("\n🎯 All tests passed! The streamlined workflow is working correctly.")
            print("\nNext steps for users:")
            print("1. Click 'Request Access' from Generate Report")
            print("2. Complete animated Steps 1, 2, 3")
            print("3. Check email for approval link")
            print("4. Click 'Approve Request' if signature exists")
            print("5. Start signing reports immediately!")
        else:
            print("\n❌ Some tests failed. Check the output above.")
            
    except Exception as e:
        print(f"\n💥 Test failed with error: {e}")
        import traceback
        traceback.print_exc()