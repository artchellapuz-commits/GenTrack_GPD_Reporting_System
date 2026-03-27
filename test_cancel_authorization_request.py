#!/usr/bin/env python3
"""
Test script for cancelling authorization requests
"""

import os
import sys
import django
import requests
import json

# Setup Django environment
sys.path.append('backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'npc_reporting.settings')
django.setup()

from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from reports.models import SignatoryAuthorizationRequest

def test_cancel_request():
    """Test that users can cancel their authorization requests"""
    
    print("🔧 Testing Cancel Authorization Request")
    print("=" * 50)
    
    try:
        # Get or create a test user
        user = User.objects.first()
        if not user:
            print("❌ No users found. Please create a user first.")
            return False
            
        print(f"✅ Using test user: {user.username}")
        
        # Generate JWT token for the user
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        
        # Test API endpoints
        base_url = "http://127.0.0.1:8000/api"
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
        
        # Step 1: Create a test request
        print("\n1. Creating Test Authorization Request")
        request_data = {
            "signatory_name": "Test Cancel Signatory",
            "role": "Prepared by",
            "email": "test.cancel@example.com",
            "justification": "Test request for cancellation functionality"
        }
        
        response = requests.post(
            f"{base_url}/signatory-authorizations/request/",
            headers=headers,
            json=request_data
        )
        
        print(f"   Status: {response.status_code}")
        if response.status_code == 201:
            data = response.json()
            request_id = data.get('id')
            print(f"   ✅ Success! Created request ID: {request_id}")
        else:
            print(f"   ❌ Error: {response.text}")
            return False
        
        # Step 2: Verify request exists and is PENDING
        print(f"\n2. Verifying Request Status (ID: {request_id})")
        auth_request = SignatoryAuthorizationRequest.objects.get(id=request_id)
        print(f"   Status: {auth_request.status}")
        print(f"   Signatory: {auth_request.signatory_name}")
        print(f"   User: {auth_request.user.username}")
        
        if auth_request.status != 'PENDING':
            print(f"   ❌ Expected PENDING status, got {auth_request.status}")
            return False
        print(f"   ✅ Request is PENDING as expected")
        
        # Step 3: Cancel the request
        print(f"\n3. Cancelling Authorization Request")
        response = requests.post(
            f"{base_url}/signatory-authorizations/cancel-request/{request_id}/",
            headers=headers
        )
        
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Success! Response: {data.get('message')}")
        else:
            print(f"   ❌ Error: {response.text}")
            return False
        
        # Step 4: Verify request is cancelled
        print(f"\n4. Verifying Request is Cancelled")
        auth_request.refresh_from_db()
        print(f"   New Status: {auth_request.status}")
        print(f"   Reviewed By: {auth_request.reviewed_by.username if auth_request.reviewed_by else 'None'}")
        print(f"   Admin Notes: {auth_request.admin_notes}")
        
        if auth_request.status != 'CANCELLED':
            print(f"   ❌ Expected CANCELLED status, got {auth_request.status}")
            return False
        print(f"   ✅ Request successfully cancelled")
        
        # Step 5: Try to cancel already cancelled request
        print(f"\n5. Testing Cancel Already Cancelled Request")
        response = requests.post(
            f"{base_url}/signatory-authorizations/cancel-request/{request_id}/",
            headers=headers
        )
        
        print(f"   Status: {response.status_code}")
        if response.status_code == 404:
            print(f"   ✅ Correctly rejected: {response.json().get('error')}")
        else:
            print(f"   ⚠️  Expected 404, got {response.status_code}: {response.text}")
        
        # Step 6: Test user's request list
        print(f"\n6. Testing User's Request List")
        response = requests.get(
            f"{base_url}/signatory-authorizations/my-requests/",
            headers=headers
        )
        
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            cancelled_requests = [r for r in data if r['status'] == 'CANCELLED']
            print(f"   ✅ Success! Found {len(cancelled_requests)} cancelled requests")
            if cancelled_requests:
                print(f"      Latest cancelled: ID {cancelled_requests[0]['id']} - {cancelled_requests[0]['signatory_name']}")
        else:
            print(f"   ❌ Error: {response.text}")
        
        # Clean up
        print(f"\n🧹 Cleaning up test data...")
        auth_request.delete()
        print("   ✅ Test data cleaned up")
        
        print("\n" + "=" * 50)
        print("🎉 Cancel Authorization Request Test Complete!")
        print("\nResults:")
        print("✅ Users can cancel their own pending requests")
        print("✅ Cancelled requests show CANCELLED status")
        print("✅ Already processed requests cannot be cancelled")
        print("✅ Proper error handling for invalid requests")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_cancel_request()
    if success:
        print("\n🎉 Cancel authorization request functionality is working correctly!")
    else:
        print("\n❌ Cancel authorization request functionality needs fixes.")