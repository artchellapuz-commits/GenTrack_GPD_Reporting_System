#!/usr/bin/env python3
"""
Test the new signature setup endpoint that doesn't require authentication
"""
import requests
import json

print("Testing new signature setup endpoint...")

# Get a setup token from the management command
import subprocess
import re

try:
    # Run the management command to get token info
    result = subprocess.run(
        ['python', 'manage.py', 'test_signature_setup'],
        cwd='npc-reporting-system/backend',
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        output = result.stdout
        print("Management command output:")
        print(output)
        
        # Extract the setup token from the output
        token_match = re.search(r'Setup token: ([A-Za-z0-9_-]+)', output)
        if token_match:
            setup_token = token_match.group(1)
            print(f"\nExtracted token: {setup_token}...")
            
            # Test the new endpoint
            new_endpoint_url = f"http://localhost:8000/api/signature-setup/{setup_token}/"
            
            print(f"Testing new endpoint: {new_endpoint_url}")
            
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
            else:
                print(f"Unexpected status: {response.status_code}")
        else:
            print("❌ Could not extract setup token from management command output")
    else:
        print(f"❌ Management command failed: {result.stderr}")
        
except Exception as e:
    print(f"❌ Error: {e}")