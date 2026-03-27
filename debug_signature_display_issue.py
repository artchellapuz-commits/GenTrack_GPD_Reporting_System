#!/usr/bin/env python3
"""
Debug script to investigate why drawn signatures are showing as typed text
in the View Signatures modal.
"""

import os
import sys
import django

# Add the backend directory to Python path
sys.path.append('npc-reporting-system/backend')

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'npc_reporting.settings')
django.setup()

from reports.models import DigitalSignature, SignatureRequest, Document
from django.utils import timezone
from datetime import timedelta

def debug_signature_display():
    """Debug signature display issue"""
    print("=== SIGNATURE DISPLAY DEBUG ===\n")
    
    # Get recent signatures
    recent_signatures = DigitalSignature.objects.all().order_by('-signing_timestamp')[:5]
    
    if not recent_signatures:
        print("No signatures found in database.")
        return
    
    print(f"Found {recent_signatures.count()} recent signatures:\n")
    
    for i, sig in enumerate(recent_signatures, 1):
        print(f"--- Signature {i} ---")
        print(f"ID: {sig.id}")
        print(f"Signature Type: {sig.signature_type}")
        print(f"Signature Image Path: {sig.signature_image}")
        print(f"Signature Data (first 100 chars): {sig.signature_data[:100]}...")
        print(f"Signer: {sig.signature_request.signer_name}")
        print(f"Document: {sig.signature_request.document.title}")
        print(f"Status: {sig.signature_request.status}")
        print(f"Signed At: {sig.signing_timestamp}")
        print(f"Width x Height: {sig.width} x {sig.height}")
        
        # Check if image file exists
        if sig.signature_image:
            image_path = f"npc-reporting-system/backend/media/{sig.signature_image}"
            file_exists = os.path.exists(image_path)
            print(f"Image File Exists: {file_exists}")
            if file_exists:
                file_size = os.path.getsize(image_path)
                print(f"Image File Size: {file_size} bytes")
        
        print()
    
    # Check for any signature requests with JMM_MATA
    print("=== SEARCHING FOR JMM_MATA SIGNATURES ===\n")
    jmm_requests = SignatureRequest.objects.filter(signer_name__icontains='JMM')
    
    for req in jmm_requests:
        print(f"Signature Request ID: {req.id}")
        print(f"Signer: {req.signer_name}")
        print(f"Email: {req.signer_email}")
        print(f"Status: {req.status}")
        print(f"Document: {req.document.title}")
        
        if hasattr(req, 'signature') and req.signature:
            sig = req.signature
            print(f"Digital Signature ID: {sig.id}")
            print(f"Signature Type: {sig.signature_type}")
            print(f"Image Path: {sig.signature_image}")
            print(f"Data Preview: {sig.signature_data[:50]}...")
        else:
            print("No digital signature found for this request")
        print()

if __name__ == "__main__":
    debug_signature_display()