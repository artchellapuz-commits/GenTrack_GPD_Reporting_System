#!/usr/bin/env python3
"""
Debug script to check if the signature API is returning the correct data
"""

import requests
import json

def debug_signature_api():
    """Debug the signature API response"""
    print("🔍 Debugging Signature API Response")
    print("=" * 50)
    
    try:
        # Test the authorization API endpoint
        url = "http://localhost:8000/api/signatory-authorizations/"
        
        print(f"📡 Making request to: {url}")
        
        # You'll need to add authentication headers if required
        headers = {
            'Content-Type': 'application/json',
            # Add authentication headers here if needed
        }
        
        response = requests.get(url, headers=headers)
        
        print(f"📊 Response Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"📋 Response Data:")
            print(json.dumps(data, indent=2))
            
            # Check if any authorization has signature data
            if isinstance(data, list) and len(data) > 0:
                for i, auth in enumerate(data):
                    print(f"\n🔍 Authorization {i+1}:")
                    print(f"   Signatory Name: {auth.get('signatory_name', 'N/A')}")
                    print(f"   Signature Created: {auth.get('signature_created', 'N/A')}")
                    print(f"   Has Signature: {auth.get('has_signature', 'N/A')}")
                    print(f"   Signature URL: {auth.get('signature_url', 'N/A')}")
            else:
                print("❌ No authorization data found")
        else:
            print(f"❌ API Error: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    debug_signature_api()