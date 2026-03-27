#!/usr/bin/env python3
"""
Test the current API workflow to see which method is being called
"""
import requests
import json

# Test data
test_data = {
    "signatory_name": "TEST WORKFLOW",
    "role": "Test Role",
    "email": "test@example.com",
    "justification": "Testing which method gets called for API requests"
}

# API endpoint
url = "http://localhost:8000/api/signatory-authorizations/request/"

print("Testing API workflow...")
print(f"URL: {url}")
print(f"Data: {json.dumps(test_data, indent=2)}")

try:
    # Make the request
    response = requests.post(url, json=test_data, headers={
        'Content-Type': 'application/json'
    })
    
    print(f"\nResponse Status: {response.status_code}")
    print(f"Response Headers: {dict(response.headers)}")
    
    if response.text:
        try:
            response_data = response.json()
            print(f"Response Data: {json.dumps(response_data, indent=2)}")
        except:
            print(f"Response Text: {response.text}")
    
    # Check debug log
    try:
        with open('npc-reporting-system/backend/debug_log.txt', 'r') as f:
            log_content = f.read()
            if log_content:
                print(f"\nDebug Log Content:\n{log_content}")
            else:
                print("\nDebug log is empty")
    except FileNotFoundError:
        print("\nDebug log file not found")
        
except Exception as e:
    print(f"Error: {e}")