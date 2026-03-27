#!/usr/bin/env python3
"""
Test what signatures look like when displayed in the View Signatures modal
"""

import os
import sys
import django
import requests

# Add the backend directory to Python path
sys.path.append('npc-reporting-system/backend')

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'npc_reporting.settings')
django.setup()

from reports.models import DigitalSignature, SignatureRequest, Document

def test_signature_display():
    """Test how signatures appear in the API responses"""
    print("=== SIGNATURE DISPLAY TEST ===\n")
    
    # Get all signatures
    signatures = DigitalSignature.objects.all().order_by('-signing_timestamp')
    
    print(f"Found {signatures.count()} signatures:\n")
    
    for i, sig in enumerate(signatures, 1):
        print(f"--- Signature {i} ---")
        print(f"ID: {sig.id}")
        print(f"Type: {sig.signature_type}")
        print(f"Signer: {sig.signature_request.signer_name}")
        print(f"Document: {sig.signature_request.document.title}")
        print(f"Image Path: {sig.signature_image}")
        print(f"Image URL: http://localhost:8000{sig.signature_image}")
        
        # Check if image file exists
        if sig.signature_image:
            image_path = f"npc-reporting-system/backend/media/{sig.signature_image}"
            if os.path.exists(image_path):
                file_size = os.path.getsize(image_path)
                print(f"Image File: EXISTS ({file_size} bytes)")
                
                # Test if the image URL is accessible
                try:
                    response = requests.get(f"http://localhost:8000{sig.signature_image}")
                    if response.status_code == 200:
                        print(f"Image URL: ACCESSIBLE (HTTP {response.status_code})")
                    else:
                        print(f"Image URL: NOT ACCESSIBLE (HTTP {response.status_code})")
                except Exception as e:
                    print(f"Image URL: ERROR ({e})")
            else:
                print(f"Image File: NOT FOUND")
        
        print()
    
    # Test the API endpoints that the frontend uses
    print("=== TESTING API ENDPOINTS ===\n")
    
    try:
        # Test signature requests endpoint
        response = requests.get("http://localhost:8000/api/signature-requests/")
        print(f"Signature Requests API: HTTP {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"  Found {len(data.get('results', data))} signature requests")
        
        # Test digital signatures endpoint  
        response = requests.get("http://localhost:8000/api/digital-signatures/")
        print(f"Digital Signatures API: HTTP {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            signatures_data = data.get('results', data)
            print(f"  Found {len(signatures_data)} digital signatures")
            
            # Show details of the most recent signature
            if signatures_data:
                recent_sig = signatures_data[0]
                print(f"  Most recent signature:")
                print(f"    ID: {recent_sig.get('id')}")
                print(f"    Type: {recent_sig.get('signature_type')}")
                print(f"    Image: {recent_sig.get('signature_image')}")
                print(f"    Signer: {recent_sig.get('signer_name')}")
        
    except Exception as e:
        print(f"API Test Error: {e}")

if __name__ == "__main__":
    test_signature_display()