#!/usr/bin/env python3
"""
Test script for request_signatures endpoint
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
from reports.models import Document

def test_request_signatures():
    """Test the request_signatures endpoint"""
    
    print("🔧 Testing Request Signatures Endpoint")
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
        
        # Create a test document
        document = Document.objects.create(
            title="Test Document for Signatures",
            document_type="PSR",
            content="This is a test document for signature requests",
            created_by=user,
            status="DRAFT"
        )
        print(f"✅ Created test document ID: {document.id}")
        
        # Test the request_signatures endpoint
        base_url = "http://127.0.0.1:8000/api"
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
        
        signature_data = {
            "signers": [
                {
                    "name": "John Doe",
                    "email": "john.doe@example.com",
                    "role": "Prepared by"
                },
                {
                    "name": "Jane Smith", 
                    "email": "jane.smith@example.com",
                    "role": "Approved by"
                }
            ],
            "expires_in_hours": 72
        }
        
        print(f"\n📤 Testing POST /api/documents/{document.id}/request_signatures/")
        print(f"   Payload: {json.dumps(signature_data, indent=2)}")
        
        response = requests.post(
            f"{base_url}/documents/{document.id}/request_signatures/",
            headers=headers,
            json=signature_data
        )
        
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 201:
            data = response.json()
            print(f"   ✅ Success! Created {len(data)} signature requests")
            for i, request in enumerate(data, 1):
                print(f"      {i}. {request['signer_name']} ({request['signer_email']})")
                print(f"         Token: {request['token'][:20]}...")
                print(f"         Status: {request['status']}")
        else:
            print(f"   ❌ Error: {response.text}")
            
        # Clean up
        document.delete()
        print(f"\n🧹 Cleaned up test document")
        
        return response.status_code == 201
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

if __name__ == "__main__":
    success = test_request_signatures()
    if success:
        print("\n🎉 Request Signatures endpoint is working correctly!")
        print("The frontend error might be due to:")
        print("1. Authentication token not being sent properly")
        print("2. Frontend making request before user is logged in")
        print("3. API base URL configuration issue")
    else:
        print("\n❌ Request Signatures endpoint has issues that need to be fixed.")