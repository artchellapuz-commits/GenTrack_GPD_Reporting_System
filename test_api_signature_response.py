#!/usr/bin/env python3
"""
Test what the API returns for signature requests and digital signatures
"""

import requests
import json

def test_api_responses():
    """Test the API endpoints that the frontend uses"""
    print("=== TESTING API RESPONSES ===\n")
    
    # Test signature requests endpoint (this requires authentication)
    print("1. Testing Signature Requests API:")
    try:
        response = requests.get("http://localhost:8000/api/signature-requests/")
        print(f"   Status: {response.status_code}")
        if response.status_code == 401:
            print("   ❌ Authentication required (expected)")
        elif response.status_code == 200:
            data = response.json()
            print(f"   ✅ Success: {len(data.get('results', data))} requests")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print("\n2. Testing Digital Signatures API:")
    try:
        response = requests.get("http://localhost:8000/api/digital-signatures/")
        print(f"   Status: {response.status_code}")
        if response.status_code == 401:
            print("   ❌ Authentication required (expected)")
        elif response.status_code == 200:
            data = response.json()
            print(f"   ✅ Success: {len(data.get('results', data))} signatures")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print("\n3. Testing Image URLs:")
    image_urls = [
        "http://localhost:8000/media/signatures/2026/03/signature_20260319_060847.png",  # DRAWN
        "http://localhost:8000/media/signatures/2026/03/typed_signature_20260319_055923.png"  # TYPED
    ]
    
    for url in image_urls:
        try:
            response = requests.get(url)
            if response.status_code == 200:
                print(f"   ✅ {url.split('/')[-1]}: Accessible ({len(response.content)} bytes)")
            else:
                print(f"   ❌ {url.split('/')[-1]}: Not accessible ({response.status_code})")
        except Exception as e:
            print(f"   ❌ {url.split('/')[-1]}: Error ({e})")

def simulate_frontend_logic():
    """Simulate what the frontend viewSignatures method would do"""
    print("\n=== SIMULATING FRONTEND LOGIC ===\n")
    
    # This is what the frontend would do (without authentication for now)
    print("Frontend would:")
    print("1. Call api.getSignatureRequests() - gets all signature requests")
    print("2. Filter by document ID (20 for PSR)")
    print("3. Call api.getDigitalSignatures() - gets all digital signatures")
    print("4. Merge signature requests with their digital signatures")
    print("5. Display in the modal")
    
    print("\nExpected result for PSR document:")
    print("- Should show 2 signature entries for JMM_MATA")
    print("- Request 23: DRAWN signature (newer)")
    print("- Request 22: TYPED signature (older)")
    print("\nIf you're only seeing the TYPED signature, it could be:")
    print("1. Frontend cache needs refresh")
    print("2. API ordering issue")
    print("3. Frontend filtering issue")
    print("4. Modal showing wrong signature")

if __name__ == "__main__":
    test_api_responses()
    simulate_frontend_logic()