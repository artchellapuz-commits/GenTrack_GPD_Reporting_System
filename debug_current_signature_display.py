#!/usr/bin/env python3
"""
Debug which signature is currently being displayed in the View Signatures modal
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

def debug_current_signatures():
    """Debug which signatures are associated with PSR REPORT 2"""
    print("=== CURRENT SIGNATURE DISPLAY DEBUG ===\n")
    
    # Find PSR REPORT 2 document
    try:
        psr_doc = Document.objects.get(title="PSR REPORT 2")
        print(f"Document: {psr_doc.title} (ID: {psr_doc.id})")
    except Document.DoesNotExist:
        print("PSR REPORT 2 document not found")
        return
    
    # Get all signature requests for this document
    signature_requests = SignatureRequest.objects.filter(document=psr_doc).order_by('-created_at')
    
    print(f"\nSignature Requests for {psr_doc.title}:")
    print("-" * 50)
    
    for req in signature_requests:
        print(f"Request ID: {req.id}")
        print(f"Signer: {req.signer_name}")
        print(f"Status: {req.status}")
        print(f"Created: {req.created_at}")
        print(f"Signed: {req.signed_at}")
        
        # Check if this request has a digital signature
        if hasattr(req, 'signature') and req.signature:
            sig = req.signature
            print(f"  → Digital Signature ID: {sig.id}")
            print(f"  → Type: {sig.signature_type}")
            print(f"  → Image: {sig.signature_image}")
            print(f"  → Signed At: {sig.signing_timestamp}")
            
            # Check image accessibility
            if sig.signature_image:
                image_url = f"http://localhost:8000/media/{sig.signature_image}"
                print(f"  → Image URL: {image_url}")
        else:
            print(f"  → No digital signature")
        
        print()
    
    # Check which signature would be returned by the API
    print("=== API RESPONSE SIMULATION ===\n")
    
    # Simulate what the frontend viewSignatures method would get
    signed_requests = signature_requests.filter(status='SIGNED')
    
    print(f"Signed requests that would appear in View Signatures modal:")
    for req in signed_requests:
        print(f"Request ID: {req.id} - {req.signer_name}")
        if hasattr(req, 'signature'):
            sig = req.signature
            print(f"  Would display: {sig.signature_type} signature (ID: {sig.id})")
            if sig.signature_type == 'DRAWN':
                print(f"  Image URL: http://localhost:8000/media/{sig.signature_image}")
            else:
                print(f"  Text: {sig.signature_data}")
        print()

if __name__ == "__main__":
    debug_current_signatures()