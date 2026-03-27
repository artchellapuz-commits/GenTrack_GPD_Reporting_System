#!/usr/bin/env python3
"""
Test script for Document Manager API endpoints
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
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.tokens import RefreshToken

def test_document_api():
    """Test the Document Manager API endpoints"""
    
    print("🔧 Testing Document Manager API")
    print("=" * 50)
    
    # Get or create a test user
    try:
        user = User.objects.first()
        if not user:
            print("❌ No users found. Please create a user first.")
            return False
            
        print(f"✅ Using test user: {user.username}")
        
        # Generate JWT token for the user
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        
        print(f"✅ Generated access token")
        
        # Test API endpoints
        base_url = "http://127.0.0.1:8000/api"
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
        
        # Test 1: Get documents list
        print("\n1. Testing GET /api/documents/")
        try:
            response = requests.get(f"{base_url}/documents/", headers=headers)
            print(f"   Status: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print(f"   ✅ Success! Found {len(data.get('results', data))} documents")
            else:
                print(f"   ⚠️  Response: {response.text}")
        except Exception as e:
            print(f"   ❌ Error: {e}")
        
        # Test 2: Create a test document
        print("\n2. Testing POST /api/documents/")
        try:
            document_data = {
                "title": "Test Document for API",
                "document_type": "PSR",
                "content": "This is a test document created via API",
                "status": "DRAFT"
                # Note: created_by is set automatically by the view
            }
            response = requests.post(f"{base_url}/documents/", 
                                   headers=headers, 
                                   json=document_data)
            print(f"   Status: {response.status_code}")
            if response.status_code == 201:
                data = response.json()
                print(f"   ✅ Success! Created document ID: {data.get('id')}")
                document_id = data.get('id')
                
                # Test 3: Get specific document
                print(f"\n3. Testing GET /api/documents/{document_id}/")
                response = requests.get(f"{base_url}/documents/{document_id}/", headers=headers)
                print(f"   Status: {response.status_code}")
                if response.status_code == 200:
                    print(f"   ✅ Success! Retrieved document: {response.json().get('title')}")
                else:
                    print(f"   ⚠️  Response: {response.text}")
                    
            else:
                print(f"   ⚠️  Response: {response.text}")
        except Exception as e:
            print(f"   ❌ Error: {e}")
        
        # Test 4: Test signature requests endpoint
        print("\n4. Testing GET /api/signature-requests/")
        try:
            response = requests.get(f"{base_url}/signature-requests/", headers=headers)
            print(f"   Status: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print(f"   ✅ Success! Found {len(data.get('results', data))} signature requests")
            else:
                print(f"   ⚠️  Response: {response.text}")
        except Exception as e:
            print(f"   ❌ Error: {e}")
            
        print("\n" + "=" * 50)
        print("🎉 Document Manager API Test Complete!")
        print("\nIf all tests passed, the API is working correctly.")
        print("The frontend error might be due to:")
        print("1. User not being logged in")
        print("2. Frontend trying to access API before authentication")
        print("3. CORS issues (check browser console)")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

if __name__ == "__main__":
    test_document_api()