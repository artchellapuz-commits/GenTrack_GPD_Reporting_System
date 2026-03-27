#!/usr/bin/env python3
"""
Test the corrected media URLs
"""

import requests

def test_media_urls():
    """Test if signature images are accessible with corrected media URLs"""
    print("=== TESTING CORRECTED MEDIA URLS ===\n")
    
    # Test the signature image URLs with proper media path
    image_paths = [
        "signatures/2026/03/signature_20260319_054813.png",  # DRAWN signature
        "signatures/2026/03/typed_signature_20260319_053554.png"  # TYPED signature
    ]
    
    for path in image_paths:
        # Test with corrected media URL format
        url = f"http://localhost:8000/media/{path}"
        print(f"Testing URL: {url}")
        
        try:
            response = requests.get(url)
            print(f"  Status: HTTP {response.status_code}")
            if response.status_code == 200:
                print(f"  Content-Type: {response.headers.get('content-type', 'unknown')}")
                print(f"  Content-Length: {len(response.content)} bytes")
                print("  ✅ Image is accessible!")
            else:
                print(f"  ❌ Image not accessible")
                if response.status_code == 404:
                    print("  This might be because the Django server is not running")
        except Exception as e:
            print(f"  ❌ Error: {e}")
        print()

if __name__ == "__main__":
    test_media_urls()