#!/usr/bin/env python3
"""
Check all signatures in detail to understand what happened
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

def check_all_signatures_detailed():
    """Check all signatures in detail"""
    print("=== DETAILED SIGNATURE ANALYSIS ===\n")
    
    # Check if there are any orphaned signatures
    all_signatures = DigitalSignature.objects.all().order_by('id')
    
    print(f"Total signatures in database: {all_signatures.count()}")
    
    for sig in all_signatures:
        print(f"\n--- Signature {sig.id} ---")
        print(f"Type: {sig.signature_type}")
        print(f"Image: {sig.signature_image}")
        print(f"Signed: {sig.signing_timestamp}")
        
        try:
            req = sig.signature_request
            print(f"Request ID: {req.id}")
            print(f"Signer: {req.signer_name}")
            print(f"Request Status: {req.status}")
            
            try:
                doc = req.document
                print(f"Document: '{doc.title}' (ID: {doc.id})")
                print(f"Document Status: {doc.status}")
            except:
                print("Document: DELETED or MISSING")
                
        except:
            print("Signature Request: DELETED or MISSING")
        
        # Check if image file exists
        if sig.signature_image:
            image_path = f"npc-reporting-system/backend/media/{sig.signature_image}"
            exists = os.path.exists(image_path)
            print(f"Image File Exists: {exists}")
            if exists:
                size = os.path.getsize(image_path)
                print(f"Image Size: {size} bytes")

if __name__ == "__main__":
    check_all_signatures_detailed()