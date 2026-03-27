#!/usr/bin/env python3
"""
Find all documents and their associated signatures
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

def find_all_documents_and_signatures():
    """Find all documents and their signatures"""
    print("=== ALL DOCUMENTS AND SIGNATURES ===\n")
    
    # Get all documents
    documents = Document.objects.all().order_by('-created_at')
    
    print(f"Found {documents.count()} documents:")
    for doc in documents:
        print(f"\nDocument: '{doc.title}' (ID: {doc.id})")
        print(f"Created: {doc.created_at}")
        print(f"Status: {doc.status}")
        
        # Get signature requests for this document
        requests = SignatureRequest.objects.filter(document=doc).order_by('-created_at')
        print(f"Signature Requests: {requests.count()}")
        
        for req in requests:
            print(f"  Request {req.id}: {req.signer_name} - {req.status}")
            if hasattr(req, 'signature') and req.signature:
                sig = req.signature
                print(f"    → Signature {sig.id}: {sig.signature_type}")
                print(f"    → Image: {sig.signature_image}")
                print(f"    → Signed: {sig.signing_timestamp}")
    
    print("\n" + "="*50)
    print("ALL DIGITAL SIGNATURES:")
    print("="*50)
    
    # Get all digital signatures
    signatures = DigitalSignature.objects.all().order_by('-signing_timestamp')
    
    for sig in signatures:
        print(f"\nSignature ID: {sig.id}")
        print(f"Type: {sig.signature_type}")
        print(f"Signer: {sig.signature_request.signer_name}")
        print(f"Document: {sig.signature_request.document.title}")
        print(f"Request ID: {sig.signature_request.id}")
        print(f"Request Status: {sig.signature_request.status}")
        print(f"Image: {sig.signature_image}")
        print(f"Signed: {sig.signing_timestamp}")

if __name__ == "__main__":
    find_all_documents_and_signatures()