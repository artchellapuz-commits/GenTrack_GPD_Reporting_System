#!/usr/bin/env python3
"""
Check recent authorization requests to see their status
"""
import requests
import json

# Get auth token first
login_data = {
    "username": "admin",
    "password": "admin123"
}

print("Checking recent authorization requests...")

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
            
            # Get user's requests
            response = requests.get(
                "http://localhost:8000/api/signatory-authorizations/my-requests/",
                headers=headers
            )
            
            if response.status_code == 200:
                requests_data = response.json()
                print(f"Found {len(requests_data)} requests:")
                
                for req in requests_data[-5:]:  # Show last 5 requests
                    print(f"\nRequest ID: {req['id']}")
                    print(f"Signatory: {req['signatory_name']}")
                    print(f"Status: {req['status']} ({req['status_display']})")
                    print(f"Email: {req['email']}")
                    print(f"Created: {req['created_at']}")
                    if req['reviewed_at']:
                        print(f"Reviewed: {req['reviewed_at']}")
                        print(f"Admin Notes: {req['admin_notes']}")
            
            # Also check authorizations
            auth_response = requests.get(
                "http://localhost:8000/api/signatory-authorizations/my-authorizations/",
                headers=headers
            )
            
            if auth_response.status_code == 200:
                auth_data = auth_response.json()
                print(f"\nFound {len(auth_data)} authorizations:")
                
                for auth in auth_data[-3:]:  # Show last 3 authorizations
                    print(f"\nAuthorization ID: {auth['id']}")
                    print(f"Signatory: {auth['signatory_name']}")
                    print(f"Active: {auth['is_active']}")
                    print(f"Valid: {auth['is_valid']}")
                    print(f"Date: {auth['authorization_date']}")
                    
        else:
            print("❌ No access token in login response")
    else:
        print(f"❌ Login failed: {login_response.status_code}")
        
except Exception as e:
    print(f"❌ Error: {e}")