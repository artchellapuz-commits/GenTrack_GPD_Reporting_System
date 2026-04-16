#!/usr/bin/env python3
"""
Performance monitoring script for production
"""

import requests
import time
import json
from datetime import datetime

def test_login_performance():
    """Test login endpoint performance"""
    
    base_url = "https://your-render-app.onrender.com"
    
    # Test health check first
    print("Testing health check...")
    start = time.time()
    try:
        health_response = requests.get(f"{base_url}/health/", timeout=10)
        health_time = (time.time() - start) * 1000
        print(f"✅ Health check: {health_time:.2f}ms - Status: {health_response.status_code}")
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return
    
    # Test login endpoint
    print("\nTesting login endpoint...")
    login_data = {
        "username": "test_user",  # Use a test account
        "password": "test_password"
    }
    
    start = time.time()
    try:
        login_response = requests.post(
            f"{base_url}/api/auth/login/",
            json=login_data,
            timeout=20
        )
        login_time = (time.time() - start) * 1000
        
        if login_response.status_code == 200:
            response_data = login_response.json()
            server_time = response_data.get('response_time_ms', 'N/A')
            print(f"✅ Login successful: {login_time:.2f}ms total, {server_time}ms server")
        else:
            print(f"❌ Login failed: {login_response.status_code} - {login_time:.2f}ms")
            
    except Exception as e:
        login_time = (time.time() - start) * 1000
        print(f"❌ Login error: {e} - {login_time:.2f}ms")

if __name__ == "__main__":
    print(f"🚀 Performance Test - {datetime.now()}")
    test_login_performance()