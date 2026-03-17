#!/usr/bin/env python3
"""
Test script for e-signatures endpoint
"""

import os
import sys
import django
import requests

# Setup Django environment
sys.path.append('backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'npc_reporting.settings')
django.setup()

from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken

def test_esignatures_endpoint():
    """Test the e-signatures endpoint"""
    
    print("🔧 Testing E-Signatures Endpoint")
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
        
        # Test the e-signatures endpoint
        base_url = "http://127.0.0.1:8000/api"
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
        
        print(f"\n📤 Testing GET /api/e-signatures/")
        
        response = requests.get(f"{base_url}/e-signatures/", headers=headers)
        
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Success! Found {len(data.get('results', data))} e-signatures")
            return True
        else:
            print(f"   ❌ Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

if __name__ == "__main__":
    success = test_esignatures_endpoint()
    if success:
        print("\n🎉 E-Signatures endpoint is working correctly!")
    else:
        print("\n❌ E-Signatures endpoint has issues that need to be fixed.")