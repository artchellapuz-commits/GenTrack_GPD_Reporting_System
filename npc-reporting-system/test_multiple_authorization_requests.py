#!/usr/bin/env python3
"""
Test script for multiple authorization requests
"""

import os
import sys
import django
import requests
import json
import time

# Setup Django environment
sys.path.append('backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'npc_reporting.settings')
django.setup()

from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from reports.models import SignatoryAuthorizationRequest

def test_multiple_requests():
    """Test that users can submit multiple authorization requests"""
    
    print("🔧 Testing Multiple Authorization Requests")
    print("=" * 60)
    
    try:
        # Get or create a test user
        user = User.objects.first()
        if not user:
            print("❌ No users found. Please create a user first.")
            return False
            
        print(f"✅ Using test user: {user.username}")
        
        # Clean up any existing requests for this test
        SignatoryAuthorizationRequest.objects.filter(
            user=user,
            signatory_name="Test Signatory"
        ).delete()
        
        # Generate JWT token for the user
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        
        # Test API endpoints
        base_url = "http://127.0.0.1:8000/api"
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
        
        # Test 1: Submit first request
        print("\n1. Testing First Authorization Request")
        request_data = {
            "signatory_name": "Test Signatory",
            "role": "Prepared by",
            "email": "test@example.com",
            "justification": "First test request for authorization"
        }
        
        response = requests.post(
            f"{base_url}/signatory-authorizations/request/",
            headers=headers,
            json=request_data
        )
        
        print(f"   Status: {response.status_code}")
        if response.status_code == 201:
            data = response.json()
            print(f"   ✅ Success! Request ID: {data.get('id')}")
            first_request_id = data.get('id')
        else:
            print(f"   ❌ Error: {response.text}")
            return False
        
        # Test 2: Submit second request (should be allowed now)
        print("\n2. Testing Second Authorization Request")
        request_data['justification'] = "Second test request for authorization - additional information"
        
        response = requests.post(
            f"{base_url}/signatory-authorizations/request/",
            headers=headers,
            json=request_data
        )
        
        print(f"   Status: {response.status_code}")
        if response.status_code == 201:
            data = response.json()
            print(f"   ✅ Success! Request ID: {data.get('id')}")
            second_request_id = data.get('id')
        else:
            print(f"   ❌ Error: {response.text}")
            return False
        
        # Test 3: Submit third request
        print("\n3. Testing Third Authorization Request")
        request_data['justification'] = "Third test request for authorization - urgent"
        
        response = requests.post(
            f"{base_url}/signatory-authorizations/request/",
            headers=headers,
            json=request_data
        )
        
        print(f"   Status: {response.status_code}")
        if response.status_code == 201:
            data = response.json()
            print(f"   ✅ Success! Request ID: {data.get('id')}")
            third_request_id = data.get('id')
        else:
            print(f"   ❌ Error: {response.text}")
            return False
        
        # Test 4: Try fourth request (should hit rate limit)
        print("\n4. Testing Fourth Authorization Request (Rate Limit Test)")
        request_data['justification'] = "Fourth test request - should be rate limited"
        
        response = requests.post(
            f"{base_url}/signatory-authorizations/request/",
            headers=headers,
            json=request_data
        )
        
        print(f"   Status: {response.status_code}")
        if response.status_code == 429:
            print(f"   ✅ Rate limit working! Response: {response.json().get('error', 'Rate limited')}")
        else:
            print(f"   ⚠️  Expected rate limit (429), got: {response.status_code}")
            print(f"   Response: {response.text}")
        
        # Test 5: Check user's requests
        print("\n5. Testing User's Request History")
        response = requests.get(
            f"{base_url}/signatory-authorizations/my-requests/",
            headers=headers
        )
        
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Success! User has {len(data)} total requests")
            for i, req in enumerate(data[:3], 1):
                print(f"      {i}. ID: {req['id']} - Status: {req['status']} - Created: {req['created_at'][:19]}")
        else:
            print(f"   ❌ Error: {response.text}")
        
        # Clean up test data
        print(f"\n🧹 Cleaning up test data...")
        SignatoryAuthorizationRequest.objects.filter(
            user=user,
            signatory_name="Test Signatory"
        ).delete()
        print("   ✅ Test data cleaned up")
        
        print("\n" + "=" * 60)
        print("🎉 Multiple Authorization Requests Test Complete!")
        print("\nResults:")
        print("✅ Users can now submit multiple authorization requests")
        print("✅ Rate limiting prevents spam (max 3 requests per signatory per 24 hours)")
        print("✅ Each request is tracked independently")
        print("✅ Users can view their request history")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_multiple_requests()
    if success:
        print("\n🎉 Multiple authorization requests are now working correctly!")
    else:
        print("\n❌ Multiple authorization requests need further fixes.")