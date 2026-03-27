#!/usr/bin/env python3
"""
Test if the method is being called at all
"""
import requests
import json
import time

# Test data
test_data = {
    "signatory_name": "METHOD CALL TEST",
    "role": "Test Role",
    "email": "methodtest@example.com",
    "justification": "Testing if the method is being called at all"
}

# Get auth token first
login_data = {
    "username": "admin",
    "password": "admin123"
}

print("Testing if method is called...")

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
            
            print("Making request...")
            response = requests.post(
                "http://localhost:8000/api/signatory-authorizations/request/",
                json=test_data,
                headers=headers
            )
            
            print(f"Status: {response.status_code}")
            if response.status_code == 201:
                result = response.json()
                print(f"✅ Request created: ID={result['id']}, Status={result['status']}")
            else:
                print(f"❌ FAILED: {response.text}")
            
            # Wait a moment then check files
            time.sleep(1)
            
            # Check method_called.txt
            try:
                with open('npc-reporting-system/backend/method_called.txt', 'r', encoding='utf-8') as f:
                    method_content = f.read()
                    if method_content:
                        print(f"\n✅ METHOD WAS CALLED!")
                        print(f"Content: {method_content}")
                    else:
                        print("\n❌ method_called.txt is empty")
            except FileNotFoundError:
                print("\n❌ method_called.txt not found - METHOD WAS NOT CALLED")
            
            # Check debug_log.txt
            try:
                with open('npc-reporting-system/backend/debug_log.txt', 'r', encoding='utf-8') as f:
                    log_content = f.read()
                    if log_content:
                        print(f"\n📋 Debug Log:\n{log_content}")
                    else:
                        print("\n📋 Debug log is empty")
            except FileNotFoundError:
                print("\n📋 Debug log file not found")
                
        else:
            print("❌ No access token in login response")
    else:
        print(f"❌ Login failed: {login_response.status_code}")
        
except Exception as e:
    print(f"❌ Error: {e}")