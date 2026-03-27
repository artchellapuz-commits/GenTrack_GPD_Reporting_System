#!/usr/bin/env python3
"""
Test different URL patterns to see which one works
"""
import requests
import json

# Get auth token first
login_data = {
    "username": "admin",
    "password": "admin123"
}

print("Testing URL routing...")

try:
    # Login to get token
    login_response = requests.post(
        "http://localhost:8000/api/auth/login/",
        json=login_data,
        headers={'Content-Type': 'application/json'}
    )
    
    if login_response.status_code == 200:
        token_data = login_response.json()
        access_token = token_data.get('access')
        
        if access_token:
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {access_token}'
            }
            
            # Test different URL patterns
            urls_to_test = [
                "http://localhost:8000/api/signatory-authorizations/request/",
                "http://localhost:8000/api/signatory-authorizations/request",
                "http://localhost:8000/api/signatory-authorizations/",
            ]
            
            for url in urls_to_test:
                print(f"\nTesting URL: {url}")
                
                # Test with OPTIONS first to see what methods are allowed
                options_response = requests.options(url, headers=headers)
                print(f"OPTIONS Status: {options_response.status_code}")
                if 'Allow' in options_response.headers:
                    print(f"Allowed methods: {options_response.headers['Allow']}")
                
                # Test with GET to see if endpoint exists
                get_response = requests.get(url, headers=headers)
                print(f"GET Status: {get_response.status_code}")
                if get_response.status_code != 404:
                    print(f"GET Response: {get_response.text[:200]}...")
                
        else:
            print("❌ No access token in login response")
    else:
        print(f"❌ Login failed: {login_response.status_code}")
        
except Exception as e:
    print(f"❌ Error: {e}")