#!/usr/bin/env python3
"""
Simple test to submit one request and check the server logs
"""

import requests
import json

# Configuration
BACKEND_URL = "http://localhost:8000"

def test_simple_request():
    """Test a simple request"""
    print("🧪 Testing Simple E-Signature Request")
    
    # Login
    login_data = {"username": "testuser", "password": "testpass123"}
    login_response = requests.post(f"{BACKEND_URL}/api/auth/login/", json=login_data)
    token = login_response.json()['access']
    headers = {'Authorization': f'Bearer {token}'}
    
    # Submit request
    request_data = {
        "signatory_name": "FINAL DEBUG TEST",
        "role": "Test Role",
        "email": "finaldebug@test.com",
        "justification": "Final debug test request"
    }
    
    print("Submitting request...")
    response = requests.post(
        f"{BACKEND_URL}/api/signatory-authorizations/request/",
        json=request_data,
        headers=headers
    )
    
    print(f"Response Status: {response.status_code}")
    print(f"Response: {response.text}")

if __name__ == "__main__":
    test_simple_request()