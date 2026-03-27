#!/usr/bin/env python3
"""
Test the new signature setup endpoint directly
"""
import requests

# Use the token from the management command output
setup_token = "Ulkn_97tF_B0E3NrFURySHBLhM4zOiVQ19hRqcDV0Go"

print("Testing new signature setup endpoint...")
print(f"Token: {setup_token[:20]}...")

# Test the new endpoint
new_endpoint_url = f"http://localhost:8000/api/signature-setup/{setup_token}/"

print(f"Testing: {new_endpoint_url}")

try:
    response = requests.get(new_endpoint_url)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")
    
    if response.status_code == 200:
        print("\n🎉 SUCCESS! New signature setup endpoint works without authentication!")
        
        setup_data = response.json()
        print(f"Signatory: {setup_data.get('signatory_name')}")
        print(f"User: {setup_data.get('user_name')}")
        print(f"2FA Required: {setup_data.get('requires_2fa')}")
        
        # Test the frontend URL
        frontend_url = f"http://localhost:8081/signature-setup/{setup_token}"
        print(f"\n🔗 Frontend URL to test: {frontend_url}")
        print("Copy this URL and paste it in your browser to test the signature setup page.")
        
    elif response.status_code == 401:
        print("❌ Still requires authentication")
    elif response.status_code == 404:
        print("❌ Endpoint not found - URL pattern may not be loaded")
    elif response.status_code == 500:
        print("❌ Internal server error")
        print("Response details:", response.text)
    else:
        print(f"Unexpected status: {response.status_code}")
        
except Exception as e:
    print(f"❌ Error: {e}")