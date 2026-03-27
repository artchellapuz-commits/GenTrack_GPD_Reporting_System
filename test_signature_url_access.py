#!/usr/bin/env python3
"""
Test if signature URLs are accessible
"""

import requests

def test_signature_url_access():
    """Test if signature URLs are accessible"""
    print("Testing Signature URL Access")
    print("=" * 40)
    
    # Test a known signature URL
    test_url = "http://localhost:8000/media/admin_signatures/c_c__amigable_jr__signature.png"
    
    try:
        print(f"Testing URL: {test_url}")
        response = requests.get(test_url, timeout=5)
        print(f"Status Code: {response.status_code}")
        print(f"Content Type: {response.headers.get('content-type', 'N/A')}")
        print(f"Content Length: {len(response.content)} bytes")
        
        if response.status_code == 200:
            print("SUCCESS: Signature URL is accessible!")
        else:
            print(f"ERROR: Got status code {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("ERROR: Cannot connect to Django backend. Is it running on port 8000?")
    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    test_signature_url_access()